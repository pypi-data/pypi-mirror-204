from enum import Enum


class Mode(str, Enum):
    prod = "prod"
    dev = "dev"
    test = "test"
