# distutils: language=c++
# distutils: extra_compile_args=-fPIC -stdpar=gpu -gpu=nordc
# distutils: extra_link_args=-shared -stdpar=gpu

from libcpp.execution cimport seq, par
from libcpp.algorithm cimport sort
from libcpp.vector cimport vector
from libcpp.utility cimport move
import timeit


def time_sort(vector[double] x):
    start = timeit.default_timer()
    for i in range(100):
        sort(seq, x.begin(), x.end())
    end = timeit.default_timer()
    seq_time = end - start

    start = timeit.default_timer()
    for i in range(100):
        sort(par, x.begin(), x.end())
    end = timeit.default_timer()
    par_time = end - start
    print(f"size:{x.size()}, seq:{seq_time}, par:{par_time}")
