from pydantic import BaseModel, Extra
from typing import Optional


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    applicationinsights_connection_string: Optional[str] = ""
