
from flowhigh.model.DsType import DsType
from flowhigh.model.DsSubType import DsSubType
from flowhigh.model.DsAction import DsAction
from flowhigh.model.Out import Out
from flowhigh.model.In import In
from flowhigh.model.Filter import Filter
from flowhigh.model.Agg import Agg
from flowhigh.model.Vagg import Vagg
from flowhigh.model.Sort import Sort
from flowhigh.model.Page import Page
from flowhigh.model.MatchRecognize import MatchRecognize
from flowhigh.model.TableSample import TableSample
from flowhigh.model.Direction import Direction
from flowhigh.model.BaseExpr import BaseExpr
from flowhigh.model.ReferencableExpr import ReferencableExpr
from flowhigh.model.Named import Named
from flowhigh.model.Searchable import Searchable
from flowhigh.model.TypeCast import TypeCast


class Ds(BaseExpr, ReferencableExpr, Named, Searchable, TypeCast):
    agg: Agg = None
    refsch: str = None
    fullref: str = None
    refdb: str = None
    in_: In = None
    matchRecognize: MatchRecognize = None
    setOp: list = []
    sort: Sort = None
    type_: DsType = None
    out: Out = None
    filter_: Filter = None
    tableSample: TableSample = None
    pos: str = None
    refds: str = None
    name: str = None
    action: DsAction = None
    alias: str = None
    subType: DsSubType = None
    refTo: str = None
    page: Page = None
    vagg: Vagg = None
    sameAs: list = []
    direction: Direction = None

    def __init__(self):
        super().__init__()



from flowhigh.model.TreeNode import TreeNode

class DsBuilder (object):
    construction: Ds

    
    def __init__(self) -> None:
        super().__init__()
        self.construction = Ds()
    
    def with_agg(self, agg: Agg):
        child = agg
        if TreeNode in Agg.mro():
            self.construction.add_child(child)
        self.construction.agg = child
    
    def with_refsch(self, refsch: str):
        child = refsch
        self.construction.refsch = child
    
    def with_fullref(self, fullref: str):
        child = fullref
        self.construction.fullref = child
    
    def with_refdb(self, refdb: str):
        child = refdb
        self.construction.refdb = child
    
    def with_in(self, in_: In):
        child = in_
        if TreeNode in In.mro():
            self.construction.add_child(child)
        self.construction.in_ = child
    
    def with_setOp(self, setOp: list):
        child = setOp
        for node in list(filter(lambda el: TreeNode in el.__class__.mro(), setOp)):
            self.construction.add_child(node)
        self.construction.setOp = child
    
    def with_matchRecognize(self, matchRecognize: MatchRecognize):
        child = matchRecognize
        if TreeNode in MatchRecognize.mro():
            self.construction.add_child(child)
        self.construction.matchRecognize = child
    
    def with_sort(self, sort: Sort):
        child = sort
        if TreeNode in Sort.mro():
            self.construction.add_child(child)
        self.construction.sort = child
    
    def with_type(self, type_: DsType):
        child = type_
        self.construction.type_ = child
    
    def with_out(self, out: Out):
        child = out
        if TreeNode in Out.mro():
            self.construction.add_child(child)
        self.construction.out = child
    
    def with_tableSample(self, tableSample: TableSample):
        child = tableSample
        if TreeNode in TableSample.mro():
            self.construction.add_child(child)
        self.construction.tableSample = child
    
    def with_filter(self, filter_: Filter):
        child = filter_
        if TreeNode in Filter.mro():
            self.construction.add_child(child)
        self.construction.filter_ = child
    
    def with_pos(self, pos: str):
        child = pos
        self.construction.pos = child
    
    def with_refds(self, refds: str):
        child = refds
        self.construction.refds = child
    
    def with_name(self, name: str):
        child = name
        self.construction.name = child
    
    def with_action(self, action: DsAction):
        child = action
        self.construction.action = child
    
    def with_alias(self, alias: str):
        child = alias
        self.construction.alias = child
    
    def with_subType(self, subType: DsSubType):
        child = subType
        self.construction.subType = child
    
    def with_page(self, page: Page):
        child = page
        if TreeNode in Page.mro():
            self.construction.add_child(child)
        self.construction.page = child
    
    def with_refTo(self, refTo: str):
        child = refTo
        self.construction.refTo = child
    
    def with_vagg(self, vagg: Vagg):
        child = vagg
        if TreeNode in Vagg.mro():
            self.construction.add_child(child)
        self.construction.vagg = child
    
    def with_sameAs(self, sameAs: list):
        child = sameAs
        for node in list(filter(lambda el: TreeNode in el.__class__.mro(), sameAs)):
            self.construction.add_child(node)
        self.construction.sameAs = child
    
    def with_direction(self, direction: Direction):
        child = direction
        self.construction.direction = child

    def build(self):
        return self.construction
