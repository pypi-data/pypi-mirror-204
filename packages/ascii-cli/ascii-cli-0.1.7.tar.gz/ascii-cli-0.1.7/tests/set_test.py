from src.functions import get_char_set
from src.functions import SET1, SET2, SET3
import argparse
import unittest


class TestCharSet(unittest.TestCase):

    # see if character sets are operational
    def test_valid_set_1(self):
        args = argparse.Namespace(set="1")
        char_set = get_char_set(args.set)
        self.assertEqual(char_set, SET1)

    def test_valid_set_2(self):
        args = argparse.Namespace(set="2")
        char_set = get_char_set(args.set)
        self.assertEqual(char_set, SET2)

    def test_valid_set_3(self):
        args = argparse.Namespace(set="3")
        char_set = get_char_set(args.set)
        self.assertEqual(char_set, SET3)

    def test_invalid_set(self):
        args = argparse.Namespace(set="4")
        char_set = get_char_set(args.set)
        self.assertEqual(char_set, SET4)


if __name__ == '__main__':
    unittest.main()
