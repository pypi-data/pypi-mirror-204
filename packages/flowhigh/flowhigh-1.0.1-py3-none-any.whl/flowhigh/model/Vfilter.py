
from flowhigh.model.BaseExprCollectionHolder import BaseExprCollectionHolder


class Vfilter(BaseExprCollectionHolder):

    def __init__(self):
        super().__init__()



from flowhigh.model.TreeNode import TreeNode

class VfilterBuilder (object):
    construction: Vfilter

    
    def __init__(self) -> None:
        super().__init__()
        self.construction = Vfilter()
    
    def with_pos(self, pos: str):
        child = pos
        self.construction.pos = child
    
    def with_exprs(self, exprs: list):
        child = exprs
        for node in list(filter(lambda el: TreeNode in el.__class__.mro(), exprs)):
            self.construction.add_child(node)
        self.construction.exprs = child

    def build(self):
        return self.construction
