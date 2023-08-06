from pydantic import BaseModel, Field
from typing import Union, List, Any, Dict
from ._stage_type import StageType


class ValidationThreshold(BaseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    invalid_ratio: float = Field(default=None)
    invalid_rows: float = Field(default=None)
    max_rows: int = Field(default=None)
    min_rows: int = Field(default=None)


class BaseTable(BaseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    stage: StageType = Field(...)
    database: str = Field(...)
    name: str = Field(...)
    id: Union[str, List[str]] = Field(default=[])


class Table(BaseTable):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    depends_on: List[str] = Field(default=[])
    table_properties: Dict[str, str] = Field(default=None)
    warning_thresholds: ValidationThreshold = Field(default=None)
    exception_thresholds: ValidationThreshold = Field(default=None)


class TableMapping(BaseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    destination: Table = Field(...)
    source: Union[Dict[str, Table], Table] = Field(...)
