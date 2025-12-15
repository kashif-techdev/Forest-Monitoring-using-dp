"""
Run all functional test cases and generate output files.
"""

import os
import subprocess
import sys


def run_test(test_id: int):
    """
    Run a single test case.
    
    Args:
        test_id: Test case number
    """
    input_file = f"tests/instance_{test_id:02d}.txt"
    output_file = f"tests/output_{test_id:02d}.txt"
    
    if not os.path.exists(input_file):
        print(f"Warning: {input_file} not found")
        return False
    
    try:
        # Run the main algorithm
        result = subprocess.run(
            [sys.executable, "main.py", input_file, output_file],
            cwd=".",
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"Test {test_id:02d}: PASSED")
            return True
        else:
            print(f"Test {test_id:02d}: FAILED - {result.stderr}")
            return False
    except Exception as e:
        print(f"Test {test_id:02d}: ERROR - {e}")
        return False


def main():
    """Run all test cases."""
    # Find all test instances
    test_files = [f for f in os.listdir("tests") if f.startswith("instance_")]
    test_ids = sorted([int(f.split("_")[1].split(".")[0]) for f in test_files])
    
    passed = 0
    failed = 0
    
    for test_id in test_ids:
        if run_test(test_id):
            passed += 1
        else:
            failed += 1
    
    print(f"\nSummary: {passed} passed, {failed} failed")


if __name__ == "__main__":
    main()

