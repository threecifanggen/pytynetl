from typing import Optional
from .exceptions import NotIllegalRetryingNumber

class BaseTasker:
    """BaseTasker For ETL
    """
    def __init__(
        self,
        func,
        retrying: Optional[int] = None):
        self.func = func
        if isinstance(retrying, int) and retrying < 0:
            raise NotIllegalRetryingNumber(
            "Retrying Time must greater than 0",
            f"but got {retrying}."
        )
        self.retrying = retrying
    
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

    def __rshift__(self, other):
        return self.pipe_func(other)


def f_(retrying: Optional[int] = None):
    """Decorator For Instantialise the BaseTasker

    Args:
        retrying ([int, optional): [description]. Defaults to None.
    """
    def helper(func):
        return BaseTasker(func, retrying)
    return helper
