"""Unit tests for Graph data structure."""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.graph import Graph


class TestGraph(unittest.TestCase):

    def test_initialization(self):
        g1 = Graph(directed=False)
        self.assertFalse(g1.directed)
        self.assertEqual(g1.num_vertices(), 0)
        self.assertEqual(g1.num_edges(), 0)

        g2 = Graph(directed=True)
        self.assertTrue(g2.directed)

    def test_add_vertex(self):
        g = Graph()
        g.add_vertex("A")
        self.assertTrue(g.has_vertex("A"))
        self.assertEqual(g.num_vertices(), 1)

        g.add_vertex("B")
        g.add_vertex("C")
        self.assertEqual(g.num_vertices(), 3)

        g.add_vertex("A")  # Duplicate
        self.assertEqual(g.num_vertices(), 3)

    def test_add_vertex_invalid(self):
        g = Graph()
        with self.assertRaises(ValueError):
            g.add_vertex(None)
        with self.assertRaises(ValueError):
            g.add_vertex("")

    def test_add_edge_undirected(self):
        g = Graph(directed=False)
        g.add_edge("A", "B", 5.0)
        self.assertTrue(g.has_edge("A", "B"))
        self.assertTrue(g.has_edge("B", "A"))
        self.assertEqual(g.get_weight("A", "B"), 5.0)
        self.assertEqual(g.num_edges(), 1)

    def test_add_edge_directed(self):
        g = Graph(directed=True)
        g.add_edge("A", "B", 5.0)
        self.assertTrue(g.has_edge("A", "B"))
        self.assertFalse(g.has_edge("B", "A"))
        self.assertEqual(g.num_edges(), 1)

    def test_add_edge_invalid(self):
        g = Graph()
        with self.assertRaises(ValueError):
            g.add_edge("A", "B", -1.0)
        with self.assertRaises(ValueError):
            g.add_edge("", "B", 5.0)

    def test_get_neighbors(self):
        g = Graph()
        g.add_edge("A", "B", 5.0)
        g.add_edge("A", "C", 3.0)

        neighbors = g.get_neighbors("A")
        self.assertEqual(len(neighbors), 2)
        self.assertIn("B", neighbors)
        self.assertEqual(neighbors["B"], 5.0)

    def test_get_weight(self):
        g = Graph()
        g.add_edge("A", "B", 5.0)
        self.assertEqual(g.get_weight("A", "B"), 5.0)
        self.assertIsNone(g.get_weight("A", "C"))

    def test_get_vertices(self):
        g = Graph()
        g.add_edge("A", "B", 5.0)
        g.add_vertex("D")

        vertices = g.get_vertices()
        self.assertIn("A", vertices)
        self.assertIn("D", vertices)

    def test_get_edges(self):
        g = Graph(directed=False)
        g.add_edge("A", "B", 5.0)
        g.add_edge("B", "C", 3.0)

        edges = g.get_edges()
        self.assertEqual(len(edges), 2)

    def test_empty_graph(self):
        g = Graph()
        self.assertEqual(g.num_vertices(), 0)
        self.assertEqual(g.num_edges(), 0)
        self.assertFalse(g.has_vertex("A"))

    def test_single_vertex(self):
        g = Graph()
        g.add_vertex("A")
        self.assertEqual(g.num_vertices(), 1)
        self.assertEqual(g.num_edges(), 0)

    def test_complete_graph(self):
        g = Graph(directed=False)
        vertices = ["A", "B", "C", "D"]
        for i, u in enumerate(vertices):
            for v in vertices[i + 1:]:
                g.add_edge(u, v, 1.0)

        self.assertEqual(g.num_vertices(), 4)
        self.assertEqual(g.num_edges(), 6)

    def test_disconnected_graph(self):
        g = Graph()
        g.add_edge("A", "B", 5.0)
        g.add_edge("C", "D", 3.0)
        g.add_vertex("E")

        self.assertEqual(g.num_vertices(), 5)
        self.assertEqual(g.num_edges(), 2)


if __name__ == '__main__':
    unittest.main()
