"""
Graph data structure using adjacency list representation.
For use with Dijkstra's and Prim's algorithms.
"""

from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict


class Graph:
    """
    Weighted graph using adjacency list representation.
    Can be directed or undirected, supports weighted edges.
    """

    def __init__(self, directed: bool = False):
        self.directed = directed
        self._adj_list: Dict[str, Dict[str, float]] = defaultdict(dict)

    def add_vertex(self, vertex: str) -> None:
        """Add a vertex to the graph."""
        if vertex is None or vertex == "":
            raise ValueError("Vertex identifier cannot be None or empty")
        if vertex not in self._adj_list:
            self._adj_list[vertex] = {}

    def add_edge(self, u: str, v: str, weight: float) -> None:
        """Add a weighted edge. For undirected graphs, adds edge in both directions."""
        if u is None or u == "" or v is None or v == "":
            raise ValueError("Vertex identifiers cannot be None or empty")
        if weight < 0:
            raise ValueError("Edge weight cannot be negative")

        self.add_vertex(u)
        self.add_vertex(v)
        self._adj_list[u][v] = weight

        if not self.directed:
            self._adj_list[v][u] = weight

    def get_neighbors(self, vertex: str) -> Dict[str, float]:
        """Get all neighbors of a vertex with their edge weights."""
        if vertex not in self._adj_list:
            return {}
        return self._adj_list[vertex].copy()

    def get_weight(self, u: str, v: str) -> Optional[float]:
        """Get edge weight, or None if edge doesn't exist."""
        if u in self._adj_list and v in self._adj_list[u]:
            return self._adj_list[u][v]
        return None

    def get_vertices(self) -> Set[str]:
        """Get all vertices in the graph."""
        return set(self._adj_list.keys())

    def get_edges(self) -> List[Tuple[str, str, float]]:
        """Get all edges as list of (source, dest, weight) tuples."""
        edges = []
        seen_edges = set()

        for u in self._adj_list:
            for v, weight in self._adj_list[u].items():
                if self.directed:
                    edges.append((u, v, weight))
                else:
                    # For undirected graphs, avoid duplicates
                    edge = tuple(sorted([u, v]))
                    if edge not in seen_edges:
                        edges.append((u, v, weight))
                        seen_edges.add(edge)
        return edges

    def has_vertex(self, vertex: str) -> bool:
        """Check if vertex exists."""
        return vertex in self._adj_list

    def has_edge(self, u: str, v: str) -> bool:
        """Check if edge exists."""
        return u in self._adj_list and v in self._adj_list[u]

    def num_vertices(self) -> int:
        """Number of vertices."""
        return len(self._adj_list)

    def num_edges(self) -> int:
        """Number of edges."""
        if self.directed:
            return sum(len(neighbors) for neighbors in self._adj_list.values())
        else:
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
