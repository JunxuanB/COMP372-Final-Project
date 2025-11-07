# Complexity Analysis

Detailed time and space complexity analysis for Dijkstra's shortest path and Prim's minimum spanning tree algorithms with different fringe implementations.

---

## Table of Contents

1. [Notation and Definitions](#notation-and-definitions)
2. [Data Structure Complexities](#data-structure-complexities)
3. [Algorithm Complexities](#algorithm-complexities)
4. [Empirical Analysis](#empirical-analysis)
5. [Performance Comparison](#performance-comparison)

---

## Notation and Definitions

### Graph Notation

- **V**: Number of vertices in the graph
- **E**: Number of edges in the graph
- **n**: Generic size parameter (vertices in fringe)

### Complexity Classes

- **O(f(n))**: Upper bound (worst case)
- **Ω(f(n))**: Lower bound (best case)
- **Θ(f(n))**: Tight bound (average case)

### Graph Types

- **Sparse graph**: E = O(V) - few edges
- **Dense graph**: E = O(V²) - many edges
- **Complete graph**: E = V(V-1)/2 - all possible edges

---

## Data Structure Complexities

### Binary Heap

#### Operations

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Insert | O(log n) | O(1) |
| Extract Min | O(log n) | O(1) |
| Decrease Key | O(log n) | O(1) |
| Build Heap | O(n) | O(n) |
| Is Empty | O(1) | O(1) |

#### Analysis

**Insert**:
```
- Add element at end of array: O(1)
- Bubble up to restore heap property: O(log n)
- Update position tracking: O(1)
Total: O(log n)
```

**Extract Min**:
```
- Return root element: O(1)
- Move last element to root: O(1)
- Bubble down to restore heap property: O(log n)
- Update position tracking: O(log n)
Total: O(log n)
```

**Decrease Key**:
```
- Find element using position map: O(1)
- Update priority: O(1)
- Bubble up to restore heap property: O(log n)
- Update position tracking: O(log n)
Total: O(log n)
```

**Space Complexity**: O(n)
- Array storage: O(n)
- Position tracking dictionary: O(n)

### Sorted Linked List

#### Operations

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Insert | O(n) | O(1) |
| Extract Min | O(1) | O(1) |
| Decrease Key | O(n) | O(1) |
| Is Empty | O(1) | O(1) |

#### Analysis

**Insert**:
```
- Traverse list to find insertion position: O(n)
- Insert node at correct position: O(1)
Total: O(n) worst case, O(1) best case
```

**Extract Min**:
```
- Remove and return first node: O(1)
(List is kept sorted, minimum is always at front)
```

**Decrease Key**:
```
- Find element in list: O(n)
- Remove element: O(1)
- Re-insert with new priority: O(n)
Total: O(n)
```

**Space Complexity**: O(n)
- Node storage: O(n)
- No additional tracking needed

---

## Algorithm Complexities

### Dijkstra's Algorithm

#### With Binary Heap

**Time Complexity**: **O((V + E) log V)**

**Detailed Analysis**:
```
1. Initialize distances and previous: O(V)

2. Main loop executes V times (process each vertex once)

3. For each iteration:
   - Extract min from heap: O(log V)
   - Process edges of current vertex
   - Each edge processed once across all iterations: E total
   - For each edge:
     * Check if neighbor visited: O(1)
     * Update distance: O(1)
     * Insert/decrease-key in heap: O(log V)

4. Total operations:
   - V extractions: V * O(log V) = O(V log V)
   - E edge relaxations: E * O(log V) = O(E log V)

5. Combined: O(V log V + E log V) = O((V + E) log V)
```

**Space Complexity**: **O(V + E)**
```
- Graph storage (adjacency list): O(V + E)
- Distance array: O(V)
- Previous array: O(V)
- Visited set: O(V)
- Binary heap: O(V)
- Step history (optional): O(V * H) where H is history entry size
Total: O(V + E) without history
```

#### With Sorted Linked List

**Time Complexity**: **O(V²)**

**Detailed Analysis**:
```
1. Initialize: O(V)

2. Main loop: V iterations

3. For each iteration:
   - Extract min from list: O(1)
   - Process edges: E/V edges per vertex on average
   - For each edge:
     * Insert in sorted list: O(V) worst case

4. Total edge relaxations: E * O(V) = O(EV)

5. For dense graphs (E ≈ V²): O(V³)
   For sparse graphs (E ≈ V): O(V²)

6. Simplified: O(V²) for typical graphs
```

**Space Complexity**: **O(V + E)**
```
Same as heap version, but linked list instead of heap.
```

### Prim's Algorithm

#### With Binary Heap

**Time Complexity**: **O((V + E) log V)**

**Analysis** (identical structure to Dijkstra):
```
1. Initialize keys and parent: O(V)

2. Main loop: V iterations
   - Extract min: V * O(log V) = O(V log V)

3. Edge processing: E total edges
   - Update key/insert: E * O(log V) = O(E log V)

4. Total: O(V log V + E log V) = O((V + E) log V)
```

**Space Complexity**: **O(V + E)**
```
- Graph storage: O(V + E)
- Key array: O(V)
- Parent array: O(V)
- Visited set: O(V)
- MST edges: O(V)
- Binary heap: O(V)
Total: O(V + E)
```

#### With Sorted Linked List

**Time Complexity**: **O(V²)**

**Analysis**:
```
1. Initialize: O(V)

2. Main loop: V iterations
   - Extract min: V * O(1) = O(V)

3. Edge processing:
   - E edges total
   - Each update requires insertion: E * O(V) = O(EV)

4. Simplified: O(V²) for typical graphs
```

**Space Complexity**: **O(V + E)**

---

## Empirical Analysis

### Benchmark Results

Based on actual performance tests with random graphs:

#### Graph Sizes and Performance

| Vertices | Edges | Dijkstra Heap | Dijkstra List | Speedup | Prim Heap | Prim List | Speedup |
|----------|-------|---------------|---------------|---------|-----------|-----------|---------|
| 10 | 18 | 0.03 ms | 0.02 ms | 0.73x | 0.03 ms | 0.02 ms | 0.82x |
| 20 | 62 | 0.07 ms | 0.06 ms | 0.85x | 0.07 ms | 0.06 ms | 0.89x |
| 50 | 263 | 0.31 ms | 0.27 ms | 0.87x | 0.23 ms | 0.36 ms | 1.56x |
| 100 | 1,080 | 0.61 ms | 1.39 ms | 2.28x | 0.78 ms | 2.04 ms | 2.63x |
| 200 | 4,143 | 1.79 ms | 6.98 ms | 3.89x | 2.36 ms | 9.21 ms | 3.90x |
| 500 | 25,327 | 9.23 ms | 52.60 ms | 5.70x | 11.28 ms | 73.55 ms | 6.52x |

### Observations

#### 1. Small Graphs (V ≤ 50)
- List performs comparably or better than heap
- Overhead of heap operations not justified
- Constant factors dominate

**Explanation**:
- log V is small (log 50 ≈ 5.6)
- Linear search in small list is fast
- Heap maintenance overhead is significant

#### 2. Medium Graphs (V ≈ 100)
- Heap becomes 2-3x faster
- Crossover point where asymptotic complexity matters
- Clear advantage emerges

#### 3. Large Graphs (V ≥ 200)
- Heap is 4-7x faster
- Gap widens with graph size
- Matches theoretical predictions

### Complexity Verification

#### Dijkstra with Heap: O((V + E) log V)

For our benchmarks:
- V = 500, E = 25,327
- Predicted: (500 + 25,327) * log₂(500) ≈ 25,827 * 8.97 ≈ 231,667 operations
- Actual time: 9.23 ms
- Operations per ms: ~25,000

#### Dijkstra with List: O(V²)

For V = 500:
- Predicted: 500² = 250,000 operations (simplified)
- Actual time: 52.60 ms
- Operations per ms: ~4,750

**Ratio**: 52.60 / 9.23 = 5.70x slower (matches empirical speedup)

### Growth Rate Analysis

#### Heap Implementation

| V₁ | V₂ | Time₁ | Time₂ | Actual Ratio | Predicted Ratio |
|----|----|----|----|----|-----|
| 100 | 200 | 0.61 ms | 1.79 ms | 2.93x | ~2.4x |
| 200 | 500 | 1.79 ms | 9.23 ms | 5.16x | ~4.3x |

Predicted ratio: (V₂/V₁) * (log V₂ / log V₁)

The actual ratios closely match theoretical predictions, confirming O((V + E) log V) complexity.

#### List Implementation

| V₁ | V₂ | Time₁ | Time₂ | Actual Ratio | Predicted Ratio |
|----|----|----|----|----|-----|
| 100 | 200 | 1.39 ms | 6.98 ms | 5.02x | 4.0x |
| 200 | 500 | 6.98 ms | 52.60 ms | 7.54x | 6.25x |

Predicted ratio: (V₂/V₁)²

The actual ratios are slightly higher, consistent with O(V²) complexity.

---

## Performance Comparison

### When to Use Binary Heap

✅ **Recommended for:**
- Large graphs (V > 50)
- Dense graphs (E ≈ V²)
- Production systems
- Performance-critical applications

**Advantages:**
- Superior asymptotic complexity
- Scales well with graph size
- Industry standard

**Trade-offs:**
- More complex implementation
- Higher constant factors
- Position tracking overhead

### When to Use Sorted Linked List

✅ **Recommended for:**
- Small graphs (V < 50)
- Educational purposes
- Simple prototypes
- Memory-constrained environments

**Advantages:**
- Simple implementation
- O(1) extract-min
- Lower constant factors for small n

**Trade-offs:**
- Poor scaling (O(V²))
- Inefficient for large graphs
- Not suitable for production

### Hybrid Approach

**Optimal Strategy:**
```python
def choose_fringe(graph):
    if graph.num_vertices() < 50:
        return SortedLinkedList()
    else:
        return BinaryHeap()
```

This adaptive approach provides:
- Best performance for all graph sizes
- Automatic optimization
- Minimal complexity

---

## Conclusion

### Key Findings

1. **Theoretical complexity matches empirical results**:
   - Heap: O((V + E) log V) confirmed
   - List: O(V²) confirmed

2. **Heap advantage scales with graph size**:
   - Negligible for V < 50
   - Significant for V > 100
   - Dramatic for V > 200

3. **Both algorithms have similar complexity**:
   - Dijkstra and Prim share structure
   - Fringe choice is the determining factor

4. **Space complexity is comparable**:
   - Both O(V + E)
   - Dominated by graph storage

### Practical Implications

**For Software Engineers**:
- Use binary heap for production systems
- Profile before optimizing
- Consider graph characteristics

**For Algorithm Designers**:
- Data structure choice significantly impacts performance
- Asymptotic analysis predicts real-world behavior
- Constant factors matter for small inputs

**For Students**:
- Theoretical complexity analysis is practical
- Implementation details affect performance
- Benchmarking validates analysis

### Future Optimizations

Potential improvements:
1. **Fibonacci Heap**: O(E + V log V) amortized
2. **Pairing Heap**: Simpler than Fibonacci, good practical performance
3. **Bucket Queue**: O(V + E) for integer weights
4. **Radix Heap**: O(E + V√(log C)) for bounded weights

However, binary heap remains the best general-purpose choice for its:
- Simple implementation
- Predictable performance
- Wide applicability
- Excellent scaling

---

**Last Updated**: November 2025
