# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from typer import Typer

from .auth import app as auth_app
from .demos import app as demos_app
from .endpoints import app as endpoints_app
from .graphs import app as graphs_app
from .misc import cli_options
from .predict import predict
from .predictors import app as predictors_app
from .users import app as users_app
from ..version import __version__

# Define CLI
app = Typer(
    name=f"NatML CLI {__version__}",
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_short=True,
)

# Add top level options
app.callback()(cli_options)

# Add subcommands
app.add_typer(auth_app, name="auth", help="Login, logout, and perform other authentication tasks.")
app.add_typer(predictors_app, name="predictors", help="Manage predictors.")
app.add_typer(graphs_app, name="graphs", help="Manage predictor graphs.")
app.add_typer(endpoints_app, name="endpoints", help="Manage predictor endpoints.")
app.add_typer(users_app, name="users", help="Manage users.")
app.add_typer(demos_app, name="demos", help="Manage predictor demos.")

# Add top-level commands
app.command(
    name="predict",
    context_settings={ "allow_extra_args": True, "ignore_unknown_options": True },
    help="Make a prediction with a predictor."
)(predict)

# Run
if __name__ == "__main__":
    app()