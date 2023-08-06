from datetime import datetime
from typing import List, Optional, Any, Tuple, Union, Dict, Literal
from fluss.traits import MockableTrait, Graph
from fluss.funcs import execute, aexecute
from fluss.scalars import EventValue
from fluss.rath import FlussRath
from enum import Enum
from rath.scalars import ID
from pydantic import BaseModel, Field


class CommentableModels(str, Enum):
    FLOW_WORKSPACE = "FLOW_WORKSPACE"
    FLOW_FLOW = "FLOW_FLOW"
    FLOW_RUN = "FLOW_RUN"
    FLOW_SNAPSHOT = "FLOW_SNAPSHOT"
    FLOW_RUNLOG = "FLOW_RUNLOG"
    FLOW_RUNEVENT = "FLOW_RUNEVENT"
    FLOW_REACTIVETEMPLATE = "FLOW_REACTIVETEMPLATE"


class Scope(str, Enum):
    """Scope of the Port"""

    GLOBAL = "GLOBAL"
    LOCAL = "LOCAL"


class StreamKind(str, Enum):
    INT = "INT"
    STRING = "STRING"
    STRUCTURE = "STRUCTURE"
    LIST = "LIST"
    BOOL = "BOOL"
    ENUM = "ENUM"
    DICT = "DICT"
    UNSET = "UNSET"


class RunEventType(str, Enum):
    """An enumeration."""

    NEXT = "NEXT"
    "NEXT (Value represent Item)"
    ERROR = "ERROR"
    "Error (Value represent Exception)"
    COMPLETE = "COMPLETE"
    "COMPLETE (Value is none)"
    UNKNOWN = "UNKNOWN"
    "UNKNOWN (Should never be used)"


class ReactiveImplementationModelInput(str, Enum):
    """An enumeration."""

    ZIP = "ZIP"
    "ZIP (Zip the data)"
    COMBINELATEST = "COMBINELATEST"
    "COMBINELATEST (Combine values with latest value from each stream)"
    WITHLATEST = "WITHLATEST"
    "WITHLATEST (Combine a leading value with the latest value)"
    BUFFER_COMPLETE = "BUFFER_COMPLETE"
    "BUFFER_COMPLETE (Buffer values until complete is retrieved)"
    BUFFER_UNTIL = "BUFFER_UNTIL"
    "BUFFER_UNTIL (Buffer values until signal is send)"
    CHUNK = "CHUNK"
    "CHUNK (Chunk the data)"
    SPLIT = "SPLIT"
    "SPLIT (Split the data)"
    OMIT = "OMIT"
    "OMIT (Omit the data)"
    ENSURE = "ENSURE"
    "ENSURE (Ensure the data (discards None in the stream))"
    TO_LIST = "TO_LIST"
    "TO_LIST (Convert to list)"
    FOREACH = "FOREACH"
    "FOREACH (Foreach element in list)"
    IF = "IF"
    "IF (If condition is met)"
    AND = "AND"
    "AND (AND condition)"


class ConstantKind(str, Enum):
    STRING = "STRING"
    INT = "INT"
    BOOL = "BOOL"
    FLOAT = "FLOAT"


class SharableModels(str, Enum):
    """Sharable Models are models that can be shared amongst users and groups. They representent the models of the DB"""

    FLOW_WORKSPACE = "FLOW_WORKSPACE"
    FLOW_FLOW = "FLOW_FLOW"
    FLOW_RUN = "FLOW_RUN"
    FLOW_SNAPSHOT = "FLOW_SNAPSHOT"
    FLOW_RUNLOG = "FLOW_RUNLOG"
    FLOW_RUNEVENT = "FLOW_RUNEVENT"
    FLOW_REACTIVETEMPLATE = "FLOW_REACTIVETEMPLATE"


class MapStrategy(str, Enum):
    """Maping Strategy for the Map Operator"""

    MAP = "MAP"
    MERGEMAP = "MERGEMAP"
    SWITCHMAP = "SWITCHMAP"
    CONCATMAP = "CONCATMAP"


class EventTypeInput(str, Enum):
    """Event Type for the Event Operator"""

    NEXT = "NEXT"
    "NEXT (Value represent Item)"
    ERROR = "ERROR"
    "Error (Value represent Exception)"
    COMPLETE = "COMPLETE"
    "COMPLETE (Value is none)"
    UNKNOWN = "UNKNOWN"
    "UNKNOWN (Should never be used)"


