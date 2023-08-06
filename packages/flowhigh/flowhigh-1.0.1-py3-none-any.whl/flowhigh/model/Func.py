
from flowhigh.model.FuncType import FuncType
from flowhigh.model.Quantifier import Quantifier
from flowhigh.model.Sort import Sort
from flowhigh.model.Direction import Direction
from flowhigh.model.ExprExprCollectionHolder import ExprExprCollectionHolder
from flowhigh.model.Named import Named
from flowhigh.model.TypeCast import TypeCast


class Func(ExprExprCollectionHolder, Named, TypeCast):
    name: str = None
    withinGroup: Sort = None
    exprs: list = []
    type_: FuncType = None
    quantifier: Quantifier = None

    def __init__(self):
        super().__init__()



from flowhigh.model.TreeNode import TreeNode

class FuncBuilder (object):
    construction: Func

    
    def __init__(self) -> None:
        super().__init__()
        self.construction = Func()
    
    def with_pos(self, pos: str):
        child = pos
        self.construction.pos = child
    
    def with_withinGroup(self, withinGroup: Sort):
        child = withinGroup
        if TreeNode in Sort.mro():
            self.construction.add_child(child)
        self.construction.withinGroup = child
    
    def with_name(self, name: str):
        child = name
        self.construction.name = child
    
    def with_exprs(self, exprs: list):
        child = exprs
        for node in list(filter(lambda el: TreeNode in el.__class__.mro(), exprs)):
            self.construction.add_child(node)
        self.construction.exprs = child
    
    def with_alias(self, alias: str):
        child = alias
        self.construction.alias = child
    
    def with_quantifier(self, quantifier: Quantifier):
        child = quantifier
        self.construction.quantifier = child
    
    def with_type(self, type_: FuncType):
        child = type_
        self.construction.type_ = child
    
    def with_direction(self, direction: Direction):
        child = direction
        self.construction.direction = child

    def build(self):
        return self.construction
