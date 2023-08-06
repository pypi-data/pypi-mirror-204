from typing import TYPE_CHECKING, Optional, Any

from collections import deque

from pydantic import BaseModel
import networkx as nx


if TYPE_CHECKING:
    from kmx.flows.tasks import FlowTask


class Flow:
    """ """
    def __init__(self, name: str, context_model: Any = None):
        self.name = name
        self.context_model = context_model
        self.tasks: list['FlowTask'] = []
        self.graph = nx.DiGraph()

    def __enter__(self) -> 'Flow':
        FlowDAGContext.push_flow(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        FlowDAGContext.pop_flow()

    def get_task_by_name(self, task_name: str) -> Optional['FlowTask']:
        """ 
        Возвращает задачу по её названию
        """
        return next((t for t in self.tasks if t.name == task_name), None)

    def add_task(self, task: 'FlowTask') -> 'FlowTask':
        """ """
        if self.get_task_by_name(task.name) is None:
            self.tasks.append(task)
            self.graph.add_node(task.name)
        return task

    def add_edge(self, task_from: 'FlowTask', task_to: 'FlowTask'):
        """ """
        if self.get_task_by_name(task_from.name) is None:
            raise Exception(f"Задача {task_from.name} не добавлена в Flow")

        if self.get_task_by_name(task_to.name) is None:
            raise Exception(f"Задача {task_to.name} не добавлена в DAG {self.name}")

        self.graph.add_edge(task_from.name, task_to.name)

        return

    def heads(self) -> list['FlowTask']:
        """ """
        head_nodes = [node for node, degree in self.graph.in_degree if degree == 0]

        return [task for head_name in head_nodes if (task := self.get_task_by_name(head_name)) if not None]

    def successors(self, task_name: str) -> list['FlowTask']:
        """ """
        successor_names = self.graph.successors(task_name)

        return [task for name in successor_names if (task := self.get_task_by_name(name)) is not None]



class FlowDAGContext:
    """ """
    graphs = deque()

    @classmethod
    def push_flow(cls, graph: Flow):
        FlowDAGContext.graphs.append(graph)

    @classmethod
    def pop_flow(cls) -> Flow | None:
        return FlowDAGContext.graphs.pop() if FlowDAGContext.graphs else None

    @classmethod
    def current_flow(cls) -> Flow | None:
        return FlowDAGContext.graphs[-1] if FlowDAGContext.graphs else None


class FlowPack:
    """ """
    def __init__(self):
        """ """
        self.flows: dict[str, Flow] = {}

    def add_flow(self, flow: Flow) -> Flow:
        if flow.name in self.flows:
            raise Exception(f'Flow `{flow.name}` already added')
        self.flows[flow.name] = flow
        return flow

    @property
    def flow_names(self) -> list[str]:
        return [flow.name for _, flow in self.flows.items()]

    def flow_exists(self, flow: Flow) -> bool:
        return flow.name in self.flows.keys()

    def get_flow_by_name(self, flow_name: str) -> Flow:
        return self.flows[flow_name]

    def __getitem__(self, item: str) -> Flow:
        if item not in self.flows:
            raise Exception('Flow `name` not found in flowpack')
        return self.flows[item]
