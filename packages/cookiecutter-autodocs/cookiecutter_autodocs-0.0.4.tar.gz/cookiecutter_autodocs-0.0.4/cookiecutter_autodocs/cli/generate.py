"""Code for the generate sub-commands"""
from cookiecutter_autodocs.cli._async import AsyncTyper
from cookiecutter_autodocs.lib.files import dump_cookiecutter_json
from cookiecutter_autodocs.lib.files import load_cookiecutter_json
from cookiecutter_autodocs.schemas.description import CookieCutterDescription
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional

from aiofiles.os import path as aiopath
from markdownTable import markdownTable
from rich import print
from typer import Option, Argument

generate_app = AsyncTyper()


@generate_app.async_command()
async def desc(
    cookiecutter_json: Path = Argument(..., help="Path to the cookiecutter.json file"),
    cookiecutter_desc: Optional[Path] = Option(
        None,
        "--output",
        "-o",
        help="Path to a cookiecutter.desc file to write. If the file exists, it will be updated in place. "
        + "If not specified, the cookiecutter.desc will be written to the same directory as the cookiecutter.json file",
    ),
) -> None:
    """Generate a new or update an existing cookiecutter.desc from a cookiecutter.json file."""
    if cookiecutter_desc is None:
        cookiecutter_desc = cookiecutter_json.parent / "cookiecutter.desc"
    if await aiopath.exists(str(cookiecutter_desc)):
        print(f"Updating an existing cookiecutter.desc file at {cookiecutter_desc}")
        existing_desc = await CookieCutterDescription.from_cookiecutter_desc(cookiecutter_desc)
    else:
        print(f"Generating a new cookiecutter.desc file at {cookiecutter_desc}")
        existing_desc = CookieCutterDescription(variables={})
    existing_desc.update(await CookieCutterDescription.from_cookiecutter_json(cookiecutter_json))
    await existing_desc.to_cookiecutter_desc(cookiecutter_desc)
    print(f"Generated {cookiecutter_desc} from {cookiecutter_json}")


@generate_app.async_command()
async def cookiecutter(
    cookiecutter_desc: Path = Argument(
        ...,
        help="Path to a cookiecutter.desc file to read.",
    ),
    cookiecutter_json: Optional[Path] = Option(
        None,
        "--output",
        "-o",
        help="Path to the cookiecutter.json file.  If the file exists, it will be updated in place. If not specified, "
        + "the cookiecutter.json will be written to the same directory as the cookiecutter.json file",
    ),
) -> None:
    """Generate a new or update an existing cookiecutter.json file from a cookiecutter.desc."""
    if cookiecutter_json is None:
        cookiecutter_json = cookiecutter_desc.parent / "cookiecutter.json"
    if await aiopath.exists(str(cookiecutter_json)):
        print(f"Updating an existing cookiecutter.json file at {cookiecutter_json}")
        existing_json: Dict[str, Any] = await load_cookiecutter_json(cookiecutter_json)
    else:
        print(f"Generating a new cookiecutter.json file at {cookiecutter_json}")
        existing_json = {}
    existing_desc = await CookieCutterDescription.from_cookiecutter_desc(cookiecutter_desc)
    existing_json.update(existing_desc.cookiecutter_json)
    await dump_cookiecutter_json(cookiecutter_json, existing_json)
    print(f"Generated {cookiecutter_json} from {cookiecutter_desc}")


@generate_app.async_command()
async def markdown(
    cookiecutter_desc: Path = Argument(
        ...,
        help="Path to a cookiecutter.desc file to read.",
    ),
    markdown_file: Optional[Path] = Option(
        None,
        "--outfile",
        "-o",
        help="File to write the markdown table to. If blank, will output to stdout",
    ),
    markdown_template: Optional[Path] = Option(
        None,
        "--template",
        "-t",
        help="Template to use for writing the markdown table. If blank, will use the default template.",
    ),
) -> None:
    """Generate a Markdown table describing the cookiecutter's parameters from a cookiecutter.desc."""
    desc = await CookieCutterDescription.from_cookiecutter_desc(cookiecutter_desc)
    table = markdownTable([variable.dict(exclude=set()) for _, variable in desc.variables.items()])
    print(table.getMarkdown())


@generate_app.callback()
def doc() -> None:
    """Generate a cookiecutter.desc, cookiecutter.json or markdown."""
    pass
