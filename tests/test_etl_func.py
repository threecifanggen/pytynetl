from pytynetl.tasker_func import f_
from pytynetl.exceptions import NotIllegalRetryingNumber
import pytest


def test_func_initial():

    with pytest.raises(NotIllegalRetryingNumber):
        @f_(retrying=-1)
        def f(x):
            return x + 1

    @f_(retrying=1)
    def f(x):
        return x + 1

    @f_(retrying=2)
    def g(x):
        return x * 2

    assert f(g(1)) == 3
    assert g(f(1)) == 4


def test_pipe_run():
    @f_(retrying=1)
    def f(x):
        return x + 1

    @f_
    def g(x):
        return x * 2

    assert (f >> g)(1) == 4
    assert (g >> f)(1) == 3


def test_pipe_run_with_multiple_args():
    @f_
    def f(x, y):
        return x - y + 1

    @f_(retrying=2)
    def g(x):
        return x * 2

    assert (f >> g)(2, 1) == 4
