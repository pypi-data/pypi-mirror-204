
from flowhigh.model.BetweenType import BetweenType
from flowhigh.model.Direction import Direction
from flowhigh.model.ExprExprCollectionHolder import ExprExprCollectionHolder
from flowhigh.model.TypeCast import TypeCast


class Frame(ExprExprCollectionHolder, TypeCast):
    upperPosition: str = None
    lowerPosition: str = None
    exprs: list = []
    upperLimit: str = None
    lowerLimit: str = None
    type_: BetweenType = None

    def __init__(self):
        super().__init__()



from flowhigh.model.TreeNode import TreeNode

class FrameBuilder (object):
    construction: Frame

    
    def __init__(self) -> None:
        super().__init__()
        self.construction = Frame()
    
    def with_upperPosition(self, upperPosition: str):
        child = upperPosition
        self.construction.upperPosition = child
    
    def with_pos(self, pos: str):
        child = pos
        self.construction.pos = child
    
    def with_lowerPosition(self, lowerPosition: str):
        child = lowerPosition
        self.construction.lowerPosition = child
    
    def with_alias(self, alias: str):
        child = alias
        self.construction.alias = child
    
    def with_exprs(self, exprs: list):
        child = exprs
        for node in list(filter(lambda el: TreeNode in el.__class__.mro(), exprs)):
            self.construction.add_child(node)
        self.construction.exprs = child
    
    def with_upperLimit(self, upperLimit: str):
        child = upperLimit
        self.construction.upperLimit = child
    
    def with_lowerLimit(self, lowerLimit: str):
        child = lowerLimit
        self.construction.lowerLimit = child
    
    def with_type(self, type_: BetweenType):
        child = type_
        self.construction.type_ = child
    
    def with_direction(self, direction: Direction):
        child = direction
        self.construction.direction = child

    def build(self):
        return self.construction