class GraphInput(BaseModel):
    zoom: Optional[float]
    nodes: Tuple[Optional["NodeInput"], ...]
    edges: Tuple[Optional["EdgeInput"], ...]
    args: Tuple[Optional["PortInput"], ...]
    returns: Tuple[Optional["PortInput"], ...]
    globals: Tuple[Optional["GlobalInput"], ...]

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class NodeInput(BaseModel):
    id: str
    typename: str
    hash: Optional[str]
    interface: Optional[str]
    name: Optional[str]
    description: Optional[str]
    kind: Optional[str]
    implementation: Optional[ReactiveImplementationModelInput]
    documentation: Optional[str]
    position: "PositionInput"
    defaults: Optional[Dict]
    extra: Optional[Dict]
    instream: Tuple[Optional[Tuple[Optional["StreamItemInput"], ...]], ...]
    outstream: Tuple[Optional[Tuple[Optional["StreamItemInput"], ...]], ...]
    constream: Tuple[Optional[Tuple[Optional["StreamItemInput"], ...]], ...]
    map_strategy: Optional[MapStrategy] = Field(alias="mapStrategy")
    allow_local: Optional[bool] = Field(alias="allowLocal")
    binds: Optional["BindsInput"]
    assign_timeout: Optional[float] = Field(alias="assignTimeout")
    yield_timeout: Optional[float] = Field(alias="yieldTimeout")
    reserve_timeout: Optional[float] = Field(alias="reserveTimeout")
    parent_node: Optional[ID] = Field(alias="parentNode")

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class PositionInput(BaseModel):
    x: float
    y: float

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class StreamItemInput(BaseModel):
    key: str
    kind: StreamKind
    scope: Scope
    "The scope of this argument"
    identifier: Optional[str]
    nullable: bool
    child: Optional["StreamItemChildInput"]

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class StreamItemChildInput(BaseModel):
    kind: StreamKind
    scope: Scope
    "The scope of this argument"
    identifier: Optional[str]
    child: Optional["StreamItemChildInput"]

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class BindsInput(BaseModel):
    templates: Optional[Tuple[Optional[str], ...]]
    clients: Optional[Tuple[Optional[str], ...]]

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class EdgeInput(BaseModel):
    id: str
    typename: str
    source: str
    target: str
    source_handle: str = Field(alias="sourceHandle")
    target_handle: str = Field(alias="targetHandle")
    stream: Optional[Tuple[Optional[StreamItemInput], ...]]

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True
        allow_population_by_field_name = True


class PortInput(BaseModel):
    identifier: Optional[str]
    "The identifier"
    key: str
    "The key of the arg"
    name: Optional[str]
    "The name of this argument"
    label: Optional[str]
    "The name of this argument"
    kind: StreamKind
    "The type of this argument"
    scope: Scope
    "The scope of this argument"
    description: Optional[str]
    "The description of this argument"
    child: Optional["ChildPortInput"]
    "The child of this argument"
    assign_widget: Optional["WidgetInput"] = Field(alias="assignWidget")
    "The child of this argument"
    return_widget: Optional["ReturnWidgetInput"] = Field(alias="returnWidget")
    "The child of this argument"
    default: Optional[Any]
    "The key of the arg"
    nullable: bool
    "Is this argument nullable"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class ChildPortInput(BaseModel):
    nullable: Optional[bool]
    scope: Scope
    "The scope of this argument"
    identifier: Optional[str]
    "The identifier"
    kind: StreamKind
    "The type of this argument"
    child: Optional["ChildPortInput"]

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class WidgetInput(BaseModel):
    kind: str
    "type"
    query: Optional[str]
    "Do we have a possible"
    dependencies: Optional[Tuple[Optional[str], ...]]
    "The dependencies of this port"
    choices: Optional[Tuple[Optional["ChoiceInput"], ...]]
    "The dependencies of this port"
    max: Optional[int]
    "Max value for int widget"
    min: Optional[int]
    "Max value for int widget"
    placeholder: Optional[str]
    "Placeholder for any widget"
    as_paragraph: Optional[bool] = Field(alias="asParagraph")
    "Is this a paragraph"
    hook: Optional[str]
    "A hook for the app to call"
    ward: Optional[str]
    "A ward for the app to call"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class ChoiceInput(BaseModel):
    value: Any
    label: str

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class ReturnWidgetInput(BaseModel):
    kind: str
    "type"
    query: Optional[str]
    "Do we have a possible"
    hook: Optional[str]
    "A hook for the app to call"
    ward: Optional[str]
    "A ward for the app to call"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class GlobalInput(BaseModel):
    key: str
    value: Optional[Dict]

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class GroupAssignmentInput(BaseModel):
    permissions: Tuple[Optional[str], ...]
    group: ID

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class UserAssignmentInput(BaseModel):
    permissions: Tuple[Optional[str], ...]
    user: str
    "The user id"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class DescendendInput(BaseModel):
    children: Optional[Tuple[Optional["DescendendInput"], ...]]
    typename: Optional[str]
    "The type of the descendent"
    user: Optional[str]
    "The user that is mentioned"
    bold: Optional[bool]
    "Is this a bold leaf?"
    italic: Optional[bool]
    "Is this a italic leaf?"
    code: Optional[bool]
    "Is this a code leaf?"
    text: Optional[str]
    "The text of the leaf"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class GlobalFragment(BaseModel):
    typename: Optional[Literal["Global"]] = Field(alias="__typename", exclude=True)
    locked: Optional[bool]
    key: str
    value: Optional[Dict]
    mapped: Optional[Tuple[Optional[str], ...]]
    identifier: Optional[str]
    typename: str
    widget: Optional[Dict]

    class Config:
        frozen = True


class StreamItemChildFragmentChild(MockableTrait, BaseModel):
    typename: Optional[Literal["StreamItemChild"]] = Field(
        alias="__typename", exclude=True
    )
    kind: StreamKind
    identifier: Optional[str]

    class Config:
        frozen = True


class StreamItemChildFragment(MockableTrait, BaseModel):
    typename: Optional[Literal["StreamItemChild"]] = Field(
        alias="__typename", exclude=True
    )
    kind: StreamKind
    identifier: Optional[str]
    scope: Scope
    child: Optional[StreamItemChildFragmentChild]

    class Config:
        frozen = True


