import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import matplotlib.pyplot as plt
from utils.alphabeta import alphabeta_decision
from utils.minimax import minimax_decision
from utils.expected import expected_decision


depths = range(1, 2)
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

# Output:
# Depth: 2 started
# alphabeta: 0.0
# minimax: 0.010590076446533203
# expected: 0.002993345260620117
# Depth: 2 done
# Depth: 3 started
# alphabeta: 0.020944595336914062
# minimax: 0.029100894927978516
# expected: 0.035857439041137695
# Depth: 3 done
# Depth: 4 started
# alphabeta: 0.08601593971252441
# minimax: 0.22858309745788574
# expected: 0.20847487449645996
# Depth: 4 done
# Depth: 5 started
# alphabeta: 0.36717796325683594
# minimax: 0.22858309745788574
# expected: 0.20847487449645996
# Depth: 4 done
# Depth: 5 started
# alphabeta: 0.36717796325683594
# Depth: 4 done
# Depth: 5 started
# alphabeta: 0.36717796325683594
# alphabeta: 0.36717796325683594
# minimax: 1.4886014461517334
# expected: 1.5999999046325684
# Depth: 5 done
# Depth: 6 started
# alphabeta: 1.1268181800842285
# minimax: 11.861638069152832
# expected: 15.101814031600952
# Depth: 6 done
# Depth: 7 started
# alphabeta: 5.397247552871704
# minimax: 102.36785364151001
# expected: 111.24937868118286
# Depth: 7 done