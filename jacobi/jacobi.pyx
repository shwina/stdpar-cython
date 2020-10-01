# distutils: language=c++
# cython: cdivision=True

from libcpp.execution cimport par, seq
from libcpp.algorithm cimport any_of, for_each, swap, copy
from libcpp.vector cimport vector
from libcpp.functional cimport function
from libcpp cimport bool, float
from libc.math cimport fabs


cdef cppclass avg:
    float *fro
    float *to
    int M, N

    __init__(float* fro, float *to, int M, int N):
        this.fro, this.to, this.M, this.N = fro, to, M, N

    void call "operator()"(int i):
        if (i % N != 0 and i % N != N-1):
            this.to[i] = 0.25 * (
                this.fro[i-this.N] + this.fro[i+this.N] + this.fro[i-1] + this.fro[i+1]
            )

cdef cppclass converged:
    float *fro
    float *to
    float max_diff
    
    __init__(float* fro, float *to, float max_diff):
        this.fro, this.to, this.max_diff = fro, to, max_diff

    bool call "operator()"(int i):
        return fabs(this.to[i] - this.fro[i]) > this.max_diff

def jacobi_solver(float[:, :] data, float max_diff):
    M, N  = data.shape[0], data.shape[1]
    
    cdef vector[float] temp
    cdef vector[float] local_data
    temp.resize(M*N)
    local_data.resize(M*N)
    
    cdef vector[int] indices = range(N+1, (M-1)*N-1)
    
    copy(&data[0, 0], &data[-1, -1], temp.begin())
    copy(par, temp.begin(), temp.end(), local_data.begin())
    
    cdef int iterations = 0
    cdef float* fro = local_data.data()
    cdef float* to = temp.data()

    while True:
        iterations += 1
        for_each(par, indices.begin(), indices.end(), avg(fro, to, M, N))
        keep_going = any_of(par, indices.begin(), indices.end(), converged(fro, to, max_diff))
        swap(fro, to)
        
        if not keep_going:
            break

    if (to == &data[0, 0]):
        copy(temp.begin(), temp.end(), &data[0, 0])

    return iterations
