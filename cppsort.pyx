# distutils: language=c++
# distutils: extra_compile_args=-fPIC -stdpar=gpu -gpu=nordc -std=c++17
# distutils: extra_link_args=-shared -stdpar=gpu

from libcpp.execution cimport par
from libcpp.algorithm cimport sort, copy
from libcpp.vector cimport vector

cimport numpy as np

def cppsort(np.ndarray[np.double_t, ndim=1] x, parallel=False):
    cdef vector[double] vec
    vec.reserve(len(x))
    vec.resize(len(x))
    copy(&x[0], &x[-1], vec.begin())

    if parallel:
        sort(par, vec.begin(), vec.end())
    else:
        sort(vec.begin(), vec.end())

    copy(vec.begin(), vec.end(), &x[0])