class StreamItemFragment(MockableTrait, BaseModel):
    typename: Optional[Literal["StreamItem"]] = Field(alias="__typename", exclude=True)
    key: str
    kind: StreamKind
    identifier: Optional[str]
    scope: Scope
    nullable: bool
    child: Optional[StreamItemChildFragment]

    class Config:
        frozen = True


class FlowNodeCommonsFragmentBase(BaseModel):
    instream: Tuple[Optional[Tuple[Optional[StreamItemFragment], ...]], ...]
    outstream: Tuple[Optional[Tuple[Optional[StreamItemFragment], ...]], ...]
    constream: Tuple[Optional[Tuple[Optional[StreamItemFragment], ...]], ...]
    constants: Optional[Dict]


class ArkitektNodeFragmentBinds(BaseModel):
    typename: Optional[Literal["Binds"]] = Field(alias="__typename", exclude=True)
    clients: Optional[Tuple[Optional[str], ...]]
    templates: Optional[Tuple[Optional[str], ...]]

    class Config:
        frozen = True


class ArkitektNodeFragment(FlowNodeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["ArkitektNode"]] = Field(
        alias="__typename", exclude=True
    )
    name: Optional[str]
    description: Optional[str]
    hash: str
    kind: str
    defaults: Optional[Dict]
    binds: Optional[ArkitektNodeFragmentBinds]
    allow_local: bool = Field(alias="allowLocal")
    map_strategy: MapStrategy = Field(alias="mapStrategy")

    class Config:
        frozen = True


class LocalNodeFragment(FlowNodeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["LocalNode"]] = Field(alias="__typename", exclude=True)
    name: Optional[str]
    description: Optional[str]
    hash: str
    kind: str
    defaults: Optional[Dict]
    allow_local: bool = Field(alias="allowLocal")
    map_strategy: MapStrategy = Field(alias="mapStrategy")

    class Config:
        frozen = True


class ReactiveNodeFragment(FlowNodeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["ReactiveNode"]] = Field(
        alias="__typename", exclude=True
    )
    implementation: ReactiveImplementationModelInput
    defaults: Optional[Dict]

    class Config:
        frozen = True


class ArgNodeFragment(FlowNodeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["ArgNode"]] = Field(alias="__typename", exclude=True)

    class Config:
        frozen = True


class KwargNodeFragment(FlowNodeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["KwargNode"]] = Field(alias="__typename", exclude=True)

    class Config:
        frozen = True


class ReturnNodeFragment(FlowNodeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["ReturnNode"]] = Field(alias="__typename", exclude=True)

    class Config:
        frozen = True


class GraphNodeFragment(FlowNodeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["ReturnNode"]] = Field(alias="__typename", exclude=True)

    class Config:
        frozen = True


class FlowNodeFragmentBasePosition(BaseModel):
    typename: Optional[Literal["Position"]] = Field(alias="__typename", exclude=True)
    x: int
    y: int

    class Config:
        frozen = True


class FlowNodeFragmentBase(BaseModel):
    id: str
    position: FlowNodeFragmentBasePosition
    typename: str
    parent_node: Optional[ID] = Field(alias="parentNode")


class FlowNodeFragmentBaseArkitektNode(ArkitektNodeFragment, FlowNodeFragmentBase):
    pass


class FlowNodeFragmentBaseReactiveNode(ReactiveNodeFragment, FlowNodeFragmentBase):
    pass


class FlowNodeFragmentBaseArgNode(ArgNodeFragment, FlowNodeFragmentBase):
    pass


class FlowNodeFragmentBaseKwargNode(KwargNodeFragment, FlowNodeFragmentBase):
    pass


class FlowNodeFragmentBaseReturnNode(ReturnNodeFragment, FlowNodeFragmentBase):
    pass


class FlowNodeFragmentBaseLocalNode(LocalNodeFragment, FlowNodeFragmentBase):
    pass


class FlowNodeFragmentBaseGraphNode(GraphNodeFragment, FlowNodeFragmentBase):
    pass


FlowNodeFragment = Union[
    FlowNodeFragmentBaseArkitektNode,
    FlowNodeFragmentBaseReactiveNode,
    FlowNodeFragmentBaseArgNode,
    FlowNodeFragmentBaseKwargNode,
    FlowNodeFragmentBaseReturnNode,
    FlowNodeFragmentBaseLocalNode,
    FlowNodeFragmentBaseGraphNode,
    FlowNodeFragmentBase,
]


class FlowEdgeCommonsFragmentBase(BaseModel):
    stream: Tuple[Optional[StreamItemFragment], ...]


class LabeledEdgeFragment(FlowEdgeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["LabeledEdge"]] = Field(alias="__typename", exclude=True)

    class Config:
        frozen = True


class FancyEdgeFragment(FlowEdgeCommonsFragmentBase, BaseModel):
    typename: Optional[Literal["FancyEdge"]] = Field(alias="__typename", exclude=True)

    class Config:
        frozen = True


class FlowEdgeFragmentBase(BaseModel):
    id: str
    source: str
    source_handle: str = Field(alias="sourceHandle")
    target: str
    target_handle: str = Field(alias="targetHandle")
    typename: str


class FlowEdgeFragmentBaseLabeledEdge(LabeledEdgeFragment, FlowEdgeFragmentBase):
    pass


class FlowEdgeFragmentBaseFancyEdge(FancyEdgeFragment, FlowEdgeFragmentBase):
    pass


