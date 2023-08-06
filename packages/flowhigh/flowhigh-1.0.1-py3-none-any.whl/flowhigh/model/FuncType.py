from enum import Enum


class FuncType(Enum):
    agg = 1
    window = 2
    scalar = 3

