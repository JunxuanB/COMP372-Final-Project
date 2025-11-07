"""
Unit tests for fringe data structures (BinaryHeap and SortedLinkedList).

Tests cover:
- Insert, extract_min, and decrease_key operations
- Heap property maintenance
- Edge cases and error handling
- Comparison between implementations
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fringe import BinaryHeap, SortedLinkedList, PriorityQueue


class TestPriorityQueue(unittest.TestCase):
    """Base test class with common tests for both implementations."""

    def setUp(self):
        """Override this in subclasses to set self.pq."""
        self.pq = None

    def test_initialization(self):
        """Test priority queue initialization."""
        if self.pq is None:
            self.skipTest("Base class test")
        self.assertIsNotNone(self.pq)
        self.assertTrue(self.pq.is_empty())
        self.assertEqual(self.pq.size(), 0)

    def test_insert_and_size(self):
        """Test inserting elements and size tracking."""
        if self.pq is None:
            self.skipTest("Base class test")
        self.pq.insert("A", 5.0)
        self.assertFalse(self.pq.is_empty())
        self.assertEqual(self.pq.size(), 1)

        self.pq.insert("B", 3.0)
        self.assertEqual(self.pq.size(), 2)

        self.pq.insert("C", 7.0)
        self.assertEqual(self.pq.size(), 3)

    def test_extract_min_order(self):
        """Test that extract_min returns elements in priority order."""
        if self.pq is None:
            self.skipTest("Base class test")
        elements = [("D", 10.0), ("A", 5.0), ("C", 8.0), ("B", 3.0), ("E", 1.0)]

        for key, priority in elements:
            self.pq.insert(key, priority)

        # Should extract in priority order: E(1), B(3), A(5), C(8), D(10)
        expected_order = [("E", 1.0), ("B", 3.0), ("A", 5.0), ("C", 8.0), ("D", 10.0)]

        for expected_key, expected_priority in expected_order:
            key, priority = self.pq.extract_min()
            self.assertEqual(key, expected_key)
            self.assertEqual(priority, expected_priority)

        self.assertTrue(self.pq.is_empty())

    def test_extract_min_empty(self):
        """Test extracting from empty queue raises error."""
        if self.pq is None:
            self.skipTest("Base class test")
        with self.assertRaises(IndexError):
            self.pq.extract_min()

    def test_decrease_key(self):
        """Test decreasing priority of an element."""
        if self.pq is None:
            self.skipTest("Base class test")
        self.pq.insert("A", 10.0)
        self.pq.insert("B", 5.0)
        self.pq.insert("C", 8.0)

        # Decrease A's priority from 10 to 2
        self.pq.decrease_key("A", 2.0)

        # A should now be extracted first
        key, priority = self.pq.extract_min()
        self.assertEqual(key, "A")
        self.assertEqual(priority, 2.0)

    def test_decrease_key_invalid(self):
        """Test decrease_key with invalid inputs."""
        if self.pq is None:
            self.skipTest("Base class test")
        self.pq.insert("A", 5.0)

        # Trying to increase priority (not allowed)
        with self.assertRaises(ValueError):
            self.pq.decrease_key("A", 10.0)

        # Trying to decrease non-existent key
        with self.assertRaises(KeyError):
            self.pq.decrease_key("Z", 1.0)

    def test_duplicate_insert(self):
        """Test inserting duplicate keys."""
        if self.pq is None:
            self.skipTest("Base class test")
        self.pq.insert("A", 10.0)
        self.pq.insert("A", 5.0)  # Should update to lower priority

        key, priority = self.pq.extract_min()
        self.assertEqual(key, "A")
        self.assertEqual(priority, 5.0)

        # Size should be 1, not 2
        self.assertTrue(self.pq.is_empty())

    def test_many_elements(self):
        """Test with many elements."""
        if self.pq is None:
            self.skipTest("Base class test")
        n = 100
        for i in range(n):
            self.pq.insert(f"key_{i}", float(n - i))

        # Extract all and verify order
        prev_priority = -float('inf')
        for _ in range(n):
            key, priority = self.pq.extract_min()
            self.assertGreaterEqual(priority, prev_priority)
            prev_priority = priority

        self.assertTrue(self.pq.is_empty())

    def test_same_priorities(self):
        """Test elements with same priorities."""
        if self.pq is None:
            self.skipTest("Base class test")
        self.pq.insert("A", 5.0)
        self.pq.insert("B", 5.0)
        self.pq.insert("C", 5.0)

        self.assertEqual(self.pq.size(), 3)

        # All should have priority 5.0
        for _ in range(3):
            key, priority = self.pq.extract_min()
            self.assertEqual(priority, 5.0)

    def test_single_element(self):
        """Test with single element."""
        if self.pq is None:
            self.skipTest("Base class test")
        self.pq.insert("A", 5.0)

        self.assertFalse(self.pq.is_empty())
        self.assertEqual(self.pq.size(), 1)

        key, priority = self.pq.extract_min()
        self.assertEqual(key, "A")
        self.assertEqual(priority, 5.0)

        self.assertTrue(self.pq.is_empty())

    def test_interleaved_operations(self):
        """Test interleaved insert and extract operations."""
        if self.pq is None:
            self.skipTest("Base class test")
        self.pq.insert("A", 5.0)
        self.pq.insert("B", 3.0)

        key, priority = self.pq.extract_min()
        self.assertEqual(key, "B")

        self.pq.insert("C", 2.0)
        self.pq.insert("D", 7.0)

        key, priority = self.pq.extract_min()
        self.assertEqual(key, "C")

        key, priority = self.pq.extract_min()
        self.assertEqual(key, "A")

        self.assertEqual(self.pq.size(), 1)


class TestBinaryHeap(TestPriorityQueue):
    """Test cases specific to BinaryHeap implementation."""

    def setUp(self):
        """Initialize BinaryHeap for testing."""
        self.pq = BinaryHeap()

    def test_heap_property_after_inserts(self):
        """Test that heap property is maintained after insertions."""
        heap = BinaryHeap()

        # Insert elements in random order
        elements = [("D", 10.0), ("A", 5.0), ("C", 8.0), ("B", 3.0)]
        for key, priority in elements:
            heap.insert(key, priority)

            # After each insert, verify heap property
            self._verify_heap_property(heap)

    def test_heap_property_after_extract(self):
        """Test that heap property is maintained after extraction."""
        heap = BinaryHeap()

        # Insert several elements
        for i in range(10):
            heap.insert(f"key_{i}", float(10 - i))

        # Extract several and verify heap property after each
        for _ in range(5):
            heap.extract_min()
            if not heap.is_empty():
                self._verify_heap_property(heap)

    def test_heap_property_after_decrease_key(self):
        """Test that heap property is maintained after decrease_key."""
        heap = BinaryHeap()

        heap.insert("A", 10.0)
        heap.insert("B", 5.0)
        heap.insert("C", 8.0)
        heap.insert("D", 3.0)

        heap.decrease_key("A", 1.0)
        self._verify_heap_property(heap)

        heap.decrease_key("C", 2.0)
        self._verify_heap_property(heap)

    def _verify_heap_property(self, heap: BinaryHeap):
        """
        Verify that the min-heap property holds.

        Args:
            heap (BinaryHeap): The heap to verify.
        """
        for i in range(len(heap._heap)):
            left_child = 2 * i + 1
            right_child = 2 * i + 2

            # Check left child
            if left_child < len(heap._heap):
                self.assertLessEqual(
                    heap._heap[i][1],
                    heap._heap[left_child][1],
                    f"Heap property violated at index {i} and left child {left_child}"
                )

            # Check right child
            if right_child < len(heap._heap):
                self.assertLessEqual(
                    heap._heap[i][1],
                    heap._heap[right_child][1],
                    f"Heap property violated at index {i} and right child {right_child}"
                )

    def test_position_map_consistency(self):
        """Test that position map stays consistent with heap array."""
        heap = BinaryHeap()

        # Insert and verify position map
        heap.insert("A", 5.0)
        heap.insert("B", 3.0)
        heap.insert("C", 7.0)

        self._verify_position_map(heap)

        # Extract and verify
        heap.extract_min()
        self._verify_position_map(heap)

        # Decrease key and verify
        heap.decrease_key("C", 1.0)
        self._verify_position_map(heap)

    def _verify_position_map(self, heap: BinaryHeap):
        """
        Verify that position map correctly maps keys to indices.

        Args:
            heap (BinaryHeap): The heap to verify.
        """
        for key, index in heap._position.items():
            self.assertEqual(
                heap._heap[index][0],
                key,
                f"Position map inconsistency: key {key} maps to index {index}, but heap has {heap._heap[index][0]}"
            )

    def test_string_representation(self):
        """Test string representation of heap."""
        heap = BinaryHeap()
        heap.insert("A", 5.0)

        string_repr = str(heap)
        self.assertIn("BinaryHeap", string_repr)
        self.assertIn("size=1", string_repr)


class TestSortedLinkedList(TestPriorityQueue):
    """Test cases specific to SortedLinkedList implementation."""

    def setUp(self):
        """Initialize SortedLinkedList for testing."""
        self.pq = SortedLinkedList()

    def test_sorted_order_maintained(self):
        """Test that list maintains sorted order."""
        slist = SortedLinkedList()

        # Insert in random order
        elements = [("D", 10.0), ("A", 5.0), ("C", 8.0), ("B", 3.0), ("E", 1.0)]
        for key, priority in elements:
            slist.insert(key, priority)
            self._verify_sorted_order(slist)

    def test_sorted_order_after_decrease_key(self):
        """Test that sorted order is maintained after decrease_key."""
        slist = SortedLinkedList()

        slist.insert("A", 10.0)
        slist.insert("B", 5.0)
        slist.insert("C", 8.0)

        slist.decrease_key("A", 2.0)
        self._verify_sorted_order(slist)

        slist.decrease_key("C", 3.0)
        self._verify_sorted_order(slist)

    def _verify_sorted_order(self, slist: SortedLinkedList):
        """
        Verify that the linked list is sorted by priority.

        Args:
            slist (SortedLinkedList): The list to verify.
        """
        current = slist._head
        while current is not None and current.next is not None:
            self.assertLessEqual(
                current.priority,
                current.next.priority,
                f"List not sorted: {current.priority} > {current.next.priority}"
            )
            current = current.next

    def test_string_representation(self):
        """Test string representation of list."""
        slist = SortedLinkedList()
        slist.insert("A", 5.0)
        slist.insert("B", 3.0)

        string_repr = str(slist)
        self.assertIn("SortedLinkedList", string_repr)
        self.assertIn("size=2", string_repr)


class TestPerformanceComparison(unittest.TestCase):
    """Compare performance characteristics of both implementations."""

    def test_extract_min_from_head(self):
        """Test that extract_min is O(1) for list, O(log n) for heap."""
        # This is a structural test, not a timing test
        slist = SortedLinkedList()
        heap = BinaryHeap()

        # Insert elements
        for i in range(10):
            slist.insert(f"key_{i}", float(i))
            heap.insert(f"key_{i}", float(i))

        # For sorted list, min should be at head
        self.assertEqual(slist._head.priority, 0.0)

        # Extract min
        key, priority = slist.extract_min()
        self.assertEqual(priority, 0.0)

        key, priority = heap.extract_min()
        self.assertEqual(priority, 0.0)


if __name__ == '__main__':
    unittest.main()
