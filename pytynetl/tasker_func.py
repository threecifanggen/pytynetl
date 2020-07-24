from typing import Callable, Optional, Union, Callable, Any
from .exceptions import (
    NotIllegalRetryingNumber,
    IllegalTypeToCastAsABaseTasker
)

class BaseTasker(object):
    """BaseTasker For ETL
    """
    def __init__(
        self,
        func,
        retrying: int = 0,
        if_error: Optional[Callable[[], Any]] = None
        ):
        self.func = func
        if isinstance(retrying, int) and retrying < 0:
            raise NotIllegalRetryingNumber(
            "Retrying Time must greater than 0",
            f"but got {retrying}."
        )
        self.retrying = retrying
        self.if_error = if_error
    
    def run(self, *args, **kargs):
        """Excute functions

        Returns:
            [type]: [description]
        """
        return self.func(*args, **kargs)

    def __call__(self, *args, **kargs):
        return self.run(*args, **kargs)

    def pipe_func(self, other):
        def helper(*args, **kargs):
            return other.func(self.func(*args, **kargs))
        return helper

    def __ge__(self, other):
        return self.pipe_func(other)

    def execute(self, *args, **kargs):
        def helper(num=self.retrying + 1):
            try:
                return self.run(*args, **kargs)
            except:
                if num == 1:
                    if self.if_error is not None:
                        return self.if_error()
                    else:
                        raise
                else:
                    return helper(num-1)
        return helper()


def f_(*args, **kwargs):
    """Decorator For Instantialise the BaseTasker

    Args:
        retrying ([int, optional): [description]. Defaults to None.
    """
    if len(args) == 1 and callable(args[0]):
        ## If there has no parameter in decorator
        return BaseTasker(args[0])
    else:
        ## There has parameter(s) in decorator
        def helper(func):
            return BaseTasker(func, *args, **kwargs)
        return helper

def cast_as_base_tasker(obj: Union[Callable, BaseTasker]) -> BaseTasker:
    """cast object to a BaseTasker

    Args:
        obj (Union[Callable, BaseTasker]): object

    Raises:
        IllegalTypeToCastAsABaseTasker: Only BaseTasker
            and Callable object can be parameters

    Returns:
        BaseTasker: results
    """
    if isinstance(obj, BaseTasker):
        return obj
    elif callable(obj):
        return f_(obj)
    else:
        raise IllegalTypeToCastAsABaseTasker(
        "Requires a Callable or BaseTasker Object",
        f"But got {str(type(obj))}"
    )
