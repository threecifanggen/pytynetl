from functools import reduce
from typing import (
    NoReturn, Optional,
    Callable,
    Any,
    NoReturn,
    Dict,
    Iterable
)
from .tasker_func import (
    BaseTasker,
)
from .exceptions import (
    NotIllegalRetryingNumber
)


class ETLNode(BaseTasker):
    before_depend_node: set = set()
    before_independ_node: set = set()
    after_depend_node: set = set()
    after_independ_node: set = set()

    def __init__(self,
        func,
        task_name: str = "",
        retrying: int = 0,
        if_error: Optional[Callable[[], Any]] = None,
        dag = None
        ):
        self.func = func
        if isinstance(retrying, int) and retrying < 0:
            raise NotIllegalRetryingNumber(
            "Retrying Time must greater than 0",
            f"but got {retrying}."
        )
        self.retrying = retrying
        self.if_error = if_error
        self.task_name = task_name
        self.dag = dag

    def add_before_depend_task(self, other) -> NoReturn:
        self.before_depend_node.add(other)
    
    def add_before_independ_task(self, other) -> NoReturn:
        self.before_independ_node.add(other)

    def add_after_depend_task(self, other) -> NoReturn:
        self.after_depend_node.add(other)
    
    def add_after_independ_task(self, other) -> NoReturn:
        self.after_independ_node.add(other)

    def set_dag(self, dag):
        self.dag = dag

    def __rshift__(self, other):
        if other.dag is not None:
            self.set_dag(other.dag)
        else:
            other.set_dag(self.dag)
        other.add_before_independ_task(self)
        self.add_after_independ_task(other)
        return other
    
    def __lshift__(self, other):
        if other.dag is not None:
            self.set_dag(other.dag)
        else:
            other.set_dag(self.dag)
        other.add_after_independ_task(self)
        self.add_before_depend_task(other)
        return other
    
    def __irshift__(self, other):
        if other.dag is not None:
            self.set_dag(other.dag)
        else:
            other.set_dag(self.dag)
        other.add_before_depend_task(self)
        self.add_after_depend_task(other)
        return other

    def __ilshift__(self, other):
        if other.dag is not None:
            self.set_dag(other.dag)
        else:
            other.set_dag(self.dag)
        other.add_after_depend_task(self)
        self.add_before_depend_task(other)
        return other

    def __matmul__(self, dag):
        self.set_dag(dag)
        dag.add_node(self)


class ETLDAG(object):
    nodes: Dict[ETLNode] = dict()

    def __init__(self, nodes_iterable: Iterable[ETLNode]):
        for node in nodes_iterable:
            self.nodes[node.task_name] = node
    
    def add_node(self, node: ETLNode):
        self.nodes[node.task_name] = node

