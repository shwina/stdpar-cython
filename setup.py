import  os
import shutil
from os.path import join as pjoin
from setuptools import setup, Extension
import subprocess
import sys
from setuptools.command.build_ext import build_ext
from collections import defaultdict


NVCPP_EXE = shutil.which("nvc++")
if not NVCPP_EXE:
    NVCPP_EXE = os.environ.get("CC", None)
NVCPP_HOME = os.path.dirname(os.path.dirname(NVCPP_EXE))
NVCPP_INC_DIRS = [
    os.path.join(NVCPP_HOME, "include-stdpar")
]
NVCPP_LIB_DIRS = [
    os.path.join(NVCPP_HOME, "lib")
]

class custom_build_ext(build_ext):
    def build_extensions(self):
        # Override the compiler executables. Importantly, this
        # removes the "default" compiler flags that would
        # otherwise get passed on to nvc++, i.e.,
        # distutils.sysconfig.get_var("CFLAGS"). nvc++
        # does not support all of those "default" flags
        self.compiler.set_executable("compiler_so", NVCPP_EXE)
        self.compiler.set_executable("compiler_cxx", NVCPP_EXE)
        self.compiler.set_executable("linker_so", NVCPP_EXE)
        build_ext.build_extensions(self)
        
from Cython.Build import cythonize
ext = cythonize([
    Extension(
        '*',
        sources=['*.pyx'],
        include_dirs=NVCPP_INC_DIRS,
        library_dirs=NVCPP_LIB_DIRS,
        runtime_library_dirs=NVCPP_LIB_DIRS
    )])

setup(name='stdpar_sort',
      author='Ashwin Srinath',
      version='0.1',
      ext_modules = ext,
      zip_safe=False,
      cmdclass={'build_ext': custom_build_ext }
)
