# distutils: language=c++
# distutils: extra_compile_args=-I/home/ashwin/local/Linux_x86_64/2020/compilers/include-stdpar/ -fPIC -stdpar=gpu -gpu=nordc -Minform=inform

from libcpp.execution cimport parallel_policy
from libcpp.algorithm cimport sort
from libcpp.vector cimport vector
from libcpp.utility cimport move


cdef vector[double] x
x = [9, 8, 7]
sort(parallel_policy(), x.begin(), x.end())
print(x)

