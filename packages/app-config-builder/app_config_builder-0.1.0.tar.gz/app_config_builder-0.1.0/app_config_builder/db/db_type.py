from enum import Enum

from pydantic import Field

from ..advanced_config import AdvancedConfig
from ..constants import DB_TYPE

__all__ = [
    "config_db_type",
    "AllowedDbType",
]


class AllowedDbType(str, Enum):
    sqlite = "sqlite"
    postgresql = "postgresql"
    mysql = "mysql"


class ConfigDbType(AdvancedConfig):
    DB_TYPE: AllowedDbType | None = Field(default=DB_TYPE)


config_db_type = ConfigDbType().DB_TYPE
