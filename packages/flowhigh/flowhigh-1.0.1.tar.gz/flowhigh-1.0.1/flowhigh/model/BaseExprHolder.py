
from flowhigh.model.Expr import Expr
from flowhigh.model.CoordinateBlock import CoordinateBlock
from flowhigh.model.ExprHolder import ExprHolder


class BaseExprHolder(CoordinateBlock, ExprHolder):
    pos: str = None
    expr: Expr = None

    def __init__(self):
        super().__init__()



