from pathlib import Path
from typing import Any
from typing import Dict
from typing import TypeVar
from typing import Union

DictStrAny = TypeVar("DictStrAny", bound=Dict[str, Any])
StrOrPath = TypeVar("StrOrPath", bound=Union[str, Path])
