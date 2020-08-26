# distutils: language=c++

from libcpp.execution cimport par
from libcpp.algorithm cimport sort, copy_n
from libcpp.vector cimport vector

cimport numpy as np

def cppsort(np.ndarray[np.float32_t, ndim=1] x):
    """
    Sort the elements of x "in-place" using std::sort
    """
    cdef vector[float] vec
    vec.resize(len(x))
    copy_n(&x[0], len(x), vec.begin())
    sort(par, vec.begin(), vec.end())
    copy_n(vec.begin(), len(x), &x[0])

