from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict


class Graph:
    # weighted graph implementation with adjacency list
    # each vertex maps to a dict of neighbors and edge weights

    def __init__(self, directed: bool = False):
        self.directed = directed
        # adjacency list: vertex -> {neighbor: weight}
        self._adj_list: Dict[str, Dict[str, float]] = defaultdict(dict)

    def add_vertex(self, vertex: str) -> None:
        # add a vertex to the graph
        if vertex is None or vertex == "":
            raise ValueError("Vertex identifier cannot be None or empty")
        if vertex not in self._adj_list:
            self._adj_list[vertex] = {}

    def add_edge(self, u: str, v: str, weight: float) -> None:
        # add weighted edge between u and v
        # for undirected graphs, adds edge in both directions
        if u is None or u == "" or v is None or v == "":
            raise ValueError("Vertex identifiers cannot be None or empty")
        if weight < 0:
            raise ValueError("Edge weight cannot be negative")

        # ensure both vertices exist
        self.add_vertex(u)
        self.add_vertex(v)

        self._adj_list[u][v] = weight

        # add reverse edge for undirected graphs
        if not self.directed:
            self._adj_list[v][u] = weight

    def get_neighbors(self, vertex: str) -> Dict[str, float]:
        # return neighbors of a vertex with edge weights
        if vertex not in self._adj_list:
            return {}
        return self._adj_list[vertex].copy()

    def get_weight(self, u: str, v: str) -> Optional[float]:
        # get weight of edge (u, v), or None if doesn't exist
        if u in self._adj_list and v in self._adj_list[u]:
            return self._adj_list[u][v]
        return None

    def get_vertices(self) -> Set[str]:
        # return all vertices in the graph
        return set(self._adj_list.keys())

    def get_edges(self) -> List[Tuple[str, str, float]]:
        # return all edges as (source, dest, weight) tuples
        edges = []
        seen_edges = set()

        for u in self._adj_list:
            for v, weight in self._adj_list[u].items():
                if self.directed:
                    edges.append((u, v, weight))
                else:
                    # avoid duplicates in undirected graph
                    edge = tuple(sorted([u, v]))
                    if edge not in seen_edges:
                        edges.append((u, v, weight))
                        seen_edges.add(edge)
        return edges

    def has_vertex(self, vertex: str) -> bool:
        # check if vertex exists
        return vertex in self._adj_list

    def has_edge(self, u: str, v: str) -> bool:
        # check if edge exists
        return u in self._adj_list and v in self._adj_list[u]

    def num_vertices(self) -> int:
        # number of vertices
        return len(self._adj_list)

    def num_edges(self) -> int:
        # number of edges
        if self.directed:
            return sum(len(neighbors) for neighbors in self._adj_list.values())
        else:
            # divide by 2 since each edge stored twice
            return sum(len(neighbors) for neighbors in self._adj_list.values()) // 2

    def __str__(self) -> str:
        graph_type = "Directed" if self.directed else "Undirected"
        result = [f"{graph_type} Graph with {self.num_vertices()} vertices and {self.num_edges()} edges:"]

        for vertex in sorted(self._adj_list.keys()):
            neighbors = self._adj_list[vertex]
            if neighbors:
                neighbor_str = ", ".join(f"{v}({w})" for v, w in sorted(neighbors.items()))
                result.append(f"  {vertex} -> {neighbor_str}")
            else:
                result.append(f"  {vertex} -> (no edges)")

        return "\n".join(result)

    def __repr__(self) -> str:
        return f"Graph(directed={self.directed}, vertices={self.num_vertices()}, edges={self.num_edges()})"
