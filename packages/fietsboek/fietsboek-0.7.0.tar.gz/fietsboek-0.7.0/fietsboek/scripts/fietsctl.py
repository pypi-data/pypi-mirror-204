"""Script to do maintenance work on a Fietsboek instance."""
# pylint: disable=too-many-arguments
from typing import Optional

import click
from click_option_group import RequiredMutuallyExclusiveOptionGroup, optgroup
from pyramid.paster import bootstrap, setup_logging
from pyramid.scripting import AppEnvironment
from sqlalchemy import select

from .. import __VERSION__, hittekaart, models
from ..data import DataManager
from . import config_option

EXIT_OKAY = 0
EXIT_FAILURE = 1


def setup(config_path: str) -> AppEnvironment:
    """Sets up the logging and app environment for the scripts.

    This - for example - sets up a transaction manager in
    ``setup(...)["request"]``.

    :param config_path: Path to the configuration file.
    :return: The prepared environment.
    """
    setup_logging(config_path)
    return bootstrap(config_path)


@click.group(
    help=__doc__,
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(package_name="fietsboek")
def cli():
    """CLI main entry point."""


@cli.command("useradd")
@config_option
@click.option("--email", help="email address of the user", prompt=True)
@click.option("--name", help="name of the user", prompt=True)
@click.option(
    "--password",
    help="password of the user",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
)
@click.option("--admin", help="make the new user an admin", is_flag=True)
@click.pass_context
def cmd_useradd(ctx: click.Context, config: str, email: str, name: str, password: str, admin: bool):
    """Create a new user.

    This user creation bypasses the "enable_account_registration" setting. It
    also immediately sets the new user's account to being verified.

    If email, name or password are not given as command line arguments, they
    will be asked for interactively.

    On success, the created user's unique ID will be printed.

    Note that this function does less input validation and should therefore be used with care!
    """
    env = setup(config)

    # The UNIQUE constraint only prevents identical emails from being inserted,
    # but does not take into account the case insensitivity. The least we
    # should do here to not brick log ins for the user is to check if the email
    # already exists.
    query = models.User.query_by_email(email)
    with env["request"].tm:
        result = env["request"].dbsession.execute(query).scalar_one_or_none()
        if result is not None:
            click.echo("Error: The given email already exists!", err=True)
            ctx.exit(EXIT_FAILURE)

    user = models.User(name=name, email=email, is_verified=True, is_admin=admin)
    user.set_password(password)

    with env["request"].tm:
        dbsession = env["request"].dbsession
        dbsession.add(user)
        dbsession.flush()
        user_id = user.id

    click.echo(user_id)


@cli.command("userdel")
@config_option
@click.option("--force", "-f", help="override the safety check", is_flag=True)
@optgroup.group("User selection", cls=RequiredMutuallyExclusiveOptionGroup)
@optgroup.option("--id", "-i", "id_", help="database ID of the user", type=int)
@optgroup.option("--email", "-e", help="email of the user")
@click.pass_context
def cmd_userdel(
    ctx: click.Context,
    config: str,
    force: bool,
    id_: Optional[int],
    email: Optional[str],
):
    """Delete a user.

    This command deletes the user's account as well as any tracks associated
    with it.

    This command is destructive and irreversibly deletes data.
    """
    env = setup(config)
    if id_ is not None:
        query = select(models.User).filter_by(id=id_)
    else:
        query = models.User.query_by_email(email)
    with env["request"].tm:
        dbsession = env["request"].dbsession
        user = dbsession.execute(query).scalar_one_or_none()
        if user is None:
            click.echo("Error: No such user found.", err=True)
            ctx.exit(EXIT_FAILURE)
        click.echo(user.name)
        click.echo(user.email)
        if not force:
            if not click.confirm("Really delete this user?"):
                click.echo("Aborted by user.")
                ctx.exit(EXIT_FAILURE)
        dbsession.delete(user)
        click.echo("User deleted")


@cli.command("userlist")
@config_option
def cmd_userlist(config: str):
    """Prints a listing of all user accounts.

    The format is:

        [av] {ID} - {email} - {name}

    with one line per user. The 'a' is added for admin accounts, the 'v' is added
    for verified users.
    """
    env = setup(config)
    with env["request"].tm:
        dbsession = env["request"].dbsession
        users = dbsession.execute(select(models.User).order_by(models.User.id)).scalars()
        for user in users:
            # pylint: disable=consider-using-f-string
            tag = "[{}{}]".format(
                "a" if user.is_admin else "-",
                "v" if user.is_verified else "-",
            )
            click.echo(f"{tag} {user.id} - {user.email} - {user.name}")


@cli.command("passwd")
@config_option
@click.option("--password", help="password of the user")
@optgroup.group("User selection", cls=RequiredMutuallyExclusiveOptionGroup)
@optgroup.option("--id", "-i", "id_", help="database ID of the user", type=int)
@optgroup.option("--email", "-e", help="email of the user")
@click.pass_context
def cmd_passwd(
    ctx: click.Context,
    config: str,
    password: Optional[str],
    id_: Optional[int],
    email: Optional[str],
):
    """Change the password of a user."""
    env = setup(config)
    if id_ is not None:
        query = select(models.User).filter_by(id=id_)
    else:
        query = models.User.query_by_email(email)
    with env["request"].tm:
        dbsession = env["request"].dbsession
        user = dbsession.execute(query).scalar_one_or_none()
        if user is None:
            click.echo("Error: No such user found.", err=True)
            ctx.exit(EXIT_FAILURE)
        if not password:
            password = click.prompt("Password", hide_input=True, confirmation_prompt=True)

        user.set_password(password)
        click.echo(f"Changed password of {user.name} ({user.email})")


@cli.command("maintenance-mode")
@config_option
@click.option("--disable", help="disable the maintenance mode", is_flag=True)
@click.argument("reason", required=False)
@click.pass_context
def cmd_maintenance_mode(ctx: click.Context, config: str, disable: bool, reason: Optional[str]):
    """Check the status of the maintenance mode, or activate or deactive it.

    When REASON is given, enables the maintenance mode with the given text as
    reason.

    With neither --disable nor REASON given, just checks the state of the
    maintenance mode.
    """
    env = setup(config)
    data_manager = env["request"].data_manager
    if disable and reason:
        click.echo("Cannot enable and disable maintenance mode at the same time", err=True)
        ctx.exit(EXIT_FAILURE)
    elif not disable and not reason:
        maintenance = data_manager.maintenance_mode()
        if maintenance is None:
            click.echo("Maintenance mode is disabled")
        else:
            click.echo(f"Maintenance mode is enabled: {maintenance}")
    elif disable:
        (data_manager.data_dir / "MAINTENANCE").unlink()
    else:
        (data_manager.data_dir / "MAINTENANCE").write_text(reason, encoding="utf-8")


@cli.command("hittekaart")
@config_option
@click.option(
    "--mode",
    "modes",
    help="Heatmap type to generate",
    type=click.Choice([mode.value for mode in hittekaart.Mode]),
    multiple=True,
    default=["heatmap"],
)
@click.option("--delete", help="Delete the specified heatmap", is_flag=True)
@optgroup.group("User selection", cls=RequiredMutuallyExclusiveOptionGroup)
@optgroup.option("--id", "-i", "id_", help="database ID of the user", type=int)
@optgroup.option("--email", "-e", help="email of the user")
@click.pass_context
def cmd_hittekaart(
    ctx: click.Context,
    config: str,
    modes: list[str],
    delete: bool,
    id_: Optional[int],
    email: Optional[str],
):
    """Generate heatmap for a user."""
    env = setup(config)
    modes = [hittekaart.Mode(mode) for mode in modes]

    if id_ is not None:
        query = select(models.User).filter_by(id=id_)
    else:
        query = models.User.query_by_email(email)

    exe_path = env["request"].config.hittekaart_bin
    with env["request"].tm:
        dbsession = env["request"].dbsession
        data_manager: DataManager = env["request"].data_manager
        user = dbsession.execute(query).scalar_one_or_none()
        if user is None:
            click.echo("Error: No such user found.", err=True)
            ctx.exit(EXIT_FAILURE)

        if delete:
            try:
                user_manager = data_manager.open_user(user.id)
            except FileNotFoundError:
                return
            if hittekaart.Mode.HEATMAP in modes:
                user_manager.heatmap_path().unlink(missing_ok=True)
            if hittekaart.Mode.TILEHUNTER in modes:
                user_manager.tilehunt_path().unlink(missing_ok=True)
            return

        click.echo(f"Generating overlay maps for {user.name}...")

        for mode in modes:
            hittekaart.generate_for(user, dbsession, data_manager, mode, exe_path=exe_path)
            click.echo(f"Generated {mode.value}")


@cli.command("version")
def cmd_version():
    """Show the installed fietsboek version."""
    name = __name__.split(".", 1)[0]
    print(f"{name} {__VERSION__}")
