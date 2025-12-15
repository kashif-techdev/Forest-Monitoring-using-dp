"""
Generate functional test cases for white-box and black-box testing.
"""

from utils import graph_to_file, generate_random_graph, generate_connected_graph
import os


def create_test_case(test_id: int, graph: dict, vertices: list, description: str):
    """
    Create a test case with input and expected output files.
    
    Args:
        test_id: Test case number
        graph: Graph adjacency list
        vertices: List of vertices
        description: Description of the test case
    """
    test_dir = "tests"
    os.makedirs(test_dir, exist_ok=True)
    
    input_file = f"{test_dir}/instance_{test_id:02d}.txt"
    graph_to_file(graph, vertices, input_file)
    
    # Write description
    desc_file = f"{test_dir}/description_{test_id:02d}.txt"
    with open(desc_file, 'w') as f:
        f.write(f"Test Case {test_id}: {description}\n")


def main():
    """Generate all functional test cases."""
    
    # Test 1: Empty graph (no edges)
    graph1 = {0: set(), 1: set(), 2: set()}
    vertices1 = [0, 1, 2]
    create_test_case(1, graph1, vertices1, "Empty graph - no edges, all isolated vertices")
    
    # Test 2: Single edge
    graph2 = {0: {1}, 1: {0}}
    vertices2 = [0, 1]
    create_test_case(2, graph2, vertices2, "Single edge - minimum cover is 1")
    
    # Test 3: Path graph (P3)
    graph3 = {0: {1}, 1: {0, 2}, 2: {1}}
    vertices3 = [0, 1, 2]
    create_test_case(3, graph3, vertices3, "Path graph P3 - linear structure")
    
    # Test 4: Triangle (K3)
    graph4 = {0: {1, 2}, 1: {0, 2}, 2: {0, 1}}
    vertices4 = [0, 1, 2]
    create_test_case(4, graph4, vertices4, "Triangle K3 - complete graph on 3 vertices")
    
    # Test 5: Star graph (K1,3)
    graph5 = {0: {1, 2, 3}, 1: {0}, 2: {0}, 3: {0}}
    vertices5 = [0, 1, 2, 3]
    create_test_case(5, graph5, vertices5, "Star graph - center vertex covers all edges")
    
    # Test 6: Cycle C4
    graph6 = {0: {1, 3}, 1: {0, 2}, 2: {1, 3}, 3: {0, 2}}
    vertices6 = [0, 1, 2, 3]
    create_test_case(6, graph6, vertices6, "Cycle C4 - even cycle")
    
    # Test 7: Complete graph K4
    graph7 = {0: {1, 2, 3}, 1: {0, 2, 3}, 2: {0, 1, 3}, 3: {0, 1, 2}}
    vertices7 = [0, 1, 2, 3]
    create_test_case(7, graph7, vertices7, "Complete graph K4 - all vertices connected")
    
    # Test 8: Disconnected components
    graph8 = {0: {1}, 1: {0}, 2: {3}, 3: {2}}
    vertices8 = [0, 1, 2, 3]
    create_test_case(8, graph8, vertices8, "Disconnected graph - two separate edges")
    
    # Test 9: Graph with 5 vertices (for Task 3 example)
    graph9 = {0: {1, 2}, 1: {0, 2, 3}, 2: {0, 1, 4}, 3: {1, 4}, 4: {2, 3}}
    vertices9 = [0, 1, 2, 3, 4]
    create_test_case(9, graph9, vertices9, "5-vertex graph - example for Task 3")
    
    print(f"Generated {9} test cases in tests/ directory")


if __name__ == "__main__":
    main()

