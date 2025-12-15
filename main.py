"""
CS301 Assignment 5: Forest Monitoring Problem
Minimum Vertex Cover using Dynamic Programming over Subsets

This module implements an exact DP algorithm for finding the minimum vertex cover
of a graph, where vertices represent candidate designated points (cdps) and
edges represent shared regions that need to be monitored.
"""

from typing import Set, Tuple, List, Dict
import sys


def has_edges(graph: Dict[int, Set[int]], vertex_set: Set[int]) -> bool:
    """
    Check if the induced subgraph on vertex_set has any edges.
    
    Args:
        graph: Adjacency list representation of the graph
        vertex_set: Set of vertices to check
        
    Returns:
        True if there exists at least one edge (u,v) where both u and v are in vertex_set
    """
    for u in vertex_set:
        if u in graph:
            for v in graph[u]:
                if v in vertex_set and u < v:  # u < v to avoid counting edges twice
                    return True
    return False


def find_any_edge(graph: Dict[int, Set[int]], vertex_set: Set[int]) -> Tuple[int, int]:
    """
    Find any edge (u, v) in the induced subgraph on vertex_set.
    
    Args:
        graph: Adjacency list representation of the graph
        vertex_set: Set of vertices
        
    Returns:
        A tuple (u, v) representing an edge where both u and v are in vertex_set
    """
    for u in vertex_set:
        if u in graph:
            for v in graph[u]:
                if v in vertex_set and u < v:
                    return (u, v)
    raise ValueError("No edge found in vertex_set")


def minimum_vertex_cover_dp(graph: Dict[int, Set[int]], vertices: List[int]) -> Tuple[int, Set[int]]:
    """
    Compute minimum vertex cover using dynamic programming over subsets.
    
    DP[S] = minimum vertex cover size of the induced subgraph on subset S.
    
    Recurrence:
    - If S has no edges: DP[S] = 0
    - Otherwise, choose any edge (u, v) in S:
      DP[S] = 1 + min(DP[S \\ {u}], DP[S \\ {v}])
    
    Args:
        graph: Adjacency list representation of the graph
        vertices: List of all vertices in the graph
        
    Returns:
        A tuple (min_cover_size, min_cover_set) where min_cover_set is the
        actual minimum vertex cover
    """
    n = len(vertices)
    vertex_to_index = {v: i for i, v in enumerate(vertices)}
    
    # DP table: dp[mask] = (min_cover_size, parent_mask, removed_vertex)
    # mask is a bitmask representing a subset of vertices
    dp: Dict[int, Tuple[int, int, int]] = {}
    
    # Base case: empty set has cover size 0
    dp[0] = (0, -1, -1)
    
    # Iterate over all subsets in increasing order of size
    for mask in range(1, 1 << n):
        # Convert mask to vertex set
        vertex_set = {vertices[i] for i in range(n) if (mask >> i) & 1}
        
        # Check if induced subgraph has edges
        if not has_edges(graph, vertex_set):
            # No edges: cover size is 0
            dp[mask] = (0, -1, -1)
        else:
            # Find any edge (u, v) in the induced subgraph
            u, v = find_any_edge(graph, vertex_set)
            u_idx = vertex_to_index[u]
            v_idx = vertex_to_index[v]
            
            # Try removing u
            mask_without_u = mask & ~(1 << u_idx)
            size_without_u = dp[mask_without_u][0]
            
            # Try removing v
            mask_without_v = mask & ~(1 << v_idx)
            size_without_v = dp[mask_without_v][0]
            
            # Choose the better option
            if size_without_u <= size_without_v:
                dp[mask] = (1 + size_without_u, mask_without_u, u)
            else:
                dp[mask] = (1 + size_without_v, mask_without_v, v)
    
    # Reconstruct the minimum vertex cover
    full_mask = (1 << n) - 1
    min_size = dp[full_mask][0]
    
    # Backtrack to find the actual cover
    cover_set = set()
    current_mask = full_mask
    while current_mask != 0 and dp[current_mask][1] != -1:
        _, parent_mask, removed_vertex = dp[current_mask]
        if removed_vertex != -1:
            cover_set.add(removed_vertex)
        current_mask = parent_mask
    
    return (min_size, cover_set)


def load_graph(filename: str) -> Tuple[Dict[int, Set[int]], List[int]]:
    """
    Load graph from file.
    
    File format:
    First line: number of vertices n
    Next lines: edges as "u v" (one per line)
    
    Args:
        filename: Path to the input file
        
    Returns:
        A tuple (graph, vertices) where graph is an adjacency list and
        vertices is a list of all vertex labels
    """
    graph: Dict[int, Set[int]] = {}
    vertices_set = set()
    
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        if not lines:
            return (graph, [])
        
        # First line: number of vertices (optional, we'll infer from edges)
        n = int(lines[0]) if lines[0].isdigit() else None
        
        # If n is specified, initialize vertices 0 to n-1
        if n is not None:
            vertices_set = set(range(n))
            start_idx = 1
        else:
            vertices_set = set()
            start_idx = 0
        
        # Read edges
        for line in lines[start_idx:]:
            parts = line.split()
            if len(parts) >= 2:
                u = int(parts[0])
                v = int(parts[1])
                vertices_set.add(u)
                vertices_set.add(v)
                
                if u not in graph:
                    graph[u] = set()
                if v not in graph:
                    graph[v] = set()
                
                graph[u].add(v)
                graph[v].add(u)
    
    vertices = sorted(list(vertices_set))
    return (graph, vertices)


def save_output(filename: str, min_size: int, cover_set: Set[int]):
    """
    Save the output to a file.
    
    File format:
    First line: minimum cover size
    Next lines: vertices in the cover (one per line, sorted)
    
    Args:
        filename: Path to the output file
        min_size: Minimum vertex cover size
        cover_set: Set of vertices in the minimum cover
    """
    with open(filename, 'w') as f:
        f.write(f"{min_size}\n")
        for vertex in sorted(cover_set):
            f.write(f"{vertex}\n")


def main():
    """
    Main function: reads graph from file, computes minimum vertex cover,
    and writes results to output file.
    """
    if len(sys.argv) < 3:
        print("Usage: python main.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Load graph
    graph, vertices = load_graph(input_file)
    
    if not vertices:
        print("Error: No vertices in graph")
        sys.exit(1)
    
    # Compute minimum vertex cover
    min_size, cover_set = minimum_vertex_cover_dp(graph, vertices)
    
    # Save output
    save_output(output_file, min_size, cover_set)
    
    # Print summary
    print(f"Minimum vertex cover size: {min_size}")
    print(f"Vertices in cover: {sorted(cover_set)}")


if __name__ == "__main__":
    main()

