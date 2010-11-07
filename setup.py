from distutils.core import setup, Extension
from tests import TestCommand

pycronkite = Extension(
    "pycronkite",
    libraries = ['cronkite'],
    sources = ['src/pycronkite.c'],
    language = 'c')

setup(
    name = 'PyCronkite-c',
    version = '0.6',
    description = 'python module (in c) for libcronkite',
    url = 'http://github.com/cactus/pycronkite',
    license="MIT",
    ext_modules = [pycronkite],
    cmdclass = {'test': TestCommand})

