import os
import subprocess
import platform
from src.graph import Graph
from src.algorithms import dijkstra, prim
from src.visualizer import draw_graph, create_dijkstra_animation, create_prim_animation
import matplotlib.pyplot as plt

def open_image(filepath):
    # try to open image with system default viewer
    system = platform.system()
    try:
        if system == 'Darwin':  # macOS
            subprocess.run(['open', filepath], check=True)
        elif system == 'Windows':
            os.startfile(filepath)
        else:  # Linux
            subprocess.run(['xdg-open', filepath], check=True)
        return True
    except:
        return False


def create_sample_graph():
    # sample graph for testing - 5 vertices, 7 edges
    graph = Graph(directed=False)
    graph.add_edge('A', 'B', 4.0)
    graph.add_edge('A', 'C', 2.0)
    graph.add_edge('B', 'C', 1.0)
    graph.add_edge('B', 'D', 5.0)
    graph.add_edge('D', 'E', 2.0)
    return graph


def visualize_graph(graph, filename='temp_graph.png'):
    # save graph visualization to file
    fig, ax, pos = draw_graph(graph, title="Current Graph")
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def print_menu():
    print("\n" + "=" * 60)
    print("GRAPH ALGORITHMS - Interactive Demo")
    print("=" * 60)
    print("1. Load Sample Graph")
    print("2. Add Edge")
    print("3. Show Graph Summary")
    print("4. Generate Graph Image")
    print("5. Run and Generate GIF with Dijkstra's Algorithm")
    print("6. Run and Generate GIF with Prim's Algorithm")
    print("7. Compare Heap vs List Performance")
    print("0. Exit")
    print("=" * 60)


def show_graph_summary(graph):
    # Display graph information
    print("\n" + "=" * 60)
    print("GRAPH SUMMARY")
    print("=" * 60)
    print(f"Vertices: {graph.num_vertices()}")
    print(f"Edges: {graph.num_edges()}")
    print(f"Directed: {graph.directed}")

    if graph.num_edges() > 0:
        print("\nEdges:")
        for u, v, w in sorted(graph.get_edges()):
            print(f"  {u} -- {v}  (weight: {w:.1f})")
    else:
        print("\nNo edges in graph.")
    print("=" * 60)


def run_dijkstra_interactive(graph):
    # Run Dijkstra with user input
    print("\n" + "-" * 60)
    print("DIJKSTRA'S SHORTEST PATH ALGORITHM")
    print("-" * 60)

    if graph.num_vertices() == 0:
        print("Error: Graph is empty. Load a graph first.")
        return

    # get start vertex from user
    print(f"Available vertices: {sorted(graph.get_vertices())}")
    start = input("Enter start vertex: ").strip()

    if not graph.has_vertex(start):
        print(f"Error: Vertex '{start}' not in graph.")
        return

    # get fringe type
    print("\nFringe types: heap, list")
    fringe = input("Enter fringe type (default: heap): ").strip() or "heap"

    if fringe not in ['heap', 'list']:
        print("Invalid fringe type. Using 'heap'.")
        fringe = 'heap'

    # run algorithm and time it
    print(f"\nRunning Dijkstra from '{start}' with {fringe}...")

    import time
    start_time = time.time()
    distances, previous, history = dijkstra(graph, start, fringe)
    elapsed = (time.time() - start_time) * 1000

    # print results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Execution Time: {elapsed:.2f} ms")
    print(f"Algorithm Steps: {len(history) - 1}")
    print("\nShortest Distances from " + start + ":")
    print("-" * 60)

    for vertex in sorted(distances.keys()):
        dist = distances[vertex]
        if dist == float('inf'):
            print(f"  {vertex:5} : ∞ (unreachable)")
        else:
            print(f"  {vertex:5} : {dist:.1f}")

    print("=" * 60)

    # ask if user wants animation
    gen = input("\nGenerate animation? (y/n): ").strip().lower()
    if gen == 'y':
        os.makedirs('animations', exist_ok=True)
        filename = f'animations/dijkstra_{start}_{fringe}_demo.gif'
        print(f"Generating animation: {filename}")
        create_dijkstra_animation(graph, history, filename, duration=600)
        print(f"✓ Animation saved!")

        if open_image(filename):
            print("✓ Animation opened in viewer")


