from pydantic.env_settings import BaseSettings


def read_db_config() -> dict[str, object]:
    db_config = dict()
    return db_config



class FileConfigReader:
    settings: BaseSettings | None = None

    def __int__(self, settings: BaseSettings):
        self.settings = settings
        self.config = dict()
        self.log = dict()
        self.db = dict()
        self.app = dict()
