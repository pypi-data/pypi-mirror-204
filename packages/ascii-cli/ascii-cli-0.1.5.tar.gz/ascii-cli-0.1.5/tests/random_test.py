import unittest
from unittest.mock import MagicMock
from src.functions import randomize, SET1, SET2, SET3


class TestRandomize(unittest.TestCase):

    def test_randomize(self):
        # Test randomize when args.random is True
        args = MagicMock(random=True, set="1")
        randomize(args)
        if args.set == "1":
            self.assertNotEqual(args.set, SET1)
        elif args.set == "2":
            self.assertNotEqual(args.set, SET2)
        elif args.set == "3":
            self.assertNotEqual(args.set, SET3)


if __name__ == '__main__':
    unittest.main()
