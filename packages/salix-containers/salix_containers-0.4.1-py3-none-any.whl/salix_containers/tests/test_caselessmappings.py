"""
Run via python -m unittest in parent folder

"""


from unittest import TestCase

from caselessmapping import CaselessMapping, CaselessMutableMapping


class TestCaselessMapping(TestCase):

    def test_null_init(self):
        self.assertRaises(TypeError, CaselessMapping)

    def test_int_keys(self):
        data = {1: 10, 2: 20, 3:30}
        cd = CaselessMapping(data)
        self.assertEqual(cd, data)

    def test_str_keys(self):
        data = {'a': 'A', 'b': 'B', 'c': 'C'}
        cd = CaselessMapping(data)
        self.assertEqual(cd, data)

    def test_matching_case_retreive(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        cd = CaselessMapping(data)
        self.assertEqual(cd['a'], data['a'])
        self.assertEqual(cd['B'], data['B'])

    def test_caseless_retreive(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        cd = CaselessMapping(data)
        self.assertEqual(cd['A'], data['a'])
        self.assertEqual(cd['b'], data['B'])

    def test_len(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        cd = CaselessMapping(data)
        self.assertEqual(len(cd), 3)

    def test_iter(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        cd = CaselessMapping(data)
        orig_tups = list(data.items())
        test_tups = list(cd.items())
        self.assertListEqual(orig_tups, test_tups)

    def test_raw_name(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        cd = CaselessMapping(data)
        self.assertEqual(cd.get_raw_key_name('b'), 'B')


class TestCaselessMutableMapping(TestCase):

    def test_null_init(self):
        cd = CaselessMutableMapping()
        self.assertEqual(cd, {})

    def test_int_keys(self):
        data = {1: 10, 2: 20, 3:30}
        cd = CaselessMutableMapping(data)
        self.assertEqual(cd, data)

    def test_str_keys(self):
        data = {'a': 'A', 'b': 'B', 'c': 'C'}
        cd = CaselessMutableMapping(data)
        self.assertEqual(cd, data)

    def test_matching_case_retreive(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        cd = CaselessMutableMapping(data)
        self.assertEqual(cd['a'], data['a'])
        self.assertEqual(cd['B'], data['B'])

    def test_caseless_retreive(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        cd = CaselessMutableMapping(data)
        self.assertEqual(cd['A'], data['a'])
        self.assertEqual(cd['b'], data['B'])

    def test_len(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        cd = CaselessMutableMapping(data)
        self.assertEqual(len(cd), 3)

    def test_iter(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        cd = CaselessMutableMapping(data)
        orig_tups = list(data.items())
        test_tups = list(cd.items())
        self.assertListEqual(orig_tups, test_tups)

    def test_raw_name(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        cd = CaselessMutableMapping(data)
        self.assertEqual(cd.get_raw_key_name('b'), 'B')

    def test_add_item_str_key(self):
       cd = CaselessMutableMapping()
       cd['x'] = 'X'
       self.assertEqual(cd, {'x': 'X'})

    def test_add_item_int_key(self):
       cd = CaselessMutableMapping()
       cd[1] = 'X'
       self.assertEqual(cd, {1: 'X'})

    def test_del_item_str_key(self):
        data = {'x': 'X', 'y': 'Y'}
        cd = CaselessMutableMapping(data)
        del cd['x']
        self.assertEqual(cd, {'y': 'Y'})

    def test_del_item_int_key(self):
        data = {1: 'X', 2: 'Y'}
        cd = CaselessMutableMapping(data)
        del cd[1]
        self.assertEqual(cd, {2: 'Y'})
