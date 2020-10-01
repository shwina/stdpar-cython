import numpy as np
from jacobi import jacobi_solver

M = N = 1000

data = np.ones((M, N), dtype='float32') * 250
data[:, 0] = 100
data[:, N-1] = 400

data[0, :] = 200
data[M-1, :] = 300

mini_data = np.ones((10, 10), dtype='float32') * 0
mini_data[0, 1] = 100
mini_data[0, -2] = 200
mini_data[1, 0] = 300

iters = jacobi_solver(data, 0.01)

print(f"Iterations: {iters}")
