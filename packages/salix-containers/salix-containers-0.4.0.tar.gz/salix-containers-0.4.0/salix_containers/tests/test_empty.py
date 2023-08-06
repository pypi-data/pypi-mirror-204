"""
Run via python -m unittest in parent folder

"""

from unittest import TestCase

from empty import *


class TestEmptyDict(TestCase):

    def test_null_init(self):
        self.assertEqual(EmptyDict(), {})

    def test_init(self):
        data = {1: 10, 2: 20, 3:30}
        e = EmptyDict(data)
        self.assertEqual(e, {})

    def test_retreive(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        e = EmptyDict(data)
        self.assertRaises(KeyError, lambda x: e[x], 'a')
        self.assertIsNone(e.get('a'))

    def test_len(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        e = EmptyDict(data)
        self.assertEqual(len(e), 0)

    def test_iter(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        e = EmptyDict(data)
        self.assertListEqual(list(iter(e)), [])
        self.assertListEqual(list(e.keys()), [])
        self.assertListEqual(list(e.values()), [])
        self.assertListEqual(list(e.items()), [])

    def test_add_item_(self):
        e = EmptyDict()
        e['x'] = 'X'
        self.assertFalse('x' in e)
        self.assertIsNone(e.get('x'))
        self.assertRaises(KeyError, lambda e, x: e[x], e, 'x')

    def test_del_item(self):
        data = {'a': 'A', 'B': 'B', 'c': 'C'}
        e = EmptyDict(data)
        def f(e, x):
            del e[x]
        self.assertRaises(KeyError, f, e, 'a')
