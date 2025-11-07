"""
Fringe data structures for graph algorithms.

This module implements two priority queue data structures used as fringes
in Dijkstra's shortest path and Prim's minimum spanning tree algorithms:
1. BinaryHeap - Efficient O(log n) operations
2. SortedLinkedList - Simple O(n) insertion, O(1) extraction
"""

from typing import Any, Optional, List, Tuple
from abc import ABC, abstractmethod


class PriorityQueue(ABC):
    """
    Abstract base class for priority queue implementations.

    All fringe implementations must provide this interface to be
    interchangeable in the graph algorithms.
    """

    @abstractmethod
    def insert(self, key: Any, priority: float) -> None:
        """Insert an element with given priority."""
        pass

    @abstractmethod
    def extract_min(self) -> Tuple[Any, float]:
        """Remove and return the element with minimum priority."""
        pass

    @abstractmethod
    def decrease_key(self, key: Any, new_priority: float) -> None:
        """Decrease the priority of an element."""
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        pass

    @abstractmethod
    def size(self) -> int:
        """Return the number of elements."""
        pass


class BinaryHeap(PriorityQueue):
    """
    Min-heap implementation with decrease-key support.

    Implements a binary min-heap using an array-based representation.
    Maintains a position map for O(log n) decrease-key operations.

    Time Complexity:
        - insert: O(log n)
        - extract_min: O(log n)
        - decrease_key: O(log n)
        - is_empty: O(1)
        - size: O(1)

    Space Complexity: O(n) where n is the number of elements

    Attributes:
        _heap (List[Tuple[Any, float]]): Array storing (key, priority) pairs.
        _position (Dict[Any, int]): Maps keys to their positions in the heap.
    """

    def __init__(self):
        """Initialize an empty binary heap."""
        self._heap: List[Tuple[Any, float]] = []
        self._position: dict[Any, int] = {}

    def insert(self, key: Any, priority: float) -> None:
        """
        Insert a new element with given priority.

        If the key already exists, updates its priority to the minimum
        of the old and new priorities.

        Args:
            key (Any): The element to insert.
            priority (float): The priority value (lower = higher priority).

        Time Complexity: O(log n)
        """
        if key in self._position:
            # If key exists, update if new priority is lower
            current_priority = self._heap[self._position[key]][1]
            if priority < current_priority:
                self.decrease_key(key, priority)
        else:
            # Add new element at the end and bubble up
            self._heap.append((key, priority))
            index = len(self._heap) - 1
            self._position[key] = index
            self._bubble_up(index)

    def extract_min(self) -> Tuple[Any, float]:
        """
        Remove and return the element with minimum priority.

        Returns:
            Tuple[Any, float]: (key, priority) of the minimum element.

        Raises:
            IndexError: If the heap is empty.

        Time Complexity: O(log n)
        """
        if self.is_empty():
            raise IndexError("Cannot extract from empty heap")

        # Save the minimum element
        min_element = self._heap[0]
        del self._position[min_element[0]]

        # Move last element to root and bubble down
        if len(self._heap) > 1:
            last_element = self._heap.pop()
            self._heap[0] = last_element
            self._position[last_element[0]] = 0
            self._bubble_down(0)
        else:
            self._heap.pop()

        return min_element

    def decrease_key(self, key: Any, new_priority: float) -> None:
        """
        Decrease the priority of an existing element.

        Args:
            key (Any): The element whose priority to decrease.
            new_priority (float): The new priority (must be lower than current).

        Raises:
            KeyError: If the key doesn't exist in the heap.
            ValueError: If new_priority is greater than current priority.

        Time Complexity: O(log n)
        """
        if key not in self._position:
            raise KeyError(f"Key {key} not found in heap")

        index = self._position[key]
        current_priority = self._heap[index][1]

        if new_priority > current_priority:
            raise ValueError("New priority must be less than current priority")

        # Update priority and bubble up
        self._heap[index] = (key, new_priority)
        self._bubble_up(index)

    def is_empty(self) -> bool:
        """
        Check if the heap is empty.

        Returns:
            bool: True if heap is empty, False otherwise.

        Time Complexity: O(1)
        """
        return len(self._heap) == 0

    def size(self) -> int:
        """
        Get the number of elements in the heap.

        Returns:
            int: Number of elements.

        Time Complexity: O(1)
        """
        return len(self._heap)

    def _bubble_up(self, index: int) -> None:
        """
        Restore heap property by moving element up.

        Args:
            index (int): Index of element to bubble up.

        Time Complexity: O(log n)
        """
        while index > 0:
            parent_index = (index - 1) // 2
            if self._heap[index][1] < self._heap[parent_index][1]:
                # Swap with parent
                self._swap(index, parent_index)
                index = parent_index
            else:
                break

    def _bubble_down(self, index: int) -> None:
        """
        Restore heap property by moving element down.

        Args:
            index (int): Index of element to bubble down.

        Time Complexity: O(log n)
        """
        heap_size = len(self._heap)

        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index

            # Find smallest among node and its children
            if (left_child < heap_size and
                    self._heap[left_child][1] < self._heap[smallest][1]):
                smallest = left_child

            if (right_child < heap_size and
                    self._heap[right_child][1] < self._heap[smallest][1]):
                smallest = right_child

            # If smallest is not the current node, swap and continue
            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        """
        Swap two elements in the heap and update position map.

        Args:
            i (int): First index.
            j (int): Second index.

        Time Complexity: O(1)
        """
        # Update position map
        self._position[self._heap[i][0]] = j
        self._position[self._heap[j][0]] = i

        # Swap in heap array
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def __str__(self) -> str:
        """String representation of the heap."""
        return f"BinaryHeap(size={self.size()}, min={self._heap[0] if not self.is_empty() else None})"

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"BinaryHeap({self._heap})"


