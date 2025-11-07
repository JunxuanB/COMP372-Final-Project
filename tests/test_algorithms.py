"""
Tests for Dijkstra's and Prim's algorithms.
Uses small graphs with known, hand-verifiable results.
"""

import pytest
from src.graph import Graph
from src.algorithms import dijkstra, prim, get_shortest_path, reconstruct_mst_graph


class TestDijkstra:
    """Tests for Dijkstra's shortest path algorithm."""

    def setup_method(self):
        """Create test graphs."""
        # Simple triangle graph: A--1--B--2--C, A--4--C
        self.triangle = Graph(directed=False)
        self.triangle.add_edge('A', 'B', 1.0)
        self.triangle.add_edge('B', 'C', 2.0)
        self.triangle.add_edge('A', 'C', 4.0)

        # Directed graph for testing
        self.directed = Graph(directed=True)
        self.directed.add_edge('A', 'B', 1.0)
        self.directed.add_edge('B', 'C', 2.0)
        self.directed.add_edge('C', 'A', 1.0)  # Back edge

        # Disconnected graph
        self.disconnected = Graph(directed=False)
        self.disconnected.add_edge('A', 'B', 1.0)
        self.disconnected.add_edge('C', 'D', 1.0)

    def test_dijkstra_simple_triangle_heap(self):
        """Test Dijkstra on simple triangle graph with heap."""
        distances, previous, history = dijkstra(self.triangle, 'A', 'heap')

        assert distances['A'] == 0.0
        assert distances['B'] == 1.0
        assert distances['C'] == 3.0  # Via B, not direct
        assert previous['A'] is None
        assert previous['B'] == 'A'
        assert previous['C'] == 'B'

    def test_dijkstra_simple_triangle_list(self):
        """Test Dijkstra on simple triangle graph with list."""
        distances, previous, history = dijkstra(self.triangle, 'A', 'list')

        assert distances['A'] == 0.0
        assert distances['B'] == 1.0
        assert distances['C'] == 3.0
        assert previous['B'] == 'A'
        assert previous['C'] == 'B'

    def test_dijkstra_directed_graph(self):
        """Test Dijkstra on directed graph."""
        distances, previous, history = dijkstra(self.directed, 'A', 'heap')

        assert distances['A'] == 0.0
        assert distances['B'] == 1.0
        assert distances['C'] == 3.0

    def test_dijkstra_disconnected_graph(self):
        """Test Dijkstra on disconnected graph."""
        distances, previous, history = dijkstra(self.disconnected, 'A', 'heap')

        assert distances['A'] == 0.0
        assert distances['B'] == 1.0
        assert distances['C'] == float('inf')  # Unreachable
        assert distances['D'] == float('inf')

    def test_dijkstra_single_vertex(self):
        """Test Dijkstra on single vertex graph."""
        single = Graph(directed=False)
        single.add_vertex('A')

        distances, previous, history = dijkstra(single, 'A', 'heap')

        assert distances['A'] == 0.0
        assert previous['A'] is None
        assert len(history) == 2  # Initial + 1 iteration

    def test_dijkstra_invalid_source(self):
        """Test Dijkstra with invalid source vertex."""
        with pytest.raises(ValueError, match="Source vertex .* not in graph"):
            dijkstra(self.triangle, 'Z', 'heap')

    def test_dijkstra_invalid_fringe_type(self):
        """Test Dijkstra with invalid fringe type."""
        with pytest.raises(ValueError, match="Invalid fringe_type"):
            dijkstra(self.triangle, 'A', 'invalid')

    def test_dijkstra_step_history(self):
        """Test that step history is recorded correctly."""
        distances, previous, history = dijkstra(self.triangle, 'A', 'heap')

        assert len(history) > 0
        assert history[0]['iteration'] == 0
        assert history[0]['current'] is None

        # Check that each step has required fields
        for step in history[1:]:
            assert 'iteration' in step
            assert 'current' in step
            assert 'visited' in step
            assert 'distances' in step
            assert 'fringe_size' in step

    def test_dijkstra_larger_graph(self):
        """Test Dijkstra on a larger graph."""
        # Create a 5-vertex graph
        graph = Graph(directed=False)
        graph.add_edge('A', 'B', 4.0)
        graph.add_edge('A', 'C', 2.0)
        graph.add_edge('B', 'C', 1.0)
        graph.add_edge('B', 'D', 5.0)
        graph.add_edge('C', 'D', 8.0)
        graph.add_edge('C', 'E', 10.0)
        graph.add_edge('D', 'E', 2.0)

        distances, previous, history = dijkstra(graph, 'A', 'heap')

        # Verify some shortest paths
        assert distances['A'] == 0.0
        assert distances['B'] == 3.0  # A->C->B
        assert distances['C'] == 2.0  # A->C
        assert distances['D'] == 8.0  # A->C->B->D
        assert distances['E'] == 10.0  # A->C->B->D->E

    def test_get_shortest_path(self):
        """Test path reconstruction."""
        distances, previous, history = dijkstra(self.triangle, 'A', 'heap')

        path_to_c = get_shortest_path('A', 'C', previous)
        assert path_to_c == ['A', 'B', 'C']

        path_to_b = get_shortest_path('A', 'B', previous)
        assert path_to_b == ['A', 'B']

        path_to_a = get_shortest_path('A', 'A', previous)
        assert path_to_a == ['A']

    def test_get_shortest_path_unreachable(self):
        """Test path reconstruction for unreachable vertex."""
        distances, previous, history = dijkstra(self.disconnected, 'A', 'heap')

        path = get_shortest_path('A', 'C', previous)
        assert path is None  # No path exists


