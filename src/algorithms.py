"""
Dijkstra's shortest path and Prim's MST algorithms.
Supports both BinaryHeap and SortedLinkedList fringe types.
"""

from typing import Dict, List, Tuple, Set, Optional, Any
from src.graph import Graph
from src.fringe import BinaryHeap, SortedLinkedList


def dijkstra(
    graph: Graph,
    source: str,
    fringe_type: str = 'heap'
) -> Tuple[Dict[str, float], Dict[str, Optional[str]], List[Dict[str, Any]]]:
    """
    Dijkstra's shortest path algorithm.
    Returns (distances, predecessors, step_history).
    """
    # Validate inputs
    if not graph.has_vertex(source):
        raise ValueError(f"Source vertex '{source}' not in graph")

    # Initialize fringe
    if fringe_type == 'heap':
        fringe = BinaryHeap()
    elif fringe_type == 'list':
        fringe = SortedLinkedList()
    else:
        raise ValueError(f"Invalid fringe_type: {fringe_type}")

    # Initialize data structures
    distance: Dict[str, float] = {v: float('inf') for v in graph.get_vertices()}
    distance[source] = 0.0
    previous: Dict[str, Optional[str]] = {v: None for v in graph.get_vertices()}
    visited: Set[str] = set()
    step_history: List[Dict[str, Any]] = []

    # Start with source vertex
    fringe.insert(source, 0.0)

    # Record initial state
    step_history.append({
        'iteration': 0,
        'current': None,
        'visited': set(),
        'distances': distance.copy(),
        'fringe_size': fringe.size()
    })

    iteration = 0

    # Main algorithm loop
    while not fringe.is_empty():
        # Extract minimum distance vertex
        current, current_dist = fringe.extract_min()

        # Skip if already visited (may happen with multiple insertions)
        if current in visited:
            continue

        visited.add(current)
        iteration += 1

        # Explore neighbors
        neighbors = graph.get_neighbors(current)
        for neighbor, weight in neighbors.items():
            if neighbor not in visited:
                alt_distance = distance[current] + weight

                # Update if better path found
                if alt_distance < distance[neighbor]:
                    distance[neighbor] = alt_distance
                    previous[neighbor] = current
                    fringe.insert(neighbor, alt_distance)

        # Record step
        step_history.append({
            'iteration': iteration,
            'current': current,
            'current_distance': current_dist,
            'visited': visited.copy(),
            'distances': distance.copy(),
            'previous': previous.copy(),
            'fringe_size': fringe.size()
        })

    return distance, previous, step_history


def prim(
    graph: Graph,
    start: str,
    fringe_type: str = 'heap'
) -> Tuple[List[Tuple[str, str, float]], float, List[Dict[str, Any]]]:
    """
    Prim's minimum spanning tree algorithm.
    Returns (mst_edges, total_weight, step_history).
    """
    # Validate inputs
    if not graph.has_vertex(start):
        raise ValueError(f"Start vertex '{start}' not in graph")

    if graph.directed:
        raise ValueError("Prim's algorithm requires an undirected graph")

    # Initialize fringe
    if fringe_type == 'heap':
        fringe = BinaryHeap()
    elif fringe_type == 'list':
        fringe = SortedLinkedList()
    else:
        raise ValueError(f"Invalid fringe_type: {fringe_type}")

    # Initialize data structures
    key: Dict[str, float] = {v: float('inf') for v in graph.get_vertices()}
    key[start] = 0.0
    parent: Dict[str, Optional[str]] = {v: None for v in graph.get_vertices()}
    visited: Set[str] = set()
    mst_edges: List[Tuple[str, str, float]] = []
    step_history: List[Dict[str, Any]] = []

    # Start with initial vertex
    fringe.insert(start, 0.0)

    # Record initial state
    step_history.append({
        'iteration': 0,
        'current': None,
        'visited': set(),
        'mst_edges': [],
        'keys': key.copy(),
        'fringe_size': fringe.size()
    })

    iteration = 0

    # Main algorithm loop
    while not fringe.is_empty():
        # Extract minimum key vertex
        current, current_key = fringe.extract_min()

        # Skip if already visited
        if current in visited:
            continue

        visited.add(current)
        iteration += 1

        # Add edge to MST (except for start vertex)
        if parent[current] is not None:
            edge = (parent[current], current, key[current])
            mst_edges.append(edge)

        # Update keys for neighbors
        neighbors = graph.get_neighbors(current)
        for neighbor, weight in neighbors.items():
            if neighbor not in visited and weight < key[neighbor]:
                key[neighbor] = weight
                parent[neighbor] = current
                fringe.insert(neighbor, weight)

        # Record step
        step_history.append({
            'iteration': iteration,
            'current': current,
            'current_key': current_key,
            'visited': visited.copy(),
            'mst_edges': mst_edges.copy(),
            'keys': key.copy(),
            'parent': parent.copy(),
            'fringe_size': fringe.size()
        })

    # Calculate total weight
    total_weight = sum(weight for _, _, weight in mst_edges)

    return mst_edges, total_weight, step_history


def get_shortest_path(
    source: str,
    target: str,
    previous: Dict[str, Optional[str]]
) -> Optional[List[str]]:
    """
    Reconstruct shortest path from source to target using predecessor map.
    Returns None if no path exists.
    """
    if target not in previous:
        return None

    # Build path backwards from target
    path = []
    current = target

    while current is not None:
        path.append(current)
        current = previous[current]

    # Check if we reached the source
    if path[-1] != source:
        return None

    # Reverse to get source-to-target order
    path.reverse()
    return path


def reconstruct_mst_graph(mst_edges: List[Tuple[str, str, float]]) -> Graph:
    """
    Create a Graph object from MST edges.
    Useful for visualization.
    """
    mst_graph = Graph(directed=False)

    for u, v, weight in mst_edges:
        mst_graph.add_edge(u, v, weight)

    return mst_graph
