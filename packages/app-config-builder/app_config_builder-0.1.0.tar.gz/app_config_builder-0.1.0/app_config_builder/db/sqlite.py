import re
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Union,
    Optional,
    Match,
    Pattern,
    no_type_check,
    Dict,
    Any,
    Generator,
    cast,
)

import pydantic
from pydantic import Field, root_validator
from pydantic.config import BaseConfig
from pydantic.fields import ModelField
from pydantic.utils import update_not_none
from pydantic.validators import constr_length_validator, str_validator

from .base import AnyDB
from .drivers import SqliteDriver as Driver, AnyDriver
from .errors import (
    UrlPathError,
    UrlSchemeDialectError,
    UrlSchemeDriverError,
    DatabaseDriverPermittedError,
)
from ..utils.func import get_absolute_path

if TYPE_CHECKING:
    from typing_extensions import TypedDict

    from pydantic.typing import AnyCallable

    CallableGenerator = Generator[AnyCallable, None, None]

    class Parts(TypedDict, total=False):
        scheme: Optional[str]
        path: Optional[str]
else:
    class Parts(dict):
        pass


DB_TYPE = "sqlite"
ENV_PREFIX = "sqlite_"
DB_EXT = ".sqlite3"


class SqliteDsn(str):
    min_length = 1
    max_length = 2**16

    __slots__ = ('driver', 'database_dir', 'database')

    @no_type_check
    def __new__(cls, url: Optional[str], **kwargs) -> object:
        return str.__new__(cls, cls.build(**kwargs) if url is None else url)

    def __init__(
        self,
        url: str | None,
        *,
        driver: Union[None, str, Driver] = None,
        database_dir: Optional[str] = None,
        database: Optional[str] = None,
    ) -> None:
        str.__init__(url)
        self.driver = driver
        self.database_dir = database_dir
        self.database = database
        if self.database is None:
            field = ModelField(
                name='DATABASE_URL', type_=Optional[SqliteDsn], required=False, default=None,
                model_config=BaseConfig(), class_validators={})
            dsn = self.validate(url, field=field, config=pydantic.BaseConfig())
            self.driver = dsn.driver
            self.database_dir = dsn.database_dir
            self.database = dsn.database

    @classmethod
    def build(
        cls,
        *,
        database: str,
        database_dir: str,
        driver: Optional[str] = None,
    ) -> str:
        scheme = 'sqlite'
        if driver:
            scheme = f'{scheme}+{driver}'
        database = database.rpartition('/')[-1]
        url = f'{scheme}://{database_dir}/{database}'
        return url

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        update_not_none(field_schema)

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield cls.validate

    @classmethod
    def validate(cls, value: Any, field: 'ModelField', config: 'BaseConfig') -> 'SqliteDsn':
        if value.__class__ == cls:
            return value
        value = str_validator(value)
        value = value.strip()
        url: str = cast(str, constr_length_validator(value, field, config))

        m = cls._match_url(url)
        # the regex should always match, if it doesn't please report with details of the URL tried
        assert m, 'URL regex failed unexpectedly'

        parts = cast('Parts', m.groupdict())
        parts = cls.validate_parts(parts)

        if m.end() != len(url):
            raise pydantic.errors.UrlExtraError(extra=url[m.end():])

        return cls._build_url(parts)

    @classmethod
    def _build_url(cls, parts: 'Parts') -> 'SqliteDsn':
        dialect, driver = cls.validate_scheme(parts['scheme'])
        database, database_dir = cls.validate_path(parts['path'])

        return cls(
            None,
            driver=driver,
            database_dir=database_dir,
            database=database,
        )

    @staticmethod
    def validate_scheme(scheme: str):
        dialect = driver = None
        scheme_items = scheme.lower().split('+')

        if len(scheme_items) == 1:
            dialect = scheme_items[0]
        elif len(scheme_items) == 2:
            dialect = scheme_items[0]
            driver = scheme_items[1]

        if dialect != DB_TYPE:
            raise UrlSchemeDialectError(given=dialect, allowed_dialect=DB_TYPE)

        if driver:
            try:
                driver = Driver(driver)
            except DatabaseDriverPermittedError:
                raise UrlSchemeDriverError(given=driver, allowed_drivers=Driver.allowed_drivers)

        return dialect, driver

    @staticmethod
    def validate_path(database_path: str):
        path = Path(database_path)
        database = path.name
        if database != ':memory:':
            ext = DB_EXT if not path.suffix else ''
            database = f'{database}{ext}'
        database_dir = path.parent.as_posix().removesuffix('/')
        return database, database_dir

    @classmethod
    def validate_parts(cls, parts: 'Parts') -> 'Parts':
        """
        A method used to validate parts of a URL.
        """
        scheme = parts['scheme']
        if scheme is None:
            raise pydantic.errors.UrlSchemeError()

        path = parts['path']
        if path is None:
            raise UrlPathError()

        return parts

    @staticmethod
    def _match_url(url: str) -> Optional[Match[str]]:
        scheme_regex = r'(?:(?P<scheme>[a-z][a-z0-9+\-.]+)://)?'
        path_regex = r'(?P<path>/[^\s?#]*)?'
        pattern: Pattern[str] = re.compile(
            rf'{scheme_regex}{path_regex}',
            re.IGNORECASE,
        )
        return pattern.match(url)

    def __repr__(self) -> str:
        extra = ', '.join(f'{n}={getattr(self, n)!r}' for n in self.__slots__ if getattr(self, n) is not None)
        return f'{self.__class__.__name__}({super().__repr__()}, {extra})'


