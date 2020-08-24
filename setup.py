import  os
from os.path import join as pjoin
from setuptools import setup, Extension
import subprocess
import sys
from setuptools.command.build_ext import build_ext
from collections import defaultdict


NVCPP = {
    "nvc++": "/home/ashwin/local/Linux_x86_64/20.7/compilers/bin/nvc++",
    "home": "/home/ashwin/local/Linux_x86_64/20.7/",
    "include": [
        "/home/ashwin/local/Linux_x86_64/20.7/cuda/include/",
        "/home/ashwin/local/Linux_x86_64/2020/compilers/include/",
        "/home/ashwin/local/Linux_x86_64/20.7/compilers/include-stdpar/",
    ],
    "lib64": [
        "/home/ashwin/local/Linux_x86_64/2020/compilers/lib/",
    ]
}

def customize_compiler(self):
    """inject deep into distutils to customize how the dispatch
    to gcc/nvcc works.

    If you subclass UnixCCompiler, it's not trivial to get your subclass
    injected in, and still have the right customizations (i.e.
    distutils.sysconfig.customize_compiler) run on it. So instead of going
    the OO route, I have this. Note, it's kindof like a wierd functional
    subclassing going on."""

    # tell the compiler it can processes .cu
    self.src_extensions.append('.cu')

    # save references to the default compiler_so and _comple methods
    default_compiler_so = self.compiler_so
    default_linker_so = self.linker_so
    default_compiler_cxx = self.compiler_cxx
    super = self._compile
    super_linker = self.link_shared_object

    # now redefine the _compile method. This gets executed for each
    # object but distutils doesn't have the ability to change compilers
    # based on source extension: we add it.
    def _compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
        postargs = extra_postargs
        self.set_executable('compiler_so', NVCPP['nvc++'])
        super(obj, src, ext, cc_args, postargs, pp_opts)
        # reset the default compiler_so, which we might have changed for cuda
        self.compiler_so = default_compiler_so

    def link_shared_object(*args, **kwargs):
        
        linker_so = [
            NVCPP["nvc++"],
            "-stdpar=gpu",
            "-fPIC",
            "-shared",
            "-gpu=nordc",
            f"-Wl,-rpath={NVCPP['lib64']}"
        ]
        self.set_executable("linker_so", linker_so)
        self.set_executable("compiler_cxx", linker_so)
        super_linker(*args, **kwargs)
        self.compiler_cxx = default_compiler_cxx
        self.linker_so = default_linker_so

    # inject our redefined _compile method into the class
    self._compile = _compile
    self.link_shared_object = link_shared_object

# run the customize_compiler
class custom_build_ext(build_ext):
    def build_extensions(self):
        customize_compiler(self.compiler)
        build_ext.build_extensions(self)
        
from Cython.Build import cythonize
ext = cythonize([
    Extension(
        '*',
        sources=['*.pyx'],
    )])

setup(name='stdpar_sort',
      author='Ashwin Srinath',
      version='0.1',
      ext_modules = ext,
      zip_safe=False,
      cmdclass={'build_ext': custom_build_ext }
)
