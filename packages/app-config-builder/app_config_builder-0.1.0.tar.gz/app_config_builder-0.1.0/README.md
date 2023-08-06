# app_configs

Fast, highly flexible and intuitive creation of application configurations with built-in data validation.

The basic idea is to store multiple settings of the same type, such as database connection settings, and switch instantly when one or more arguments or environment variables are changed. Almost all settings can be overridden without any python programming experience.

The project is inspired by and based on the [Pedantic](https://github.com/pydantic/pydantic) data validation library.

The package is currently a work in progress and subject to significant change.


## Roadmap

The plan is to add the most flexible Dsn configuration for the many python packages that use network connectivity, such as PostgreSql, MySql, MsSql, Oracle, MongoDb, ClickHouse, Rabbit, Redis, Tarantool, Kafka, etc.
