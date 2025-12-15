"""
Generate runtime plot from benchmark results.
"""

import json
import matplotlib.pyplot as plt
import numpy as np


def plot_runtime():
    """
    Load benchmark results and create a plot of CPU time vs input size.
    """
    # Load results
    with open("benchmark_results.json", "r") as f:
        results = json.load(f)
    
    # Extract data
    sizes = sorted([int(k) for k in results.keys()])
    avg_times = [results[str(n)]["average"] for n in sizes]
    min_times = [results[str(n)]["min"] for n in sizes]
    max_times = [results[str(n)]["max"] for n in sizes]
    
    # Create plot
    plt.figure(figsize=(10, 6))
    
    # Plot average times
    plt.plot(sizes, avg_times, 'b-o', label='Average CPU Time', linewidth=2, markersize=6)
    
    # Plot error bars (min-max range)
    plt.fill_between(sizes, min_times, max_times, alpha=0.2, color='blue', label='Min-Max Range')
    
    # Plot theoretical O(2^n) curve (scaled to fit)
    # Scale factor to match the data
    if avg_times:
        scale_factor = avg_times[-1] / (2 ** sizes[-1])
        theoretical = [scale_factor * (2 ** n) for n in sizes]
        plt.plot(sizes, theoretical, 'r--', label='Theoretical O(2^n) (scaled)', linewidth=2)
    
    plt.xlabel('Input Size (Number of Vertices)', fontsize=12)
    plt.ylabel('CPU Time (seconds)', fontsize=12)
    plt.title('Empirical Runtime Analysis: Minimum Vertex Cover DP Algorithm', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Use log scale for better visualization
    plt.tight_layout()
    
    # Save plot
    plt.savefig('plot_runtime.png', dpi=300, bbox_inches='tight')
    print("Plot saved to plot_runtime.png")
    
    # Also save as PDF for report
    plt.savefig('plot_runtime.pdf', bbox_inches='tight')
    print("Plot saved to plot_runtime.pdf")


if __name__ == "__main__":
    try:
        plot_runtime()
    except ImportError:
        print("matplotlib not available. Install with: pip install matplotlib")
    except FileNotFoundError:
        print("benchmark_results.json not found. Run run_benchmarks.py first.")

