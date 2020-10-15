# Examples of using Cython and nvc++ to GPU accelerate Python

These Notebooks demonstrate how to accelerate Python code on the GPU
using Cython and [nvc++ with stdpar](https://developer.nvidia.com/blog/accelerating-standard-c-with-gpus-using-stdpar/).

1. [Simple sort example](sort.ipynb)
2. [Jacobi solver example](jacobi.ipynb)

## Requirements

1. First, you'll need the [NVIDIA HPC SDK](https://developer.nvidia.com/hpc-sdk), which
   provides the `nvc++` compiler. A minimum version of 20.9 is required to run these examples.

2. You will also need the development version of [Cython](https://github.com/cython/cython).
   The simplest way to get the minimum required version is to use `pip`:

   ```
   python -m pip install git+https://github.com/cython/cython@90684ac416f0349761074e242be4d981de40ce0f
   ```

3. This step is optional. To run the CPU Parallel benchmarks, you will need `gcc >= 9.1`
   as well as the [TBB](https://github.com/oneapi-src/oneTBB) library. On Ubuntu 20.04
   `gcc-9` should already be the default, and I did `apt install libtbb-dev` to get
   TBB.
