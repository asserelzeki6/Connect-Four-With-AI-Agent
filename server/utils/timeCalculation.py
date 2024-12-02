import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import matplotlib.pyplot as plt
from utils.alphabeta import alphabeta_decision
from utils.minimax import minimax_decision
from utils.expected import expected_decision


depths = range(2, 9)
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
    print(f"Depth: {depth*2} done")

plt.plot(depths, times_algo1, label='Alphabeta')
plt.plot(depths, times_algo2, label='Minimax')
plt.plot(depths, times_algo3, label='Expected Minimax')

plt.xlabel('Depth')
plt.ylabel('Time (seconds)')
plt.title('Runtime of Algorithms for Different Depths')
plt.legend()
plt.show()
plt.savefig(os.path.join(os.path.dirname(__file__), 'algorithm_runtime.png'))