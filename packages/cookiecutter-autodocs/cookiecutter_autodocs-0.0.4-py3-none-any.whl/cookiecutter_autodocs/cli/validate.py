"""Code for the validate CLI sub-command"""
from cookiecutter_autodocs.cli.app import app
from cookiecutter_autodocs.schemas.description import CookieCutterDescription
from cookiecutter_autodocs.lib.files import load_cookiecutter_json

from typer import Argument, Option, Exit
from pathlib import Path
from typing import Optional
from rich import print


@app.async_command()
async def validate(
    cookiecutter_desc: Path = Argument(
        ...,
        help="Path to the cookiecutter.desc file",
    ),
    cookiecutter_json: Optional[Path] = Argument(
        None,
        help="Path to the cookiecutter.json file. If not specified, the cookiecutter.json will be read from the same"
        + " directory as the cookiecutter.desc file",
    ),
    allow_empty_description: bool = Option(
        False, help="Allow empty descriptions. If not set, an empty description will cause an error."
    ),
) -> None:
    if cookiecutter_json is None:
        cookiecutter_json = cookiecutter_desc.parent / "cookiecutter.json"
    desc = await CookieCutterDescription.from_cookiecutter_desc(cookiecutter_desc)
    validated, errors = desc.validate_cookiecutter_json(
        await load_cookiecutter_json(cookiecutter_json), allow_empty_desc=allow_empty_description
    )
    if not validated:
        print("Validation failed:")
        print(errors)
        raise Exit(1)
    print("Validation succeeded")
