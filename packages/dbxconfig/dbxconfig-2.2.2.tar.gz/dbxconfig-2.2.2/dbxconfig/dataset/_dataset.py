import logging
from pydantic import BaseModel, Field, PrivateAttr
from .._utils import JinjaVariables
from typing import Any, Dict
from .._timeslice import Timeslice
from .._stage_type import StageType


class DataSet(BaseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._logger = logging.getLogger(self.__class__.__name__)

    _logger: Any = PrivateAttr(default=None)
    _replacements: Dict[JinjaVariables, str] = PrivateAttr(default=None)
    database: str = Field(...)
    destination_table: str = Field(...)
    table: str = Field(...)
    container: str = Field(...)
    root: str = Field(...)
    path: str = Field(default=None)
    options: dict = Field(...)
    timeslice: Timeslice = Field(...)
    checkpoint: str = Field(default=None)
    stage: StageType = Field(...)
    config_path: str = Field(...)

    def _render(self):
        pass
