from libcpp cimport bool

cdef extern from "<algorithm>" namespace "std" nogil:
    OutputIt copy_n[ExecutionPolicy, InputIt, Size, OutputIt](ExecutionPolicy&& policy, InputIt first, Size count, OutputIt result) except +
    OutputIt copy[ExecutionPolicy, InputIt, OutputIt](ExecutionPolicy&& policy, InputIt first, InputIt last, OutputIt d_first) except +
    void sort[ExecutionPolicy, Iter](ExecutionPolicy&& policy, Iter first, Iter last) except +
    bool any_of[ExecutionPolicy, Iter, Pred](ExecutionPolicy&& policy, Iter first, Iter last, Pred pred) except +
    void for_each[ExecutionPolicy, Iter, UnaryFunction](ExecutionPolicy&& policy, Iter first, Iter last, UnaryFunction f) except +  # actually returns f
