from typing import Literal
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

import logging

class Config(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=(".env.dev", ".env"),
        env_ignore_empty=True,
        case_sensitive=False,
        extra="ignore",
    )

    vendor: str = ''
    model: str = ''
    daemon: bool = False
    alarm: Literal['ignore', 'dbus', 'poweroff'] = 'ignore'
    interval: int = 3
    loglevel: int

    #
    @field_validator('loglevel', mode='before')
    def validate_loglevel(ll: str) -> int:
        retval = logging.getLevelName(ll.upper())

        # dummy check 
        if not isinstance(retval, int):
            retval = logging.NOTSET

        return retval