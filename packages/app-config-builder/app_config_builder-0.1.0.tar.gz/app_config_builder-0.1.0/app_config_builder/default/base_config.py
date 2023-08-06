from pathlib import Path
from typing import (
    Literal,
)

from pydantic.config import Extra
from pydantic.fields import Field

from ..advanced_config import AdvancedConfig
from ..constants import (
    BASE_DIR,
    WINDOWS,
    PROJECT_NAME,
    MODE,
    DEBUG,
    # LOGS_DIR,
    # CREATE_LOG_FILES,
    # ROOT_LOGGER,
)


class AppDefaultConfig(AdvancedConfig, extra=Extra.allow):
    """App default config."""

    BASE_DIR: str | Path = Field(default=BASE_DIR, const=True)
    WINDOWS: bool = Field(default=WINDOWS, exclude=True, const=True)

    PROJECT_NAME: str = Field(PROJECT_NAME)
    MODE: Literal['prod', 'dev', 'test'] = Field(MODE)
    DEBUG: bool = Field(DEBUG)

    # LOGS_DIR: str = Field(LOGS_DIR)
    # CREATE_LOG_FILES: bool = Field(CREATE_LOG_FILES)
    # ROOT_LOGGER: str = Field(ROOT_LOGGER)


# def add_fields(cls, **field_definitions: Any):
#     new_fields: Dict[str, ModelField] = {}
#     new_annotations: Dict[str, Optional[type]] = {}
#
#     for f_name, f_def in field_definitions.items():
#         if isinstance(f_def, tuple):
#             try:
#                 f_annotation, f_value = f_def
#             except ValueError as e:
#                 raise Exception(
#                     'field definitions should either be a tuple of (<type>, <default>) or just a '
#                     'default value, unfortunately this means tuples as '
#                     'default values are not allowed'
#                 ) from e
#         else:
#             f_annotation, f_value = None, f_def
#
#         if f_annotation:
#             new_annotations[f_name] = f_annotation
#
#         new_fields[f_name] = ModelField.infer(
#             name=f_name,
#             value=f_value,
#             annotation=f_annotation,
#             class_validators=None,
#             config=cls.__config__
#         )
#         setattr(cls, f_name, f_value)
#
#     cls.__fields__.update(new_fields)
#     cls.__annotations__.update(new_annotations)
