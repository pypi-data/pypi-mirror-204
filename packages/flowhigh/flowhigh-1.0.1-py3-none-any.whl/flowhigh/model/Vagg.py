
from flowhigh.model.Vfilter import Vfilter
from flowhigh.model.CoordinateBlock import CoordinateBlock


class Vagg(CoordinateBlock):
    vfilter: Vfilter = None

    def __init__(self):
        super().__init__()



from flowhigh.model.TreeNode import TreeNode

class VaggBuilder (object):
    construction: Vagg

    
    def __init__(self) -> None:
        super().__init__()
        self.construction = Vagg()
    
    def with_pos(self, pos: str):
        child = pos
        self.construction.pos = child
    
    def with_vfilter(self, vfilter: Vfilter):
        child = vfilter
        if TreeNode in Vfilter.mro():
            self.construction.add_child(child)
        self.construction.vfilter = child

    def build(self):
        return self.construction
