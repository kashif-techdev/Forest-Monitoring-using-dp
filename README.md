# Forest-Monitoring-using-dp

Forest Monitoring — Minimum Vertex Cover on a forest using dynamic programming.

## Overview

This repository implements a linear-time dynamic programming solution for the Minimum Vertex Cover problem on trees (and forests). It also includes scripts to generate tests and benchmarks, run them, and plot runtime results.

## Contents

- `main.py` — solver for minimum vertex cover on a forest (tree DP).
- `utils.py` — helper functions for parsing and building graphs/trees.
- `generate_tests.py` — create correctness testcases.
- `run_tests.py` — run solver against testcases.
- `generate_benchmarks.py`, `run_benchmarks.py` — generate and execute benchmark instances.
- `plot_runtime.py` — plot benchmark results saved in `benchmark_results.json`.
- `benchmarks/` — directory for generated benchmark inputs.
- `tests/` — directory for test inputs (add expected outputs here).
- `benchmark_results.json`, `plot_runtime.png/.pdf` — example benchmark results and plot.

## Algorithm (brief)

For each tree in the forest, root arbitrarily and compute for each node u:
- `dp[u][1]` = size of min vertex cover for subtree if u is included
- `dp[u][0]` = size of min vertex cover for subtree if u is excluded

Recurrences:
```
dp[u][1] = 1 + sum(min(dp[v][0], dp[v][1])) for v children of u
dp[u][0] = sum(dp[v][1]) for v children of u
```
Answer for each tree is min(dp[root][0], dp[root][1]); total answer is sum over components.

## Quickstart
```
python main.py 
```

Run unit tests:
```
python run_tests.py
# or (if using pytest)
pytest -q
```

Run benchmarks:
```
python run_benchmarks.py --sizes 100 1000 5000 --repeats 5
python plot_runtime.py benchmark_results.json
```

# tests
5.	Functional Testing 
Test Instances 
We designed 9 test instances covering a wide range of graph structures and important edge cases. 
<img width="576" height="341" alt="image" src="https://github.com/user-attachments/assets/88f49e8b-f7c5-4eba-8925-894c2dca0d3e" />
Test Results Table 
<img width="576" height="352" alt="image" src="https://github.com/user-attachments/assets/dddc1281-1999-4472-a272-1297ae208918" />
Properties Tested:  
White-box: Base cases, recursion correctness, edge selection, subset enumeration  Black-box: Correctness on various graph structures, optimality, edge case handling 

# Benchmark Analysis 
Benchmark Suite Description 
We generated 200 benchmark instances across 20 different input sizes (n = 5 to 24), with 10 instances per size. The instances vary in edge density: 
•	Sparse graphs (20% edge probability) 
•	Medium density (40% edge probability) 
•	Dense graphs (60% edge probability) 
This ensures diversity in the benchmark suite, ranging from instances solvable in seconds (n ≤ 10) to instances requiring hours (n ≥ 20). 
Experimental Results 
The benchmark results show exponential growth in CPU time as input size increases, consistent with the O(2^n) theoretical complexity. 
Sample Results: 
•	Size 5: ~0.19s average 
•	Size 10: ~0.19s average 
•	Size 15: ~0.43s average 
•	Size 20: ~11.3s average 
•	Size 24: ~2622s average (43.7 minutes, with one outlier at 5.8 hours) 
Key Observations: 
1.	Exponential Growth: CPU time increases exponentially with n, confirming O(2ⁿ) behavior 
2.	Scaling Factor: The empirical curve closely matches the theoretical O(2ⁿ) curve when scaled appropriately 
3.	Practical Limits: For n ≤ 15, instances solve in seconds. For n = 20, instances take ~10-12 seconds. For n ≥ 22, instances require minutes to hours 
4. Variability: Instances of the same size show variation based on edge density and structure (e.g., size 24 ranged from 7.3 minutes to 5.8 hours) 
Empirical vs Theoretical Analysis 
The experimental results confirm the asymptotic time complexity analysis: 
•	Theoretical: O(2ⁿ · |E|) or O(2^n) when |E| is polynomial in n 
•	Empirical: The log-scale plot shows a linear relationship between log(time) and n, indicating exponential growth with base 2 
The empirical runtime plot demonstrates that: 



## Contact

Repository maintained by `kashif-techdev`.