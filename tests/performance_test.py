"""
Performance benchmarking for Dijkstra and Prim algorithms.
Compares BinaryHeap vs SortedLinkedList fringe implementations.
"""

import time
import random
import csv
import os
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt

from src.graph import Graph
from src.algorithms import dijkstra, prim


def generate_random_graph(num_vertices: int, edge_probability: float = 0.3) -> Graph:
    """
    Generate a random connected graph.
    edge_probability: chance of creating an edge between any two vertices
    """
    graph = Graph(directed=False)

    # Create vertices
    vertices = [chr(65 + i) if i < 26 else f"V{i}" for i in range(num_vertices)]

    # Add random edges
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.random() < edge_probability:
                weight = random.uniform(1.0, 10.0)
                graph.add_edge(vertices[i], vertices[j], weight)

    # Ensure connectivity by creating a spanning tree first
    if num_vertices > 1:
        for i in range(1, num_vertices):
            # Connect each vertex to a random previous vertex
            j = random.randint(0, i - 1)
            weight = random.uniform(1.0, 10.0)
            if not graph.has_edge(vertices[i], vertices[j]):
                graph.add_edge(vertices[i], vertices[j], weight)

    return graph


def benchmark_algorithm(
    graph: Graph,
    algorithm: str,
    fringe_type: str,
    start_node: str,
    num_runs: int = 5
) -> Tuple[float, int]:
    """
    Benchmark an algorithm and return average time and number of steps.
    Returns (avg_time_ms, num_steps)
    """
    times = []

    for _ in range(num_runs):
        start_time = time.perf_counter()

        if algorithm == 'dijkstra':
            distances, previous, history = dijkstra(graph, start_node, fringe_type)
        else:  # prim
            mst_edges, total_weight, history = prim(graph, start_node, fringe_type)

        elapsed = (time.perf_counter() - start_time) * 1000  # Convert to ms
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    num_steps = len(history) - 1  # Subtract initial state

    return avg_time, num_steps


def run_benchmarks() -> List[Dict]:
    """
    Run comprehensive benchmarks and return results.
    """
    graph_sizes = [10, 20, 50, 100, 200, 500]
    algorithms = ['dijkstra', 'prim']
    fringe_types = ['heap', 'list']
    results = []

    print("Running performance benchmarks...")
    print("=" * 70)

    for size in graph_sizes:
        print(f"\nTesting graph size: {size} vertices")

        # Generate random graph
        graph = generate_random_graph(size, edge_probability=0.2)
        num_edges = graph.num_edges()
        start_node = list(graph.get_vertices())[0]

        print(f"  Edges: {num_edges}")

        for algorithm in algorithms:
            for fringe_type in fringe_types:
                print(f"  Running {algorithm} with {fringe_type}...", end=" ")

                try:
                    avg_time, num_steps = benchmark_algorithm(
                        graph, algorithm, fringe_type, start_node, num_runs=3
                    )

                    result = {
                        'vertices': size,
                        'edges': num_edges,
                        'algorithm': algorithm,
                        'fringe': fringe_type,
                        'time_ms': avg_time,
                        'steps': num_steps
                    }
                    results.append(result)

                    print(f"{avg_time:.2f} ms")

                except Exception as e:
                    print(f"ERROR: {e}")

    print("\n" + "=" * 70)
    print("Benchmarks complete!")

    return results


def save_results_csv(results: List[Dict], filename: str = 'results/performance_data.csv'):
    """Save benchmark results to CSV file."""
    os.makedirs('results', exist_ok=True)

    with open(filename, 'w', newline='') as f:
        fieldnames = ['vertices', 'edges', 'algorithm', 'fringe', 'time_ms', 'steps']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"\nResults saved to: {filename}")


