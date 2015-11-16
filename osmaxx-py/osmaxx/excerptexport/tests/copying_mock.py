# see https://docs.python.org/3/library/unittest.mock-examples.html#coping-with-mutable-arguments
from copy import deepcopy
from unittest.mock import MagicMock


class CopyingMock(MagicMock):
    def __call__(self, *args, **kwargs):
        args = deepcopy(args)
        kwargs = deepcopy(kwargs)
        return super(CopyingMock, self).__call__(*args, **kwargs)
