import json
from cookiecutter_autodocs.lib.typing import StrOrPath
from typing import Any
from typing import Dict

import aiofiles
import toml
from aiofiles.os import path as aiopath


async def load_cookiecutter_json(path_or_str: StrOrPath) -> Dict[str, Any]:
    """Load a cookiecutter.json file.

    Args:
        cookiecutter_path (Path): Path to the cookiecutter.json file.

    Returns:
        dict: The cookiecutter.json file as a dictionary.
    """
    if not await aiopath.exists(str(path_or_str)):
        raise FileNotFoundError(f"File not found: {path_or_str}")

    async with aiofiles.open(str(path_or_str), "r") as afh:
        return json.loads(await afh.read())


async def dump_cookiecutter_json(path_or_str: StrOrPath, cookiecutter: Dict[str, Any]) -> None:
    """Dump a cookiecutter.json file.

    Args:
        cookiecutter_path (StrOrPath): Path to the cookiecutter.json file.
        cookiecutter (dict): The cookiecutter.json file as a dictionary.
    """
    async with aiofiles.open(str(path_or_str), "w") as afh:
        await afh.write(json.dumps(cookiecutter, indent=2))


async def load_cookiecutter_description(path_or_str: StrOrPath) -> Dict[str, Any]:
    """
    Load a cookiecutter.desc file.

    Args:
        path_or_str (StrOrPath): path to load from

    Returns:
        DictStrAny: CookiecutterDesc represented as a dict
    """
    if not await aiopath.exists(str(path_or_str)):
        raise FileNotFoundError(f"File not found: {path_or_str}")

    async with aiofiles.open(str(path_or_str), "r") as afh:
        return toml.loads(await afh.read())


async def dump_cookiecutter_description(path_or_str: StrOrPath, cookiecutter_desc: Dict[str, Any]) -> None:
    """
    Write a cookiecutter.desc file.

    Args:
        path_or_str (StrOrPath): path to write to
        cookiecutter_desc (DictStrAny): CookiecutterDesc represented as a dict
    """
    async with aiofiles.open(str(path_or_str), "w") as afh:
        await afh.write(toml.dumps(cookiecutter_desc))
