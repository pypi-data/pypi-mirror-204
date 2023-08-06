from enum import Enum


class WFuncType(Enum):
    agg = 1
    rank = 2
    general = 3
    regression = 4
    estimation = 5
    statistics = 6
    unknown = 7