class SortedLinkedList(PriorityQueue):
    """
    Sorted linked list implementation of priority queue.

    Maintains elements in sorted order by priority. Simple but less
    efficient than binary heap for large datasets.

    Time Complexity:
        - insert: O(n)
        - extract_min: O(1)
        - decrease_key: O(n)
        - is_empty: O(1)
        - size: O(1)

    Space Complexity: O(n) where n is the number of elements
    """

    class _Node:
        """Internal node class for linked list."""

        def __init__(self, key: Any, priority: float, next_node: Optional['SortedLinkedList._Node'] = None):
            self.key = key
            self.priority = priority
            self.next = next_node

    def __init__(self):
        """Initialize an empty sorted linked list."""
        self._head: Optional[SortedLinkedList._Node] = None
        self._size: int = 0

    def insert(self, key: Any, priority: float) -> None:
        """
        Insert a new element maintaining sorted order.

        If the key already exists, updates to the minimum priority.

        Args:
            key (Any): The element to insert.
            priority (float): The priority value (lower = higher priority).

        Time Complexity: O(n)
        """
        # Check if key already exists and remove it
        if self._contains(key):
            self._remove(key)

        # Insert at appropriate position to maintain sorted order
        new_node = self._Node(key, priority)

        # If list is empty or new node has smallest priority
        if self._head is None or priority < self._head.priority:
            new_node.next = self._head
            self._head = new_node
        else:
            # Find position to insert
            current = self._head
            while current.next is not None and current.next.priority < priority:
                current = current.next

            new_node.next = current.next
            current.next = new_node

        self._size += 1

    def extract_min(self) -> Tuple[Any, float]:
        """
        Remove and return the element with minimum priority.

        Returns:
            Tuple[Any, float]: (key, priority) of the minimum element.

        Raises:
            IndexError: If the list is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Cannot extract from empty list")

        min_node = self._head
        self._head = self._head.next
        self._size -= 1

        return (min_node.key, min_node.priority)

    def decrease_key(self, key: Any, new_priority: float) -> None:
        """
        Decrease the priority of an existing element.

        Args:
            key (Any): The element whose priority to decrease.
            new_priority (float): The new priority (must be lower than current).

        Raises:
            KeyError: If the key doesn't exist in the list.
            ValueError: If new_priority is greater than current priority.

        Time Complexity: O(n)
        """
        # Find and verify the key exists
        current = self._head
        while current is not None:
            if current.key == key:
                if new_priority > current.priority:
                    raise ValueError("New priority must be less than current priority")

                # Remove and reinsert with new priority
                self._remove(key)
                self.insert(key, new_priority)
                return

            current = current.next

        raise KeyError(f"Key {key} not found in list")

    def is_empty(self) -> bool:
        """
        Check if the list is empty.

        Returns:
            bool: True if list is empty, False otherwise.

        Time Complexity: O(1)
        """
        return self._head is None

    def size(self) -> int:
        """
        Get the number of elements in the list.

        Returns:
            int: Number of elements.

        Time Complexity: O(1)
        """
        return self._size

    def _contains(self, key: Any) -> bool:
        """
        Check if a key exists in the list.

        Args:
            key (Any): The key to search for.

        Returns:
            bool: True if key exists, False otherwise.

        Time Complexity: O(n)
        """
        current = self._head
        while current is not None:
            if current.key == key:
                return True
            current = current.next
        return False

    def _remove(self, key: Any) -> None:
        """
        Remove a key from the list.

        Args:
            key (Any): The key to remove.

        Time Complexity: O(n)
        """
        if self._head is None:
            return

        # Special case: remove head
        if self._head.key == key:
            self._head = self._head.next
            self._size -= 1
            return

        # Find and remove key
        current = self._head
        while current.next is not None:
            if current.next.key == key:
                current.next = current.next.next
                self._size -= 1
                return
            current = current.next

    def __str__(self) -> str:
        """String representation of the list."""
        elements = []
        current = self._head
        while current is not None:
            elements.append(f"({current.key}, {current.priority})")
            current = current.next
        return f"SortedLinkedList(size={self.size()}, elements=[{', '.join(elements)}])"

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return self.__str__()
