from enum import Enum


class StageType(str, Enum):
    landing = "read"
    raw = "deltalake"
    base = "deltalake"
    curated = "deltalake"
    extract = "write"
