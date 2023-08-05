from setuptools import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

setup(
    ext_modules =[ Extension('pankmer.index',
        sources=["src/pankmer/index.pyx"], language='c++',
        extra_compile_args = ["-std=c++11", "-fopenmp"],
        extra_link_args=["-fopenmp"])],
    cmdclass = {'build_ext': build_ext},
    include_dirs=[numpy.get_include()]
)
