"""
Priority queue implementations for graph algorithms.
BinaryHeap: O(log n) operations
SortedLinkedList: O(n) insert, O(1) extract
"""

from typing import Any, Optional, List, Tuple
from abc import ABC, abstractmethod


class PriorityQueue(ABC):
    """Base class for priority queue implementations."""

    @abstractmethod
    def insert(self, key: Any, priority: float) -> None:
        pass

    @abstractmethod
    def extract_min(self) -> Tuple[Any, float]:
        pass

    @abstractmethod
    def decrease_key(self, key: Any, new_priority: float) -> None:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def size(self) -> int:
        pass


class BinaryHeap(PriorityQueue):
    """Min-heap with decrease-key support for Dijkstra/Prim."""

    def __init__(self):
        self._heap: List[Tuple[Any, float]] = []
        self._position: dict[Any, int] = {}

    def insert(self, key: Any, priority: float) -> None:
        """Insert element with given priority."""
        if key in self._position:
            current_priority = self._heap[self._position[key]][1]
            if priority < current_priority:
                self.decrease_key(key, priority)
        else:
            self._heap.append((key, priority))
            index = len(self._heap) - 1
            self._position[key] = index
            self._bubble_up(index)

    def extract_min(self) -> Tuple[Any, float]:
        """Remove and return minimum priority element."""
        if self.is_empty():
            raise IndexError("Cannot extract from empty heap")

        min_element = self._heap[0]
        del self._position[min_element[0]]

        if len(self._heap) > 1:
            last_element = self._heap.pop()
            self._heap[0] = last_element
            self._position[last_element[0]] = 0
            self._bubble_down(0)
        else:
            self._heap.pop()

        return min_element

    def decrease_key(self, key: Any, new_priority: float) -> None:
        """Decrease priority of an element."""
        if key not in self._position:
            raise KeyError(f"Key {key} not found in heap")

        index = self._position[key]
        current_priority = self._heap[index][1]

        if new_priority > current_priority:
            raise ValueError("New priority must be less than current priority")

        self._heap[index] = (key, new_priority)
        self._bubble_up(index)

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)

    def _bubble_up(self, index: int) -> None:
        """Move element up to restore heap property."""
        while index > 0:
            parent_index = (index - 1) // 2
            if self._heap[index][1] < self._heap[parent_index][1]:
                self._swap(index, parent_index)
                index = parent_index
            else:
                break

    def _bubble_down(self, index: int) -> None:
        """Move element down to restore heap property."""
        heap_size = len(self._heap)

        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index

            if (left_child < heap_size and
                    self._heap[left_child][1] < self._heap[smallest][1]):
                smallest = left_child

            if (right_child < heap_size and
                    self._heap[right_child][1] < self._heap[smallest][1]):
                smallest = right_child

            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        """Swap two elements and update position map."""
        self._position[self._heap[i][0]] = j
        self._position[self._heap[j][0]] = i
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def __str__(self) -> str:
        return f"BinaryHeap(size={self.size()}, min={self._heap[0] if not self.is_empty() else None})"


class SortedLinkedList(PriorityQueue):
    """Sorted linked list priority queue (simpler but slower)."""

    class _Node:
        def __init__(self, key: Any, priority: float, next_node: Optional['SortedLinkedList._Node'] = None):
            self.key = key
            self.priority = priority
            self.next = next_node

    def __init__(self):
        self._head: Optional[SortedLinkedList._Node] = None
        self._size: int = 0

    def insert(self, key: Any, priority: float) -> None:
        """Insert element maintaining sorted order."""
        if self._contains(key):
            self._remove(key)

        new_node = self._Node(key, priority)

        if self._head is None or priority < self._head.priority:
            new_node.next = self._head
            self._head = new_node
        else:
            current = self._head
            while current.next is not None and current.next.priority < priority:
                current = current.next

            new_node.next = current.next
            current.next = new_node

        self._size += 1

    def extract_min(self) -> Tuple[Any, float]:
        """Remove and return minimum priority element."""
        if self.is_empty():
            raise IndexError("Cannot extract from empty list")

        min_node = self._head
        self._head = self._head.next
        self._size -= 1

        return (min_node.key, min_node.priority)

    def decrease_key(self, key: Any, new_priority: float) -> None:
        """Decrease priority of an element."""
        current = self._head
        while current is not None:
            if current.key == key:
                if new_priority > current.priority:
                    raise ValueError("New priority must be less than current priority")
                self._remove(key)
                self.insert(key, new_priority)
                return
            current = current.next

        raise KeyError(f"Key {key} not found in list")

    def is_empty(self) -> bool:
        return self._head is None

    def size(self) -> int:
        return self._size

    def _contains(self, key: Any) -> bool:
        """Check if key exists in list."""
        current = self._head
        while current is not None:
            if current.key == key:
                return True
            current = current.next
        return False

    def _remove(self, key: Any) -> None:
        """Remove a key from the list."""
        if self._head is None:
            return

        if self._head.key == key:
            self._head = self._head.next
            self._size -= 1
            return

        current = self._head
        while current.next is not None:
            if current.next.key == key:
                current.next = current.next.next
                self._size -= 1
                return
            current = current.next

    def __str__(self) -> str:
        elements = []
        current = self._head
        while current is not None:
            elements.append(f"({current.key}, {current.priority})")
            current = current.next
        return f"SortedLinkedList(size={self.size()}, elements=[{', '.join(elements)}])"
