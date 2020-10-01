import  os
import shutil
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize


include_dirs = []
library_dirs = []
libraries = []

# Try to find nvc++:
NVCPP_EXE = shutil.which("nvc++")
if NVCPP_EXE is None:
    NVCPP_EXE = os.environ.get("CC", None)

if NVCPP_EXE is not None:
    NVCPP_EXE = NVCPP_EXE if NVCPP_EXE.endswith("nvc++") else None

if NVCPP_EXE is not None:
    NVCPP_HOME = os.path.dirname(os.path.dirname(NVCPP_EXE))
    include_dirs += [
        os.path.join(NVCPP_HOME, "include-stdpar")
    ]
    library_dirs += [
        os.path.join(NVCPP_HOME, "lib")
    ]
else:
    libraries += ["tbb"]


class custom_build_ext(build_ext):
    def build_extensions(self):
        if NVCPP_EXE:
            # Override the compiler executables. Importantly, this
            # removes the "default" compiler flags that would
            # otherwise get passed on to nvc++, i.e.,
            # distutils.sysconfig.get_var("CFLAGS"). nvc++
            # does not support all of those "default" flags
            compile_args = "-fPIC -stdpar -gpu=nordc -std=c++17"
            link_args = "-shared -stdpar"
            self.compiler.set_executable(
                "compiler_so",
                NVCPP_EXE + " " + compile_args
            )
            self.compiler.set_executable("compiler_cxx", NVCPP_EXE)
            self.compiler.set_executable(
                "linker_so",
                NVCPP_EXE + " " + link_args
            )
        build_ext.build_extensions(self)


ext = cythonize([
    Extension(
        '*',
        sources=['*.pyx'],
        libraries=libraries,
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        runtime_library_dirs=library_dirs,
        extra_compile_args=["-std=c++17"]
    )])

setup(
    name='cppsort',
    author='Ashwin Srinath',
    version='0.1',
    ext_modules=ext,
    zip_safe=False,
    cmdclass={'build_ext': custom_build_ext}
)
