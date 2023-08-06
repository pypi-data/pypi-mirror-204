from typing import Any, Optional, ClassVar

from pydantic import BaseModel, Field

from .drivers import AnyDriver
from ..advanced_config import AdvancedConfig
from ..constants import (
    DB_ASYNC,
    ECHO_SQL,
)


__all__ = [
    "AnyDB",
    "BaseDBConfig",
]


# class DbModeConfig(AdvancedConfig):
#     DB_MODE: str | None = Field(default=None, env='db_mode')


class AbstractDB(BaseModel):
    DRIVER: Any = ...
    DATABASE_URL: Any = ...


class DefaultConfigDB(AdvancedConfig):

    DB_TYPE: str = Field(..., const=True)
    DB_ASYNC: bool | None = Field(default=DB_ASYNC, env='db_async')
    ECHO_SQL: bool = Field(default=ECHO_SQL, env='echo_sql')
    DB_MODE: str | None = Field(default=None, env='db_mode')


class AnyDB(AbstractDB, DefaultConfigDB):
    """Common configuration any database."""

    __dialect__ = "default"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__name__ != 'BaseDBConfig' and not cls.__dialect__:
            raise NotImplementedError(f'attribute __dialect__ for {cls.__name__} is required')
        # print(f'{cls.__name__} --- {cls.__class__.__name__}._db_type = {cls.__dialect__}')

    def __int__(self, *args, **kwargs):
        # super(AnyDB, self).__int__(*args, *kwargs)
        # super(AnyDB, self).__int__(*args, *kwargs)
        # self.DB_TYPE = self._db_type
        # print(f'{self.__class__.__name__}._db_type = {self._db_type}')
        print('+|'*50)

    @classmethod
    def post_validate_is_async_and_driver(
        cls,
        driver: Optional[AnyDriver],
        db_is_async: Optional[bool],
        driver_cls: type[AnyDriver],
        db_type: str
    ) -> tuple[bool, Optional[AnyDriver]]:
        async_drivers = driver_cls.async_drivers
        if db_is_async is None and driver is None:
            # Set asynchronous connection to the database by default
            db_is_async = True
            if async_drivers:
                async_driver = async_drivers[0]
            else:
                raise ValueError(f"{db_type} does not support asynchronous connection")
            driver = driver_cls(
                async_driver,
                is_async=db_is_async
            )
        elif db_is_async and driver is None:
            # Set asynchronous driver
            if async_drivers:
                async_driver = async_drivers[0]
            else:
                raise ValueError(f"{db_type} does not support asynchronous connection")
            driver = driver_cls(
                async_driver,
                is_async=db_is_async
            )
        elif db_is_async is None and driver:
            db_is_async = driver.is_async

        if db_is_async is False and driver and driver.is_async:
            raise ValueError(
                f"Can't create synchronous connection to database with asynchronous driver={driver}. "
                f"Please change DRIVER or DB_ASYNC."
            )
        elif db_is_async and driver and not driver.is_async:
            raise ValueError(
                f"Can't create asynchronous connection to database with synchronous driver={driver}. "
                f"Please change DRIVER or DB_ASYNC."
            )
        return db_is_async, driver

class BaseDBConfig(AnyDB):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    DATABASE: str

    # class Config:
    #     env_prefix = ""
    #     fields = {
    #         'HOST': {
    #             'env': [f'{env_prefix}host', 'host'],
    #         },
    #         'PORT': {
    #             'env': [f'{env_prefix}port', 'port']
    #         },
    #         'USER': {
    #             'env': [f'{env_prefix}user', 'user']
    #         },
    #         'PASSWORD': {
    #             'env': [f'{env_prefix}password', 'password']
    #         },
    #         'DATABASE': {
    #             'env': [f'{env_prefix}database', 'database']
    #         },
    #     }
