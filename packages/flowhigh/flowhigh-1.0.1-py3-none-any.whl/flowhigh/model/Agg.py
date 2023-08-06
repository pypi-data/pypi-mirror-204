
from flowhigh.model.Filter import Filter
from flowhigh.model.BaseExprCollectionHolder import BaseExprCollectionHolder
from flowhigh.model.Searchable import Searchable


class Agg(BaseExprCollectionHolder, Searchable):
    filter_: Filter = None

    def __init__(self):
        super().__init__()



from flowhigh.model.TreeNode import TreeNode

class AggBuilder (object):
    construction: Agg

    
    def __init__(self) -> None:
        super().__init__()
        self.construction = Agg()
    
    def with_filter(self, filter_: Filter):
        child = filter_
        if TreeNode in Filter.mro():
            self.construction.add_child(child)
        self.construction.filter_ = child
    
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
