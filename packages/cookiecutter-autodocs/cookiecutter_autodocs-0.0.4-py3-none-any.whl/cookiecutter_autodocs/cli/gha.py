from cookiecutter_autodocs.cli._async import AsyncTyper
from typer import Argument, Option
from pathlib import Path
from enum import Enum
from cookiecutter_autodocs.cli.generate import desc, cookiecutter, markdown
from cookiecutter_autodocs.cli.validate import validate

gha_app = AsyncTyper()


class GHAAction(str, Enum):
    validate = "validate"
    generate_desc = "generate-desc"
    generate_cookiecutter = "generate-cookiecutter"
    generate_markdown = "generate-markdown"


@gha_app.async_command()
async def gha(
    action: GHAAction = Argument(..., help="What action to take"),
    cookiecutter_desc_path: Path = Argument(..., help="Path to cookiecutter.desc"),
    cookiecutter_json_path: Path = Argument(..., help="Path to cookiecutter.json"),
    # allow_empty_description is a string instead of a bool with a flag to make it easier
    # to pass from a GitHub Action input
    allow_empty_description: str = Option("false", help="Allow empty descriptions when validating"),
) -> None:
    """Code for the gha CLI sub-command"""
    if action == "validate":
        await validate(
            cookiecutter_desc=cookiecutter_desc_path,
            cookiecutter_json=cookiecutter_json_path,
            allow_empty_description=allow_empty_description.lower() == "true",
        )
        return

    if action == "generate-desc":
        await desc(
            cookiecutter_json=cookiecutter_json_path,
            cookiecutter_desc=cookiecutter_desc_path,
        )
        return

    if action == "generate-cookiecutter":
        await cookiecutter(
            cookiecutter_json=cookiecutter_json_path,
            cookiecutter_desc=cookiecutter_desc_path,
        )
        return

    if action == "generate-markdown":
        await markdown(
            cookiecutter_desc=cookiecutter_desc_path,
        )
        return
