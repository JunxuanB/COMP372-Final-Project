# Usage Guide

## Running Tests

Run all tests:
```bash
python3 -m unittest discover tests -v
```

Run specific test file:
```bash
python3 -m unittest tests.test_graph -v
python3 -m unittest tests.test_fringe -v
```

## Using the Graph Class

```python
from src.graph import Graph

# Create graph
g = Graph(directed=False)

# Add edges (vertices auto-created)
g.add_edge("A", "B", 5.0)
g.add_edge("B", "C", 3.0)

# Query graph
print(g.get_neighbors("A"))  # {'B': 5.0}
print(g.get_weight("A", "B"))  # 5.0
```

## Using Priority Queues

```python
from src.fringe import BinaryHeap, SortedLinkedList

# Binary Heap (faster)
heap = BinaryHeap()
heap.insert("task1", 5.0)
heap.insert("task2", 2.0)
key, priority = heap.extract_min()  # Returns task2

# Sorted List (simpler)
slist = SortedLinkedList()
slist.insert("task1", 5.0)
key, priority = slist.extract_min()
```

## Key Methods

**Graph:**
- `add_edge(u, v, weight)` - Add weighted edge
- `get_neighbors(v)` - Get adjacent vertices
- `get_weight(u, v)` - Get edge weight

**Priority Queue:**
- `insert(key, priority)` - Insert element
- `extract_min()` - Remove minimum
- `decrease_key(key, new_priority)` - Update priority

## Project Status

Phase 1 & 2: Complete ✓
- Graph and priority queue data structures implemented
- All tests passing

Next: Phase 3 - Implement Dijkstra and Prim algorithms
