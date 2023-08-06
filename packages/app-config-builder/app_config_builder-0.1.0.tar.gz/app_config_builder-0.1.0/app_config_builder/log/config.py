from pydantic import Field, root_validator

from ..advanced_config import AdvancedConfig
from ..constants import (
    USE_LOGGING,
    LOGS_DIR,
    CREATE_LOG_FILES,
    ROOT_LOGGER,
)
from ..utils.func import get_absolute_path

__all__ = [
    'LoggerConfig',
    'UseLoggingConfig',
]


class UseLoggingConfig(AdvancedConfig):
    USE_LOGGING: bool = Field(USE_LOGGING)


class LoggingConfig(AdvancedConfig):
    """Logging Config."""

    ROOT_LOGGER: str = Field(ROOT_LOGGER)
    LOGS_DIR: str = Field(LOGS_DIR)
    CREATE_LOG_FILES: bool = Field(CREATE_LOG_FILES)
    PATH_LOG_IS_ABSOLUTE: bool = Field(default=False, env='path_log_is_absolute', exclude=True)

    @root_validator
    def post_load(cls, values): # noqa
        logs_dir: str = values.get('LOGS_DIR')
        if not values.get('PATH_LOG_IS_ABSOLUTE'):
            logs_dir = values.get('LOGS_DIR')
            logs_dir = get_absolute_path(logs_dir)
        else:
            if not logs_dir.startswith('/'):
                logs_dir = f'/{logs_dir}'
        values['LOGS_DIR'] = logs_dir
        # values['PATH_LOG_IS_ABSOLUTE'] = True
        return values


LoggerConfig: type | None = None

if UseLoggingConfig().USE_LOGGING:
    LoggerConfig = LoggingConfig