FlowEdgeFragment = Union[
    FlowEdgeFragmentBaseLabeledEdge, FlowEdgeFragmentBaseFancyEdge, FlowEdgeFragmentBase
]


class WidgetFragmentChoices(BaseModel):
    typename: Optional[Literal["Choice"]] = Field(alias="__typename", exclude=True)
    label: str
    value: Any

    class Config:
        frozen = True


class WidgetFragment(BaseModel):
    typename: Optional[Literal["Widget"]] = Field(alias="__typename", exclude=True)
    kind: str
    "type"
    query: Optional[str]
    "Do we have a possible"
    hook: Optional[str]
    "A hook for the app to call"
    placeholder: Optional[str]
    "Placeholder for any widget"
    choices: Optional[Tuple[Optional[WidgetFragmentChoices], ...]]
    "The dependencies of this port"
    ward: Optional[str]
    "A hook for the app to call"

    class Config:
        frozen = True


class ReturnWidgetFragmentChoices(BaseModel):
    typename: Optional[Literal["Choice"]] = Field(alias="__typename", exclude=True)
    label: str
    value: Any

    class Config:
        frozen = True


class ReturnWidgetFragment(BaseModel):
    typename: Optional[Literal["ReturnWidget"]] = Field(
        alias="__typename", exclude=True
    )
    kind: str
    "type"
    choices: Optional[Tuple[Optional[ReturnWidgetFragmentChoices], ...]]
    "The dependencies of this port"

    class Config:
        frozen = True


class PortChildFragmentChild(BaseModel):
    typename: Optional[Literal["PortChild"]] = Field(alias="__typename", exclude=True)
    scope: Scope
    kind: StreamKind
    identifier: Optional[str]

    class Config:
        frozen = True


class PortChildFragment(BaseModel):
    typename: Optional[Literal["PortChild"]] = Field(alias="__typename", exclude=True)
    kind: StreamKind
    identifier: Optional[str]
    nullable: Optional[bool]
    scope: Scope
    child: Optional[PortChildFragmentChild]

    class Config:
        frozen = True


class PortFragment(BaseModel):
    typename: Optional[Literal["Port"]] = Field(alias="__typename", exclude=True)
    key: str
    label: Optional[str]
    identifier: Optional[str]
    kind: StreamKind
    name: Optional[str]
    scope: Scope
    description: Optional[str]
    assign_widget: Optional[WidgetFragment] = Field(alias="assignWidget")
    return_widget: Optional[ReturnWidgetFragment] = Field(alias="returnWidget")
    child: Optional[PortChildFragment]
    nullable: bool
    "The key of the arg"

    class Config:
        frozen = True


class FlowFragmentGraph(Graph, BaseModel):
    typename: Optional[Literal["FlowGraph"]] = Field(alias="__typename", exclude=True)
    nodes: Tuple[Optional[FlowNodeFragment], ...]
    edges: Tuple[Optional[FlowEdgeFragment], ...]
    globals: Tuple[Optional[GlobalFragment], ...]
    args: Tuple[Optional[PortFragment], ...]
    returns: Tuple[Optional[PortFragment], ...]

    class Config:
        frozen = True


