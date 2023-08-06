from typing import Any

from pydantic.env_settings import BaseSettings


def file_settings(settings: BaseSettings) -> dict[str, Any]:
    conf = dict(
        auth_key='AUTH_KEY_config_file',
        other_key='OTHER_KEY_config_file',

    )
    return conf
