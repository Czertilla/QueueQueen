from enum import Enum


class AEnum(Enum):
    __default__ = None
# TODO uncomment _missing_ meth
    # def _missing_(cls, value=None):
    #     return cls.__default__
