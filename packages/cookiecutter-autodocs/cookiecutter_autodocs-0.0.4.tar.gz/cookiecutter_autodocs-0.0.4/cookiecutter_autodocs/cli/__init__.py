from cookiecutter_autodocs.cli.app import app
from cookiecutter_autodocs.cli.gha import gha_app
from cookiecutter_autodocs.cli.generate import generate_app  # noqa: F401
from cookiecutter_autodocs.cli import validate  # noqa: F401
from typer.main import get_command
import os
from rich import print


def main() -> None:  # pragma: no cover
    # if we're running in GHA, launch the simplifed GHA app instead
    if os.environ.get("IN_GHA", "false").lower() == "true":
        print("[bold green]Running in GHA[/bold green]")
        gha_app()
        return

    # otherwise, launch the normal cli app
    app()


# Create the typer click object to generate docs with sphinx-click
typer_click_object = get_command(app)

if __name__ == "__main__":
    main()  # pragma: no cover
