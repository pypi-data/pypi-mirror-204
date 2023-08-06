import unittest

from orderedset import OrderedSet
from orderedset import FrozenOrderedSet

class TestOrderedset(unittest.TestCase):
    def test_toset(self):
        self.assertEqual({1, 2, 3}, set(OrderedSet([3, 1, 2])))

    def test_tolist(self):
        self.assertEqual([3, 1, 2], list(OrderedSet([3, 1, 2])))

    def test_eq(self):
        self.assertTrue(OrderedSet([1, 2, 3]) == OrderedSet([1, 2, 3]))

    def test_eq_set(self):
        self.assertTrue({1, 2, 3} == OrderedSet([3, 1, 2]))

    def test_eq_list(self):
        self.assertTrue([3, 1, 2] == OrderedSet([3, 1, 2]))

    def test_ne(self):
        self.assertTrue(OrderedSet([1, 2, 3]) != OrderedSet([3, 2, 1]))

    def test_str(self):
        self.assertEqual("{3, 1, 2}", str(OrderedSet([3, 1, 2])))

    def test_str_frozen(self):
        self.assertEqual("{3, 1, 2}", str(FrozenOrderedSet([3, 1, 2])))

    def test_repr(self):
        self.assertEqual(
            "OrderedSet({3: None, 1: None, 2: None})", repr(OrderedSet([3, 1, 2])))

    def test_add(self):
        s: OrderedSet[int] = OrderedSet([3, 1, 2])
        s.add(0)
        self.assertEqual(OrderedSet([3, 1, 2, 0]), s)

    def test_clear(self):
        s: OrderedSet[int] = OrderedSet([3, 1, 2])
        s.clear()
        self.assertFalse(s)
        self.assertEqual(0, len(s))

    def test_difference(self):
        s_1 = OrderedSet([3, 1, 2])
        s_2 = OrderedSet([1, 7])
        self.assertEqual(OrderedSet([3, 2]), s_1.difference(s_2))
        self.assertFalse(s_1.difference(s_1))

    def test_difference_update(self):
        s_1 = OrderedSet([3, 1, 2])
        s_2 = OrderedSet([1, 7])
        s_1.difference_update(s_2)
        self.assertEqual(OrderedSet([3, 2]), s_1)

    def test_discard(self):
        s = OrderedSet([3, 1, 2])
        s.discard(1)
        self.assertEqual(OrderedSet([3, 2]), s)

        try:
            s.discard(42)
            self.fail()
        except KeyError:
            pass

    def test_remove(self):
        s = OrderedSet([3, 1, 2])
        s.remove(1)
        self.assertEqual(OrderedSet([3, 2]), s)

        try:
            s.remove(42)
            self.fail()
        except KeyError:
            pass

    def test_intersection(self):
        s_1 = OrderedSet([3, 1, 2])
        s_2 = OrderedSet([1, 7])
        self.assertEqual(OrderedSet([1]), s_1.intersection(s_2))
        self.assertEqual(s_1, s_1.intersection(s_1))

    def test_intersection_update(self):
        s_1 = OrderedSet([3, 1, 2])
        s_2 = OrderedSet([1, 7])
        s_1.intersection_update(s_2)
        self.assertEqual(OrderedSet([1]), s_1)

    def test_disjoint(self):
        s_1 = OrderedSet([3, 1, 2])
        s_2 = OrderedSet([1, 7])
        self.assertFalse(s_1.isdisjoint(s_2))

        s_3 = OrderedSet([10, 7])
        self.assertTrue(s_1.isdisjoint(s_3))

    def test_issubset(self):
        s_1 = OrderedSet([3, 1, 2])
        s_2 = OrderedSet([1, 7])
        self.assertFalse(s_2.issubset(s_1))
        s_2.discard(7)
        self.assertTrue(s_2.issubset(s_1))
        self.assertTrue(OrderedSet().issubset(s_1))

    def test_issuperset(self):
        s_1 = OrderedSet([3, 1, 2])
        s_2 = OrderedSet([1, 7])
        self.assertFalse(s_1.issuperset(s_2))
        s_2.discard(7)
        self.assertTrue(s_1.issuperset(s_2))
        self.assertTrue(OrderedSet(s_1).issuperset(s_2))

    def test_pop(self):
        s_1 = OrderedSet([3, 1, 2])
        self.assertEqual(2, s_1.pop())
        self.assertEqual(OrderedSet([3, 1]), s_1)

    def test_symmetric_difference(self):
        s_1 = OrderedSet([3, 1, 2])
        s_2 = OrderedSet([1, 7])
        self.assertEqual(OrderedSet([3, 2, 7]), s_1.symmetric_difference(s_2))

    def test_union(self):
        s_1 = OrderedSet([3, 1, 2])
        s_2 = OrderedSet([1, 7])
        self.assertEqual(OrderedSet([3, 1, 2, 7]), s_1.union(s_2))

    def test_contains(self):
        s = OrderedSet([3, 1, 2])
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertTrue(3 in s)
        self.assertFalse(4 in s)

    def test_le(self):
        self.assertLessEqual(OrderedSet([1, 2, 3]), OrderedSet([1, 2, 3]))
        self.assertLessEqual(OrderedSet([1, 2]), OrderedSet([1, 2, 3]))
        self.assertFalse(OrderedSet([1, 2, 3]) <= OrderedSet([1, 2]))

    def test_lt(self):
        self.assertLess(OrderedSet([1, 2]), OrderedSet([1, 2, 3]))
        self.assertFalse(OrderedSet([1, 2, 3]) < OrderedSet([1, 2, 3]))

    def test_ge(self):
        self.assertGreaterEqual(OrderedSet([1, 2, 3]), OrderedSet([1, 2, 3]))
        self.assertGreaterEqual(OrderedSet([1, 2, 3]), OrderedSet([1, 2]))
        self.assertFalse(OrderedSet([1, 2]) >= OrderedSet([1, 2, 3]))

    def test_gt(self):
        self.assertGreater(OrderedSet([1, 2, 3]), OrderedSet([1, 2]))
        self.assertFalse(OrderedSet([1, 2, 3]) > OrderedSet([1, 2, 3]))

    def test_get(self):
        self.assertEqual(OrderedSet([1])[0], 1)
        self.assertEqual(OrderedSet([3, 2, 1])[0], 3)
        self.assertEqual(OrderedSet([3, 2, 1])[1], 2)
        self.assertEqual(OrderedSet([3, 2, 1])[2], 1)


if __name__ == '__main__':
    unittest.main()
