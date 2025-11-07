"""
Graph visualization and animation generation.
Creates step-by-step animations of Dijkstra's and Prim's algorithms.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from PIL import Image
from typing import Dict, List, Set, Tuple, Optional, Any
import os
from src.graph import Graph


def draw_graph(
    graph: Graph,
    pos: Optional[Dict[str, Tuple[float, float]]] = None,
    ax: Optional[plt.Axes] = None,
    title: str = "Graph",
    highlighted_nodes: Optional[Set[str]] = None,
    highlighted_edges: Optional[List[Tuple[str, str]]] = None,
    node_labels: Optional[Dict[str, str]] = None,
    current_node: Optional[str] = None
) -> Tuple[plt.Figure, plt.Axes, Dict[str, Tuple[float, float]]]:
    """
    Draw a static graph.
    Returns (figure, axes, node_positions) for reuse.
    """
    # Create figure if needed
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    else:
        fig = ax.figure

    # Convert to NetworkX graph for layout
    G = nx.Graph() if not graph.directed else nx.DiGraph()

    for vertex in graph.get_vertices():
        G.add_node(vertex)

    for u, v, weight in graph.get_edges():
        G.add_edge(u, v, weight=weight)

    # Generate layout if not provided
    if pos is None:
        if len(G.nodes) > 0:
            pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        else:
            pos = {}

    # Define colors
    default_node_color = '#D3D3D3'  # Light gray
    visited_node_color = '#87CEEB'   # Sky blue
    current_node_color = '#FF6B6B'   # Red
    edge_color = '#999999'           # Gray
    highlighted_edge_color = '#4CAF50'  # Green

    # Determine node colors
    node_colors = []
    for node in G.nodes():
        if current_node and node == current_node:
            node_colors.append(current_node_color)
        elif highlighted_nodes and node in highlighted_nodes:
            node_colors.append(visited_node_color)
        else:
            node_colors.append(default_node_color)

    # Draw all edges first (non-highlighted)
    edge_list = []
    edge_weights = []
    for u, v, data in G.edges(data=True):
        is_highlighted = False
        if highlighted_edges:
            for edge_u, edge_v in highlighted_edges:
                if (u == edge_u and v == edge_v) or (u == edge_v and v == edge_u):
                    is_highlighted = True
                    break

        if not is_highlighted:
            edge_list.append((u, v))
            edge_weights.append(data['weight'])

    if edge_list:
        nx.draw_networkx_edges(
            G, pos, edgelist=edge_list,
            edge_color=edge_color, width=1.5, ax=ax, alpha=0.6
        )

    # Draw highlighted edges (MST or shortest path)
    if highlighted_edges:
        highlighted_edge_list = []
        for edge_u, edge_v in highlighted_edges:
            if G.has_edge(edge_u, edge_v):
                highlighted_edge_list.append((edge_u, edge_v))

        if highlighted_edge_list:
            nx.draw_networkx_edges(
                G, pos, edgelist=highlighted_edge_list,
                edge_color=highlighted_edge_color, width=3.0, ax=ax
            )

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos, node_color=node_colors,
        node_size=700, ax=ax, edgecolors='black', linewidths=2
    )

    # Draw node labels with distances/keys if provided
    if node_labels:
        labels = node_labels
    else:
        labels = {node: node for node in G.nodes()}

    nx.draw_networkx_labels(
        G, pos, labels, font_size=10, font_weight='bold', ax=ax
    )

    # Draw edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    # Format weights to 1 decimal place
    edge_labels = {k: f'{v:.1f}' for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels, font_size=8, ax=ax
    )

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.axis('off')

    # Add legend
    legend_elements = [
        mpatches.Patch(color=default_node_color, label='Unvisited'),
        mpatches.Patch(color=visited_node_color, label='Visited'),
        mpatches.Patch(color=current_node_color, label='Current'),
        mpatches.Patch(color=highlighted_edge_color, label='Selected Edge')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9)

    return fig, ax, pos


def draw_dijkstra_step(
    graph: Graph,
    step: Dict[str, Any],
    pos: Dict[str, Tuple[float, float]],
    ax: Optional[plt.Axes] = None
) -> Tuple[plt.Figure, plt.Axes]:
    """Draw a single step of Dijkstra's algorithm."""
    iteration = step['iteration']
    current = step.get('current')
    visited = step.get('visited', set())
    distances = step.get('distances', {})
    previous = step.get('previous', {})

    # Build highlighted edges (shortest path tree so far)
    highlighted_edges = []
    if previous:
        for node, pred in previous.items():
            if pred is not None and node in visited:
                highlighted_edges.append((pred, node))

    # Create node labels with distances
    node_labels = {}
    for node in graph.get_vertices():
        dist = distances.get(node, float('inf'))
        if dist == float('inf'):
            node_labels[node] = f"{node}\n∞"
        else:
            node_labels[node] = f"{node}\n{dist:.1f}"

    # Title
    if current:
        title = f"Dijkstra's Algorithm - Step {iteration}\nProcessing: {current}"
    else:
        title = f"Dijkstra's Algorithm - Initial State"

    return draw_graph(
        graph, pos, ax, title,
        highlighted_nodes=visited,
        highlighted_edges=highlighted_edges,
        node_labels=node_labels,
        current_node=current
    )


