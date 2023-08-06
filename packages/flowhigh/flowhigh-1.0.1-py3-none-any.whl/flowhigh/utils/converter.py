import requests
import json

from requests import RequestException, Timeout
from typing import Type, Tuple, Union
from flowhigh.auth import Authentication
from flowhigh.model.TreeNode import RegistryBase, TreeNode
from flowhigh.model import *
from flowhigh.model.Delete import DeleteBuilder
from flowhigh.model.Op import OpBuilder
from flowhigh.model.InlineTable import InlineTableBuilder
from flowhigh.model.Page import PageBuilder
from flowhigh.model.Insert import InsertBuilder
from flowhigh.model.Update import UpdateBuilder
from flowhigh.model.DeleteStatement import DeleteStatementBuilder
from flowhigh.model.CreateView import CreateViewBuilder
from flowhigh.model.InsertStatement import InsertStatementBuilder
from flowhigh.model.Attr import AttrBuilder
from flowhigh.model.CreateStage import CreateStageBuilder
from flowhigh.model.Sort import SortBuilder
from flowhigh.model.Then import ThenBuilder
from flowhigh.model.MergeStatement import MergeStatementBuilder
from flowhigh.model.MultiValue import MultiValueBuilder
from flowhigh.model.AntiPattern import AntiPatternBuilder
from flowhigh.model.UpdateStatement import UpdateStatementBuilder
from flowhigh.model.QueryingStage import QueryingStageBuilder
from flowhigh.model.Position import PositionBuilder
from flowhigh.model.Const import ConstBuilder
from flowhigh.model.ColumnDef import ColumnDefBuilder
from flowhigh.model.Vfilter import VfilterBuilder
from flowhigh.model.Ds import DsBuilder
from flowhigh.model.Out import OutBuilder
from flowhigh.model.Copy import CopyBuilder
from flowhigh.model.Current import CurrentBuilder
from flowhigh.model.Cast import CastBuilder
from flowhigh.model.Frame import FrameBuilder
from flowhigh.model.Vagg import VaggBuilder
from flowhigh.model.Rotate import RotateBuilder
from flowhigh.model.In import InBuilder
from flowhigh.model.Func import FuncBuilder
from flowhigh.model.Case import CaseBuilder
from flowhigh.model.StructRef import StructRefBuilder
from flowhigh.model.AntiPatterns import AntiPatternsBuilder
from flowhigh.model.Create import CreateBuilder
from flowhigh.model.MatchRecognize import MatchRecognizeBuilder
from flowhigh.model.Asterisk import AsteriskBuilder
from flowhigh.model.Agg import AggBuilder
from flowhigh.model.Wfunc import WfuncBuilder
from flowhigh.model.Statement import StatementBuilder
from flowhigh.model.ParSeQL import ParSeQLBuilder
from flowhigh.model.TableSample import TableSampleBuilder
from flowhigh.model.Error import ErrorBuilder
from flowhigh.model.Join import JoinBuilder
from flowhigh.model.When import WhenBuilder
from flowhigh.model.Merge import MergeBuilder
from flowhigh.model.Filter import FilterBuilder
from flowhigh.model.TableFunc import TableFuncBuilder
from flowhigh.model.Else import ElseBuilder
from flowhigh.model.Edge import EdgeBuilder


