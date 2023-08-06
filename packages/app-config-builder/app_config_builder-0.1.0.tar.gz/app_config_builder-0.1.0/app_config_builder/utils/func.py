from pathlib import Path
from typing import (
    Any,
    Dict,
    Optional,
)

from pydantic import BaseModel
from pydantic.fields import ModelField

from ..constants import BASE_DIR

def add_fields(cls:BaseModel, **field_definitions: Any):
    """Динамическое добавление полей в модель pydantic."""

    new_fields: Dict[str, ModelField] = {}
    new_annotations: Dict[str, Optional[type]] = {}

    for f_name, f_def in field_definitions.items():
        if isinstance(f_def, tuple):
            try:
                f_annotation, f_value = f_def
            except ValueError as e:
                raise Exception(
                    'field definitions should either be a tuple of (<type>, <default>) or just a '
                    'default value, unfortunately this means tuples as '
                    'default values are not allowed'
                ) from e
        else:
            f_annotation, f_value = None, f_def

        if f_annotation:
            new_annotations[f_name] = f_annotation

        new_fields[f_name] = ModelField.infer(
            name=f_name,
            value=f_value,
            annotation=f_annotation,
            class_validators=None,
            config=cls.__config__
        )
        setattr(cls, f_name, f_value)

    cls.__fields__.update(new_fields)
    cls.__annotations__.update(new_annotations)


def get_absolute_path(path: str | Path) -> str:
    if isinstance(path, Path):
        path = path.as_posix()

    base_dir = str(BASE_DIR).removesuffix("/")
    if not path.startswith(base_dir):
        path = path.removeprefix('/')
        if not path:
            return base_dir
        path = f'{base_dir}/{path}'
    return path
