import re
from typing import Any

from pydantic.validators import strict_str_validator


class Username(str):

    min_len = 4
    max_len = 40
    pattern = re.compile(r'^(?=.*[a-zA-Z])[\w+.-]+$')

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update(type='string', format='username', example='sasha_molodez')

    @classmethod
    def __get_validators__(cls):
        yield strict_str_validator
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        if cls.pattern.match(v) is None:
            raise ValueError('Username is invalid')
        if getattr(cls, 'max_len', None) and len(v) > cls.max_len:
            raise ValueError('Username is too long')
        if getattr(cls, 'min_len', None) and len(v) < cls.min_len:
            raise ValueError('Username is too short')
        return cls(v)