class FlowHighSubmissionClass (object):

    _message: dict

    @property
    def json_message(self):
        return json.dumps({k: v for k, v in self._message.items() if k != 'xml'}, indent=4)

    @property
    def xml_message(self):
        return self._message['xml']

    def __init__(self, response: dict):
        self._message = response
        self._parsed_tree = self._convert_node(response)

    @classmethod
    def from_txt_response(cls, res: str):
        json_data = json.loads(res)
        return cls(response=json_data)

    @classmethod
    def from_sql(cls, sql: str):
        try:
            access_token = Authentication.authenticate_user()
            assert access_token, "UNAUTHENTICATED!"
            headers = {
                "User-Agent": "python/sqlanalyzer-0.0.1",
                "Content-type": "application/json",
                "Authorization": "Bearer " + access_token
            }
            url = "https://fhdev.sonra.io/api/process"
            data = {"sql": sql, "json": True, "xml": True}
            response = requests.post(url, json=data, headers=headers, timeout=5)
            # refresh token is invalid -> retry authentication
            if response.status_code == 401:
                access_token = Authentication.request_device_code()
                headers = {
                    "User-Agent": "python/sqlanalyzer-0.0.1",
                    "Content-type": "application/json",
                    "Authorization": "Bearer " + access_token
                }
                response = requests.post(url, json=data, headers=headers, timeout=5)
            # empty response from client
            if response.status_code == 204:
                raise RequestException("API is not available")
            # status code >= 400
            response.raise_for_status()
            json_data = json.loads(response.content)
            return cls(response=json_data)
        except Timeout as e:
            raise RequestException("API is not available") from e

    @classmethod
    def from_file(cls, name: str):
        if not name.endswith(".sql"):
            name = name + ".sql"
        with open(name, "r") as fp:
            txt = "".join(fp.readlines())
        return cls.from_sql(sql=txt)

    def get_statements(self):
        return self._parsed_tree.statement

    @classmethod
    def get_main_dataset(cls, statement: Statement):
        return statement.ds[-1]

    def get_input(self, statement: Statement):
        return self.get_main_dataset(statement).in_

    def get_antipattern_of_statement(self, statement: Statement):
        """
        Returns the Anti-patterns for a statement
        :param statement: The Statement object whose Anti-patterns needs to be returned
        :return: Anti-patterns of the Statement object
        """
        return statement.antiPatterns

    def get_all_antipatterns(self):
        """
        Returns Anti-Patterns of all the statements
        :return: List of Anti-patterns of all the statements
        """
        antipatterns: list = []
        statements = self.get_statements()
        for statement in statements:
            antipatterns.extend(statement.antiPatterns)

        return antipatterns

    @classmethod
    def get_nodes_by_types(cls, types: Union[Tuple, str]):
        """
        Get the list of nodes in tree of a given type
        :param types: the type or the tuple of types
        :return: list of nodes that match the given types
        """
        return list(filter(lambda x: isinstance(x, types), RegistryBase.get_registry()))

    @classmethod
    def get_raw_query(cls, statement: Statement):
        """
        Get the raw query text
        :param statement:
        :return: the sql input
        """
        return statement.rawInput

    @classmethod
    def get_node_raw_text(cls, node):
        """
        Get the sql text at the node's coordinates in query
        :param node:
        :return: the sql at the node's coordinates
        """
        if not node.pos:
            return
        stat = cls.find_first_ancestor_of_type(node, Statement)
        source_lower_bound, source_upper_bound = node.pos.split('-')
        return cls.get_raw_query(stat)[int(source_lower_bound): int(source_upper_bound)]

    @classmethod
    def get_ds_name(cls, node):
        """
        Get the node's dataset name
        :param node:
        :return: name of the node's dataset
        """
        if getattr(node, "alias", None):
            return node.alias
        if getattr(node, "refds", None):
            return node.refds
        ancestor = cls.find_first_ancestor_of_type(node, Ds)
        return ancestor.alias or ancestor.refds

    @classmethod
    def is_set_operation(cls, statement: Statement):
        """
        Check if input queries are combined by set operators
        :param statement:
        :return: True if any of INTERSECT/MINUS/EXCEPT/UNION [ ALL ] in query
        """
        return getattr(cls.get_main_dataset(statement), "setOp", None)

    @classmethod
    def get_set_operator(cls, statement: Statement):
        """
        Extract the set operator from query
        :param statement:
        :return: Any of INTERSECT/MINUS/EXCEPT/UNION [ ALL ]
        """
        return cls.get_main_dataset(statement).setOp

    @classmethod
    def search_node_by_id(cls, node_id: int):
        """
        Find a node in the tree based on its id
        :param node_id:
        :return: a node with the given id or None
        """
        return RegistryBase.search(node_id)

    @classmethod
    def search_node_by_pos(cls, pos: str):
        """
        Find a node based on its position in query
        :param pos:
        :return: the node at the given coordinates or None
        """
        return next(filter(lambda x: x.pos == pos, RegistryBase.get_registry()), None)

    @classmethod
    def get_out_columns(cls, statement):
        """
        Get the set of columns returned by the input query
        :param statement:
        :return: the set of columns returned by the input query
        """
        out = cls.get_main_dataset(statement).out
        return out.exprs

    @classmethod
    def find_first_ancestor_of_type(cls, node: TreeNode, clazz: Union[Tuple, TreeNode]):
        """
        Find the node's immediate ancestor by its type
        :param node:
        :param clazz:
        :return: the node's ancestor or None
        """
        if node.get_parent() is None:
            return None
        parent_obj = node.get_parent()
        if isinstance(parent_obj, clazz):
            return parent_obj
        return cls.find_first_ancestor_of_type(parent_obj, clazz)

    @classmethod
    def find_descendants_of_type(cls, node: TreeNode, clazz: Union[Tuple, TreeNode]):
        """
        Find the list of children based on their type
        :param node:
        :param clazz:
        :return: the set of descendants
        """
        def _find_descendants_of_type(source_obj, accum):
            if not source_obj:
                return
            if isinstance(source_obj, clazz):
                accum.append(source_obj)
                return
            for child in source_obj.get_children():
                _find_descendants_of_type(child, accum)
        l = []
        _find_descendants_of_type(node, l)
        return l

    
    def _convert_Delete(self, kwargs):
        obj = DeleteBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "ds" in kwargs:
            obj.with_ds(self._convert_node(kwargs["ds"]))
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Op(self, kwargs):
        obj = OpBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "exprs" in kwargs:
            obj.with_exprs([self._convert_node(f) for f in kwargs["exprs"]])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_InlineTable(self, kwargs):
        obj = InlineTableBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "exprs" in kwargs:
            obj.with_exprs([self._convert_node(f) for f in kwargs["exprs"]])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Page(self, kwargs):
        obj = PageBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "value" in kwargs:
            obj.with_value(self._convert_node(kwargs["value"]))
        return obj.build()
    
    def _convert_Insert(self, kwargs):
        obj = InsertBuilder()
        if "isElse" in kwargs:
            obj.with_isElse(kwargs["isElse"])
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "elseIntos" in kwargs:
            obj.with_elseIntos([self._convert_node(f) for f in kwargs["elseIntos"]])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "insert_type" in kwargs:
            obj.with_insert_type(kwargs["insert_type"])
        if "conditionalIntos" in kwargs:
            obj.with_conditionalIntos([self._convert_node(f) for f in kwargs["conditionalIntos"]])
        if "overwrite" in kwargs:
            obj.with_overwrite(kwargs["overwrite"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Update(self, kwargs):
        obj = UpdateBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "ds" in kwargs:
            obj.with_ds(self._convert_node(kwargs["ds"]))
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_DeleteStatement(self, kwargs):
        obj = DeleteStatementBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "merge" in kwargs:
            obj.with_merge([self._convert_node(f) for f in kwargs["merge"]])
        if "create" in kwargs:
            obj.with_create([self._convert_node(f) for f in kwargs["create"]])
        if "antiPatterns" in kwargs:
            obj.with_antiPatterns([self._convert_node(f) for f in kwargs["antiPatterns"]])
        if "createStage" in kwargs:
            obj.with_createStage([self._convert_node(f) for f in kwargs["createStage"]])
        if "insert" in kwargs:
            obj.with_insert([self._convert_node(f) for f in kwargs["insert"]])
        if "update" in kwargs:
            obj.with_update([self._convert_node(f) for f in kwargs["update"]])
        if "rawInput" in kwargs:
            obj.with_rawInput(kwargs["rawInput"])
        if "copy" in kwargs:
            obj.with_copy([self._convert_node(f) for f in kwargs["copy"]])
        if "createView" in kwargs:
            obj.with_createView([self._convert_node(f) for f in kwargs["createView"]])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "delete" in kwargs:
            obj.with_delete([self._convert_node(f) for f in kwargs["delete"]])
        if "ds" in kwargs:
            obj.with_ds([self._convert_node(f) for f in kwargs["ds"]])
        return obj.build()
    
    def _convert_CreateView(self, kwargs):
        obj = CreateViewBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "columns" in kwargs:
            obj.with_columns([self._convert_node(f) for f in kwargs["columns"]])
        if "query" in kwargs:
            obj.with_query(self._convert_node(kwargs["query"]))
        if "notExists" in kwargs:
            obj.with_notExists(kwargs["notExists"])
        if "replace" in kwargs:
            obj.with_replace(kwargs["replace"])
        if "dataset" in kwargs:
            obj.with_dataset(self._convert_node(kwargs["dataset"]))
        return obj.build()
    
    def _convert_InsertStatement(self, kwargs):
        obj = InsertStatementBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "merge" in kwargs:
            obj.with_merge([self._convert_node(f) for f in kwargs["merge"]])
        if "create" in kwargs:
            obj.with_create([self._convert_node(f) for f in kwargs["create"]])
        if "antiPatterns" in kwargs:
            obj.with_antiPatterns([self._convert_node(f) for f in kwargs["antiPatterns"]])
        if "createStage" in kwargs:
            obj.with_createStage([self._convert_node(f) for f in kwargs["createStage"]])
        if "insert" in kwargs:
            obj.with_insert([self._convert_node(f) for f in kwargs["insert"]])
        if "update" in kwargs:
            obj.with_update([self._convert_node(f) for f in kwargs["update"]])
        if "rawInput" in kwargs:
            obj.with_rawInput(kwargs["rawInput"])
        if "copy" in kwargs:
            obj.with_copy([self._convert_node(f) for f in kwargs["copy"]])
        if "createView" in kwargs:
            obj.with_createView([self._convert_node(f) for f in kwargs["createView"]])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "delete" in kwargs:
            obj.with_delete([self._convert_node(f) for f in kwargs["delete"]])
        if "ds" in kwargs:
            obj.with_ds([self._convert_node(f) for f in kwargs["ds"]])
        return obj.build()
    
    def _convert_Attr(self, kwargs):
        obj = AttrBuilder()
        if "refsch" in kwargs:
            obj.with_refsch(kwargs["refsch"])
        if "fullref" in kwargs:
            obj.with_fullref(kwargs["fullref"])
        if "refvar" in kwargs:
            obj.with_refvar(kwargs["refvar"])
        if "refdb" in kwargs:
            obj.with_refdb(kwargs["refdb"])
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "refds" in kwargs:
            obj.with_refds(kwargs["refds"])
        if "refatt" in kwargs:
            obj.with_refatt(kwargs["refatt"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "refoutidx" in kwargs:
            obj.with_refoutidx(kwargs["refoutidx"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_CreateStage(self, kwargs):
        obj = CreateStageBuilder()
        if "with" in kwargs:
            obj.with_with(kwargs["with"])
        if "comments" in kwargs:
            obj.with_comments(kwargs["comments"])
        if "stageName" in kwargs:
            obj.with_stageName(kwargs["stageName"])
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "directoryParam" in kwargs:
            obj.with_directoryParam(kwargs["directoryParam"])
        if "location" in kwargs:
            obj.with_location(kwargs["location"])
        if "tag" in kwargs:
            obj.with_tag(self._convert_node(kwargs["tag"]))
        if "copyOptions" in kwargs:
            obj.with_copyOptions(kwargs["copyOptions"])
        if "fileFormat" in kwargs:
            obj.with_fileFormat(kwargs["fileFormat"])
        return obj.build()
    
    def _convert_Sort(self, kwargs):
        obj = SortBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "exprs" in kwargs:
            obj.with_exprs([self._convert_node(f) for f in kwargs["exprs"]])
        return obj.build()
    
    def _convert_Then(self, kwargs):
        obj = ThenBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "expr" in kwargs:
            obj.with_expr(self._convert_node(kwargs["expr"]))
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_MergeStatement(self, kwargs):
        obj = MergeStatementBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "merge" in kwargs:
            obj.with_merge([self._convert_node(f) for f in kwargs["merge"]])
        if "create" in kwargs:
            obj.with_create([self._convert_node(f) for f in kwargs["create"]])
        if "antiPatterns" in kwargs:
            obj.with_antiPatterns([self._convert_node(f) for f in kwargs["antiPatterns"]])
        if "createStage" in kwargs:
            obj.with_createStage([self._convert_node(f) for f in kwargs["createStage"]])
        if "insert" in kwargs:
            obj.with_insert([self._convert_node(f) for f in kwargs["insert"]])
        if "update" in kwargs:
            obj.with_update([self._convert_node(f) for f in kwargs["update"]])
        if "rawInput" in kwargs:
            obj.with_rawInput(kwargs["rawInput"])
        if "copy" in kwargs:
            obj.with_copy([self._convert_node(f) for f in kwargs["copy"]])
        if "createView" in kwargs:
            obj.with_createView([self._convert_node(f) for f in kwargs["createView"]])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "delete" in kwargs:
            obj.with_delete([self._convert_node(f) for f in kwargs["delete"]])
        if "ds" in kwargs:
            obj.with_ds([self._convert_node(f) for f in kwargs["ds"]])
        return obj.build()
    
    def _convert_MultiValue(self, kwargs):
        obj = MultiValueBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "exprs" in kwargs:
            obj.with_exprs([self._convert_node(f) for f in kwargs["exprs"]])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_AntiPattern(self, kwargs):
        obj = AntiPatternBuilder()
        if "severity" in kwargs:
            obj.with_severity(kwargs["severity"])
        if "readability" in kwargs:
            obj.with_readability(kwargs["readability"])
        if "correctness" in kwargs:
            obj.with_correctness(kwargs["correctness"])
        if "performance" in kwargs:
            obj.with_performance(kwargs["performance"])
        if "pos" in kwargs:
            obj.with_pos(self._convert_node(kwargs["pos"]))
        if "link" in kwargs:
            obj.with_link(kwargs["link"])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
            obj.with_link(kwargs["type"])
            obj.with_severity(kwargs["type"])
            obj.with_readability(kwargs["type"])
            obj.with_correctness(kwargs["type"])
            obj.with_performance(kwargs["type"])
        return obj.build()
    
    def _convert_UpdateStatement(self, kwargs):
        obj = UpdateStatementBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "merge" in kwargs:
            obj.with_merge([self._convert_node(f) for f in kwargs["merge"]])
        if "create" in kwargs:
            obj.with_create([self._convert_node(f) for f in kwargs["create"]])
        if "antiPatterns" in kwargs:
            obj.with_antiPatterns([self._convert_node(f) for f in kwargs["antiPatterns"]])
        if "createStage" in kwargs:
            obj.with_createStage([self._convert_node(f) for f in kwargs["createStage"]])
        if "insert" in kwargs:
            obj.with_insert([self._convert_node(f) for f in kwargs["insert"]])
        if "update" in kwargs:
            obj.with_update([self._convert_node(f) for f in kwargs["update"]])
        if "rawInput" in kwargs:
            obj.with_rawInput(kwargs["rawInput"])
        if "copy" in kwargs:
            obj.with_copy([self._convert_node(f) for f in kwargs["copy"]])
        if "createView" in kwargs:
            obj.with_createView([self._convert_node(f) for f in kwargs["createView"]])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "delete" in kwargs:
            obj.with_delete([self._convert_node(f) for f in kwargs["delete"]])
        if "ds" in kwargs:
            obj.with_ds([self._convert_node(f) for f in kwargs["ds"]])
        return obj.build()
    
    def _convert_QueryingStage(self, kwargs):
        obj = QueryingStageBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "pattern" in kwargs:
            obj.with_pattern(kwargs["pattern"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "location" in kwargs:
            obj.with_location(kwargs["location"])
        if "fileFormat" in kwargs:
            obj.with_fileFormat(kwargs["fileFormat"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Position(self, kwargs):
        obj = PositionBuilder()
        if "string" in kwargs:
            obj.with_string(self._convert_node(kwargs["string"]))
        if "subString" in kwargs:
            obj.with_subString(self._convert_node(kwargs["subString"]))
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Const(self, kwargs):
        obj = ConstBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "value" in kwargs:
            obj.with_value(kwargs["value"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_ColumnDef(self, kwargs):
        obj = ColumnDefBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "precision" in kwargs:
            obj.with_precision(kwargs["precision"])
        if "name" in kwargs:
            obj.with_name(kwargs["name"])
        if "scale" in kwargs:
            obj.with_scale(kwargs["scale"])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        return obj.build()
    
    def _convert_Vfilter(self, kwargs):
        obj = VfilterBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "exprs" in kwargs:
            obj.with_exprs([self._convert_node(f) for f in kwargs["exprs"]])
        return obj.build()
    
    def _convert_Ds(self, kwargs):
        obj = DsBuilder()
        if "agg" in kwargs:
            obj.with_agg(self._convert_node(kwargs["agg"]))
        if "refsch" in kwargs:
            obj.with_refsch(kwargs["refsch"])
        if "fullref" in kwargs:
            obj.with_fullref(kwargs["fullref"])
        if "refdb" in kwargs:
            obj.with_refdb(kwargs["refdb"])
        if "in" in kwargs:
            obj.with_in(self._convert_node(kwargs["in"]))
        if "setOp" in kwargs:
            obj.with_setOp([self._convert_node(f) for f in kwargs["setOp"]])
        if "matchRecognize" in kwargs:
            obj.with_matchRecognize(self._convert_node(kwargs["matchRecognize"]))
        if "sort" in kwargs:
            obj.with_sort(self._convert_node(kwargs["sort"]))
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "out" in kwargs:
            obj.with_out(self._convert_node(kwargs["out"]))
        if "tableSample" in kwargs:
            obj.with_tableSample(self._convert_node(kwargs["tableSample"]))
        if "filter" in kwargs:
            obj.with_filter(self._convert_node(kwargs["filter"]))
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "refds" in kwargs:
            obj.with_refds(kwargs["refds"])
        if "name" in kwargs:
            obj.with_name(kwargs["name"])
        if "action" in kwargs:
            obj.with_action(kwargs["action"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "subType" in kwargs:
            obj.with_subType(kwargs["subType"])
        if "page" in kwargs:
            obj.with_page(self._convert_node(kwargs["page"]))
        if "refTo" in kwargs:
            obj.with_refTo(kwargs["refTo"])
        if "vagg" in kwargs:
            obj.with_vagg(self._convert_node(kwargs["vagg"]))
        if "sameAs" in kwargs:
            obj.with_sameAs([self._convert_node(f) for f in kwargs["sameAs"]])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Out(self, kwargs):
        obj = OutBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "exprs" in kwargs:
            obj.with_exprs([self._convert_node(f) for f in kwargs["exprs"]])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "derived" in kwargs:
            obj.with_derived(kwargs["derived"])
        return obj.build()
    
    def _convert_Copy(self, kwargs):
        obj = CopyBuilder()
        if "fromExp" in kwargs:
            obj.with_fromExp([self._convert_node(f) for f in kwargs["fromExp"]])
        if "targetColumns" in kwargs:
            obj.with_targetColumns([self._convert_node(f) for f in kwargs["targetColumns"]])
        if "pattern" in kwargs:
            obj.with_pattern(kwargs["pattern"])
        if "copyOptions" in kwargs:
            obj.with_copyOptions(kwargs["copyOptions"])
        if "selectElements" in kwargs:
            obj.with_selectElements([self._convert_node(f) for f in kwargs["selectElements"]])
        if "fromStage" in kwargs:
            obj.with_fromStage(self._convert_node(kwargs["fromStage"]))
        if "into" in kwargs:
            obj.with_into(self._convert_node(kwargs["into"]))
        if "file" in kwargs:
            obj.with_file(kwargs["file"])
        if "partition" in kwargs:
            obj.with_partition([self._convert_node(f) for f in kwargs["partition"]])
        if "fromQuery" in kwargs:
            obj.with_fromQuery(self._convert_node(kwargs["fromQuery"]))
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "header" in kwargs:
            obj.with_header(kwargs["header"])
        if "validation" in kwargs:
            obj.with_validation(kwargs["validation"])
        if "fileFormat" in kwargs:
            obj.with_fileFormat(kwargs["fileFormat"])
        return obj.build()
    
    def _convert_Current(self, kwargs):
        obj = CurrentBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Cast(self, kwargs):
        obj = CastBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "dataType" in kwargs:
            obj.with_dataType(kwargs["dataType"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "expr" in kwargs:
            obj.with_expr(self._convert_node(kwargs["expr"]))
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Frame(self, kwargs):
        obj = FrameBuilder()
        if "upperPosition" in kwargs:
            obj.with_upperPosition(kwargs["upperPosition"])
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "lowerPosition" in kwargs:
            obj.with_lowerPosition(kwargs["lowerPosition"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "exprs" in kwargs:
            obj.with_exprs([self._convert_node(f) for f in kwargs["exprs"]])
        if "upperLimit" in kwargs:
            obj.with_upperLimit(kwargs["upperLimit"])
        if "lowerLimit" in kwargs:
            obj.with_lowerLimit(kwargs["lowerLimit"])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Vagg(self, kwargs):
        obj = VaggBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "vfilter" in kwargs:
            obj.with_vfilter(self._convert_node(kwargs["vfilter"]))
        return obj.build()
    
    def _convert_Rotate(self, kwargs):
        obj = RotateBuilder()
        if "nameColumn" in kwargs:
            obj.with_nameColumn(kwargs["nameColumn"])
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "valueColumn" in kwargs:
            obj.with_valueColumn(kwargs["valueColumn"])
        if "columnList" in kwargs:
            obj.with_columnList([self._convert_node(f) for f in kwargs["columnList"]])
        if "pivotColumn" in kwargs:
            obj.with_pivotColumn(self._convert_node(kwargs["pivotColumn"]))
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "columnAlias" in kwargs:
            obj.with_columnAlias([self._convert_node(f) for f in kwargs["columnAlias"]])
        if "aggregate" in kwargs:
            obj.with_aggregate(kwargs["aggregate"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_In(self, kwargs):
        obj = InBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "exprs" in kwargs:
            obj.with_exprs([self._convert_node(f) for f in kwargs["exprs"]])
        return obj.build()
    
    def _convert_Func(self, kwargs):
        obj = FuncBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "withinGroup" in kwargs:
            obj.with_withinGroup(self._convert_node(kwargs["withinGroup"]))
        if "name" in kwargs:
            obj.with_name(kwargs["name"])
        if "exprs" in kwargs:
            obj.with_exprs([self._convert_node(f) for f in kwargs["exprs"]])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "quantifier" in kwargs:
            obj.with_quantifier(kwargs["quantifier"])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Case(self, kwargs):
        obj = CaseBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "Else" in kwargs:
            obj.with_Else(self._convert_node(kwargs["Else"]))
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "expr" in kwargs:
            obj.with_expr(self._convert_node(kwargs["expr"]))
        if "when" in kwargs:
            obj.with_when([self._convert_node(f) for f in kwargs["when"]])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_StructRef(self, kwargs):
        obj = StructRefBuilder()
        if "refsch" in kwargs:
            obj.with_refsch(kwargs["refsch"])
        if "fullref" in kwargs:
            obj.with_fullref(kwargs["fullref"])
        if "refvar" in kwargs:
            obj.with_refvar(kwargs["refvar"])
        if "refdb" in kwargs:
            obj.with_refdb(kwargs["refdb"])
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "refds" in kwargs:
            obj.with_refds(kwargs["refds"])
        if "refpath" in kwargs:
            obj.with_refpath(kwargs["refpath"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "refatt" in kwargs:
            obj.with_refatt(kwargs["refatt"])
        if "refoutidx" in kwargs:
            obj.with_refoutidx(kwargs["refoutidx"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_AntiPatterns(self, kwargs):
        obj = AntiPatternsBuilder()
        if "antiPattern" in kwargs:
            obj.with_antiPattern([self._convert_node(f) for f in kwargs["antiPattern"]])
        return obj.build()
    
    def _convert_Create(self, kwargs):
        obj = CreateBuilder()
        if "refsch" in kwargs:
            obj.with_refsch(kwargs["refsch"])
        if "refdb" in kwargs:
            obj.with_refdb(kwargs["refdb"])
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "scope" in kwargs:
            obj.with_scope(kwargs["scope"])
        if "refds" in kwargs:
            obj.with_refds(kwargs["refds"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "columnDef" in kwargs:
            obj.with_columnDef([self._convert_node(f) for f in kwargs["columnDef"]])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        if "ds" in kwargs:
            obj.with_ds(self._convert_node(kwargs["ds"]))
        if "clusterBy" in kwargs:
            obj.with_clusterBy([self._convert_node(f) for f in kwargs["clusterBy"]])
        return obj.build()
    
    def _convert_MatchRecognize(self, kwargs):
        obj = MatchRecognizeBuilder()
        if "partitionBy" in kwargs:
            obj.with_partitionBy(kwargs["partitionBy"])
        if "measures" in kwargs:
            obj.with_measures(kwargs["measures"])
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "define" in kwargs:
            obj.with_define(kwargs["define"])
        if "pattern" in kwargs:
            obj.with_pattern(kwargs["pattern"])
        if "rowMatchAction" in kwargs:
            obj.with_rowMatchAction(kwargs["rowMatchAction"])
        if "orderBy" in kwargs:
            obj.with_orderBy(kwargs["orderBy"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "rowMatchCondition" in kwargs:
            obj.with_rowMatchCondition(kwargs["rowMatchCondition"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Asterisk(self, kwargs):
        obj = AsteriskBuilder()
        if "refsch" in kwargs:
            obj.with_refsch(kwargs["refsch"])
        if "fullref" in kwargs:
            obj.with_fullref(kwargs["fullref"])
        if "refdb" in kwargs:
            obj.with_refdb(kwargs["refdb"])
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "refds" in kwargs:
            obj.with_refds(kwargs["refds"])
        if "refatt" in kwargs:
            obj.with_refatt(kwargs["refatt"])
        if "exprs" in kwargs:
            obj.with_exprs([self._convert_node(f) for f in kwargs["exprs"]])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Agg(self, kwargs):
        obj = AggBuilder()
        if "filter" in kwargs:
            obj.with_filter(self._convert_node(kwargs["filter"]))
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "exprs" in kwargs:
            obj.with_exprs([self._convert_node(f) for f in kwargs["exprs"]])
        return obj.build()
    
    def _convert_Wfunc(self, kwargs):
        obj = WfuncBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "name" in kwargs:
            obj.with_name(kwargs["name"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "expr" in kwargs:
            obj.with_expr(self._convert_node(kwargs["expr"]))
        if "sort" in kwargs:
            obj.with_sort(self._convert_node(kwargs["sort"]))
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "frame" in kwargs:
            obj.with_frame(self._convert_node(kwargs["frame"]))
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Statement(self, kwargs):
        obj = StatementBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "merge" in kwargs:
            obj.with_merge([self._convert_node(f) for f in kwargs["merge"]])
        if "rawInput" in kwargs:
            obj.with_rawInput(kwargs["rawInput"])
        if "update" in kwargs:
            obj.with_update([self._convert_node(f) for f in kwargs["update"]])
        if "insert" in kwargs:
            obj.with_insert([self._convert_node(f) for f in kwargs["insert"]])
        if "createStage" in kwargs:
            obj.with_createStage([self._convert_node(f) for f in kwargs["createStage"]])
        if "create" in kwargs:
            obj.with_create([self._convert_node(f) for f in kwargs["create"]])
        if "antiPatterns" in kwargs:
            obj.with_antiPatterns([self._convert_node(f) for f in kwargs["antiPatterns"]])
        if "copy" in kwargs:
            obj.with_copy([self._convert_node(f) for f in kwargs["copy"]])
        if "createView" in kwargs:
            obj.with_createView([self._convert_node(f) for f in kwargs["createView"]])
        if "delete" in kwargs:
            obj.with_delete([self._convert_node(f) for f in kwargs["delete"]])
        if "ds" in kwargs:
            obj.with_ds([self._convert_node(f) for f in kwargs["ds"]])
        return obj.build()
    
    def _convert_ParSeQL(self, kwargs):
        obj = ParSeQLBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "statement" in kwargs:
            obj.with_statement([self._convert_node(f) for f in kwargs["statement"]])
        if "error" in kwargs:
            obj.with_error([self._convert_node(f) for f in kwargs["error"]])
        if "version" in kwargs:
            obj.with_version(kwargs["version"])
        if "ts" in kwargs:
            obj.with_ts(kwargs["ts"])
        if "status" in kwargs:
            obj.with_status(kwargs["status"])
        return obj.build()
    
    def _convert_TableSample(self, kwargs):
        obj = TableSampleBuilder()
        if "sampleMethod" in kwargs:
            obj.with_sampleMethod(kwargs["sampleMethod"])
        if "seed" in kwargs:
            obj.with_seed(kwargs["seed"])
        if "seedType" in kwargs:
            obj.with_seedType(kwargs["seedType"])
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "probability" in kwargs:
            obj.with_probability(kwargs["probability"])
        if "num" in kwargs:
            obj.with_num(kwargs["num"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "sampleType" in kwargs:
            obj.with_sampleType(kwargs["sampleType"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Error(self, kwargs):
        obj = ErrorBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "message" in kwargs:
            obj.with_message(kwargs["message"])
        return obj.build()
    
    def _convert_Join(self, kwargs):
        obj = JoinBuilder()
        if "op" in kwargs:
            obj.with_op(self._convert_node(kwargs["op"]))
        if "natural" in kwargs:
            obj.with_natural(kwargs["natural"])
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "subType" in kwargs:
            obj.with_subType(kwargs["subType"])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "ds" in kwargs:
            obj.with_ds(self._convert_node(kwargs["ds"]))
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_When(self, kwargs):
        obj = WhenBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "expr" in kwargs:
            obj.with_expr(self._convert_node(kwargs["expr"]))
        if "then" in kwargs:
            obj.with_then(self._convert_node(kwargs["then"]))
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Merge(self, kwargs):
        obj = MergeBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "ds" in kwargs:
            obj.with_ds([self._convert_node(f) for f in kwargs["ds"]])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    
    def _convert_Filter(self, kwargs):
        obj = FilterBuilder()
        if "op" in kwargs:
            obj.with_op(self._convert_node(kwargs["op"]))
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        return obj.build()
    
    def _convert_TableFunc(self, kwargs):
        obj = TableFuncBuilder()
        if "agg" in kwargs:
            obj.with_agg(self._convert_node(kwargs["agg"]))
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "out" in kwargs:
            obj.with_out(self._convert_node(kwargs["out"]))
        if "partition" in kwargs:
            obj.with_partition([self._convert_node(f) for f in kwargs["partition"]])
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "refds" in kwargs:
            obj.with_refds(kwargs["refds"])
        if "options" in kwargs:
            obj.with_options([self._convert_node(f) for f in kwargs["options"]])
        if "action" in kwargs:
            obj.with_action(kwargs["action"])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "refTo" in kwargs:
            obj.with_refTo(kwargs["refTo"])
        if "tableFuncType" in kwargs:
            obj.with_tableFuncType(kwargs["tableFuncType"])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        if "refsch" in kwargs:
            obj.with_refsch(kwargs["refsch"])
        if "fullref" in kwargs:
            obj.with_fullref(kwargs["fullref"])
        if "refdb" in kwargs:
            obj.with_refdb(kwargs["refdb"])
        if "in" in kwargs:
            obj.with_in(self._convert_node(kwargs["in"]))
        if "matchRecognize" in kwargs:
            obj.with_matchRecognize(self._convert_node(kwargs["matchRecognize"]))
        if "setOp" in kwargs:
            obj.with_setOp([self._convert_node(f) for f in kwargs["setOp"]])
        if "sort" in kwargs:
            obj.with_sort(self._convert_node(kwargs["sort"]))
        if "subQuery" in kwargs:
            obj.with_subQuery(self._convert_node(kwargs["subQuery"]))
        if "filter" in kwargs:
            obj.with_filter(self._convert_node(kwargs["filter"]))
        if "tableSample" in kwargs:
            obj.with_tableSample(self._convert_node(kwargs["tableSample"]))
        if "names" in kwargs:
            obj.with_names([self._convert_node(f) for f in kwargs["names"]])
        if "name" in kwargs:
            obj.with_name(kwargs["name"])
        if "subType" in kwargs:
            obj.with_subType(kwargs["subType"])
        if "page" in kwargs:
            obj.with_page(self._convert_node(kwargs["page"]))
        if "vagg" in kwargs:
            obj.with_vagg(self._convert_node(kwargs["vagg"]))
        if "sameAs" in kwargs:
            obj.with_sameAs([self._convert_node(f) for f in kwargs["sameAs"]])
        if "frame" in kwargs:
            obj.with_frame(self._convert_node(kwargs["frame"]))
        return obj.build()
    
    def _convert_Else(self, kwargs):
        obj = ElseBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "expr" in kwargs:
            obj.with_expr(self._convert_node(kwargs["expr"]))
        return obj.build()
    
    def _convert_Edge(self, kwargs):
        obj = EdgeBuilder()
        if "pos" in kwargs:
            obj.with_pos(kwargs["pos"])
        if "generator" in kwargs:
            obj.with_generator(kwargs["generator"])
        if "exprs" in kwargs:
            obj.with_exprs([self._convert_node(f) for f in kwargs["exprs"]])
        if "alias" in kwargs:
            obj.with_alias(kwargs["alias"])
        if "type" in kwargs:
            obj.with_type(kwargs["type"])
        if "columnAlias" in kwargs:
            obj.with_columnAlias([self._convert_node(f) for f in kwargs["columnAlias"]])
        if "direction" in kwargs:
            obj.with_direction(kwargs["direction"])
        return obj.build()
    

    def _convert_node(self, kwargs):
        if not is_iterable(kwargs):
            return kwargs
        if "eltype" not in kwargs:
            return kwargs
        if kwargs["eltype"].lower() == "delete":
            return self._convert_Delete(kwargs)
        if kwargs["eltype"].lower() == "op":
            return self._convert_Op(kwargs)
        if kwargs["eltype"].lower() == "inlinetable":
            return self._convert_InlineTable(kwargs)
        if kwargs["eltype"].lower() == "page":
            return self._convert_Page(kwargs)
        if kwargs["eltype"].lower() == "insert":
            return self._convert_Insert(kwargs)
        if kwargs["eltype"].lower() == "update":
            return self._convert_Update(kwargs)
        if kwargs["eltype"].lower() == "deletestatement":
            return self._convert_DeleteStatement(kwargs)
        if kwargs["eltype"].lower() == "createview":
            return self._convert_CreateView(kwargs)
        if kwargs["eltype"].lower() == "insertstatement":
            return self._convert_InsertStatement(kwargs)
        if kwargs["eltype"].lower() == "attr":
            return self._convert_Attr(kwargs)
        if kwargs["eltype"].lower() == "createstage":
            return self._convert_CreateStage(kwargs)
        if kwargs["eltype"].lower() == "sort":
            return self._convert_Sort(kwargs)
        if kwargs["eltype"].lower() == "then":
            return self._convert_Then(kwargs)
        if kwargs["eltype"].lower() == "mergestatement":
            return self._convert_MergeStatement(kwargs)
        if kwargs["eltype"].lower() == "multivalue":
            return self._convert_MultiValue(kwargs)
        if kwargs["eltype"].lower() == "antipattern":
            return self._convert_AntiPattern(kwargs)
        if kwargs["eltype"].lower() == "updatestatement":
            return self._convert_UpdateStatement(kwargs)
        if kwargs["eltype"].lower() == "queryingstage":
            return self._convert_QueryingStage(kwargs)
        if kwargs["eltype"].lower() == "position":
            return self._convert_Position(kwargs)
        if kwargs["eltype"].lower() == "const":
            return self._convert_Const(kwargs)
        if kwargs["eltype"].lower() == "columndef":
            return self._convert_ColumnDef(kwargs)
        if kwargs["eltype"].lower() == "vfilter":
            return self._convert_Vfilter(kwargs)
        if kwargs["eltype"].lower() == "ds":
            return self._convert_Ds(kwargs)
        if kwargs["eltype"].lower() == "out":
            return self._convert_Out(kwargs)
        if kwargs["eltype"].lower() == "copy":
            return self._convert_Copy(kwargs)
        if kwargs["eltype"].lower() == "current":
            return self._convert_Current(kwargs)
        if kwargs["eltype"].lower() == "cast":
            return self._convert_Cast(kwargs)
        if kwargs["eltype"].lower() == "frame":
            return self._convert_Frame(kwargs)
        if kwargs["eltype"].lower() == "vagg":
            return self._convert_Vagg(kwargs)
        if kwargs["eltype"].lower() == "rotate":
            return self._convert_Rotate(kwargs)
        if kwargs["eltype"].lower() == "in":
            return self._convert_In(kwargs)
        if kwargs["eltype"].lower() == "func":
            return self._convert_Func(kwargs)
        if kwargs["eltype"].lower() == "case":
            return self._convert_Case(kwargs)
        if kwargs["eltype"].lower() == "structref":
            return self._convert_StructRef(kwargs)
        if kwargs["eltype"].lower() == "antipatterns":
            return self._convert_AntiPatterns(kwargs)
        if kwargs["eltype"].lower() == "create":
            return self._convert_Create(kwargs)
        if kwargs["eltype"].lower() == "matchrecognize":
            return self._convert_MatchRecognize(kwargs)
        if kwargs["eltype"].lower() == "asterisk":
            return self._convert_Asterisk(kwargs)
        if kwargs["eltype"].lower() == "agg":
            return self._convert_Agg(kwargs)
        if kwargs["eltype"].lower() == "wfunc":
            return self._convert_Wfunc(kwargs)
        if kwargs["eltype"].lower() == "statement":
            return self._convert_Statement(kwargs)
        if kwargs["eltype"].lower() == "parseql":
            return self._convert_ParSeQL(kwargs)
        if kwargs["eltype"].lower() == "tablesample":
            return self._convert_TableSample(kwargs)
        if kwargs["eltype"].lower() == "error":
            return self._convert_Error(kwargs)
        if kwargs["eltype"].lower() == "join":
            return self._convert_Join(kwargs)
        if kwargs["eltype"].lower() == "when":
            return self._convert_When(kwargs)
        if kwargs["eltype"].lower() == "merge":
            return self._convert_Merge(kwargs)
        if kwargs["eltype"].lower() == "filter":
            return self._convert_Filter(kwargs)
        if kwargs["eltype"].lower() == "tablefunc":
            return self._convert_TableFunc(kwargs)
        if kwargs["eltype"].lower() == "else":
            return self._convert_Else(kwargs)
        if kwargs["eltype"].lower() == "edge":
            return self._convert_Edge(kwargs)

def is_iterable(obj):
    try:
        it = iter(obj)
    except TypeError:
        return False
    return True
