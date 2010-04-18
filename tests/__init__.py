import sys
sys.bytecodebase = None
import os
import unittest
import exceptions
from distutils.core import Command
from unittest import TextTestRunner, TestLoader
from glob import glob
from os.path import splitext, basename, join as pjoin, walk

class TestCommand(Command):
    description = "run unittests"
    user_options = [ ]
    #    ('test-dir=', None, 'Directory or file containing unittests')]

    def initialize_options(self):
        self._dir = os.path.dirname(os.path.realpath(__file__))

    def finalize_options(self):
        pass

    def run(self):
        '''
        Finds all the tests modules in tests/, and runs them.
        '''
        testfiles = [ ]
        for t in glob(pjoin(self._dir, 'test*.py')):
            if not t.endswith('__init__.py'):
                testfiles.append('.'.join(
                    ['tests', splitext(basename(t))[0]])
                )

        tests = TestLoader().loadTestsFromNames(testfiles)
        t = TextTestRunner(verbosity = 1)
        t.run(tests)
