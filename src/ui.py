"""
Interactive Tkinter GUI for graph algorithms.
Allows incremental edge addition and algorithm execution.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import os
import sys
from typing import Optional

from src.graph import Graph
from src.algorithms import dijkstra, prim, get_shortest_path
from src.visualizer import draw_graph, create_dijkstra_animation, create_prim_animation


class GraphAlgorithmGUI:
    """Interactive GUI for Dijkstra's and Prim's algorithms."""

    def __init__(self, root):
        self.root = root
        self.root.title("Graph Algorithms - Dijkstra & Prim")
        self.root.geometry("1200x800")

        # Data
        self.graph = Graph(directed=False)
        self.pos = None  # Node positions for consistent layout
        self.last_result = None  # Store last algorithm result

        # Create UI components
        self.create_widgets()

        # Load sample graph
        self.load_sample_graph()

    def create_widgets(self):
        """Create all UI components."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Left panel - Graph visualization
        self.create_graph_panel(main_frame)

        # Right panel - Controls
        self.create_control_panel(main_frame)

    def create_graph_panel(self, parent):
        """Create graph visualization panel."""
        graph_frame = ttk.LabelFrame(parent, text="Graph Visualization", padding="10")
        graph_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        graph_frame.rowconfigure(0, weight=1)
        graph_frame.columnconfigure(0, weight=1)

        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Initial draw
        self.update_graph_display()

    def create_control_panel(self, parent):
        """Create control panel with input fields and buttons."""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        row = 0

        # Edge Input Section
        edge_frame = ttk.LabelFrame(control_frame, text="Add Edge", padding="10")
        edge_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        row += 1

        ttk.Label(edge_frame, text="Node 1:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.node1_entry = ttk.Entry(edge_frame, width=15)
        self.node1_entry.grid(row=0, column=1, pady=2)

        ttk.Label(edge_frame, text="Node 2:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.node2_entry = ttk.Entry(edge_frame, width=15)
        self.node2_entry.grid(row=1, column=1, pady=2)

        ttk.Label(edge_frame, text="Weight:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.weight_entry = ttk.Entry(edge_frame, width=15)
        self.weight_entry.grid(row=2, column=1, pady=2)

        ttk.Button(edge_frame, text="Add Edge", command=self.add_edge).grid(
            row=3, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E)
        )

        ttk.Button(edge_frame, text="Clear Graph", command=self.clear_graph).grid(
            row=4, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E)
        )

        ttk.Button(edge_frame, text="Load Sample", command=self.load_sample_graph).grid(
            row=5, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E)
        )

        # Algorithm Selection Section
        algo_frame = ttk.LabelFrame(control_frame, text="Algorithm", padding="10")
        algo_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        row += 1

        self.algorithm_var = tk.StringVar(value="dijkstra")
        ttk.Radiobutton(algo_frame, text="Dijkstra (Shortest Path)",
                       variable=self.algorithm_var, value="dijkstra").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        ttk.Radiobutton(algo_frame, text="Prim (MST)",
                       variable=self.algorithm_var, value="prim").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )

        ttk.Label(algo_frame, text="Start Node:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.start_entry = ttk.Entry(algo_frame, width=15)
        self.start_entry.grid(row=3, column=0, pady=2)
        self.start_entry.insert(0, "A")

        ttk.Label(algo_frame, text="Fringe Type:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.fringe_var = tk.StringVar(value="heap")
        fringe_combo = ttk.Combobox(algo_frame, textvariable=self.fringe_var,
                                    values=["heap", "list"], state="readonly", width=12)
        fringe_combo.grid(row=5, column=0, pady=2)

        ttk.Button(algo_frame, text="Run Algorithm", command=self.run_algorithm).grid(
            row=6, column=0, pady=10, sticky=(tk.W, tk.E)
        )

        ttk.Button(algo_frame, text="Generate Animation", command=self.generate_animation).grid(
            row=7, column=0, pady=5, sticky=(tk.W, tk.E)
        )

        # Results Section
        results_frame = ttk.LabelFrame(control_frame, text="Results", padding="10")
        results_frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        control_frame.rowconfigure(row, weight=1)
        row += 1

        self.results_text = scrolledtext.ScrolledText(results_frame, width=30, height=15,
                                                      wrap=tk.WORD, state='disabled')
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.rowconfigure(0, weight=1)
        results_frame.columnconfigure(0, weight=1)

    def add_edge(self):
        """Add an edge to the graph."""
        try:
            node1 = self.node1_entry.get().strip()
            node2 = self.node2_entry.get().strip()
            weight_str = self.weight_entry.get().strip()

            if not node1 or not node2 or not weight_str:
                messagebox.showwarning("Input Error", "Please fill all fields")
                return

            weight = float(weight_str)

            if weight < 0:
                messagebox.showwarning("Input Error", "Weight cannot be negative")
                return

            self.graph.add_edge(node1, node2, weight)
            self.update_graph_display()
            self.update_results(f"Added edge: {node1} -- {node2} (weight: {weight})")

            # Clear inputs
            self.node1_entry.delete(0, tk.END)
            self.node2_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Input Error", "Weight must be a number")

    def clear_graph(self):
        """Clear all edges from the graph."""
        self.graph = Graph(directed=False)
        self.pos = None
        self.last_result = None
        self.update_graph_display()
        self.update_results("Graph cleared")

    def load_sample_graph(self):
        """Load a sample graph for testing."""
        self.graph = Graph(directed=False)
        self.graph.add_edge('A', 'B', 4.0)
        self.graph.add_edge('A', 'C', 2.0)
        self.graph.add_edge('B', 'C', 1.0)
        self.graph.add_edge('B', 'D', 5.0)
        self.graph.add_edge('C', 'D', 8.0)
        self.graph.add_edge('C', 'E', 10.0)
        self.graph.add_edge('D', 'E', 2.0)
        self.pos = None
        self.update_graph_display()
        self.update_results("Sample graph loaded (5 vertices, 7 edges)")

    def run_algorithm(self):
        """Run the selected algorithm."""
        if self.graph.num_vertices() == 0:
            messagebox.showwarning("Graph Empty", "Please add edges to the graph first")
            return

        start_node = self.start_entry.get().strip()
        if not start_node:
            messagebox.showwarning("Input Error", "Please enter a start node")
            return

        if not self.graph.has_vertex(start_node):
            messagebox.showwarning("Invalid Node", f"Node '{start_node}' not in graph")
            return

        algorithm = self.algorithm_var.get()
        fringe_type = self.fringe_var.get()

        try:
            start_time = time.time()

            if algorithm == "dijkstra":
                distances, previous, history = dijkstra(self.graph, start_node, fringe_type)
                elapsed = (time.time() - start_time) * 1000  # Convert to ms

                self.last_result = {
                    'type': 'dijkstra',
                    'distances': distances,
                    'previous': previous,
                    'history': history,
                    'start': start_node
                }

                # Display results
                result_text = f"Dijkstra's Algorithm (Fringe: {fringe_type})\n"
                result_text += f"Start: {start_node}\n"
                result_text += f"Execution Time: {elapsed:.2f} ms\n"
                result_text += f"Steps: {len(history) - 1}\n\n"
                result_text += "Shortest Distances:\n"
                for node in sorted(distances.keys()):
                    dist = distances[node]
                    if dist == float('inf'):
                        result_text += f"  {node}: ∞ (unreachable)\n"
                    else:
                        result_text += f"  {node}: {dist:.1f}\n"

                self.update_results(result_text)

            else:  # prim
                mst_edges, total_weight, history = prim(self.graph, start_node, fringe_type)
                elapsed = (time.time() - start_time) * 1000

                self.last_result = {
                    'type': 'prim',
                    'mst_edges': mst_edges,
                    'total_weight': total_weight,
                    'history': history,
                    'start': start_node
                }

                # Display results
                result_text = f"Prim's Algorithm (Fringe: {fringe_type})\n"
                result_text += f"Start: {start_node}\n"
                result_text += f"Execution Time: {elapsed:.2f} ms\n"
                result_text += f"Steps: {len(history) - 1}\n"
                result_text += f"Total MST Weight: {total_weight:.1f}\n\n"
                result_text += "MST Edges:\n"
                for u, v, w in mst_edges:
                    result_text += f"  {u} -- {v} (weight: {w:.1f})\n"

                self.update_results(result_text)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def generate_animation(self):
        """Generate animation for the last run algorithm."""
        if self.last_result is None:
            messagebox.showwarning("No Results", "Please run an algorithm first")
            return

        os.makedirs('animations', exist_ok=True)

        result_type = self.last_result['type']
        history = self.last_result['history']
        start = self.last_result['start']
        fringe_type = self.fringe_var.get()

        timestamp = int(time.time())
        filename = f"animations/{result_type}_{start}_{fringe_type}_{timestamp}.gif"

        try:
            if result_type == 'dijkstra':
                create_dijkstra_animation(self.graph, history, filename, duration=600)
            else:
                create_prim_animation(self.graph, history, filename, duration=600)

            self.update_results(f"Animation saved: {filename}")
            messagebox.showinfo("Success", f"Animation saved to:\n{filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create animation:\n{str(e)}")

    def update_graph_display(self):
        """Update the graph visualization."""
        self.ax.clear()

        if self.graph.num_vertices() == 0:
            self.ax.text(0.5, 0.5, 'Empty Graph\nAdd edges to begin',
                        ha='center', va='center', fontsize=14)
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.ax.axis('off')
        else:
            _, _, self.pos = draw_graph(self.graph, self.pos, self.ax, "Current Graph")

        self.canvas.draw()

    def update_results(self, text: str):
        """Update the results text area."""
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, text)
        self.results_text.config(state='disabled')


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = GraphAlgorithmGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
