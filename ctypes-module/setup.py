from distutils.core import setup
import sys
sys.path.append('..')
from tests import TestCommand

setup(
    name = 'PyCronkite-ctypes',
    version = '0.6',
    description = 'python module (ctypes) for libcronkite',
    url = 'http://github.com/cactus/pycronkite',
    license="MIT",
    py_modules = ['pycronkite'],
    cmdclass = {'test': TestCommand})

