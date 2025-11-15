import pytest
from src.graph import Graph
from src.algorithms import dijkstra, prim, get_shortest_path, reconstruct_mst_graph


class TestDijkstra:
    def setup_method(self):
        # Create a simple test graph.
        # Triangle graph: A--1--B--2--C, A--4--C
        self.graph = Graph(directed=False)
        self.graph.add_edge('A', 'B', 1.0)
        self.graph.add_edge('B', 'C', 2.0)
        self.graph.add_edge('A', 'C', 4.0)

    def test_dijkstra_with_heap(self):
        distances, previous, history = dijkstra(self.graph, 'A', 'heap')

        assert distances['A'] == 0.0
        assert distances['B'] == 1.0
        assert distances['C'] == 3.0  # Via B, not direct
        assert previous['B'] == 'A'
        assert previous['C'] == 'B'

    def test_dijkstra_with_list(self):
        distances, previous, history = dijkstra(self.graph, 'A', 'list')

        assert distances['A'] == 0.0
        assert distances['B'] == 1.0
        assert distances['C'] == 3.0
        assert previous['B'] == 'A'
        assert previous['C'] == 'B'

    def test_shortest_path_reconstruction(self):
        distances, previous, history = dijkstra(self.graph, 'A', 'heap')

        path = get_shortest_path('A', 'C', previous)
        assert path == ['A', 'B', 'C']


class TestPrim:

    def setup_method(self):
        """Create a simple test graph."""
        # Triangle graph: A--1--B--2--C, A--4--C
        self.graph = Graph(directed=False)
        self.graph.add_edge('A', 'B', 1.0)
        self.graph.add_edge('B', 'C', 2.0)
        self.graph.add_edge('A', 'C', 4.0)

    def test_prim_with_heap(self):
        mst_edges, total_weight, history = prim(self.graph, 'A', 'heap')

        assert len(mst_edges) == 2  # MST has V-1 edges
        assert total_weight == 3.0  # Should exclude edge A-C (weight 4)

    def test_prim_with_list(self):
        mst_edges, total_weight, history = prim(self.graph, 'A', 'list')

        assert len(mst_edges) == 2
        assert total_weight == 3.0

    def test_mst_graph_reconstruction(self):
        mst_edges, total_weight, history = prim(self.graph, 'A', 'heap')

        mst_graph = reconstruct_mst_graph(mst_edges)
        assert mst_graph.num_vertices() == 3
        assert mst_graph.num_edges() == 2
