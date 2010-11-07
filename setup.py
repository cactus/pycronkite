from distutils.core import setup, Extension
import sys
sys.path.append('..')
from tests import TestCommand

cronkite = Extension(
    "cronkite",
    libraries = ['cronkite'],
    sources = ['pycronkite.c'],
    language = 'c')

setup(
    name = 'PyCronkite-c',
    version = '0.6',
    description = 'python module (in c) for libcronkite',
    url = 'http://github.com/cactus/pycronkite',
    license="MIT",
    ext_modules = [cronkite],
    cmdclass = {'test': TestCommand})

