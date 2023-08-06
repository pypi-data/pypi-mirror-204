from pydantic import BaseSettings

from .constants import AM_I_RUNNING_IN_DOCKER
from .constants import BASE_DIR


class AdvancedConfig(BaseSettings):
    class Config:
        secrets_dir = (BASE_DIR / "secrets").as_posix()
        if AM_I_RUNNING_IN_DOCKER:
            secrets_dir = "/run/secrets"
        if not AM_I_RUNNING_IN_DOCKER:
            env_file = ".env"
