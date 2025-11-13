"""Unit tests for priority queue data structures - basic functionality only."""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fringe import BinaryHeap, SortedLinkedList


class TestBinaryHeap(unittest.TestCase):
    """Basic tests for BinaryHeap priority queue."""

    def test_insert_and_size(self):
        """Test inserting elements and checking size."""
        heap = BinaryHeap()
        self.assertTrue(heap.is_empty())

        heap.insert("A", 5.0)
        heap.insert("B", 3.0)

        self.assertFalse(heap.is_empty())
        self.assertEqual(heap.size(), 2)

    def test_extract_min_order(self):
        """Test that extract_min returns elements in priority order."""
        heap = BinaryHeap()
        heap.insert("D", 10.0)
        heap.insert("A", 5.0)
        heap.insert("B", 3.0)

        key1, priority1 = heap.extract_min()
        self.assertEqual(key1, "B")
        self.assertEqual(priority1, 3.0)

        key2, priority2 = heap.extract_min()
        self.assertEqual(key2, "A")
        self.assertEqual(priority2, 5.0)

    def test_decrease_key(self):
        """Test decreasing priority of an element."""
        heap = BinaryHeap()
        heap.insert("A", 10.0)
        heap.insert("B", 5.0)

        heap.decrease_key("A", 2.0)

        key, priority = heap.extract_min()
        self.assertEqual(key, "A")
        self.assertEqual(priority, 2.0)


class TestSortedLinkedList(unittest.TestCase):
    """Basic tests for SortedLinkedList priority queue."""

    def test_insert_and_extract(self):
        """Test inserting and extracting elements."""
        slist = SortedLinkedList()
        slist.insert("C", 8.0)
        slist.insert("A", 5.0)
        slist.insert("B", 3.0)

        key, priority = slist.extract_min()
        self.assertEqual(key, "B")
        self.assertEqual(priority, 3.0)


if __name__ == '__main__':
    unittest.main()
