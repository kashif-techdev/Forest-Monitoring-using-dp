"""
Utility functions for graph generation and testing.
"""

from typing import Dict, Set, List, Tuple
import random


def generate_random_graph(n: int, edge_probability: float = 0.3, seed: int = None) -> Tuple[Dict[int, Set[int]], List[int]]:
    """
    Generate a random graph with n vertices.
    
    Args:
        n: Number of vertices (labeled 0 to n-1)
        edge_probability: Probability of including each edge
        seed: Random seed for reproducibility
        
    Returns:
        A tuple (graph, vertices) where graph is an adjacency list
    """
    if seed is not None:
        random.seed(seed)
    
    graph: Dict[int, Set[int]] = {i: set() for i in range(n)}
    vertices = list(range(n))
    
    # Generate edges
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < edge_probability:
                graph[u].add(v)
                graph[v].add(u)
    
    return (graph, vertices)


def generate_connected_graph(n: int, m: int, seed: int = None) -> Tuple[Dict[int, Set[int]], List[int]]:
    """
    Generate a connected graph with n vertices and approximately m edges.
    
    Args:
        n: Number of vertices
        m: Target number of edges
        seed: Random seed for reproducibility
        
    Returns:
        A tuple (graph, vertices) where graph is an adjacency list
    """
    if seed is not None:
        random.seed(seed)
    
    graph: Dict[int, Set[int]] = {i: set() for i in range(n)}
    vertices = list(range(n))
    
    # First, ensure connectivity: create a spanning tree
    for i in range(1, n):
        parent = random.randint(0, i - 1)
        graph[parent].add(i)
        graph[i].add(parent)
    
    # Add remaining edges randomly
    edges_added = n - 1
    max_edges = n * (n - 1) // 2
    target_edges = min(m, max_edges)
    
    while edges_added < target_edges:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and v not in graph[u]:
            graph[u].add(v)
            graph[v].add(u)
            edges_added += 1
    
    return (graph, vertices)


def graph_to_file(graph: Dict[int, Set[int]], vertices: List[int], filename: str):
    """
    Write graph to file in the expected format.
    
    Args:
        graph: Adjacency list representation
        vertices: List of all vertices
        filename: Output file path
    """
    with open(filename, 'w') as f:
        f.write(f"{len(vertices)}\n")
        edges_written = set()
        for u in vertices:
            if u in graph:
                for v in graph[u]:
                    if u < v:  # Write each edge only once
                        f.write(f"{u} {v}\n")
                        edges_written.add((u, v))


def count_edges(graph: Dict[int, Set[int]]) -> int:
    """
    Count the number of edges in the graph.
    
    Args:
        graph: Adjacency list representation
        
    Returns:
        Number of edges
    """
    edge_count = 0
    for u in graph:
        for v in graph[u]:
            if u < v:
                edge_count += 1
    return edge_count

