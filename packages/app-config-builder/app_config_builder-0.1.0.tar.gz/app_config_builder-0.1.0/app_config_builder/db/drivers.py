from typing import (
    TYPE_CHECKING,
    Optional,
    Dict,
    Any,
    Generator,
)

from pydantic.utils import update_not_none
from pydantic.validators import str_validator

from .errors import (
    DatabaseDriverPermittedError,
)

if TYPE_CHECKING:
    from pydantic.typing import AnyCallable

    CallableGenerator = Generator[AnyCallable, None, None]


__all__ = [
    "AnyDriver",
    "SqliteDriver",
    "PostgresqlDriver",
    "MySqlDriver",
]


class AnyDriver(str):
    sync_drivers: list[str] = []
    async_drivers: list[str] = []
    allowed_drivers: set[str] = set()
    min_length = 1
    max_length = 20

    __slots__ = ('is_async', )

    def __new__(cls, name: str, **kwargs) -> object:
        return str.__new__(cls,  name)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not cls.allowed_drivers:
            cls.allowed_drivers = set(cls.sync_drivers) | set(cls.async_drivers)

    def __init__(
        self,
        name: str,
        *,
        is_async: Optional[bool] = None,
    ) -> None:
        str.__init__(name)
        self.is_async = is_async
        if self.is_async is None:
            self.is_async = self.validate(name).is_async
        # if not self.allowed_drivers:
        #     self.allowed_drivers = set(self.sync_drivers) | set(self.async_drivers)

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        update_not_none(field_schema, minLength=cls.min_length, maxLength=cls.max_length)

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> 'AnyDriver':
        if value.__class__ == cls:
            return value
        value = str_validator(value)
        driver = value.strip()

        if driver not in cls.allowed_drivers:
            raise DatabaseDriverPermittedError(given=driver, allowed_drivers=cls.allowed_drivers)

        is_async = False
        if value in cls.async_drivers:
            is_async = True

        return cls(driver, is_async=is_async)

    def __repr__(self) -> str:
        extra = ', '.join(f'{n}={getattr(self, n)!r}' for n in self.__slots__ if getattr(self, n) is not None)
        return f'{self.__class__.__name__}({super().__repr__()}, {extra})'


class SqliteDriver(AnyDriver):
    sync_drivers = [
        "pysqlite",
    ]
    async_drivers = [
        "aiosqlite",
    ]


class PostgresqlDriver(AnyDriver):
    sync_drivers = [
        "psycopg2",
        "psycopg",
        "pg8000",
        "psycopg2cffi",     # является адаптацией psycopg2, использующей CFFI для уровня C. Настраивается как psycopg2
        # "pypostgresql",     # Не используется в SqlAlchemy2.0
        # "pygresql",         # Не используется в SqlAlchemy2.0
    ]
    async_drivers = [
        "asyncpg",          # https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#prepared-statement-name
        "psycopg",          # В sqlalchemy отличается только функция создания движка
        "psycopg_async",    # тот же psycopg, толь
    ]


class MySqlDriver(AnyDriver):
    # TODO: Все драйвера для MySql надо тестировать
    sync_drivers = [
        "mysqldb",  # Предпочтительный стабильный драйвер подключения, рекомендует Google
        "pymysql",  # стабильный драйвер подключения
        "mariadbconnector", # mariadb+mariadbconnector://требуется для использования этого драйвера.
        # "mysqlconnector",   # не тестируется, есть проблемы
        # "cymysql",    # не тестируется
        "pyodbc",   # внимательно подойти к созданию Dsn !!!!
    ]
    async_drivers = [
        "asyncmy",
        # "aiomysql",  # Устарел. Не работает с python >= 3.10
    ]
