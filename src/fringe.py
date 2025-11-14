from typing import Any, Optional, List, Tuple
from abc import ABC, abstractmethod

class PriorityQueue(ABC):
    # abstract base class for priority queues
    # defines the interface all implementations must follow

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
    # min-heap using array-based binary tree
    # supports O(log n) insert, extract_min, and decrease_key

    def __init__(self):
        self._heap: List[Tuple[Any, float]] = []  # stores (key, priority) pairs
        self._position: dict[Any, int] = {}  # maps keys to heap positions

    def insert(self, key: Any, priority: float) -> None:
        # insert element with given priority
        # if key exists, update if new priority is lower
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
        # remove and return element with minimum priority
        if self.is_empty():
            raise IndexError("Cannot extract from empty heap")

        min_element = self._heap[0]
        del self._position[min_element[0]]

        if len(self._heap) > 1:
            # move last element to root and restore heap property
            last_element = self._heap.pop()
            self._heap[0] = last_element
            self._position[last_element[0]] = 0
            self._bubble_down(0)
        else:
            self._heap.pop()

        return min_element

    def decrease_key(self, key: Any, new_priority: float) -> None:
        # decrease priority of existing element
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
        # restore heap property by moving element upward
        while index > 0:
            parent_index = (index - 1) // 2
            if self._heap[index][1] < self._heap[parent_index][1]:
                self._swap(index, parent_index)
                index = parent_index
            else:
                break

    def _bubble_down(self, index: int) -> None:
        # restore heap property by moving element downward
        heap_size = len(self._heap)

        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index

            # find smallest among node and its children
            if (left_child < heap_size and
                    self._heap[left_child][1] < self._heap[smallest][1]):
                smallest = left_child

            if (right_child < heap_size and
                    self._heap[right_child][1] < self._heap[smallest][1]):
                smallest = right_child

            # swap with smallest child if needed
            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        # swap two elements and update position map
        self._position[self._heap[i][0]] = j
        self._position[self._heap[j][0]] = i
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def __str__(self) -> str:
        return f"BinaryHeap(size={self.size()}, min={self._heap[0] if not self.is_empty() else None})"


class SortedLinkedList(PriorityQueue):
    class _Node:
        # node for linked list
        def __init__(self, key: Any, priority: float, next_node: Optional['SortedLinkedList._Node'] = None):
            self.key = key
            self.priority = priority
            self.next = next_node

    def __init__(self):
        self._head: Optional[SortedLinkedList._Node] = None
        self._size: int = 0

    def insert(self, key: Any, priority: float) -> None:
        # insert while maintaining sorted order (lowest priority first)
        # if key exists, remove old one first
        if self._contains(key):
            self._remove(key)

        new_node = self._Node(key, priority)

        # insert at head if empty or smallest priority
        if self._head is None or priority < self._head.priority:
            new_node.next = self._head
            self._head = new_node
        else:
            # find correct position
            current = self._head
            while current.next is not None and current.next.priority < priority:
                current = current.next

            new_node.next = current.next
            current.next = new_node

        self._size += 1

    def extract_min(self) -> Tuple[Any, float]:
        # remove and return minimum (always at head)
        if self.is_empty():
            raise IndexError("Cannot extract from empty list")

        min_node = self._head
        self._head = self._head.next
        self._size -= 1

        return (min_node.key, min_node.priority)

    def decrease_key(self, key: Any, new_priority: float) -> None:
        # decrease priority by removing and re-inserting
        current = self._head
        while current is not None:
            if current.key == key:
                if new_priority > current.priority:
                    raise ValueError("New priority must be less than current priority")
                # remove and reinsert with new priority
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
        # check if key exists
        current = self._head
        while current is not None:
            if current.key == key:
                return True
            current = current.next
        return False

    def _remove(self, key: Any) -> None:
        # remove a key from list
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