class TestPrim:
    """Tests for Prim's minimum spanning tree algorithm."""

    def setup_method(self):
        """Create test graphs."""
        # Simple triangle: A--1--B--2--C, A--4--C
        self.triangle = Graph(directed=False)
        self.triangle.add_edge('A', 'B', 1.0)
        self.triangle.add_edge('B', 'C', 2.0)
        self.triangle.add_edge('A', 'C', 4.0)

        # Square with diagonal
        self.square = Graph(directed=False)
        self.square.add_edge('A', 'B', 1.0)
        self.square.add_edge('B', 'C', 2.0)
        self.square.add_edge('C', 'D', 1.0)
        self.square.add_edge('D', 'A', 2.0)
        self.square.add_edge('A', 'C', 5.0)  # Diagonal (should not be in MST)

    def test_prim_simple_triangle_heap(self):
        """Test Prim on simple triangle graph with heap."""
        mst_edges, total_weight, history = prim(self.triangle, 'A', 'heap')

        assert len(mst_edges) == 2  # MST has V-1 edges
        assert total_weight == 3.0  # 1 + 2

        # Check edges are correct
        edges_set = {(min(u, v), max(u, v)) for u, v, w in mst_edges}
        assert ('A', 'B') in edges_set
        assert ('B', 'C') in edges_set

    def test_prim_simple_triangle_list(self):
        """Test Prim on simple triangle graph with list."""
        mst_edges, total_weight, history = prim(self.triangle, 'A', 'list')

        assert len(mst_edges) == 2
        assert total_weight == 3.0

    def test_prim_square_graph(self):
        """Test Prim on square graph."""
        mst_edges, total_weight, history = prim(self.square, 'A', 'heap')

        assert len(mst_edges) == 3  # 4 vertices -> 3 edges
        assert total_weight == 4.0  # 1 + 2 + 1

        # Diagonal should NOT be in MST
        for u, v, w in mst_edges:
            assert not (u == 'A' and v == 'C' and w == 5.0)
            assert not (u == 'C' and v == 'A' and w == 5.0)

    def test_prim_single_vertex(self):
        """Test Prim on single vertex graph."""
        single = Graph(directed=False)
        single.add_vertex('A')

        mst_edges, total_weight, history = prim(single, 'A', 'heap')

        assert len(mst_edges) == 0
        assert total_weight == 0.0

    def test_prim_invalid_start(self):
        """Test Prim with invalid start vertex."""
        with pytest.raises(ValueError, match="Start vertex .* not in graph"):
            prim(self.triangle, 'Z', 'heap')

    def test_prim_directed_graph_error(self):
        """Test that Prim rejects directed graphs."""
        directed = Graph(directed=True)
        directed.add_edge('A', 'B', 1.0)

        with pytest.raises(ValueError, match="undirected graph"):
            prim(directed, 'A', 'heap')

    def test_prim_invalid_fringe_type(self):
        """Test Prim with invalid fringe type."""
        with pytest.raises(ValueError, match="Invalid fringe_type"):
            prim(self.triangle, 'A', 'invalid')

    def test_prim_step_history(self):
        """Test that step history is recorded correctly."""
        mst_edges, total_weight, history = prim(self.triangle, 'A', 'heap')

        assert len(history) > 0
        assert history[0]['iteration'] == 0
        assert history[0]['current'] is None

        # Check that each step has required fields
        for step in history[1:]:
            assert 'iteration' in step
            assert 'current' in step
            assert 'visited' in step
            assert 'mst_edges' in step
            assert 'keys' in step
            assert 'fringe_size' in step

    def test_prim_larger_graph(self):
        """Test Prim on a larger graph."""
        graph = Graph(directed=False)
        graph.add_edge('A', 'B', 4.0)
        graph.add_edge('A', 'C', 8.0)
        graph.add_edge('B', 'C', 11.0)
        graph.add_edge('B', 'D', 8.0)
        graph.add_edge('C', 'D', 7.0)
        graph.add_edge('C', 'E', 1.0)
        graph.add_edge('D', 'E', 6.0)

        mst_edges, total_weight, history = prim(graph, 'A', 'heap')

        assert len(mst_edges) == 4  # 5 vertices -> 4 edges
        # Known MST weight for this graph: A-B(4) + B-D(8) + C-E(1) + D-E(6) or similar
        assert total_weight == 19.0  # Actual MST weight

    def test_reconstruct_mst_graph(self):
        """Test MST graph reconstruction."""
        mst_edges, total_weight, history = prim(self.triangle, 'A', 'heap')

        mst_graph = reconstruct_mst_graph(mst_edges)

        assert mst_graph.num_vertices() == 3
        assert mst_graph.num_edges() == 2
        assert not mst_graph.directed


class TestAlgorithmComparison:
    """Tests comparing heap vs list performance."""

    def test_both_fringe_types_same_result_dijkstra(self):
        """Verify heap and list give same Dijkstra results."""
        graph = Graph(directed=False)
        graph.add_edge('A', 'B', 1.0)
        graph.add_edge('B', 'C', 2.0)
        graph.add_edge('A', 'C', 4.0)

        dist_heap, prev_heap, _ = dijkstra(graph, 'A', 'heap')
        dist_list, prev_list, _ = dijkstra(graph, 'A', 'list')

        assert dist_heap == dist_list
        assert prev_heap == prev_list

    def test_both_fringe_types_same_result_prim(self):
        """Verify heap and list give same Prim results."""
        graph = Graph(directed=False)
        graph.add_edge('A', 'B', 1.0)
        graph.add_edge('B', 'C', 2.0)
        graph.add_edge('A', 'C', 4.0)

        edges_heap, weight_heap, _ = prim(graph, 'A', 'heap')
        edges_list, weight_list, _ = prim(graph, 'A', 'list')

        assert weight_heap == weight_list
        assert len(edges_heap) == len(edges_list)
