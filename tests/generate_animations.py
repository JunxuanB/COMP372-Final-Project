"""
Generate sample animations for Dijkstra and Prim algorithms.
Creates GIF files in the animations/ directory.
"""

from src.graph import Graph
from src.algorithms import dijkstra, prim
from src.visualizer import create_dijkstra_animation, create_prim_animation
import os


def create_sample_graphs():
    """Create sample test graphs."""
    # Small triangle graph
    triangle = Graph(directed=False)
    triangle.add_edge('A', 'B', 1.0)
    triangle.add_edge('B', 'C', 2.0)
    triangle.add_edge('C', 'D', 1.0)
    triangle.add_edge('A', 'D', 4.0)

    # Medium graph (5 vertices)
    medium = Graph(directed=False)
    medium.add_edge('A', 'B', 4.0)
    medium.add_edge('A', 'C', 2.0)
    medium.add_edge('B', 'C', 1.0)
    medium.add_edge('B', 'D', 5.0)
    medium.add_edge('C', 'D', 8.0)
    medium.add_edge('C', 'E', 10.0)
    medium.add_edge('D', 'E', 2.0)

    return {'triangle': triangle, 'medium': medium}


def main():
    """Generate all sample animations."""
    print("Generating sample animations...")

    # Create animations directory
    os.makedirs('animations', exist_ok=True)

    graphs = create_sample_graphs()

    # Generate Dijkstra animations
    print("\nGenerating Dijkstra animations...")
    for graph_name, graph in graphs.items():
        source = 'A'

        # Heap version
        print(f"  {graph_name} with heap...")
        distances, previous, history = dijkstra(graph, source, 'heap')
        create_dijkstra_animation(
            graph, history,
            f'animations/dijkstra_{graph_name}_heap.gif',
            duration=600
        )

        # List version
        print(f"  {graph_name} with list...")
        distances, previous, history = dijkstra(graph, source, 'list')
        create_dijkstra_animation(
            graph, history,
            f'animations/dijkstra_{graph_name}_list.gif',
            duration=600
        )

    # Generate Prim animations
    print("\nGenerating Prim animations...")
    for graph_name, graph in graphs.items():
        start = 'A'

        # Heap version
        print(f"  {graph_name} with heap...")
        mst_edges, total_weight, history = prim(graph, start, 'heap')
        create_prim_animation(
            graph, history,
            f'animations/prim_{graph_name}_heap.gif',
            duration=600
        )
        print(f"    MST weight: {total_weight:.1f}")

        # List version
        print(f"  {graph_name} with list...")
        mst_edges, total_weight, history = prim(graph, start, 'list')
        create_prim_animation(
            graph, history,
            f'animations/prim_{graph_name}_list.gif',
            duration=600
        )
        print(f"    MST weight: {total_weight:.1f}")

    print("\n✓ All animations generated successfully!")
    print("Check the animations/ directory for GIF files.")


if __name__ == '__main__':
    main()
