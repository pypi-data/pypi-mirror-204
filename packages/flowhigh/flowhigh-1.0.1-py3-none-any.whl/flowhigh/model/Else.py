
from flowhigh.model.Expr import Expr
from flowhigh.model.BaseExprHolder import BaseExprHolder


class Else(BaseExprHolder):

    def __init__(self):
        super().__init__()



from flowhigh.model.TreeNode import TreeNode

class ElseBuilder (object):
    construction: Else

    
    def __init__(self) -> None:
        super().__init__()
        self.construction = Else()
    
    def with_pos(self, pos: str):
        child = pos
        self.construction.pos = child
    
    def with_expr(self, expr: Expr):
        child = expr
        if TreeNode in Expr.mro():
            self.construction.add_child(child)
        self.construction.expr = child

    def build(self):
        return self.construction
