
from collections.abc import MutableMapping


class EmptyDict(MutableMapping):

    def __init__(self, *args, **kwargs):
        super().__init__()

    def __getitem__(self, key, *args, **kwargs):
        raise KeyError(key)

    def __len__(self):
        return 0

    def __iter__(self):
        return iter([])

    def __setitem__(self, *args, **kwargs):
        pass

    def __delitem__(self, key, *args, **kwargs):
        raise KeyError(key)