def generate_comparison_charts(results: List[Dict]):
    """Generate performance comparison charts."""
    os.makedirs('results', exist_ok=True)

    # Separate results by algorithm
    dijkstra_results = [r for r in results if r['algorithm'] == 'dijkstra']
    prim_results = [r for r in results if r['algorithm'] == 'prim']

    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Performance Comparison: Binary Heap vs Sorted Linked List', fontsize=16, fontweight='bold')

    # 1. Dijkstra execution time
    dijkstra_heap = [(r['vertices'], r['time_ms']) for r in dijkstra_results if r['fringe'] == 'heap']
    dijkstra_list = [(r['vertices'], r['time_ms']) for r in dijkstra_results if r['fringe'] == 'list']

    ax1.plot([v for v, _ in dijkstra_heap], [t for _, t in dijkstra_heap],
             'o-', label='Binary Heap', linewidth=2, markersize=8)
    ax1.plot([v for v, _ in dijkstra_list], [t for _, t in dijkstra_list],
             's-', label='Sorted Linked List', linewidth=2, markersize=8)
    ax1.set_xlabel('Number of Vertices', fontsize=11)
    ax1.set_ylabel('Execution Time (ms)', fontsize=11)
    ax1.set_title("Dijkstra's Algorithm", fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Prim execution time
    prim_heap = [(r['vertices'], r['time_ms']) for r in prim_results if r['fringe'] == 'heap']
    prim_list = [(r['vertices'], r['time_ms']) for r in prim_results if r['fringe'] == 'list']

    ax2.plot([v for v, _ in prim_heap], [t for _, t in prim_heap],
             'o-', label='Binary Heap', linewidth=2, markersize=8)
    ax2.plot([v for v, _ in prim_list], [t for _, t in prim_list],
             's-', label='Sorted Linked List', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Vertices', fontsize=11)
    ax2.set_ylabel('Execution Time (ms)', fontsize=11)
    ax2.set_title("Prim's Algorithm", fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. Speedup comparison (Dijkstra)
    speedup_dijkstra = []
    for v in sorted(set(r['vertices'] for r in dijkstra_results)):
        heap_time = next((r['time_ms'] for r in dijkstra_results
                         if r['vertices'] == v and r['fringe'] == 'heap'), None)
        list_time = next((r['time_ms'] for r in dijkstra_results
                         if r['vertices'] == v and r['fringe'] == 'list'), None)
        if heap_time and list_time and heap_time > 0:
            speedup_dijkstra.append((v, list_time / heap_time))

    ax3.bar([v for v, _ in speedup_dijkstra], [s for _, s in speedup_dijkstra],
            color='steelblue', alpha=0.7)
    ax3.axhline(y=1, color='r', linestyle='--', label='No speedup')
    ax3.set_xlabel('Number of Vertices', fontsize=11)
    ax3.set_ylabel('Speedup Factor (List Time / Heap Time)', fontsize=11)
    ax3.set_title('Dijkstra Heap Advantage', fontsize=12, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')

    # 4. Speedup comparison (Prim)
    speedup_prim = []
    for v in sorted(set(r['vertices'] for r in prim_results)):
        heap_time = next((r['time_ms'] for r in prim_results
                         if r['vertices'] == v and r['fringe'] == 'heap'), None)
        list_time = next((r['time_ms'] for r in prim_results
                         if r['vertices'] == v and r['fringe'] == 'list'), None)
        if heap_time and list_time and heap_time > 0:
            speedup_prim.append((v, list_time / heap_time))

    ax4.bar([v for v, _ in speedup_prim], [s for _, s in speedup_prim],
            color='coral', alpha=0.7)
    ax4.axhline(y=1, color='r', linestyle='--', label='No speedup')
    ax4.set_xlabel('Number of Vertices', fontsize=11)
    ax4.set_ylabel('Speedup Factor (List Time / Heap Time)', fontsize=11)
    ax4.set_title('Prim Heap Advantage', fontsize=12, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('results/comparison_charts.png', dpi=150, bbox_inches='tight')
    print("Comparison charts saved to: results/comparison_charts.png")

    plt.close()


def print_summary(results: List[Dict]):
    """Print summary statistics."""
    print("\n" + "=" * 70)
    print("PERFORMANCE SUMMARY")
    print("=" * 70)

    for algorithm in ['dijkstra', 'prim']:
        print(f"\n{algorithm.upper()}'S ALGORITHM:")
        algo_results = [r for r in results if r['algorithm'] == algorithm]

        for size in sorted(set(r['vertices'] for r in algo_results)):
            heap_time = next((r['time_ms'] for r in algo_results
                            if r['vertices'] == size and r['fringe'] == 'heap'), None)
            list_time = next((r['time_ms'] for r in algo_results
                            if r['vertices'] == size and r['fringe'] == 'list'), None)

            if heap_time and list_time:
                speedup = list_time / heap_time if heap_time > 0 else 0
                print(f"  {size} vertices: Heap={heap_time:.2f}ms, List={list_time:.2f}ms, "
                      f"Speedup={speedup:.2f}x")


def main():
    """Main benchmark execution."""
    print("Graph Algorithm Performance Benchmark")
    print("Comparing Binary Heap vs Sorted Linked List\n")

    # Set random seed for reproducibility
    random.seed(42)

    # Run benchmarks
    results = run_benchmarks()

    # Save results
    save_results_csv(results)

    # Generate charts
    generate_comparison_charts(results)

    # Print summary
    print_summary(results)

    print("\n✓ Performance analysis complete!")


if __name__ == '__main__':
    main()
