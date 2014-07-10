#!/usr/bin/python3

"""Part of the test suite concerned with util module testing.
"""

import json
import os
import shutil
import unittest
import warnings

import bearton


#######
# Flags
#######

DEBUG = True
# Base of the test directory
BASE_PATH=os.path.abspath(os.path.split(__file__)[0])
# Test build path (containing .bearton repository directory)
TEST_BUILD_PATH=os.path.join(BASE_PATH, 'build')
# Test repository path (sometimes may be useful)
TEST_REPO_PATH=os.path.join(TEST_BUILD_PATH, '.bearton')


class InitialisationModuleTests(unittest.TestCase):
    def testInitialisationCreatesNecessaryStructures(self):
        files = [
                ('config.json',),
        ]
        bearton.init.new(TEST_REPO_PATH)
        for i in bearton.init.REQUIRED_REPO_DIRECTORIES:
            path = os.path.normpath(os.path.join(TEST_REPO_PATH, os.path.join(*i)))
            if DEBUG: print('checking for directory: "{0}"'.format(path))
            self.assertTrue(os.path.isdir(path))
        for i in files:
            path = os.path.normpath(os.path.join(TEST_REPO_PATH, os.path.join(*i)))
            if DEBUG: print('checking for file: "{0}"'.format(path))
            self.assertTrue(os.path.isfile(path))


if __name__ == '__main__':
    if os.path.isdir(TEST_REPO_PATH): shutil.rmtree(TEST_REPO_PATH)
    tmpfiles = [i for i in os.listdir('/tmp') if i.startswith('bearton_testing')]
    for i in tmpfiles:
        os.remove(os.path.join('/tmp', i))
    unittest.main()
