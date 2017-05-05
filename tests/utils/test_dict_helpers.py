from unittest.case import TestCase

from osmaxx.utils.dict_helpers import are_all_keys_in


class AreAllKeysInTest(TestCase):
    def test_when_dict_empty_and_keys_empty_returns_true(self):
        self.assertTrue(are_all_keys_in({}, keys=[]))

    def test_when_dict_non_empty_and_keys_empty_returns_true(self):
        self.assertTrue(are_all_keys_in({'a': 'b'}, keys=[]))

    def test_when_dict_empty_and_keys_non_empty_returns_false(self):
        self.assertFalse(are_all_keys_in({}, keys=['a']))

    def test_when_all_keys_in_dict_returns_true(self):
        self.assertTrue(are_all_keys_in({'a': 'b', 'c': 'd'}, keys=['a', 'c']))

    def test_when_some_but_not_all_keys_in_dict_returns_false(self):
        self.assertFalse(are_all_keys_in({'a': 'b', 'c': 'd'}, keys=['a', 'c', 'e']))
