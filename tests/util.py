#!/usr/bin/python3

"""Part of the test suite concerned with util module testing.
"""

import json
import os
import shutil
import unittest
import warnings

import bearton


# Flags
DEBUG = False
BASE_PATH=os.path.split(__file__)[0]


class UtilIOModuleTests(unittest.TestCase):
    def testReadingFile(self):
        expected = 'Hello World!\n'
        got = bearton.util.io.read(os.path.join(BASE_PATH, './files/hello_world.txt'))
        self.assertEqual(expected, got)

    def testReadingFileThatDoesNotExistAndHasNoDefaultValueRaisesAnError(self):
        self.assertRaises(FileNotFoundError, bearton.util.io.read, os.path.join(BASE_PATH, './files/does_not_exist.txt'))

    def testReadingFileWithDefaultValue(self):
        expected = 'Hello World!'
        got = bearton.util.io.read(os.path.join(BASE_PATH, './files/no_hello_world.txt'), default='Hello World!')
        self.assertEqual(expected, got)

    def testReadingFileWithDefaultValueDoesNotOverrideActuallyReadValue(self):
        expected = 'Hello World!\n'
        got = bearton.util.io.read(os.path.join(BASE_PATH, './files/hello_world.txt'), default='This will fail')
        self.assertEqual(expected, got)

    def testWritingToFile(self):
        string = 'Hello World!'
        path = '/tmp/bearton_testing.writing_to_file.txt'
        bearton.util.io.write(path, string)
        self.assertEqual(string, bearton.util.io.read(path))


class UtilEnvModuleTests(unittest.TestCase):
    def testWithoutEnvGettingRepoPath(self):
        self.assertRaises(bearton.errors.RepositoryNotFoundError, bearton.util.env.getrepopath, start=os.path.join(BASE_PATH, 'tmp'))


if __name__ == '__main__':
    tmpfiles = [i for i in os.listdir('/tmp') if i.startswith('bearton_testing')]
    for i in tmpfiles:
        os.remove(os.path.join('/tmp', i))
    unittest.main()