class SqliteDB(AnyDB):
    """SQLITE database settings."""

    __dialect__ = "sqlite"

    DB_TYPE: str = Field(default=DB_TYPE, const=True)
    # DB_ASYNC: bool | None = Field(default=DB_ASYNC, env='db_async')
    # ECHO_SQL: bool = Field(default=ECHO_SQL, env='echo_sql')
    # DB_MODE: str = Field(default=DB_MODE, env='db_mode')
    DRIVER: Driver | None = Field(default=None, env=[f'{ENV_PREFIX}driver', 'driver'])
    DATABASE: str = Field(default=":memory:", env=[f'{ENV_PREFIX}database', 'database'])
    DATABASE_DIR: str = Field(default='db', env=[f'{ENV_PREFIX}database_dir', 'database_dir'])
    PATH_DB_IS_ABSOLUTE: bool = Field(
        default=False,
        env=[f'{ENV_PREFIX}path_db_is_absolute', 'path_db_is_absolute'],
        exclude=True
    )
    DATABASE_URL: SqliteDsn | None = Field(default=None, env=[f'{ENV_PREFIX}database_url', 'database_url'])

    @root_validator
    def post_load(cls, values):     # noqa
        db_type: str = values.get('DB_TYPE')
        db_is_async: bool | None = values.get('DB_ASYNC')
        driver: Driver = values.get('DRIVER')
        database: str = values.get('DATABASE')
        database_dir: str = values.get('DATABASE_DIR')
        database_url: SqliteDsn = values.get('DATABASE_URL')
        path_is_absolute: bool = values.get('PATH_DB_IS_ABSOLUTE')

        if database_url:
            database = database_url.database
            database_dir = database_url.database_dir
            driver = database_url.driver
            db_is_async = driver.is_async if driver is not None else False
        else:
            db_is_async, driver = cls.post_validate_is_async_and_driver(driver, db_is_async, Driver, db_type)
            # async_drivers = Driver.async_drivers
            # if db_is_async is None and driver is None:
            #     # Set asynchronous connection to the database by default
            #     db_is_async = True
            #     if async_drivers:
            #         async_driver = async_drivers[0]
            #     else:
            #         raise ValueError(f"{DB_TYPE} does not support asynchronous connection")
            #     driver = Driver(
            #         async_driver,
            #         is_async=db_is_async
            #     )
            # elif db_is_async and driver is None:
            #     # Set asynchronous driver
            #     if async_drivers:
            #         async_driver = async_drivers[0]
            #     else:
            #         raise ValueError(f"{DB_TYPE} does not support asynchronous connection")
            #     driver = Driver(
            #         async_driver,
            #         is_async=db_is_async
            #     )
            # elif db_is_async is None and driver:
            #     db_is_async = driver.is_async
            #
            # if db_is_async is False and driver and driver.is_async:
            #     raise ValueError(
            #         f"Can't create synchronous connection to database with asynchronous driver={driver}. "
            #         f"Please change DRIVER or DB_ASYNC."
            #     )
            # elif db_is_async and driver and not driver.is_async:
            #     raise ValueError(
            #         f"Can't create asynchronous connection to database with synchronous driver={driver}. "
            #         f"Please change DRIVER or DB_ASYNC."
            #     )

        database = database.removesuffix('/').removeprefix('/')
        if database == ':memory:':
            database_dir = ''
        else:
            path = Path(database)
            ext = DB_EXT if not path.suffix else ''
            database = f'{database}{ext}'
            database_dir = database_dir.removesuffix('/').removeprefix('/')
            if database_dir:
                database_dir = f'/{database_dir}'

        database = database.rpartition('/')[-1]

        if not path_is_absolute:
            if database != ':memory:':
                database_dir = get_absolute_path(database_dir)

        database_url = SqliteDsn(
            None,
            database=database,
            database_dir=database_dir,
            driver=driver,
        )

        values['DB_ASYNC'] = db_is_async
        values['DATABASE'] = database
        values['DATABASE_DIR'] = database_dir
        values['DRIVER'] = driver
        values['DATABASE_URL'] = database_url
        values['PATH_DB_IS_ABSOLUTE'] = True

        return values

    class Config:
        @classmethod
        def customise_sources(
                cls,
                init_settings,
                env_settings,
                file_secret_settings,
        ):
            return (
                init_settings,
                env_settings,
                file_secret_settings,
            )


