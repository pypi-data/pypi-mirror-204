from typing import Any
from typing import Dict, Optional
from typing import Set

from pydantic import BaseModel


class SchemaBase(BaseModel):
    def dict(self, **kwargs) -> Dict[str, Any]:
        exclude_from_kwargs: Optional[Set[str]] = kwargs.pop("exclude", None)
        exclude: Set[str] = (
            getattr(self.Config, "exclude", set()) if exclude_from_kwargs is None else exclude_from_kwargs
        )
        return super().dict(exclude=exclude if len(exclude) > 0 else set(), **kwargs)
