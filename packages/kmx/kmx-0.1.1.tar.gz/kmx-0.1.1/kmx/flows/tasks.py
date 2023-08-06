from typing import Protocol, Callable

import abc
import inspect

from pydantic import BaseModel

from .models import FlowRun
from .flow import Flow, FlowDAGContext


# -------------------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------------
class FlowTask(Protocol):
    """ 
    Определение задачи в потоке 
    """

    name: str
    flow: Flow | None

    def __rshift__(self, other: 'FlowTask') -> 'FlowTask':
        """ """
        ...

    async def run(self, context: BaseModel | dict, flow_run: FlowRun):
        """ """


# -------------------------------------------------------------------------------------------------
# Базовый класс для задач
# ----------------------------------------------------------------------------------------------------------------------
class FlowTaskBase:
    """ """
    def __init__(self, name: str, flow: Flow | None = None):
        """ """
        if not name:
            raise Exception('Empty task name is not allowed')
        
        self.name = name
        self.flow = flow or FlowDAGContext.current_flow()

        if self.flow is None:
            raise Exception('No flow in context')

        self.flow.add_task(self)

    def __rshift__(self, other: FlowTask) -> FlowTask:
        """
        Add dependency between tasks in flow
        """
        if self.flow is None:
            raise Exception(f'Task `{self.name}` has no assigned flow')
        
        if other.flow is None:
            raise Exception(f'Task `{other.name}` has no assigned flow')
        
        if self.flow != other.flow:
            raise Exception(f"DAG for task {self.name} is not the same as for {other.name} "
                            f"(DAGs: {self.flow.name} and {other.flow.name})")
        
        self.flow.add_edge(self, other)
        
        return other

    @abc.abstractmethod
    async def run(self, context: BaseModel | dict, flow_run: FlowRun):
        """ """


class PythonTask(FlowTaskBase):
    """ 
    Задача, которая выполняет определенный питоновский код
    """
    def __init__(self, name: str, cb: Callable, flow: Flow | None = None):
        super().__init__(name=name, flow=flow)
        self.cb = cb

    async def run(self, context: BaseModel | dict, flow_run: FlowRun):
        cb_args = {}

        cb_spec = inspect.getfullargspec(self.cb)
        if 'context' in cb_spec.args:
            cb_args['context'] = context
        if 'flow_run' in cb_spec.args:
            cb_args['flow_run'] = flow_run

        await self.cb(**cb_args)
