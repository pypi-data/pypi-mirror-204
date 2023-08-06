"""Fietsboek GPX transformers.

A "transformer" is something like a filter - it takes in a GPX file and applies
some small corrections, such as smoothing out the elevation. In order to avoid
confusion with the naming (and the "filters" you have when searching for
tracks), we call those "GPX filters" *transformers*.

This module defines the abstract interface for transformers, as well as
function to load and apply transformers.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Mapping
from itertools import islice
from typing import Literal, NamedTuple, TypeVar

from gpxpy.gpx import GPX, GPXTrackPoint
from pydantic import BaseModel
from pyramid.i18n import TranslationString
from pyramid.request import Request

_ = TranslationString

T = TypeVar("T", bound="Transformer")


class ParameterDefinition(NamedTuple):
    """A parameter definition for the UI to render."""

    type: Literal["int", "str"]
    """Type of the parameter."""

    name: str
    """Name of the parameter.

    This is the machine-readable identifier, not the human readable name.
    """

    label: TranslationString
    """Human-readable label of the parameter."""

    value: str
    """The serialized value of the parameter."""


class Parameters(BaseModel):
    """Parameters for a transformer.

    This is basically a wrapper around pydantic models that allows the
    parameters to be serialized from and to POST request parameters.
    """

    def html_ui(self) -> list[ParameterDefinition]:
        """Renders a HTML UI for this parameter set.

        :return: The rendered UI, ready for inclusion.
        """
        return []

    def read_from_request(self, data: Mapping[str, str]):
        """Parses the parameters from the given request data.

        :param data: The request data, e.g. from the POST values.
        """


class Transformer(ABC):
    """A :class:`Transformer` is the main interface for track manipulation."""

    @classmethod
    @abstractmethod
    def identifier(cls: type[T]) -> str:
        """Returns a string identifier for this transformer.

        This identifier is used when serializing/deserializing the filters.

        :return: A machine-readable identifier for this transformer.
        """

    @classmethod
    @abstractmethod
    def name(cls: type[T]) -> TranslationString:
        """The human-readable name of this transformer, as a translateable string.

        :return: The transformer's name.
        """

    @classmethod
    @abstractmethod
    def description(cls: type[T]) -> TranslationString:
        """A short description of what this transformer does.

        :return: The transformer's description.
        """

    @classmethod
    @abstractmethod
    def parameter_model(cls: type[T]) -> type[Parameters]:
        """Returns the parameter model that this transformer expects.

        :return: The parameter model class.
        """

    @property
    @abstractmethod
    def parameters(self) -> Parameters:
        """Returns the parameters of this transformer.

        Note that the caller may modify the parameters, which should be
        reflected in future applications of the transformer.

        :return: The parameters.
        """

    @parameters.setter
    @abstractmethod
    def parameters(self, value: Parameters):
        pass

    @abstractmethod
    def execute(self, gpx: GPX):
        """Run the transformation on the input gpx.

        This is expected to modify the GPX object to represent the new state.

        :param gpx: The GPX object to transform. Note that this object will be
            mutated!
        """


class FixNullElevation(Transformer):
    """A transformer that fixes points with zero elevation."""

    @classmethod
    def identifier(cls) -> str:
        return "fix-null-elevation"

    @classmethod
    def name(cls) -> TranslationString:
        return _("transformers.fix-null-elevation.title")

    @classmethod
    def description(cls) -> TranslationString:
        return _("transformers.fix-null-elevation.description")

    @classmethod
    def parameter_model(cls) -> type[Parameters]:
        return Parameters

    @property
    def parameters(self) -> Parameters:
        return Parameters()

    @parameters.setter
    def parameters(self, value):
        pass

    def execute(self, gpx: GPX):
        def all_points():
            return gpx.walk(only_points=True)

        def rev_points():
            # We cannot use reversed(gpx.walk(...)) since that is not a
            # generator, so we do it manually.
            return (
                point
                for track in reversed(gpx.tracks)
                for segment in reversed(track.segments)
                for point in reversed(segment.points)
            )

        # First, from the front
        self.fixup(all_points)
        # Then, from the back
        self.fixup(rev_points)

    @classmethod
    def fixup(cls, points: Callable[[], Iterable[GPXTrackPoint]]):
        """Fixes the given GPX points.

        This iterates over the points and checks for the first point that has a
        non-zero elevation, and a slope that doesn't exceed 100%. All previous
        points will have their elevation adjusted to match this first "good
        point".

        :param points: A function that generates the iterable of points.
        """
        max_slope = 1.0

        bad_until = 0
        final_elevation = 0.0
        for i, (point, next_point) in enumerate(zip(points(), islice(points(), 1, None))):
            if (
                point.elevation is not None
                and point.elevation != 0.0
                and cls.slope(point, next_point) < max_slope
            ):
                bad_until = i
                final_elevation = point.elevation
                break

        for point in islice(points(), None, bad_until):
            point.elevation = final_elevation

    @staticmethod
    def slope(point_a: GPXTrackPoint, point_b: GPXTrackPoint) -> float:
        """Returns the slope between two GPX points.

        This is defined as delta_h / euclid_distance.

        :param point_a: First point.
        :param point_b: Second point.
        :return: The slope, as percentage.
        """
        if point_a.elevation is None or point_b.elevation is None:
            return 0.0
        delta_h = abs(point_a.elevation - point_b.elevation)
        dist = point_a.distance_2d(point_b)
        if dist == 0.0 or dist is None:
            return 0.0
        return delta_h / dist


def list_transformers() -> list[type[Transformer]]:
    """Returns a list of all available transformers.

    :return: A list of transformers.
    """
    # pylint: disable=import-outside-toplevel,cyclic-import
    from .breaks import RemoveBreaks

    return [
        FixNullElevation,
        RemoveBreaks,
    ]


def extract_from_request(request: Request) -> list[Transformer]:
    """Extracts the list of transformers to execute from the given request.

    Note that this sets up the transformers with the right parameters.

    :param request: The pyramid request.
    :return: The list of prepared transformers.
    """
    transformers = []
    for tfm in list_transformers():
        ident = tfm.identifier()
        prefix = f"transformer[{ident}]"
        req_params = {}
        for name, val in request.params.items():
            if name.startswith(prefix):
                name = name[len(prefix) :]
                name = name.strip("[]")
                req_params[name] = val

        if req_params.get("") == "on":
            instance = tfm()
            instance.parameters.read_from_request(req_params)
            transformers.append(instance)

    return transformers


__all__ = ["Parameters", "Transformer", "list_transformers"]
