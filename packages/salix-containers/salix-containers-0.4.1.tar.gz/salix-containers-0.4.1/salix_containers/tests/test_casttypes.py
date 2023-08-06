"""
Run via python -m unittest in parent folder

"""


import sys
import unittest

from casttypes import *


class TestCastDict(unittest.TestCase):

    def test_init1(self):
        d = {1: 10, 2:20}
        cd = CastDict(d, cast_map={})
        self.assertDictEqual(cd, d)

    def test_init2(self):
        d = {1: 10, 2:20}
        cd = CastDict([(1, 10), (2, 20)], cast_map={})
        self.assertDictEqual(cd, d)

    def test_init3(self):
        d = {(1, 10): 100, (2, 20): 200}
        cd = CastDict(d, cast_map={})
        self.assertDictEqual(cd, d)

    def test_init4(self):
        d = {1: [1, 2, 3], 2: [2, 3, 4]}
        cd = CastDict(d, cast_map={})
        self.assertDictEqual(cd, d)

    def test_init5(self):
        d = {1: {10: ['a', 'b'], 20: ['A', 'B']}, '2': (5, 6)}
        cd = CastDict(d, cast_map={})
        self.assertDictEqual(cd, d)

    def test_cast1(self):
        d = {1: {10: 100}}
        cd = CastDict(d, cast_map={dict: dict})
        self.assertDictEqual(cd, d)

    def test_cast2(self):
        d = {1: {10: 100}}
        cd = CastDict(d, cast_map={list: list})
        self.assertDictEqual(cd, d)

    def test_cast3(self):
        d = {1: {10: 100}}
        cd = CastDict(d, cast_map={dict: list})
        self.assertDictEqual(cd, {1: [10]})

    def test_cast4(self):
        d = {1: [(1, 10), (2, 20)]}
        cd = CastDict(d, cast_map={list: dict})
        self.assertDictEqual(cd, {1: {1: 10, 2: 20}})

    def test_cast5(self):
        d = {'1': '10', '2': '20'}
        cd = CastDict(d, cast_map={str: int})
        self.assertDictEqual(cd, {'1': 10, '2': 20})

    def test_cast6(self):
        d = {1: (2, 3, 4)}
        cd = CastDict(d, cast_map={list: str})
        self.assertDictEqual(cd, d)

    def test_cast7(self):
        d = {1: {10: {100: '111'}, 20: '222'}, 2: '22'}
        cd = CastDict(d, cast_map={str: int})
        self.assertDictEqual(cd, {1: {10: {100: 111}, 20: 222}, 2: 22})
        self.assertIsInstance(cd[1], CastDict)
        self.assertIsInstance(cd[1][10], CastDict)

    def test_cast8(self):
        d = {1: [{2: '20'}, {3: '30'}]}
        cd = CastDict(d, cast_map={str: int})
        self.assertDictEqual(cd, {1: [{2: 20}, {3: 30}]})
        self.assertIsInstance(cd[1], CastList)
        self.assertIsInstance(cd[1][0], CastDict)

    def test_cast9(self):
        d = {1: (1, 2, 3)}
        cd = CastDict(d, cast_map={tuple: sum})
        self.assertDictEqual(cd, {1: 6})

    def test_cast10(self):
        d = {1: ('a', 'b', 'c'), 2: ('1', '2', '3')}
        cd = CastDict(d, cast_map={tuple: lambda x: ':'.join(x)})
        self.assertDictEqual(cd, {1: 'a:b:c', 2: '1:2:3'})

