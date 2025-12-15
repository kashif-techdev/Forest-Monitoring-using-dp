"""
Run benchmark suite and measure CPU time.
"""

import os
import subprocess
import sys
import time
import json
from collections import defaultdict


def run_benchmark_instance(input_file: str, output_file: str) -> float:
    """
    Run a single benchmark instance and measure CPU time.
    
    Args:
        input_file: Path to input graph file
        output_file: Path to output file
        
    Returns:
        CPU time in seconds
    """
    start_time = time.perf_counter()
    
    try:
        result = subprocess.run(
            [sys.executable, "main.py", input_file, output_file],
            cwd=".",
            capture_output=True,
            text=True
        )
        
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        
        if result.returncode == 0:
            return elapsed
        else:
            print(f"Error running {input_file}: {result.stderr}")
            return -1
    except Exception as e:
        print(f"Exception running {input_file}: {e}")
        return -1


def run_benchmark_suite():
    """
    Run all benchmark instances and collect timing data.
    """
    base_dir = "benchmarks"
    
    if not os.path.exists(base_dir):
        print(f"Error: {base_dir} directory not found")
        return
    
    # Collect timing data by size
    timing_data = defaultdict(list)
    
    # Iterate over size directories
    for size_dir in sorted(os.listdir(base_dir)):
        size_path = os.path.join(base_dir, size_dir)
        if not os.path.isdir(size_path):
            continue
        
        # Extract size number
        try:
            n = int(size_dir.split("_")[1])
        except:
            continue
        
        print(f"Running benchmarks for size {n}...")
        
        # Run all instances for this size
        instance_files = sorted([f for f in os.listdir(size_path) if f.startswith("instance_")])
        
        for instance_file in instance_files:
            input_file = os.path.join(size_path, instance_file)
            output_file = os.path.join(size_path, instance_file.replace("instance_", "output_"))
            
            elapsed = run_benchmark_instance(input_file, output_file)
            if elapsed >= 0:
                timing_data[n].append(elapsed)
                print(f"  {instance_file}: {elapsed:.4f}s")
    
    # Calculate averages
    results = {}
    for n in sorted(timing_data.keys()):
        times = timing_data[n]
        avg_time = sum(times) / len(times) if times else 0
        results[n] = {
            "average": avg_time,
            "min": min(times) if times else 0,
            "max": max(times) if times else 0,
            "count": len(times)
        }
        print(f"Size {n}: avg={avg_time:.4f}s, min={min(times):.4f}s, max={max(times):.4f}s, count={len(times)}")
    
    # Save results to JSON
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to benchmark_results.json")
    return results


if __name__ == "__main__":
    run_benchmark_suite()

