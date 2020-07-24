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
        if task_name == "":
            self.task_name = func.__name__
        else:
            self.task_name = task_name
        self.retrying = retrying
        self.if_error = if_error
        
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

    def update_dag(self, other) -> NoReturn:
        if other.dag is not None:
            self @ other.dag
        else:
            other @ self.dag

    def __rshift__(self, other):
        self.update_dag(other)
        other.add_before_independ_task(self)
        self.add_after_independ_task(other)
        return other
    
    def __lshift__(self, other):
        self.update_dag(other)
        other.add_after_independ_task(self)
        self.add_before_depend_task(other)
        return other
    
    def __irshift__(self, other):
        self.update_dag(other)
        other.add_before_depend_task(self)
        self.add_after_depend_task(other)
        return other

    def __ilshift__(self, other):
        self.update_dag(other)
        other.add_after_depend_task(self)
        self.add_before_depend_task(other)
        return other

    def __matmul__(self, dag):
        self.set_dag(dag)
        dag.add_node(self)
        return self


class ETLDAG(object):
    """ETLDAG
    """
    nodes: Dict[str, ETLNode] = dict()

    def __init__(self, nodes_iterable: Iterable[ETLNode] = None):
        if nodes_iterable:
            for node in nodes_iterable:
                self.nodes[node.task_name] = node
                node.set_dag(self)
        else:
            pass
    
    def add_node(self, node: ETLNode):
        self.nodes[node.task_name] = node

    def node_(self, *args, **kwargs):
        if len(args) == 1 and callable(args[0]):
            node = ETLNode(args[0])
            return (node @ self)
        else:
            def helper(func):
                node = ETLNode(func, *args, **kwargs)
                return (node @ self)
            return helper

    def __contains__(self, node: ETLNode) -> bool:
        """Contain operator

        Examples:

            >>> node in dag
            True

        Args:
            node (ETLNode): checking node

        Returns:
            bool: Where node is in DAQ
        """
        if node.task_name in self.nodes.keys():
            return node.__hash__ == self.nodes[node.task_name].__hash__
        else:
            False

    def __getitem__(self, k):
        return self.nodes[k]


def node_(*args, **kwargs) -> ETLNode:
    """ETLNode Maker Decorator

    Returns:
        ETLNode
    """
    if len(args) == 1 and callable(args[0]):
        return ETLNode(args[0])
    else:
        def helper(func):
            return ETLNode(func, *args, **kwargs)
        return helper

def etl_dag(*args) -> ETLDAG:
    """Using args as ETLDAG to DAQ

    Returns:
        ETLDAG: Generater DAQ
    """
    return ETLDAG(args)
