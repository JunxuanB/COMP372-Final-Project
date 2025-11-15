import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.graph import Graph


class TestGraph(unittest.TestCase):
    def test_initialization(self):
        g = Graph(directed=False)
        self.assertFalse(g.directed)
        self.assertEqual(g.num_vertices(), 0)
        self.assertEqual(g.num_edges(), 0)

    def test_add_vertex(self):
        g = Graph()
        g.add_vertex("A")
        g.add_vertex("B")

        self.assertTrue(g.has_vertex("A"))
        self.assertTrue(g.has_vertex("B"))
        self.assertEqual(g.num_vertices(), 2)

    def test_add_edge_undirected(self):
        g = Graph(directed=False)
        g.add_edge("A", "B", 5.0)

        self.assertTrue(g.has_edge("A", "B"))
        self.assertTrue(g.has_edge("B", "A"))
        self.assertEqual(g.get_weight("A", "B"), 5.0)
        self.assertEqual(g.num_edges(), 1)

    def test_get_neighbors(self):
        g = Graph()
        g.add_edge("A", "B", 5.0)
        g.add_edge("A", "C", 3.0)

        neighbors = g.get_neighbors("A")
        self.assertEqual(len(neighbors), 2)
        self.assertIn("B", neighbors)
        self.assertIn("C", neighbors)
        self.assertEqual(neighbors["B"], 5.0)
        self.assertEqual(neighbors["C"], 3.0)

    def test_multiple_edges(self):
        g = Graph(directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 2.0)
        g.add_edge("C", "D", 3.0)

        self.assertEqual(g.num_vertices(), 4)
        self.assertEqual(g.num_edges(), 3)


if __name__ == '__main__':
    unittest.main()