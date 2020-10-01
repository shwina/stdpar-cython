# distutils: language=c++

from libcpp.algorithm cimport sort, copy
from libcpp.vector cimport vector


def cppsort(int[:] x):
    cdef vector[int] vec = vector[int](len(x))
    copy(&x[0], &x[-1], vec.begin())
    sort(vec.begin(), vec.end())
    copy(vec.begin(), vec.end(), &x[0])

