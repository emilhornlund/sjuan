# tests/test_constants.py

import unittest

from lib.constants import Rank


class TestRank(unittest.TestCase):

    def test_rank_comparison(self):
        # Test that an ACE rank is considered less than a TWO rank
        self.assertTrue(Rank.ACE < Rank.TWO)
        # Test that a KING rank is not considered less than an ACE rank
        self.assertFalse(Rank.KING < Rank.ACE)
        # Test that a KING rank is considered greater than an ACE rank
        self.assertTrue(Rank.KING > Rank.ACE)
        # Test that an ACE rank is not considered greater than a TWO rank
        self.assertFalse(Rank.ACE > Rank.TWO)

    def test_rank_above(self):
        # Test that the rank above ACE is TWO
        self.assertEqual(Rank.ACE.get_rank_above(), Rank.TWO)
        # Test that the rank above KING is KING itself, as there is no rank above KING
        self.assertEqual(Rank.KING.get_rank_above(), Rank.KING)

    def test_rank_below(self):
        # Test that the rank below ACE is ACE itself, as there is no rank below ACE
        self.assertEqual(Rank.ACE.get_rank_below(), Rank.ACE)
        # Test that the rank below TWO is ACE
        self.assertEqual(Rank.TWO.get_rank_below(), Rank.ACE)


if __name__ == '__main__':
    unittest.main()
