# Algorithm Pseudocode and Design

This document provides detailed pseudocode for Dijkstra's shortest path and Prim's minimum spanning tree algorithms, along with design rationale and alternative approaches.

---

## Table of Contents

1. [Dijkstra's Shortest Path Algorithm](#dijkstras-shortest-path-algorithm)
2. [Prim's Minimum Spanning Tree Algorithm](#prims-minimum-spanning-tree-algorithm)
3. [Alternative Approaches](#alternative-approaches)
4. [Design Decisions](#design-decisions)

---

## Dijkstra's Shortest Path Algorithm

### Purpose

Find the shortest paths from a source vertex to all other vertices in a weighted graph with non-negative edge weights.

### Pseudocode

```
DIJKSTRA(Graph G, vertex source, fringe_type)
    Input:  G = (V, E) weighted graph with non-negative edges
            source = starting vertex
            fringe_type = 'heap' or 'list' for priority queue type
    Output: distance[] = shortest distances from source to all vertices
            previous[] = predecessor map for path reconstruction
            history[] = step-by-step execution trace

    // Initialize data structures
    FOR each vertex v in V DO
        distance[v] ← ∞
        previous[v] ← NULL
    END FOR

    distance[source] ← 0
    visited ← empty set

    // Create priority queue (fringe)
    IF fringe_type = 'heap' THEN
        fringe ← new BinaryHeap()
    ELSE
        fringe ← new SortedLinkedList()
    END IF

    fringe.insert(source, 0)
    history ← [initial_state]

    // Main algorithm loop
    WHILE fringe is not empty DO
        // Extract vertex with minimum distance
        (current, current_dist) ← fringe.extract_min()

        // Skip if already visited (handles duplicate insertions)
        IF current in visited THEN
            CONTINUE
        END IF

        visited.add(current)

        // Relax all edges from current vertex
        FOR each neighbor of current DO
            IF neighbor not in visited THEN
                alt_distance ← distance[current] + weight(current, neighbor)

                // Update if better path found
                IF alt_distance < distance[neighbor] THEN
                    distance[neighbor] ← alt_distance
                    previous[neighbor] ← current
                    fringe.insert(neighbor, alt_distance)
                END IF
            END IF
        END FOR

        // Record step for visualization
        history.append(current_state)
    END WHILE

    RETURN (distance, previous, history)
END DIJKSTRA
```

### Line-by-Line Explanation

1. **Initialization (Lines 8-11)**: Set all distances to infinity and predecessors to NULL. This represents "unknown" distance until a path is found.

2. **Source Setup (Line 13)**: The source vertex has distance 0 to itself.

3. **Fringe Selection (Lines 17-21)**: Choose priority queue implementation. The heap provides better performance for large graphs.

4. **Main Loop (Line 26)**: Continue until all reachable vertices are processed.

5. **Extract Minimum (Line 28)**: Get the unvisited vertex with the smallest tentative distance. This is the "greedy" choice that guarantees optimality.

6. **Skip Duplicates (Lines 31-33)**: Since we insert vertices multiple times with updated priorities, skip if already processed.

7. **Edge Relaxation (Lines 38-47)**: For each neighbor, check if going through current vertex provides a shorter path. This is the core of the algorithm.

8. **Update Path (Lines 43-46)**: If a shorter path is found, update the distance and predecessor, then add to fringe for future processing.

### Correctness Argument

**Invariant**: After processing vertex v, distance[v] contains the shortest path distance from source to v.

**Proof Sketch**:
1. All edge weights are non-negative
2. At each step, we process the vertex with minimum tentative distance
3. Once a vertex is processed, no shorter path can be found (due to non-negative weights)
4. Therefore, the greedy choice is optimal

---

## Prim's Minimum Spanning Tree Algorithm

### Purpose

Construct a minimum spanning tree (MST) for a connected, undirected, weighted graph.

### Pseudocode

```
PRIM(Graph G, vertex start, fringe_type)
    Input:  G = (V, E) undirected weighted graph
            start = initial vertex
            fringe_type = 'heap' or 'list'
    Output: mst_edges[] = list of MST edges
            total_weight = sum of MST edge weights
            history[] = execution trace

    // Initialize data structures
    FOR each vertex v in V DO
        key[v] ← ∞
        parent[v] ← NULL
    END FOR

    key[start] ← 0
    visited ← empty set
    mst_edges ← empty list

    // Create priority queue
    IF fringe_type = 'heap' THEN
        fringe ← new BinaryHeap()
    ELSE
        fringe ← new SortedLinkedList()
    END IF

    fringe.insert(start, 0)
    history ← [initial_state]

    // Main algorithm loop
    WHILE fringe is not empty DO
        // Extract vertex with minimum key
        (current, current_key) ← fringe.extract_min()

        // Skip if already in MST
        IF current in visited THEN
            CONTINUE
        END IF

        visited.add(current)

        // Add edge to MST (except for start vertex)
        IF parent[current] is not NULL THEN
            edge ← (parent[current], current, key[current])
            mst_edges.append(edge)
        END IF

        // Update keys for adjacent vertices
        FOR each neighbor of current DO
            edge_weight ← weight(current, neighbor)

            IF neighbor not in visited AND edge_weight < key[neighbor] THEN
                key[neighbor] ← edge_weight
                parent[neighbor] ← current
                fringe.insert(neighbor, edge_weight)
            END IF
        END FOR

        // Record step for visualization
        history.append(current_state)
    END WHILE

    // Calculate total MST weight
    total_weight ← sum of weights in mst_edges

    RETURN (mst_edges, total_weight, history)
END PRIM
```

### Line-by-Line Explanation

1. **Initialization (Lines 10-13)**: Set all keys to infinity. The key represents the minimum weight edge connecting a vertex to the growing MST.

2. **Start Vertex (Line 15)**: Start with any vertex (key = 0).

3. **Main Loop (Line 30)**: Continue until all vertices are added to the MST.

4. **Extract Minimum (Line 32)**: Get the vertex with the minimum key (lightest edge to MST).

5. **Skip Processed (Lines 35-37)**: Vertices already in MST should not be reprocessed.

6. **Add Edge (Lines 42-45)**: Add the edge connecting current vertex to the MST (except for the first vertex).

7. **Update Keys (Lines 48-55)**: For each neighbor not in MST, check if the edge to current is lighter than the neighbor's current key. Update if so.

### Correctness Argument

**Invariant**: The growing set of edges forms a minimum spanning tree of the visited vertices.

**Proof Sketch**:
1. Start with a single vertex (trivial MST)
2. At each step, add the lightest edge connecting MST to a new vertex
3. By the cut property of MSTs, this greedy choice is always safe
4. When all vertices are included, we have a complete MST

---

## Alternative Approaches

### For Shortest Paths

#### 1. Bellman-Ford Algorithm

**Advantages**:
- Handles negative edge weights
- Detects negative cycles

**Disadvantages**:
- Time complexity: O(VE) - slower than Dijkstra
- Less efficient for non-negative weights

**When to use**: Graphs with negative weights or when cycle detection is needed.

#### 2. A* Search Algorithm

**Advantages**:
- Faster for single-target searches with good heuristic
- Time complexity: O(E) in best case

**Disadvantages**:
- Requires domain-specific heuristic function
- Only finds path to one target, not all

**When to use**: Single source-target queries with available heuristic (e.g., geographic distance).

#### 3. Floyd-Warshall Algorithm

**Advantages**:
- Finds all-pairs shortest paths
- Handles negative weights
- Simple implementation

**Disadvantages**:
- Time complexity: O(V³) - very slow
- Space complexity: O(V²)

**When to use**: Small graphs where all-pairs distances are needed.

### For Minimum Spanning Trees

#### 1. Kruskal's Algorithm

**Approach**: Sort all edges, add smallest edges that don't create cycles

**Advantages**:
- Simpler to implement
- Edge-based (vs vertex-based)
- Better for sparse graphs

**Disadvantages**:
- Requires sorting all edges: O(E log E)
- Needs union-find data structure

**Comparison**:
- Kruskal: O(E log E) - better for sparse graphs (E << V²)
- Prim: O((V+E) log V) with heap - better for dense graphs

#### 2. Borůvka's Algorithm

**Approach**: Parallel-friendly, processes all vertices simultaneously

**Advantages**:
- Highly parallelizable
- Time complexity: O(E log V)

**Disadvantages**:
- More complex implementation
- Not significantly better than Kruskal/Prim for sequential execution

**When to use**: Parallel/distributed systems.

---

## Design Decisions

### Why Dijkstra and Prim?

1. **Educational Value**: Classic algorithms that demonstrate greedy approach
2. **Practical Applications**: Widely used in real-world problems
3. **Similar Structure**: Both use priority queues, allowing direct fringe comparison
4. **Non-trivial Complexity**: Interesting performance characteristics

### Why Two Fringe Types?

**Binary Heap**:
- Optimal theoretical complexity: O(log n) operations
- Standard choice for production systems
- More complex implementation

**Sorted Linked List**:
- Simpler to understand and implement
- Demonstrates importance of data structure choice
- Good teaching tool for complexity analysis
- Adequate for small graphs

### Key Implementation Choices

#### 1. Adjacency List Representation
**Rationale**: O(1) neighbor lookup, space-efficient for sparse graphs

**Alternative**: Adjacency matrix
- Pros: O(1) edge existence check
- Cons: O(V²) space, inefficient for sparse graphs

#### 2. Duplicate Insertions vs Decrease-Key
**Our Approach**: Insert vertices multiple times with updated priorities, skip duplicates

**Rationale**:
- Simpler implementation
- Works with any priority queue
- Small overhead for typical graphs

**Alternative**: True decrease-key operation
- Pros: No duplicate processing
- Cons: Requires position tracking (already implemented in our heap)

#### 3. Step History Recording
**Rationale**: Essential for visualization and animation

**Trade-off**:
- Increased memory usage
- Slower execution (copying state)
- Valuable for educational purposes and debugging

#### 4. Graph Type Validation
**Prim requires undirected graphs**: Check at runtime

**Rationale**:
- MST concept only applies to undirected graphs
- Better to fail fast with clear error message
- Dijkstra works on both directed and undirected

---

## Conclusion

Both Dijkstra's and Prim's algorithms demonstrate the power of the greedy approach combined with efficient priority queue operations. The choice of fringe data structure significantly impacts performance, especially for larger graphs. The binary heap provides superior asymptotic complexity, while the sorted linked list offers simplicity for small-scale applications.

The algorithms share structural similarities but solve fundamentally different problems:
- **Dijkstra**: Finds optimal paths from source to all vertices
- **Prim**: Constructs a minimum-weight connected subgraph

Understanding these algorithms and their implementation trade-offs provides valuable insights into algorithm design, data structure selection, and performance optimization.