def run_prim_interactive(graph):
    # Run Prim's MST with user input
    print("\n" + "-" * 60)
    print("PRIM'S MINIMUM SPANNING TREE ALGORITHM")
    print("-" * 60)

    if graph.num_vertices() == 0:
        print("Error: Graph is empty. Load a graph first.")
        return

    if graph.directed:
        print("Error: Prim's algorithm requires an undirected graph.")
        return

    # get start vertex
    print(f"Available vertices: {sorted(graph.get_vertices())}")
    start = input("Enter start vertex: ").strip()

    if not graph.has_vertex(start):
        print(f"Error: Vertex '{start}' not in graph.")
        return

    # get fringe type
    print("\nFringe types: heap, list")
    fringe = input("Enter fringe type (default: heap): ").strip() or "heap"

    if fringe not in ['heap', 'list']:
        print("Invalid fringe type. Using 'heap'.")
        fringe = 'heap'

    # run and time the algorithm
    print(f"\nRunning Prim from '{start}' with {fringe}...")

    import time
    start_time = time.time()
    mst_edges, total_weight, history = prim(graph, start, fringe)
    elapsed = (time.time() - start_time) * 1000

    # show results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Execution Time: {elapsed:.2f} ms")
    print(f"Algorithm Steps: {len(history) - 1}")
    print(f"Total MST Weight: {total_weight:.1f}")
    print("\nMST Edges:")
    print("-" * 60)

    for u, v, w in mst_edges:
        print(f"  {u} -- {v}  (weight: {w:.1f})")

    print("=" * 60)

    # optional animation
    gen = input("\nGenerate animation? (y/n): ").strip().lower()
    if gen == 'y':
        os.makedirs('animations', exist_ok=True)
        filename = f'animations/prim_{start}_{fringe}_demo.gif'
        print(f"Generating animation: {filename}")
        create_prim_animation(graph, history, filename, duration=600)
        print(f"✓ Animation saved!")

        if open_image(filename):
            print("✓ Animation opened in viewer")


def compare_performance(graph):
    # compare heap vs list performance for both algorithms
    print("\n" + "-" * 60)
    print("PERFORMANCE COMPARISON: Heap vs List")
    print("-" * 60)

    if graph.num_vertices() == 0:
        print("Error: Graph is empty. Load a graph first.")
        return

    vertices = list(graph.get_vertices())
    start = vertices[0]

    print(f"Running both algorithms from vertex '{start}'...")
    print("Testing with both heap and list...\n")

    import time

    # Dijkstra with both fringe types
    start_time = time.time()
    dijkstra(graph, start, 'heap')
    dijk_heap_time = (time.time() - start_time) * 1000

    start_time = time.time()
    dijkstra(graph, start, 'list')
    dijk_list_time = (time.time() - start_time) * 1000

    # Prim with both fringe types
    start_time = time.time()
    prim(graph, start, 'heap')
    prim_heap_time = (time.time() - start_time) * 1000

    start_time = time.time()
    prim(graph, start, 'list')
    prim_list_time = (time.time() - start_time) * 1000

    # print comparison
    print("=" * 60)
    print("PERFORMANCE RESULTS")
    print("=" * 60)
    print(f"Graph: {graph.num_vertices()} vertices, {graph.num_edges()} edges\n")

    print("Dijkstra's Algorithm:")
    print(f"  Heap: {dijk_heap_time:.3f} ms")
    print(f"  List: {dijk_list_time:.3f} ms")
    if dijk_heap_time > 0:
        speedup = dijk_list_time / dijk_heap_time
        print(f"  Speedup: {speedup:.2f}x")

    print("\nPrim's Algorithm:")
    print(f"  Heap: {prim_heap_time:.3f} ms")
    print(f"  List: {prim_list_time:.3f} ms")
    if prim_heap_time > 0:
        speedup = prim_list_time / prim_heap_time
        print(f"  Speedup: {speedup:.2f}x")

    print("=" * 60)


def main():
    # main loop
    graph = Graph(directed=False)

    print("\n" + "=" * 60)
    print("Welcome to Graph Algorithms Interactive Demo!")
    print("=" * 60)
    print("\nThis demo uses matplotlib to generate visualizations.")
    print("Images and animations will be saved to the current directory.")

    while True:
        print_menu()
        choice = input("\nEnter choice: ").strip()

        if choice == '0':
            print("\nGoodbye!")
            break

        elif choice == '1':
            graph = create_sample_graph()
            print("\n✓ Sample graph loaded (5 vertices, 7 edges)")
            show_graph_summary(graph)

        elif choice == '2':
            print("\n" + "-" * 60)
            print("ADD EDGE")
            print("-" * 60)
            node1 = input("Node 1: ").strip()
            node2 = input("Node 2: ").strip()
            try:
                weight = float(input("Weight: ").strip())
                if weight < 0:
                    print("Error: Weight must be non-negative.")
                else:
                    graph.add_edge(node1, node2, weight)
                    print(f"✓ Added edge: {node1} -- {node2} (weight: {weight})")
            except ValueError:
                print("Error: Weight must be a number.")

        elif choice == '3':
            show_graph_summary(graph)

        elif choice == '4':
            print("\nGenerating graph visualization...")
            filename = visualize_graph(graph)
            print(f"✓ Graph saved to: {filename}")
            if open_image(filename):
                print("✓ Image opened in viewer")
            else:
                print(f"  Please open '{filename}' manually")

        elif choice == '5':
            run_dijkstra_interactive(graph)

        elif choice == '6':
            run_prim_interactive(graph)

        elif choice == '7':
            compare_performance(graph)

        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
