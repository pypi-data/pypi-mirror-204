from .db_type import config_db_type, AllowedDbType
from .sqlite import SqliteDB

DatabaseConfig: type | None = None

if config_db_type == AllowedDbType.sqlite:
    DatabaseConfig = SqliteDB
# elif config_db_type == AllowedDbType.postgresql:
    # DatabaseConfig = PostgresqlDB
