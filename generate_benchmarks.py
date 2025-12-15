"""
Generate benchmark instances for performance evaluation.
"""

from utils import graph_to_file, generate_random_graph, generate_connected_graph
import os
import random


def generate_benchmark_suite():
    """
    Generate at least 200 benchmark instances across at least 20 different sizes,
    with at least 10 instances per size.
    """
    base_dir = "benchmarks"
    os.makedirs(base_dir, exist_ok=True)
    
    # Define size ranges: from small (n=5) to large (n=20+)
    # We'll generate instances for sizes: 5, 6, 7, ..., 24 (20 sizes)
    sizes = list(range(5, 25))  # 20 different sizes
    
    total_instances = 0
    
    for n in sizes:
        size_dir = os.path.join(base_dir, f"size_{n}")
        os.makedirs(size_dir, exist_ok=True)
        
        # Generate at least 10 instances per size
        instances_per_size = 10
        
        for i in range(instances_per_size):
            # Vary edge density for diversity
            if i < 3:
                # Sparse graphs
                edge_prob = 0.2
            elif i < 6:
                # Medium density
                edge_prob = 0.4
            else:
                # Denser graphs
                edge_prob = 0.6
            
            # Generate graph
            graph, vertices = generate_random_graph(n, edge_prob, seed=n * 100 + i)
            
            # Write to file
            instance_file = os.path.join(size_dir, f"instance_{i+1:02d}.txt")
            graph_to_file(graph, vertices, instance_file)
            
            total_instances += 1
    
    print(f"Generated {total_instances} benchmark instances across {len(sizes)} sizes")
    print(f"Size range: {min(sizes)} to {max(sizes)} vertices")
    return total_instances


if __name__ == "__main__":
    generate_benchmark_suite()