def draw_prim_step(
    graph: Graph,
    step: Dict[str, Any],
    pos: Dict[str, Tuple[float, float]],
    ax: Optional[plt.Axes] = None
) -> Tuple[plt.Figure, plt.Axes]:
    """Draw a single step of Prim's algorithm."""
    iteration = step['iteration']
    current = step.get('current')
    visited = step.get('visited', set())
    mst_edges = step.get('mst_edges', [])
    keys = step.get('keys', {})

    # Build highlighted edges (MST edges)
    highlighted_edges = [(u, v) for u, v, w in mst_edges]

    # Create node labels with keys
    node_labels = {}
    for node in graph.get_vertices():
        key = keys.get(node, float('inf'))
        if key == float('inf'):
            node_labels[node] = f"{node}\n∞"
        else:
            node_labels[node] = f"{node}\n{key:.1f}"

    # Calculate MST weight so far
    mst_weight = sum(w for _, _, w in mst_edges)

    # Title
    if current:
        title = f"Prim's Algorithm - Step {iteration}\nProcessing: {current} | MST Weight: {mst_weight:.1f}"
    else:
        title = f"Prim's Algorithm - Initial State"

    return draw_graph(
        graph, pos, ax, title,
        highlighted_nodes=visited,
        highlighted_edges=highlighted_edges,
        node_labels=node_labels,
        current_node=current
    )


def create_dijkstra_animation(
    graph: Graph,
    step_history: List[Dict[str, Any]],
    output_path: str,
    duration: int = 800
) -> None:
    """
    Create animated GIF of Dijkstra's algorithm execution.
    Duration in milliseconds per frame.
    """
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate consistent layout
    G = nx.Graph()
    for v in graph.get_vertices():
        G.add_node(v)
    for u, v, w in graph.get_edges():
        G.add_edge(u, v)
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    frames = []
    temp_files = []

    try:
        # Create frame for each step
        for i, step in enumerate(step_history):
            fig, ax = plt.subplots(figsize=(10, 8))
            draw_dijkstra_step(graph, step, pos, ax)

            # Save frame
            temp_file = f"/tmp/dijkstra_frame_{i}.png"
            plt.savefig(temp_file, dpi=100, bbox_inches='tight')
            plt.close(fig)

            frames.append(Image.open(temp_file))
            temp_files.append(temp_file)

        # Create GIF
        if frames:
            # First and last frame display longer
            durations = [duration * 2] + [duration] * (len(frames) - 2) + [duration * 3]
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0
            )
            print(f"Animation saved to: {output_path}")

    finally:
        # Cleanup temp files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)


def create_prim_animation(
    graph: Graph,
    step_history: List[Dict[str, Any]],
    output_path: str,
    duration: int = 800
) -> None:
    """
    Create animated GIF of Prim's algorithm execution.
    Duration in milliseconds per frame.
    """
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate consistent layout
    G = nx.Graph()
    for v in graph.get_vertices():
        G.add_node(v)
    for u, v, w in graph.get_edges():
        G.add_edge(u, v)
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    frames = []
    temp_files = []

    try:
        # Create frame for each step
        for i, step in enumerate(step_history):
            fig, ax = plt.subplots(figsize=(10, 8))
            draw_prim_step(graph, step, pos, ax)

            # Save frame
            temp_file = f"/tmp/prim_frame_{i}.png"
            plt.savefig(temp_file, dpi=100, bbox_inches='tight')
            plt.close(fig)

            frames.append(Image.open(temp_file))
            temp_files.append(temp_file)

        # Create GIF
        if frames:
            # First and last frame display longer
            durations = [duration * 2] + [duration] * (len(frames) - 2) + [duration * 3]
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0
            )
            print(f"Animation saved to: {output_path}")

    finally:
        # Cleanup temp files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
