from functools import reduce
from .tasker_func import (
    f_,
    BaseTasker,
    cast_as_base_tasker
)


class ETLList:
    def __init__(
        self,
        *args,
        is_depend: bool = False
        ):
        self.etl_list = [
            cast_as_base_tasker(task) for task in args
        ]

    def run(self):
        if self.is_depend:
            pass