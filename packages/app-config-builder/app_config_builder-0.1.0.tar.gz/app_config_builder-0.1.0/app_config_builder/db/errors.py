from pydantic.errors import PydanticValueError, UrlError


__all__ = [
    "UrlPathError",
    "UrlSchemeDialectError",
    "UrlSchemeDriverError",
    "DatabaseDriverPermittedError",
]


class UrlPathError(UrlError):
    code = 'url.path'
    msg_template = 'invalid or missing URL path'


class UrlSchemeDialectError(UrlError):
    code = 'url.scheme.dialect'
    msg_template = 'invalid or missing URL scheme dialect'

    def __init__(self, given: str, allowed_dialect: str):
        super().__init__(given=given, allowed_dialect=allowed_dialect)


class UrlSchemeDriverError(UrlError):
    code = 'url.scheme.driver'
    msg_template = 'invalid URL scheme driver'

    def __init__(self, given: str, allowed_drivers: set[str]):
        super().__init__(given=given, allowed_drivers=allowed_drivers)


class DatabaseDriverPermittedError(PydanticValueError):
    code = 'database.driver'
    msg_template = 'database driver not permitted'

    def __init__(self, given: str, allowed_drivers: set[str]):
        super().__init__(given=given, allowed_drivers=allowed_drivers)
