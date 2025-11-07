"""
Unit tests for the Graph data structure.

Tests cover:
- Vertex and edge operations
- Weighted and directed/undirected graphs
- Edge cases and error handling
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graph import Graph


class TestGraph(unittest.TestCase):
    """Test cases for Graph class."""

    def test_initialization(self):
        """Test graph initialization."""
        # Undirected graph
        g1 = Graph(directed=False)
        self.assertFalse(g1.directed)
        self.assertEqual(g1.num_vertices(), 0)
        self.assertEqual(g1.num_edges(), 0)

        # Directed graph
        g2 = Graph(directed=True)
        self.assertTrue(g2.directed)
        self.assertEqual(g2.num_vertices(), 0)

    def test_add_vertex(self):
        """Test adding vertices."""
        g = Graph()

        g.add_vertex("A")
        self.assertTrue(g.has_vertex("A"))
        self.assertEqual(g.num_vertices(), 1)

        g.add_vertex("B")
        g.add_vertex("C")
        self.assertEqual(g.num_vertices(), 3)

        # Adding duplicate vertex should not increase count
        g.add_vertex("A")
        self.assertEqual(g.num_vertices(), 3)

    def test_add_vertex_invalid(self):
        """Test adding invalid vertices."""
        g = Graph()

        with self.assertRaises(ValueError):
            g.add_vertex(None)

        with self.assertRaises(ValueError):
            g.add_vertex("")

    def test_add_edge_undirected(self):
        """Test adding edges to undirected graph."""
        g = Graph(directed=False)

        g.add_edge("A", "B", 5.0)
        self.assertTrue(g.has_edge("A", "B"))
        self.assertTrue(g.has_edge("B", "A"))  # Undirected
        self.assertEqual(g.get_weight("A", "B"), 5.0)
        self.assertEqual(g.get_weight("B", "A"), 5.0)
        self.assertEqual(g.num_edges(), 1)  # Count as single edge

        g.add_edge("B", "C", 3.0)
        self.assertEqual(g.num_edges(), 2)
        self.assertEqual(g.num_vertices(), 3)

    def test_add_edge_directed(self):
        """Test adding edges to directed graph."""
        g = Graph(directed=True)

        g.add_edge("A", "B", 5.0)
        self.assertTrue(g.has_edge("A", "B"))
        self.assertFalse(g.has_edge("B", "A"))  # Directed
        self.assertEqual(g.num_edges(), 1)

        g.add_edge("B", "A", 3.0)
        self.assertTrue(g.has_edge("B", "A"))
        self.assertEqual(g.num_edges(), 2)

    def test_add_edge_invalid(self):
        """Test adding invalid edges."""
        g = Graph()

        with self.assertRaises(ValueError):
            g.add_edge("A", "B", -1.0)  # Negative weight

        with self.assertRaises(ValueError):
            g.add_edge("", "B", 5.0)  # Empty vertex

        with self.assertRaises(ValueError):
            g.add_edge("A", None, 5.0)  # None vertex

    def test_get_neighbors(self):
        """Test getting vertex neighbors."""
        g = Graph()

        g.add_edge("A", "B", 5.0)
        g.add_edge("A", "C", 3.0)
        g.add_edge("B", "C", 2.0)

        neighbors_a = g.get_neighbors("A")
        self.assertEqual(len(neighbors_a), 2)
        self.assertIn("B", neighbors_a)
        self.assertIn("C", neighbors_a)
        self.assertEqual(neighbors_a["B"], 5.0)
        self.assertEqual(neighbors_a["C"], 3.0)

        # Non-existent vertex
        neighbors_d = g.get_neighbors("D")
        self.assertEqual(len(neighbors_d), 0)

    def test_get_weight(self):
        """Test getting edge weights."""
        g = Graph()

        g.add_edge("A", "B", 5.0)
        self.assertEqual(g.get_weight("A", "B"), 5.0)

        # Non-existent edge
        self.assertIsNone(g.get_weight("A", "C"))
        self.assertIsNone(g.get_weight("X", "Y"))

    def test_get_vertices(self):
        """Test getting all vertices."""
        g = Graph()

        g.add_edge("A", "B", 5.0)
        g.add_edge("B", "C", 3.0)
        g.add_vertex("D")

        vertices = g.get_vertices()
        self.assertEqual(len(vertices), 4)
        self.assertIn("A", vertices)
        self.assertIn("B", vertices)
        self.assertIn("C", vertices)
        self.assertIn("D", vertices)

    def test_get_edges(self):
        """Test getting all edges."""
        g = Graph(directed=False)

        g.add_edge("A", "B", 5.0)
        g.add_edge("B", "C", 3.0)
        g.add_edge("A", "C", 2.0)

        edges = g.get_edges()
        self.assertEqual(len(edges), 3)

        # Check all edges are present
        edge_set = {(min(u, v), max(u, v)) for u, v, w in edges}
        self.assertIn(("A", "B"), edge_set)
        self.assertIn(("B", "C"), edge_set)
        self.assertIn(("A", "C"), edge_set)

    def test_get_edges_directed(self):
        """Test getting all edges from directed graph."""
        g = Graph(directed=True)

        g.add_edge("A", "B", 5.0)
        g.add_edge("B", "C", 3.0)
        g.add_edge("C", "A", 2.0)

        edges = g.get_edges()
        self.assertEqual(len(edges), 3)

    def test_empty_graph(self):
        """Test operations on empty graph."""
        g = Graph()

        self.assertEqual(g.num_vertices(), 0)
        self.assertEqual(g.num_edges(), 0)
        self.assertEqual(len(g.get_vertices()), 0)
        self.assertEqual(len(g.get_edges()), 0)
        self.assertFalse(g.has_vertex("A"))
        self.assertFalse(g.has_edge("A", "B"))

    def test_single_vertex(self):
        """Test graph with single vertex and no edges."""
        g = Graph()

        g.add_vertex("A")
        self.assertEqual(g.num_vertices(), 1)
        self.assertEqual(g.num_edges(), 0)
        self.assertEqual(len(g.get_neighbors("A")), 0)

    def test_complete_graph(self):
        """Test complete graph (all vertices connected)."""
        g = Graph(directed=False)

        vertices = ["A", "B", "C", "D"]
        for i, u in enumerate(vertices):
            for v in vertices[i + 1:]:
                g.add_edge(u, v, 1.0)

        # K4 has 4 vertices and 6 edges
        self.assertEqual(g.num_vertices(), 4)
        self.assertEqual(g.num_edges(), 6)

        # Every vertex should have 3 neighbors
        for vertex in vertices:
            self.assertEqual(len(g.get_neighbors(vertex)), 3)

    def test_disconnected_graph(self):
        """Test graph with disconnected components."""
        g = Graph()

        # Component 1: A-B
        g.add_edge("A", "B", 5.0)

        # Component 2: C-D
        g.add_edge("C", "D", 3.0)

        # Isolated vertex
        g.add_vertex("E")

        self.assertEqual(g.num_vertices(), 5)
        self.assertEqual(g.num_edges(), 2)

        # Verify no connection between components
        self.assertIsNone(g.get_weight("A", "C"))
        self.assertIsNone(g.get_weight("B", "D"))

    def test_string_representation(self):
        """Test string representation of graph."""
        g = Graph()

        g.add_edge("A", "B", 5.0)
        g.add_edge("B", "C", 3.0)

        string_repr = str(g)
        self.assertIn("Graph", string_repr)
        self.assertIn("3 vertices", string_repr)
        self.assertIn("2 edges", string_repr)

        dev_repr = repr(g)
        self.assertIn("Graph", dev_repr)
        self.assertIn("vertices=3", dev_repr)
        self.assertIn("edges=2", dev_repr)


if __name__ == '__main__':
    unittest.main()
