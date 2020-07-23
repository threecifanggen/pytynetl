from typing import Optional
from .exceptions import NotIllegalRetryingNumber

class BaseTasker:
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
        return self.func(*args, **kargs)

    def __call__(self, *args, **kargs):
        return self.run(*args, **kargs)

def f_(retrying: Optional[int] = None):
    """Decorator For Instantialise the BaseTasker

    Args:
        retrying ([int, optional): [description]. Defaults to None.
    """
    def helper(func):
        return BaseTasker(func, retrying)
    return helper
