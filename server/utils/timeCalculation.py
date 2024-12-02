import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import matplotlib.pyplot as plt
from utils.alphabeta import alphabeta_decision
from utils.minimax import minimax_decision
from utils.expected import expected_decision


depths = range(2, 8)
times_algo1 = []
times_algo2 = []
times_algo3 = []
base_board = [['.' for _ in range(7)] for _ in range(6)]
for depth in depths:
    print(f"Depth: {depth} started")
    start_time = time.time()
    alphabeta_decision(base_board, 'r', depth)
    times_algo1.append(time.time() - start_time)
    print(f"alphabeta: {time.time() - start_time}")
    start_time = time.time()
    minimax_decision(base_board, 'r', depth)
    times_algo2.append(time.time() - start_time)
    print(f"minimax: {time.time() - start_time}")
    start_time = time.time()
    expected_decision(base_board, 'r', depth*2)
    times_algo3.append(time.time() - start_time)
    print(f"expected: {time.time() - start_time}")
    print(f"Depth: {depth} done")

plt.plot(depths, times_algo2, label='Minimax')
plt.plot(depths, times_algo1, label='Minimax with Alphabeta Pruning')
plt.plot(depths, times_algo3, label='Expected Minimax')

plt.xlabel('Depth')
plt.ylabel('Time (seconds)')
plt.title('Runtime of Algorithms for Different Depths')
plt.legend()
plt.savefig(os.path.join(os.path.dirname(__file__), 'algorithm_runtime.png'))
plt.show()

# last output:
# Depth: 2 started
# alphabeta: 0.017586231231689453
# minimax: 0.02162337303161621
# expected: 0.027234554290771484
# Depth: 2 done
# minimax: 0.02162337303161621
# minimax: 0.02162337303161621
# minimax: 0.02162337303161621
# expected: 0.027234554290771484
# Depth: 2 done
# Depth: 3 started
# alphabeta: 0.07280325889587402
# minimax: 0.14037299156188965
# minimax: 0.02162337303161621
# expected: 0.027234554290771484
# Depth: 2 done
# Depth: 3 started
# alphabeta: 0.07280325889587402
# minimax: 0.02162337303161621
# expected: 0.027234554290771484
# Depth: 2 done
# Depth: 3 started
# alphabeta: 0.07280325889587402
# expected: 0.027234554290771484
# Depth: 2 done
# Depth: 3 started
# Depth: 3 started
# alphabeta: 0.07280325889587402
# minimax: 0.14037299156188965
# expected: 0.15262269973754883
# Depth: 3 done
# Depth: 4 started
# alphabeta: 0.37639498710632324
# minimax: 1.3120026588439941
# expected: 1.1063189506530762
# Depth: 4 done
# minimax: 0.14037299156188965
# expected: 0.15262269973754883
# Depth: 3 done
# Depth: 4 started
# alphabeta: 0.37639498710632324
# minimax: 1.3120026588439941
# expected: 1.1063189506530762
# Depth: 4 done
# Depth: 5 started
# expected: 0.15262269973754883
# Depth: 3 done
# Depth: 4 started
# alphabeta: 0.37639498710632324
# minimax: 1.3120026588439941
# expected: 1.1063189506530762
# Depth: 4 done
# Depth: 5 started
# minimax: 1.3120026588439941
# expected: 1.1063189506530762
# Depth: 4 done
# Depth: 5 started
# expected: 1.1063189506530762
# Depth: 4 done
# Depth: 5 started
# alphabeta: 1.3431437015533447
# Depth: 5 started
# alphabeta: 1.3431437015533447
# minimax: 7.7818989753723145
# alphabeta: 1.3431437015533447
# minimax: 7.7818989753723145
# minimax: 7.7818989753723145
# expected: 7.456750154495239
# Depth: 5 done
# Depth: 6 started
# Depth: 5 done
# Depth: 6 started
# alphabeta: 5.468378067016602
# minimax: 64.97731494903564
# expected: 79.64130449295044
# Depth: 6 done
# Depth: 6 done
# Depth: 7 started
# alphabeta: 32.1421172618866
# minimax: 453.0930805206299
# expected: 461.7324643135071
# Depth: 7 done