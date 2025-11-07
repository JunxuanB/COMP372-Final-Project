"""Unit tests for priority queue data structures."""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fringe import BinaryHeap, SortedLinkedList


class TestPriorityQueue(unittest.TestCase):
    """Base test class for both implementations."""

    def setUp(self):
        self.pq = None

    def test_initialization(self):
        if self.pq is None:
            self.skipTest("Base class test")
        self.assertTrue(self.pq.is_empty())
        self.assertEqual(self.pq.size(), 0)

    def test_insert_and_size(self):
        if self.pq is None:
            self.skipTest("Base class test")
        self.pq.insert("A", 5.0)
        self.assertFalse(self.pq.is_empty())
        self.assertEqual(self.pq.size(), 1)

    def test_extract_min_order(self):
        if self.pq is None:
            self.skipTest("Base class test")
        elements = [("D", 10.0), ("A", 5.0), ("C", 8.0), ("B", 3.0), ("E", 1.0)]

        for key, priority in elements:
            self.pq.insert(key, priority)

        expected = [("E", 1.0), ("B", 3.0), ("A", 5.0), ("C", 8.0), ("D", 10.0)]
        for expected_key, expected_priority in expected:
            key, priority = self.pq.extract_min()
            self.assertEqual(key, expected_key)
            self.assertEqual(priority, expected_priority)

        self.assertTrue(self.pq.is_empty())

    def test_extract_min_empty(self):
        if self.pq is None:
            self.skipTest("Base class test")
        with self.assertRaises(IndexError):
            self.pq.extract_min()

    def test_decrease_key(self):
        if self.pq is None:
            self.skipTest("Base class test")
        self.pq.insert("A", 10.0)
        self.pq.insert("B", 5.0)
        self.pq.decrease_key("A", 2.0)

        key, priority = self.pq.extract_min()
        self.assertEqual(key, "A")
        self.assertEqual(priority, 2.0)

    def test_decrease_key_invalid(self):
        if self.pq is None:
            self.skipTest("Base class test")
        self.pq.insert("A", 5.0)

        with self.assertRaises(ValueError):
            self.pq.decrease_key("A", 10.0)

        with self.assertRaises(KeyError):
            self.pq.decrease_key("Z", 1.0)

    def test_duplicate_insert(self):
        if self.pq is None:
            self.skipTest("Base class test")
        self.pq.insert("A", 10.0)
        self.pq.insert("A", 5.0)

        key, priority = self.pq.extract_min()
        self.assertEqual(priority, 5.0)
        self.assertTrue(self.pq.is_empty())


class TestBinaryHeap(TestPriorityQueue):

    def setUp(self):
        self.pq = BinaryHeap()

    def test_heap_property(self):
        heap = BinaryHeap()
        elements = [("D", 10.0), ("A", 5.0), ("C", 8.0), ("B", 3.0)]
        for key, priority in elements:
            heap.insert(key, priority)
            self._verify_heap_property(heap)

    def _verify_heap_property(self, heap: BinaryHeap):
        for i in range(len(heap._heap)):
            left = 2 * i + 1
            right = 2 * i + 2

            if left < len(heap._heap):
                self.assertLessEqual(heap._heap[i][1], heap._heap[left][1])

            if right < len(heap._heap):
                self.assertLessEqual(heap._heap[i][1], heap._heap[right][1])


class TestSortedLinkedList(TestPriorityQueue):

    def setUp(self):
        self.pq = SortedLinkedList()

    def test_sorted_order(self):
        slist = SortedLinkedList()
        elements = [("D", 10.0), ("A", 5.0), ("C", 8.0), ("B", 3.0)]
        for key, priority in elements:
            slist.insert(key, priority)
            self._verify_sorted(slist)

    def _verify_sorted(self, slist: SortedLinkedList):
        current = slist._head
        while current and current.next:
            self.assertLessEqual(current.priority, current.next.priority)
            current = current.next


if __name__ == '__main__':
    unittest.main()
