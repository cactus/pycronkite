from distutils.core import setup
import sys
sys.path.append('..')
from tests import TestCommand

setup(
    name = 'PyCronkite-ctypes',
    version = '0.6',
    description = 'python module (ctypes) for libcronkite',
    url = 'http://github.com/cactus/cronkite',
    license="MIT",
    py_modules = ['cronkite'],
    cmdclass = {'test': TestCommand})

