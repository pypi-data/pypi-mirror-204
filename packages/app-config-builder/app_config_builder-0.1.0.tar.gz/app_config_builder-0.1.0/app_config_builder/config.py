from pydantic import BaseSettings
from pydantic.fields import Field

from .default import AppDefaultConfig
from .db.config import DatabaseConfig
from .log.config import LoggerConfig
from .utils.func import add_fields


def get_dynamic_config() -> BaseSettings:
    config = AppDefaultConfig()

    if LoggerConfig is not None:
        add_fields(config, log=(LoggerConfig, LoggerConfig()))

    if DatabaseConfig is not None:
        add_fields(config, db=(DatabaseConfig, DatabaseConfig()))

    return config


class AppBaseConfig(AppDefaultConfig):
    log: LoggerConfig = Field(
        default=LoggerConfig() if LoggerConfig else None,
        exclude=LoggerConfig is None or set(),
        const=True
    )
    db: DatabaseConfig = Field(
        default=DatabaseConfig() if DatabaseConfig else None,
        exclude=DatabaseConfig is None or set(),
        const=True
    )