class FlowFragmentWorkspace(BaseModel):
    typename: Optional[Literal["Workspace"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: Optional[str]

    class Config:
        frozen = True


class FlowFragment(BaseModel):
    typename: Optional[Literal["Flow"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    graph: FlowFragmentGraph
    brittle: bool
    "Is this a brittle flow? aka. should the flow fail on any exception?"
    created_at: datetime = Field(alias="createdAt")
    workspace: Optional[FlowFragmentWorkspace]
    hash: str

    class Config:
        frozen = True


class ListFlowFragment(BaseModel):
    typename: Optional[Literal["Flow"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    hash: str

    class Config:
        frozen = True


class WorkspaceFragment(BaseModel):
    typename: Optional[Literal["Workspace"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: Optional[str]
    latest_flow: Optional[FlowFragment] = Field(alias="latestFlow")
    "The latest flow"

    class Config:
        frozen = True


class ListWorkspaceFragmentFlows(BaseModel):
    typename: Optional[Literal["Flow"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        frozen = True


class ListWorkspaceFragment(BaseModel):
    typename: Optional[Literal["Workspace"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: Optional[str]
    flows: Tuple[ListWorkspaceFragmentFlows, ...]

    class Config:
        frozen = True


class RunFragmentFlow(BaseModel):
    typename: Optional[Literal["Flow"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        frozen = True


class RunFragmentEvents(BaseModel):
    typename: Optional[Literal["RunEvent"]] = Field(alias="__typename", exclude=True)
    type: RunEventType
    t: int
    caused_by: Optional[Tuple[Optional[int], ...]] = Field(alias="causedBy")
    created_at: datetime = Field(alias="createdAt")
    source: str
    value: Optional[EventValue]

    class Config:
        frozen = True


class RunFragment(BaseModel):
    typename: Optional[Literal["Run"]] = Field(alias="__typename", exclude=True)
    id: ID
    assignation: Optional[str]
    flow: Optional[RunFragmentFlow]
    events: Tuple[RunFragmentEvents, ...]
    created_at: datetime = Field(alias="createdAt")

    class Config:
        frozen = True


class RunMutationStart(BaseModel):
    typename: Optional[Literal["Run"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        frozen = True


class RunMutation(BaseModel):
    """Start a run on fluss"""

    start: Optional[RunMutationStart]

    class Arguments(BaseModel):
        assignation: ID
        flow: ID

    class Meta:
        document = "mutation run($assignation: ID!, $flow: ID!) {\n  start(assignation: $assignation, flow: $flow) {\n    id\n  }\n}"


class RunlogMutationAlog(BaseModel):
    typename: Optional[Literal["RunLog"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        frozen = True


class RunlogMutation(BaseModel):
    """Start a run on fluss"""

    alog: Optional[RunlogMutationAlog]

    class Arguments(BaseModel):
        run: ID
        message: str

    class Meta:
        document = "mutation runlog($run: ID!, $message: String!) {\n  alog(run: $run, message: $message) {\n    id\n  }\n}"


class SnapshotMutationSnapshot(BaseModel):
    typename: Optional[Literal["Snapshot"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        frozen = True


class SnapshotMutation(BaseModel):
    """Snapshot the current state on the fluss platform"""

    snapshot: Optional[SnapshotMutationSnapshot]

    class Arguments(BaseModel):
        run: ID
        events: List[Optional[ID]]
        t: int

    class Meta:
        document = "mutation snapshot($run: ID!, $events: [ID]!, $t: Int!) {\n  snapshot(run: $run, events: $events, t: $t) {\n    id\n  }\n}"


class TrackMutationTrack(BaseModel):
    typename: Optional[Literal["RunEvent"]] = Field(alias="__typename", exclude=True)
    id: ID
    source: str
    handle: str
    type: RunEventType
    value: Optional[EventValue]
    caused_by: Optional[Tuple[Optional[int], ...]] = Field(alias="causedBy")

    class Config:
        frozen = True


class TrackMutation(BaseModel):
    """Track a new event on the fluss platform"""

    track: Optional[TrackMutationTrack]

    class Arguments(BaseModel):
        run: ID
        source: str
        handle: str
        type: EventTypeInput
        value: Optional[EventValue]
        caused_by: List[Optional[int]]
        t: int

    class Meta:
        document = "mutation track($run: ID!, $source: String!, $handle: String!, $type: EventTypeInput!, $value: EventValue, $caused_by: [Int]!, $t: Int!) {\n  track(\n    run: $run\n    source: $source\n    handle: $handle\n    type: $type\n    value: $value\n    causedBy: $caused_by\n    t: $t\n  ) {\n    id\n    source\n    handle\n    type\n    value\n    causedBy\n  }\n}"


class Get_flowQuery(BaseModel):
    flow: Optional[FlowFragment]

    class Arguments(BaseModel):
        id: Optional[ID]

    class Meta:
        document = "fragment StreamItemChild on StreamItemChild {\n  kind\n  identifier\n  scope\n  child {\n    kind\n    identifier\n  }\n}\n\nfragment StreamItem on StreamItem {\n  key\n  kind\n  identifier\n  scope\n  nullable\n  child {\n    ...StreamItemChild\n  }\n}\n\nfragment FlowEdgeCommons on FlowEdgeCommons {\n  stream {\n    ...StreamItem\n  }\n}\n\nfragment FlowNodeCommons on FlowNodeCommons {\n  instream {\n    ...StreamItem\n  }\n  outstream {\n    ...StreamItem\n  }\n  constream {\n    ...StreamItem\n  }\n  constants\n}\n\nfragment Widget on Widget {\n  kind\n  query\n  hook\n  placeholder\n  choices {\n    label\n    value\n  }\n  ward\n}\n\nfragment PortChild on PortChild {\n  kind\n  identifier\n  nullable\n  scope\n  child {\n    scope\n    kind\n    identifier\n  }\n}\n\nfragment KwargNode on KwargNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment GraphNode on ReturnNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment ReactiveNode on ReactiveNode {\n  ...FlowNodeCommons\n  __typename\n  implementation\n  defaults\n}\n\nfragment ArgNode on ArgNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment LabeledEdge on LabeledEdge {\n  ...FlowEdgeCommons\n  __typename\n}\n\nfragment ArkitektNode on ArkitektNode {\n  ...FlowNodeCommons\n  __typename\n  name\n  description\n  hash\n  kind\n  defaults\n  binds {\n    clients\n    templates\n  }\n  allowLocal\n  mapStrategy\n}\n\nfragment ReturnWidget on ReturnWidget {\n  kind\n  choices {\n    label\n    value\n  }\n}\n\nfragment LocalNode on LocalNode {\n  ...FlowNodeCommons\n  __typename\n  name\n  description\n  hash\n  kind\n  defaults\n  allowLocal\n  mapStrategy\n}\n\nfragment ReturnNode on ReturnNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment FancyEdge on FancyEdge {\n  ...FlowEdgeCommons\n  __typename\n}\n\nfragment FlowNode on FlowNode {\n  id\n  position {\n    x\n    y\n  }\n  typename\n  parentNode\n  ...ArkitektNode\n  ...ReactiveNode\n  ...ArgNode\n  ...KwargNode\n  ...ReturnNode\n  ...LocalNode\n  ...GraphNode\n}\n\nfragment Port on Port {\n  key\n  label\n  identifier\n  kind\n  name\n  scope\n  description\n  assignWidget {\n    ...Widget\n  }\n  returnWidget {\n    ...ReturnWidget\n  }\n  child {\n    ...PortChild\n  }\n  nullable\n}\n\nfragment Global on Global {\n  locked\n  key\n  value\n  mapped\n  identifier\n  typename\n  widget\n}\n\nfragment FlowEdge on FlowEdge {\n  id\n  source\n  sourceHandle\n  target\n  targetHandle\n  typename\n  ...LabeledEdge\n  ...FancyEdge\n}\n\nfragment Flow on Flow {\n  __typename\n  id\n  name\n  graph {\n    nodes {\n      ...FlowNode\n    }\n    edges {\n      ...FlowEdge\n    }\n    globals {\n      ...Global\n    }\n    args {\n      ...Port\n    }\n    returns {\n      ...Port\n    }\n  }\n  brittle\n  createdAt\n  workspace {\n    id\n    name\n  }\n  hash\n}\n\nquery get_flow($id: ID) {\n  flow(id: $id) {\n    ...Flow\n  }\n}"


class Search_flowsQueryOptions(BaseModel):
    typename: Optional[Literal["Flow"]] = Field(alias="__typename", exclude=True)
    value: ID
    label: str

    class Config:
        frozen = True


class Search_flowsQuery(BaseModel):
    options: Optional[Tuple[Optional[Search_flowsQueryOptions], ...]]

    class Arguments(BaseModel):
        search: Optional[str]
        values: Optional[List[Optional[ID]]]

    class Meta:
        document = "query search_flows($search: String, $values: [ID]) {\n  options: flows(name: $search, ids: $values) {\n    value: id\n    label: name\n  }\n}"


class List_flowsQuery(BaseModel):
    flows: Optional[Tuple[Optional[ListFlowFragment], ...]]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment ListFlow on Flow {\n  id\n  name\n  hash\n}\n\nquery list_flows {\n  flows {\n    ...ListFlow\n  }\n}"


class WorkspaceQuery(BaseModel):
    workspace: Optional[WorkspaceFragment]

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment StreamItemChild on StreamItemChild {\n  kind\n  identifier\n  scope\n  child {\n    kind\n    identifier\n  }\n}\n\nfragment StreamItem on StreamItem {\n  key\n  kind\n  identifier\n  scope\n  nullable\n  child {\n    ...StreamItemChild\n  }\n}\n\nfragment FlowEdgeCommons on FlowEdgeCommons {\n  stream {\n    ...StreamItem\n  }\n}\n\nfragment FlowNodeCommons on FlowNodeCommons {\n  instream {\n    ...StreamItem\n  }\n  outstream {\n    ...StreamItem\n  }\n  constream {\n    ...StreamItem\n  }\n  constants\n}\n\nfragment Widget on Widget {\n  kind\n  query\n  hook\n  placeholder\n  choices {\n    label\n    value\n  }\n  ward\n}\n\nfragment PortChild on PortChild {\n  kind\n  identifier\n  nullable\n  scope\n  child {\n    scope\n    kind\n    identifier\n  }\n}\n\nfragment KwargNode on KwargNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment GraphNode on ReturnNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment ReactiveNode on ReactiveNode {\n  ...FlowNodeCommons\n  __typename\n  implementation\n  defaults\n}\n\nfragment ArgNode on ArgNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment LabeledEdge on LabeledEdge {\n  ...FlowEdgeCommons\n  __typename\n}\n\nfragment ArkitektNode on ArkitektNode {\n  ...FlowNodeCommons\n  __typename\n  name\n  description\n  hash\n  kind\n  defaults\n  binds {\n    clients\n    templates\n  }\n  allowLocal\n  mapStrategy\n}\n\nfragment ReturnWidget on ReturnWidget {\n  kind\n  choices {\n    label\n    value\n  }\n}\n\nfragment LocalNode on LocalNode {\n  ...FlowNodeCommons\n  __typename\n  name\n  description\n  hash\n  kind\n  defaults\n  allowLocal\n  mapStrategy\n}\n\nfragment ReturnNode on ReturnNode {\n  ...FlowNodeCommons\n  __typename\n}\n\nfragment FancyEdge on FancyEdge {\n  ...FlowEdgeCommons\n  __typename\n}\n\nfragment FlowNode on FlowNode {\n  id\n  position {\n    x\n    y\n  }\n  typename\n  parentNode\n  ...ArkitektNode\n  ...ReactiveNode\n  ...ArgNode\n  ...KwargNode\n  ...ReturnNode\n  ...LocalNode\n  ...GraphNode\n}\n\nfragment Port on Port {\n  key\n  label\n  identifier\n  kind\n  name\n  scope\n  description\n  assignWidget {\n    ...Widget\n  }\n  returnWidget {\n    ...ReturnWidget\n  }\n  child {\n    ...PortChild\n  }\n  nullable\n}\n\nfragment Global on Global {\n  locked\n  key\n  value\n  mapped\n  identifier\n  typename\n  widget\n}\n\nfragment FlowEdge on FlowEdge {\n  id\n  source\n  sourceHandle\n  target\n  targetHandle\n  typename\n  ...LabeledEdge\n  ...FancyEdge\n}\n\nfragment Flow on Flow {\n  __typename\n  id\n  name\n  graph {\n    nodes {\n      ...FlowNode\n    }\n    edges {\n      ...FlowEdge\n    }\n    globals {\n      ...Global\n    }\n    args {\n      ...Port\n    }\n    returns {\n      ...Port\n    }\n  }\n  brittle\n  createdAt\n  workspace {\n    id\n    name\n  }\n  hash\n}\n\nfragment Workspace on Workspace {\n  id\n  name\n  latestFlow {\n    ...Flow\n  }\n}\n\nquery Workspace($id: ID!) {\n  workspace(id: $id) {\n    ...Workspace\n  }\n}"


class MyWorkspacesQuery(BaseModel):
    myworkspaces: Optional[Tuple[Optional[ListWorkspaceFragment], ...]]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment ListWorkspace on Workspace {\n  id\n  name\n  flows {\n    id\n  }\n}\n\nquery MyWorkspaces {\n  myworkspaces {\n    ...ListWorkspace\n  }\n}"


class GetRunQuery(BaseModel):
    run: Optional[RunFragment]

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Run on Run {\n  id\n  assignation\n  flow {\n    id\n    name\n  }\n  events {\n    type\n    t\n    causedBy\n    createdAt\n    source\n    value\n  }\n  createdAt\n}\n\nquery GetRun($id: ID!) {\n  run(id: $id) {\n    ...Run\n  }\n}"


class SearchRunsQueryOptions(BaseModel):
    typename: Optional[Literal["Run"]] = Field(alias="__typename", exclude=True)
    value: ID
    label: Optional[str]

    class Config:
        frozen = True


class SearchRunsQuery(BaseModel):
    options: Optional[Tuple[Optional[SearchRunsQueryOptions], ...]]

    class Arguments(BaseModel):
        search: Optional[str]
        values: Optional[List[Optional[ID]]]

    class Meta:
        document = "query SearchRuns($search: String, $values: [ID]) {\n  options: runs(name: $search, ids: $values) {\n    value: id\n    label: assignation\n  }\n}"


async def arun(
    assignation: ID, flow: ID, rath: FlussRath = None
) -> Optional[RunMutationStart]:
    """run

     Start a run on fluss

    Arguments:
        assignation (ID): assignation
        flow (ID): flow
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[RunMutationStart]"""
    return (
        await aexecute(
            RunMutation, {"assignation": assignation, "flow": flow}, rath=rath
        )
    ).start


def run(
    assignation: ID, flow: ID, rath: FlussRath = None
) -> Optional[RunMutationStart]:
    """run

     Start a run on fluss

    Arguments:
        assignation (ID): assignation
        flow (ID): flow
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[RunMutationStart]"""
    return execute(
        RunMutation, {"assignation": assignation, "flow": flow}, rath=rath
    ).start


async def arunlog(
    run: ID, message: str, rath: FlussRath = None
) -> Optional[RunlogMutationAlog]:
    """runlog

     Start a run on fluss

    Arguments:
        run (ID): run
        message (str): message
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[RunlogMutationAlog]"""
    return (
        await aexecute(RunlogMutation, {"run": run, "message": message}, rath=rath)
    ).alog


def runlog(
    run: ID, message: str, rath: FlussRath = None
) -> Optional[RunlogMutationAlog]:
    """runlog

     Start a run on fluss

    Arguments:
        run (ID): run
        message (str): message
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[RunlogMutationAlog]"""
    return execute(RunlogMutation, {"run": run, "message": message}, rath=rath).alog


async def asnapshot(
    run: ID, events: List[Optional[ID]], t: int, rath: FlussRath = None
) -> Optional[SnapshotMutationSnapshot]:
    """snapshot

     Snapshot the current state on the fluss platform

    Arguments:
        run (ID): run
        events (List[Optional[ID]]): events
        t (int): t
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[SnapshotMutationSnapshot]"""
    return (
        await aexecute(
            SnapshotMutation, {"run": run, "events": events, "t": t}, rath=rath
        )
    ).snapshot


def snapshot(
    run: ID, events: List[Optional[ID]], t: int, rath: FlussRath = None
) -> Optional[SnapshotMutationSnapshot]:
    """snapshot

     Snapshot the current state on the fluss platform

    Arguments:
        run (ID): run
        events (List[Optional[ID]]): events
        t (int): t
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[SnapshotMutationSnapshot]"""
    return execute(
        SnapshotMutation, {"run": run, "events": events, "t": t}, rath=rath
    ).snapshot


async def atrack(
    run: ID,
    source: str,
    handle: str,
    type: EventTypeInput,
    caused_by: List[Optional[int]],
    t: int,
    value: Optional[EventValue] = None,
    rath: FlussRath = None,
) -> Optional[TrackMutationTrack]:
    """track

     Track a new event on the fluss platform

    Arguments:
        run (ID): run
        source (str): source
        handle (str): handle
        type (EventTypeInput): type
        caused_by (List[Optional[int]]): caused_by
        t (int): t
        value (Optional[EventValue], optional): value.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[TrackMutationTrack]"""
    return (
        await aexecute(
            TrackMutation,
            {
                "run": run,
                "source": source,
                "handle": handle,
                "type": type,
                "value": value,
                "caused_by": caused_by,
                "t": t,
            },
            rath=rath,
        )
    ).track


def track(
    run: ID,
    source: str,
    handle: str,
    type: EventTypeInput,
    caused_by: List[Optional[int]],
    t: int,
    value: Optional[EventValue] = None,
    rath: FlussRath = None,
) -> Optional[TrackMutationTrack]:
    """track

     Track a new event on the fluss platform

    Arguments:
        run (ID): run
        source (str): source
        handle (str): handle
        type (EventTypeInput): type
        caused_by (List[Optional[int]]): caused_by
        t (int): t
        value (Optional[EventValue], optional): value.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[TrackMutationTrack]"""
    return execute(
        TrackMutation,
        {
            "run": run,
            "source": source,
            "handle": handle,
            "type": type,
            "value": value,
            "caused_by": caused_by,
            "t": t,
        },
        rath=rath,
    ).track


async def aget_flow(
    id: Optional[ID] = None, rath: FlussRath = None
) -> Optional[FlowFragment]:
    """get_flow



    Arguments:
        id (Optional[ID], optional): id.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[FlowFragment]"""
    return (await aexecute(Get_flowQuery, {"id": id}, rath=rath)).flow


def get_flow(id: Optional[ID] = None, rath: FlussRath = None) -> Optional[FlowFragment]:
    """get_flow



    Arguments:
        id (Optional[ID], optional): id.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[FlowFragment]"""
    return execute(Get_flowQuery, {"id": id}, rath=rath).flow


async def asearch_flows(
    search: Optional[str] = None,
    values: Optional[List[Optional[ID]]] = None,
    rath: FlussRath = None,
) -> Optional[List[Optional[Search_flowsQueryOptions]]]:
    """search_flows



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[Optional[ID]]], optional): values.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[Search_flowsQueryFlows]]]"""
    return (
        await aexecute(
            Search_flowsQuery, {"search": search, "values": values}, rath=rath
        )
    ).flows


def search_flows(
    search: Optional[str] = None,
    values: Optional[List[Optional[ID]]] = None,
    rath: FlussRath = None,
) -> Optional[List[Optional[Search_flowsQueryOptions]]]:
    """search_flows



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[Optional[ID]]], optional): values.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[Search_flowsQueryFlows]]]"""
    return execute(
        Search_flowsQuery, {"search": search, "values": values}, rath=rath
    ).flows


async def alist_flows(
    rath: FlussRath = None,
) -> Optional[List[Optional[ListFlowFragment]]]:
    """list_flows



    Arguments:
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ListFlowFragment]]]"""
    return (await aexecute(List_flowsQuery, {}, rath=rath)).flows


def list_flows(rath: FlussRath = None) -> Optional[List[Optional[ListFlowFragment]]]:
    """list_flows



    Arguments:
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ListFlowFragment]]]"""
    return execute(List_flowsQuery, {}, rath=rath).flows


async def aworkspace(id: ID, rath: FlussRath = None) -> Optional[WorkspaceFragment]:
    """Workspace



    Arguments:
        id (ID): id
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[WorkspaceFragment]"""
    return (await aexecute(WorkspaceQuery, {"id": id}, rath=rath)).workspace


def workspace(id: ID, rath: FlussRath = None) -> Optional[WorkspaceFragment]:
    """Workspace



    Arguments:
        id (ID): id
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[WorkspaceFragment]"""
    return execute(WorkspaceQuery, {"id": id}, rath=rath).workspace


async def amy_workspaces(
    rath: FlussRath = None,
) -> Optional[List[Optional[ListWorkspaceFragment]]]:
    """MyWorkspaces



    Arguments:
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ListWorkspaceFragment]]]"""
    return (await aexecute(MyWorkspacesQuery, {}, rath=rath)).myworkspaces


def my_workspaces(
    rath: FlussRath = None,
) -> Optional[List[Optional[ListWorkspaceFragment]]]:
    """MyWorkspaces



    Arguments:
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[ListWorkspaceFragment]]]"""
    return execute(MyWorkspacesQuery, {}, rath=rath).myworkspaces


async def aget_run(id: ID, rath: FlussRath = None) -> Optional[RunFragment]:
    """GetRun



    Arguments:
        id (ID): id
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[RunFragment]"""
    return (await aexecute(GetRunQuery, {"id": id}, rath=rath)).run


def get_run(id: ID, rath: FlussRath = None) -> Optional[RunFragment]:
    """GetRun



    Arguments:
        id (ID): id
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[RunFragment]"""
    return execute(GetRunQuery, {"id": id}, rath=rath).run


async def asearch_runs(
    search: Optional[str] = None,
    values: Optional[List[Optional[ID]]] = None,
    rath: FlussRath = None,
) -> Optional[List[Optional[SearchRunsQueryOptions]]]:
    """SearchRuns



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[Optional[ID]]], optional): values.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[SearchRunsQueryRuns]]]"""
    return (
        await aexecute(SearchRunsQuery, {"search": search, "values": values}, rath=rath)
    ).runs


def search_runs(
    search: Optional[str] = None,
    values: Optional[List[Optional[ID]]] = None,
    rath: FlussRath = None,
) -> Optional[List[Optional[SearchRunsQueryOptions]]]:
    """SearchRuns



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[Optional[ID]]], optional): values.
        rath (fluss.rath.FlussRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Optional[List[Optional[SearchRunsQueryRuns]]]"""
    return execute(
        SearchRunsQuery, {"search": search, "values": values}, rath=rath
    ).runs


ChildPortInput.update_forward_refs()
DescendendInput.update_forward_refs()
GraphInput.update_forward_refs()
NodeInput.update_forward_refs()
PortInput.update_forward_refs()
StreamItemChildInput.update_forward_refs()
StreamItemInput.update_forward_refs()
WidgetInput.update_forward_refs()
