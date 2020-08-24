# distutils: language=c++
# distutils: extra_compile_args=-fPIC -stdpar=gpu -gpu=nordc
# distutils: extra_link_args=-shared -stdpar=gpu

from libcpp.execution cimport parallel_policy
from libcpp.algorithm cimport sort
from libcpp.vector cimport vector
from libcpp.utility cimport move

cdef vector[double] x
x = [9, 8, 7]
sort(parallel_policy(), x.begin(), x.end())
print(x)

