# Graph Algorithms: Dijkstra's Shortest Path and Prim's MST

**COMP372 Final Project**
Implementation and performance comparison of Dijkstra's shortest path and Prim's minimum spanning tree algorithms with different fringe data structures.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [System Requirements](#system-requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Running Tests](#running-tests)
8. [Performance Analysis](#performance-analysis)
9. [Documentation](#documentation)

---

## Overview

This project implements two fundamental graph algorithms:
- **Dijkstra's Algorithm**: Finds shortest paths from a source vertex to all other vertices
- **Prim's Algorithm**: Constructs a minimum spanning tree (MST)

Both algorithms are implemented with two different fringe (priority queue) data structures:
- **Binary Heap**: O(log n) operations
- **Sorted Linked List**: O(n) insert, O(1) extract

The project includes:
- Interactive command-line demo
- Step-by-step algorithm visualization
- Animated GIF generation
- Comprehensive performance benchmarking
- Extensive test suite

---

## Features

### Core Implementation
✅ Dijkstra's shortest path algorithm
✅ Prim's minimum spanning tree algorithm
✅ Binary heap with decrease-key operation
✅ Sorted linked list for comparison
✅ Graph data structure with adjacency list

### Interactive Demo
✅ Command-line interface for algorithm testing
✅ Incremental edge addition
✅ Algorithm selection (Dijkstra/Prim)
✅ Fringe type selection (Heap/List)
✅ Graph visualization (saves images)
✅ Results display with execution time
✅ Performance comparison mode

### Visualization
✅ Step-by-step algorithm animation
✅ GIF generation with color-coded states
✅ Automatic image viewing
✅ Color scheme:
  - 🔴 Red: Current node being processed
  - 🔵 Blue: Visited nodes
  - 🟢 Green: Selected edges (MST/shortest path)
  - ⚫ Gray: Unvisited nodes/edges

### Performance Analysis
✅ Benchmark tests on graphs with 10-500 vertices
✅ Execution time measurement
✅ Heap vs List comparison charts
✅ CSV export of results

---

## System Requirements

### Software
- **Python**: 3.9 or higher
- **Operating System**: macOS, Linux, or Windows

### Python Libraries
- `matplotlib` (≥3.5.0): Visualization and plotting
- `networkx` (≥2.6.0): Graph layout algorithms
- `Pillow` (≥9.0.0): GIF animation generation
- `numpy` (≥1.21.0): Numerical operations (optional)
- `pytest` (≥8.0.0): Testing framework

---

## Installation

### Step 1: Navigate to Project Directory
```bash
cd /path/to/COMP372-Final-Project
```

### Step 2: Install Dependencies
```bash
python3 -m pip install -r requirements.txt
```

Or install manually:
```bash
python3 -m pip install matplotlib networkx Pillow numpy pytest
```

### Step 3: Verify Installation
```bash
python3 -m pytest tests/ -v
```

You should see all tests passing (60+ tests).

---

## Usage

### Running the Interactive Demo

Launch the interactive command-line interface:
```bash
PYTHONPATH=. python3 src/ui.py
```

**Interactive Menu:**
```
1. Load Sample Graph
2. Add Edge
3. View Graph (generates image)
4. Run Dijkstra's Algorithm
5. Run Prim's MST Algorithm
6. Compare Heap vs List Performance
7. Generate Animation
8. Show Graph Summary
0. Exit
```

**Example Workflow:**
```bash
# Start demo
PYTHONPATH=. python3 src/ui.py

# Choose option 1 to load sample graph
# Choose option 3 to view graph (opens image)
# Choose option 4 to run Dijkstra
#   - Enter start node: A
#   - Choose fringe: heap
#   - Generate animation: y
# Choose option 6 to compare performance
```

### Running Algorithms Programmatically

```python
from src.graph import Graph
from src.algorithms import dijkstra, prim

# Create graph
graph = Graph(directed=False)
graph.add_edge('A', 'B', 4.0)
graph.add_edge('B', 'C', 2.0)
graph.add_edge('A', 'C', 5.0)

# Run Dijkstra
distances, previous, history = dijkstra(graph, 'A', fringe_type='heap')
print(f"Shortest distances: {distances}")

# Run Prim
mst_edges, total_weight, history = prim(graph, 'A', fringe_type='heap')
print(f"MST weight: {total_weight}")
print(f"MST edges: {mst_edges}")
```

### Generating Animations

Generate sample animations:
```bash
PYTHONPATH=. python3 tests/generate_animations.py
```

Animations will be saved in the `animations/` directory as GIF files.

### Running Performance Benchmarks

Execute performance tests:
```bash
PYTHONPATH=. python3 tests/performance_test.py
```

Results:
- `results/performance_data.csv`: Raw benchmark data
- `results/comparison_charts.png`: Visual comparison charts

---

## Project Structure

```
COMP372-Final-Project/
│
├── src/                      # Source code
│   ├── __init__.py
│   ├── graph.py              # Graph data structure (adjacency list)
│   ├── fringe.py             # Binary heap and sorted linked list
│   ├── algorithms.py         # Dijkstra and Prim implementations
│   └── visualizer.py         # Animation and visualization
│
├── tests/                    # Tests and utilities
│   ├── test_graph.py         # Graph unit tests
│   ├── test_fringe.py        # Fringe unit tests
│   ├── test_algorithms.py    # Algorithm unit tests
│   ├── interactive_demo.py   # Interactive command-line demo
│   ├── generate_animations.py # Animation generator
│   └── performance_test.py   # Performance benchmarks
│
├── animations/               # Generated GIF animations
├── results/                  # Performance results and charts
│
├── docs/                     # Technical documentation
│   ├── pseudocode.md         # Algorithm pseudocode
│   └── complexity_analysis.md # Time/space complexity
│
├── README.md                 # This file (user manual)
├── requirements.txt          # Python dependencies
├── PROJECT_PLAN.md           # Development roadmap
└── Requirement.md            # Original assignment
```

---

## Running Tests

### Run All Tests
```bash
python3 -m pytest tests/ -v
```

### Run Specific Test Files
```bash
# Test graph data structure
python3 -m pytest tests/test_graph.py -v

# Test fringe implementations
python3 -m pytest tests/test_fringe.py -v

# Test algorithms
python3 -m pytest tests/test_algorithms.py -v
```

### Expected Results
- **60+ tests** covering all components
- **100% pass rate**
- Tests include edge cases: empty graphs, single nodes, disconnected components

---

## Performance Analysis

### Key Findings

Based on benchmarks with graphs of 10-500 vertices:

**Small Graphs (10-50 vertices):**
- Heap and List perform similarly
- Overhead of heap operations not justified

**Medium Graphs (100 vertices):**
- Heap becomes **2-3x faster** than List
- Crossover point where heap advantages emerge

**Large Graphs (500 vertices):**
- Heap is **5-7x faster** than List
- Dijkstra: 9ms (heap) vs 53ms (list)
- Prim: 11ms (heap) vs 74ms (list)

### Theoretical Complexity

| Operation | Binary Heap | Sorted Linked List |
|-----------|-------------|-------------------|
| Insert | O(log n) | O(n) |
| Extract Min | O(log n) | O(1) |
| Decrease Key | O(log n) | O(n) |

**Algorithm Complexity:**
- Dijkstra with Heap: **O((V+E) log V)**
- Dijkstra with List: **O(V²)**
- Prim with Heap: **O((V+E) log V)**
- Prim with List: **O(V²)**

---

## Documentation

### Technical Documentation

- **[pseudocode.md](docs/pseudocode.md)**: Detailed algorithm pseudocode and explanations
- **[complexity_analysis.md](docs/complexity_analysis.md)**: Time and space complexity analysis
- **PROJECT_REPORT.pdf**: Comprehensive project report (final deliverable)

### Code Documentation

All functions include docstrings with:
- Purpose and functionality
- Parameter descriptions
- Return value descriptions

Example:
```python
def dijkstra(graph: Graph, source: str, fringe_type: str = 'heap'):
    """
    Dijkstra's shortest path algorithm.
    Returns (distances, predecessors, step_history).
    """
```

---

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`
**Solution**: Set PYTHONPATH before running:
```bash
PYTHONPATH=. python3 src/ui.py
```

**Issue**: Tests fail with import errors
**Solution**: Install pytest:
```bash
python3 -m pip install pytest
```

**Issue**: Animation generation is slow
**Solution**: Reduce graph size or animation duration in code

**Issue**: Images don't open automatically
**Solution**: Images are saved in current directory. Open manually:
- `temp_graph.png` - Graph visualization
- `animations/*.gif` - Algorithm animations

---

## Contact

For questions or issues related to this project:
- Check the `PROJECT_PLAN.md` for implementation details
- Review test files for usage examples
- Refer to the comprehensive `PROJECT_REPORT.pdf`

---

## Acknowledgments

- **Course**: COMP372 - Data Structures and Algorithms
- **Algorithms**: Based on classical graph algorithms by Dijkstra and Prim
- **Libraries**: matplotlib, networkx, Pillow, numpy

---

**Last Updated**: November 2025
**Version**: 1.0
**Status**: ✅ Complete
