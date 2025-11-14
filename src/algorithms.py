from typing import Dict, List, Tuple, Set, Optional, Any
from src.graph import Graph
from src.fringe import BinaryHeap, SortedLinkedList


def dijkstra(
    graph: Graph,
    source: str,
    fringe_type: str = 'heap'
) -> Tuple[Dict[str, float], Dict[str, Optional[str]], List[Dict[str, Any]]]:
    # Dijkstra's algorithm
    # Returns: (distances dict, previous dict, step-by-step history)

    # Step 1: validate inputs
    if not graph.has_vertex(source):
        raise ValueError(f"Source vertex '{source}' not in graph")

    # Step 2: initialize fringe (priority queue)
    if fringe_type == 'heap':
        fringe = BinaryHeap()
    elif fringe_type == 'list':
        fringe = SortedLinkedList()
    else:
        raise ValueError(f"Invalid fringe_type: {fringe_type}")

    # Step 3: initialize distance and predecessor structures
    distance: Dict[str, float] = {v: float('inf') for v in graph.get_vertices()}
    distance[source] = 0.0  # distance to source is 0
    previous: Dict[str, Optional[str]] = {v: None for v in graph.get_vertices()}
    visited: Set[str] = set()
    step_history: List[Dict[str, Any]] = []

    # Step 4: add source to fringe
    fringe.insert(source, 0.0)

    # record initial state
    step_history.append({
        'iteration': 0,
        'current': None,
        'visited': set(),
        'distances': distance.copy(),
        'fringe_size': fringe.size()
    })

    iteration = 0

    # Step 5: main loop - process vertices by distance
    while not fringe.is_empty():
        # extract vertex with minimum distance
        current, current_dist = fringe.extract_min()

        # skip if already visited
        if current in visited:
            continue

        visited.add(current)
        iteration += 1

        # Step 6: explore neighbors
        neighbors = graph.get_neighbors(current)
        for neighbor, weight in neighbors.items():
            if neighbor not in visited:
                # calculate distance through current vertex
                alt_distance = distance[current] + weight

                # Step 7: update if we found a shorter path
                if alt_distance < distance[neighbor]:
                    distance[neighbor] = alt_distance
                    previous[neighbor] = current
                    fringe.insert(neighbor, alt_distance)

        # record this step for visualization
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
    # Prim's algorithm
    # Returns: (MST edges, total weight, step history)

    # Step 1: validate inputs
    if not graph.has_vertex(start):
        raise ValueError(f"Start vertex '{start}' not in graph")

    if graph.directed:
        raise ValueError("Prim's algorithm requires an undirected graph")

    # Step 2: initialize fringe
    if fringe_type == 'heap':
        fringe = BinaryHeap()
    elif fringe_type == 'list':
        fringe = SortedLinkedList()
    else:
        raise ValueError(f"Invalid fringe_type: {fringe_type}")

    # Step 3: initialize key values and parent pointers
    # key = minimum edge weight to connect vertex to MST
    key: Dict[str, float] = {v: float('inf') for v in graph.get_vertices()}
    key[start] = 0.0  # start has key 0
    parent: Dict[str, Optional[str]] = {v: None for v in graph.get_vertices()}
    visited: Set[str] = set()
    mst_edges: List[Tuple[str, str, float]] = []
    step_history: List[Dict[str, Any]] = []

    # Step 4: add start vertex
    fringe.insert(start, 0.0)

    # record initial state
    step_history.append({
        'iteration': 0,
        'current': None,
        'visited': set(),
        'mst_edges': [],
        'keys': key.copy(),
        'fringe_size': fringe.size()
    })

    iteration = 0

    # Step 5: main loop - grow MST one vertex at a time
    while not fringe.is_empty():
        # extract vertex with minimum key
        current, current_key = fringe.extract_min()

        # skip if already visited
        if current in visited:
            continue

        visited.add(current)
        iteration += 1

        # Step 6: add edge to MST (except for start vertex)
        if parent[current] is not None:
            edge = (parent[current], current, key[current])
            mst_edges.append(edge)

        # Step 7: update keys for neighbors
        neighbors = graph.get_neighbors(current)
        for neighbor, weight in neighbors.items():
            # if neighbor not in MST and edge weight is smaller
            if neighbor not in visited and weight < key[neighbor]:
                key[neighbor] = weight
                parent[neighbor] = current
                fringe.insert(neighbor, weight)

        # record this step
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

    # calculate total MST weight
    total_weight = sum(weight for _, _, weight in mst_edges)

    return mst_edges, total_weight, step_history


def get_shortest_path(
    source: str,
    target: str,
    previous: Dict[str, Optional[str]]
) -> Optional[List[str]]:
    # returns None if no path exists

    if target not in previous:
        return None

    # Step 1: build path backwards from target
    path = []
    current = target

    while current is not None:
        path.append(current)
        current = previous[current]

    # Step 2: check if we reached source
    if path[-1] != source:
        return None  # no path exists

    # Step 3: reverse to get source-to-target order
    path.reverse()
    return path


def reconstruct_mst_graph(mst_edges: List[Tuple[str, str, float]]) -> Graph:
    # for visualization
    mst_graph = Graph(directed=False)

    # add all MST edges
    for u, v, weight in mst_edges:
        mst_graph.add_edge(u, v, weight)

    return mst_graph
