
from collections.abc import Mapping, MutableMapping


class CaselessMapping(Mapping):

    def __init__(self, init):
        init_dict = dict(init)
        self._data = {self.norm_key(key): (key, value) for key, value in init_dict.items()}

    @staticmethod
    def norm_key(key):
        if isinstance(key, str):
            return key.lower()
        else:
            return key

    def __getitem__(self, key):
        return self._data[self.norm_key(key)][1]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        for key in self._data.keys():
            yield self._data[key][0]

    def get_raw_key_name(self, key):
        return self._data[self.norm_key(key)][0]


class CaselessMutableMapping(MutableMapping, CaselessMapping):

    def __init__(self, init=None):
        super().__init__(init if init is not None else {})

    def __setitem__(self, key, value):
        self._data[self.norm_key(key)] = (key, value)

    def __delitem__(self, key):
        del self._data[self.norm_key(key)]

