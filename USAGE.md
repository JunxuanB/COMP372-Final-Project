# Usage Guide - COMP372 Final Project

**Current Status**: Phase 1 & 2 Complete (Data Structures)
**Last Updated**: 2025-11-07

---

## Table of Contents
1. [Project Status](#project-status)
2. [Installation](#installation)
3. [Running Tests](#running-tests)
4. [Using the Graph Class](#using-the-graph-class)
5. [Using Priority Queue Data Structures](#using-priority-queue-data-structures)
6. [Code Examples](#code-examples)
7. [Next Steps](#next-steps)

---

## Project Status

### ✅ Completed Components

**Phase 1: Environment Setup**
- Python 3.9.6 environment configured
- All dependencies installed (matplotlib, networkx, Pillow, numpy)
- Project directory structure created

**Phase 2: Core Data Structures**
- **Graph** ([src/graph.py](src/graph.py)): Adjacency list representation with O(1) lookups
- **BinaryHeap** ([src/fringe.py](src/fringe.py)): Min-heap with O(log n) operations
- **SortedLinkedList** ([src/fringe.py](src/fringe.py)): Sorted list with O(1) extraction
- **Comprehensive Tests**: 58 unit tests, 100% passing

### 🔲 Upcoming Components

**Phase 3: Algorithms** (Next)
- Dijkstra's shortest path algorithm
- Prim's minimum spanning tree algorithm

**Phase 4-7**: Visualization, UI, Testing, Documentation

---

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup Steps

1. **Navigate to project directory:**
   ```bash
   cd /Users/junxuanb/Documents/COMP372-Final-Project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   This installs:
   - matplotlib 3.9.4
   - networkx 3.2.1
   - Pillow 11.3.0
   - numpy 2.0.2

3. **Verify installation:**
   ```bash
   python3 -c "import matplotlib, networkx, PIL, numpy; print('All dependencies installed!')"
   ```

---

## Running Tests

### Run All Tests
```bash
# Run all unit tests
python3 -m unittest discover tests -v

# Expected output: 58 tests passed
```

### Run Specific Test Files

**Test Graph Implementation:**
```bash
python3 -m unittest tests.test_graph -v

# Expected: 16 tests passed
# Tests cover: vertex/edge operations, directed/undirected graphs, edge cases
```

**Test Fringe Data Structures:**
```bash
python3 -m unittest tests.test_fringe -v

# Expected: 42 tests passed (11 skipped base class tests)
# Tests cover: insert, extract_min, decrease_key, heap properties
```

### Test Coverage Summary
- **Graph Tests**: 16 tests covering all methods and edge cases
- **Binary Heap Tests**: 16 tests verifying heap properties and operations
- **Sorted List Tests**: 15 tests verifying sorted order and operations
- **Performance Tests**: 1 test comparing data structure characteristics

---

## Using the Graph Class

### Basic Usage

```python
import sys
sys.path.insert(0, 'src')

from graph import Graph

# Create an undirected graph
g = Graph(directed=False)

# Add edges (vertices created automatically)
g.add_edge("A", "B", 5.0)
g.add_edge("B", "C", 3.0)
g.add_edge("A", "C", 2.0)

# Query the graph
print(f"Vertices: {g.get_vertices()}")  # {'A', 'B', 'C'}
print(f"Edges: {g.num_edges()}")        # 3
print(f"A's neighbors: {g.get_neighbors('A')}")  # {'B': 5.0, 'C': 2.0}
```

### Creating a Directed Graph

```python
# Create a directed graph
g = Graph(directed=True)

g.add_edge("A", "B", 5.0)
g.add_edge("B", "A", 3.0)  # Different weight in reverse direction

# Edges are directional
print(g.has_edge("A", "B"))  # True
print(g.has_edge("B", "A"))  # True
print(g.get_weight("A", "B"))  # 5.0
print(g.get_weight("B", "A"))  # 3.0
```

### Graph Methods Reference

| Method | Time Complexity | Description |
|--------|----------------|-------------|
| `add_vertex(v)` | O(1) | Add a vertex |
| `add_edge(u, v, w)` | O(1) | Add weighted edge |
| `get_neighbors(v)` | O(1) | Get vertex neighbors |
| `get_weight(u, v)` | O(1) | Get edge weight |
| `has_vertex(v)` | O(1) | Check if vertex exists |
| `has_edge(u, v)` | O(1) | Check if edge exists |
| `get_vertices()` | O(V) | Get all vertices |
| `get_edges()` | O(V+E) | Get all edges |
| `num_vertices()` | O(1) | Count vertices |
| `num_edges()` | O(V) | Count edges |

---

## Using Priority Queue Data Structures

Both `BinaryHeap` and `SortedLinkedList` implement the same `PriorityQueue` interface, making them interchangeable for algorithm implementations.

### BinaryHeap (Recommended for Performance)

```python
from fringe import BinaryHeap

# Create a min-heap
heap = BinaryHeap()

# Insert elements with priorities (lower priority = extracted first)
heap.insert("TaskA", 5.0)
heap.insert("TaskB", 2.0)
heap.insert("TaskC", 8.0)

# Extract minimum priority element
key, priority = heap.extract_min()
print(f"{key}: {priority}")  # TaskB: 2.0

# Decrease priority (important for Dijkstra/Prim)
heap.insert("TaskD", 10.0)
heap.decrease_key("TaskD", 1.0)  # Now TaskD has priority 1.0

key, priority = heap.extract_min()
print(f"{key}: {priority}")  # TaskD: 1.0
```

### SortedLinkedList (Simpler, Slower)

```python
from fringe import SortedLinkedList

# Create a sorted list
slist = SortedLinkedList()

# Same interface as BinaryHeap
slist.insert("TaskA", 5.0)
slist.insert("TaskB", 2.0)
slist.insert("TaskC", 8.0)

# Extract minimum (O(1) for list, but insert is O(n))
key, priority = slist.extract_min()
print(f"{key}: {priority}")  # TaskB: 2.0
```

### Priority Queue Methods Reference

| Method | BinaryHeap | SortedLinkedList | Description |
|--------|-----------|-----------------|-------------|
| `insert(key, priority)` | O(log n) | O(n) | Insert element |
| `extract_min()` | O(log n) | O(1) | Remove minimum |
| `decrease_key(key, new_priority)` | O(log n) | O(n) | Update priority |
| `is_empty()` | O(1) | O(1) | Check if empty |
| `size()` | O(1) | O(1) | Get element count |

**Performance Comparison:**
- **BinaryHeap**: Better for large datasets, balanced operations
- **SortedLinkedList**: Good for small datasets, fastest extraction

---

## Code Examples

### Example 1: Building a Simple Graph

```python
from src.graph import Graph

# Create a simple road network
roads = Graph(directed=False)

# Add roads between cities
roads.add_edge("New York", "Boston", 215.0)      # miles
roads.add_edge("New York", "Philadelphia", 95.0)
roads.add_edge("Philadelphia", "Washington", 140.0)
roads.add_edge("Boston", "Philadelphia", 310.0)

# Display the network
print(roads)
# Output:
# Undirected Graph with 4 vertices and 4 edges:
#   Boston -> New York(215.0), Philadelphia(310.0)
#   New York -> Boston(215.0), Philadelphia(95.0)
#   Philadelphia -> New York(95.0), Boston(310.0), Washington(140.0)
#   Washington -> Philadelphia(140.0)

# Find shortest route from New York
print("\nCities reachable from New York:")
for city, distance in roads.get_neighbors("New York").items():
    print(f"  → {city}: {distance} miles")
```

### Example 2: Using Heap for Task Scheduling

```python
from src.fringe import BinaryHeap

# Create a task priority queue
tasks = BinaryHeap()

# Add tasks with priorities (1 = highest, 10 = lowest)
tasks.insert("Fix critical bug", 1.0)
tasks.insert("Write documentation", 5.0)
tasks.insert("Code review", 3.0)
tasks.insert("Deploy to production", 2.0)

# Process tasks in priority order
print("Task execution order:")
while not tasks.is_empty():
    task, priority = tasks.extract_min()
    print(f"  [{priority}] {task}")

# Output:
#   [1.0] Fix critical bug
#   [2.0] Deploy to production
#   [3.0] Code review
#   [5.0] Write documentation
```

### Example 3: Comparing Heap vs List Performance

```python
from src.fringe import BinaryHeap, SortedLinkedList
import time

def benchmark_priority_queue(pq_class, n=1000):
    """Benchmark a priority queue implementation."""
    pq = pq_class()

    # Measure insertion time
    start = time.time()
    for i in range(n):
        pq.insert(f"item_{i}", float(n - i))
    insert_time = time.time() - start

    # Measure extraction time
    start = time.time()
    for _ in range(n):
        pq.extract_min()
    extract_time = time.time() - start

    return insert_time, extract_time

# Compare implementations
print("Performance Comparison (1000 elements):")

heap_insert, heap_extract = benchmark_priority_queue(BinaryHeap)
print(f"BinaryHeap:    Insert={heap_insert:.4f}s, Extract={heap_extract:.4f}s")

list_insert, list_extract = benchmark_priority_queue(SortedLinkedList)
print(f"SortedList:    Insert={list_insert:.4f}s, Extract={list_extract:.4f}s")

print(f"\nHeap is {list_insert/heap_insert:.1f}x faster at insertion")
print(f"List is {heap_extract/list_extract:.1f}x faster at extraction")
```

### Example 4: Complete Graph Creation

```python
from src.graph import Graph

def create_complete_graph(n: int) -> Graph:
    """
    Create a complete graph with n vertices.

    In a complete graph, every pair of vertices is connected.
    K_n has n vertices and n(n-1)/2 edges.
    """
    g = Graph(directed=False)

    # Create vertices named 0, 1, 2, ..., n-1
    for i in range(n):
        g.add_vertex(str(i))

    # Connect every pair of vertices
    for i in range(n):
        for j in range(i + 1, n):
            # Use distance as edge weight
            g.add_edge(str(i), str(j), 1.0)

    return g

# Create K_5 (complete graph with 5 vertices)
k5 = create_complete_graph(5)
print(f"K_5: {k5.num_vertices()} vertices, {k5.num_edges()} edges")
print(f"Expected: 5 vertices, {5*4//2} edges")  # n(n-1)/2 = 10
```

---

## Project Structure

```
COMP372-Final-Project/
├── src/                      # Source code (Phase 2 ✅)
│   ├── __init__.py          # Package initialization
│   ├── graph.py             # Graph data structure (220+ lines)
│   └── fringe.py            # Priority queues (400+ lines)
│
├── tests/                    # Unit tests (Phase 2 ✅)
│   ├── __init__.py
│   ├── test_graph.py        # 16 tests for Graph
│   └── test_fringe.py       # 42 tests for priority queues
│
├── docs/                     # Documentation (Phase 7 🔲)
├── animations/               # Algorithm animations (Phase 4 🔲)
├── screenshots/              # UI screenshots (Phase 5 🔲)
├── results/                  # Performance data (Phase 6 🔲)
│
├── requirements.txt          # Python dependencies
├── PROJECT_PLAN.md          # Comprehensive implementation plan
├── INSTALLATION_LOG.md      # Installation details
├── USAGE.md                 # This file
└── Requirement.md           # Original project requirements
```

---

## Next Steps

### For Developers

**Immediate Next Tasks (Phase 3):**

1. **Implement Dijkstra's Algorithm** ([src/algorithms.py](src/algorithms.py))
   - Accept Graph and start vertex
   - Support both BinaryHeap and SortedLinkedList
   - Return distances, predecessors, and step history
   - Time complexity: O((V+E) log V) with heap

2. **Implement Prim's Algorithm** ([src/algorithms.py](src/algorithms.py))
   - Accept Graph and start vertex
   - Support both fringe types
   - Return MST edges, total weight, and step history
   - Time complexity: O((V+E) log V) with heap

3. **Write Algorithm Tests** ([tests/test_algorithms.py](tests/test_algorithms.py))
   - Test with known graphs
   - Verify correctness
   - Test edge cases (disconnected, single node)

**Suggested Implementation Order:**
1. Create [src/algorithms.py](src/algorithms.py) with function stubs
2. Implement Dijkstra with BinaryHeap
3. Test Dijkstra with small graph
4. Implement Prim with BinaryHeap
5. Test Prim with small graph
6. Add history recording for visualization
7. Write comprehensive unit tests

### For Testing

```bash
# After implementing Phase 3, run:
python3 -m unittest tests.test_algorithms -v

# Run all tests
python3 -m unittest discover tests -v
```

---

## Getting Help

### Documentation References
- **Graph Theory**: See [PROJECT_PLAN.md](PROJECT_PLAN.md) sections 3.1 and 5
- **Algorithm Pseudocode**: See [PROJECT_PLAN.md](PROJECT_PLAN.md) Phase 3 sections
- **Complexity Analysis**: See [PROJECT_PLAN.md](PROJECT_PLAN.md) sections on time/space complexity

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`
**Solution**:
```python
import sys
sys.path.insert(0, 'src')  # Add at top of your script
from graph import Graph
```

**Issue**: Tests fail with import errors
**Solution**: Run tests from project root directory:
```bash
cd /Users/junxuanb/Documents/COMP372-Final-Project
python3 -m unittest discover tests -v
```

**Issue**: Missing dependencies
**Solution**: Reinstall requirements:
```bash
pip install -r requirements.txt
```

---

## Performance Notes

### Current Implementation Characteristics

**Graph ([src/graph.py](src/graph.py)):**
- Space: O(V + E) - optimal for adjacency list
- add_edge: O(1) amortized
- get_neighbors: O(1) dictionary lookup
- get_weight: O(1) nested dictionary lookup

**BinaryHeap ([src/fringe.py](src/fringe.py)):**
- Space: O(n) for heap array + position map
- insert: O(log n) with heap property maintenance
- extract_min: O(log n) with heap restructuring
- decrease_key: O(log n) with position tracking

**SortedLinkedList ([src/fringe.py](src/fringe.py)):**
- Space: O(n) for linked nodes
- insert: O(n) to maintain sorted order
- extract_min: O(1) from head
- decrease_key: O(n) to find and reposition

### Expected Algorithm Performance (Phase 3)

With BinaryHeap:
- **Dijkstra**: O((V + E) log V)
- **Prim**: O((V + E) log V)

With SortedLinkedList:
- **Dijkstra**: O(V²)
- **Prim**: O(V²)

**Recommendation**: Use BinaryHeap for graphs with > 50 vertices

---

## Version History

- **2025-11-07**: Phase 1 & 2 complete
  - Environment setup finished
  - Core data structures implemented
  - 58 unit tests passing
  - Ready for algorithm implementation

---

**Project**: COMP372 Final Project
**Status**: 29% Complete (2 of 7 phases)
**Next Milestone**: Phase 3 - Algorithm Implementation
**Estimated Time to Next Milestone**: 3-4 hours
