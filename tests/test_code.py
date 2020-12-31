#!/usr/bin/python3

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.  See http://www.gnu.org/copyleft/lgpl.html for the full text
# of the license.

__author__ = 'Martin Pitt'
__copyright__ = '(c) 2012 Canonical Ltd.'

import sys
import unittest
import subprocess
import glob

try:
    pycodestyle = subprocess.check_output(['/bin/bash', '-ec', 'type -p pycodestyle-3 || type -p pycodestyle']).strip()
except subprocess.CalledProcessError:
    pycodestyle = None

try:
    pyflakes = subprocess.check_output(['/bin/bash', '-ec', 'type -p pyflakes-3 || type -p pyflakes3']).strip()
except subprocess.CalledProcessError:
    pyflakes = None

try:
    pylint = subprocess.check_output(['/bin/bash', '-ec', 'type -p pylint-3 || type -p pylint']).strip()
except subprocess.CalledProcessError:
    pylint = None


class StaticCodeTests(unittest.TestCase):
    @unittest.skipUnless(pyflakes, 'pyflakes3 not installed')
    def test_pyflakes(self):
        flakes = subprocess.Popen([pyflakes, '.'], stdout=subprocess.PIPE, universal_newlines=True)
        out = flakes.communicate()[0]
        self.assertEqual(flakes.returncode, 0, out)

    @unittest.skipUnless(pycodestyle, 'pycodestyle not installed')
    def test_codestyle(self):
        pep8 = subprocess.Popen([pycodestyle, '--max-line-length=130', '--ignore=E124,E402,E731,W504', '.'],
                                stdout=subprocess.PIPE, universal_newlines=True)
        out = pep8.communicate()[0]
        self.assertEqual(pep8.returncode, 0, out)

    @unittest.skipUnless(pylint, 'pylint not installed')
    def test_pylint(self):   # pylint: disable=no-self-use
        subprocess.check_call([pylint, 'setup.py'] + glob.glob('dbusmock/*.py'))
        # signatures/arguments are not determined by us, docstrings are a bit pointless, and code repetition
        # is impractical to avoid (e.g. bluez4 and bluez5)
        subprocess.check_call([pylint, '--disable=missing-function-docstring,R0801',
                               '--disable=too-many-arguments,too-many-instance-attributes',
                               'dbusmock/templates/'])
        subprocess.check_call([pylint, '--disable=missing-module-docstring,missing-class-docstring,missing-function-docstring',
                               '--disable=too-many-public-methods,R0801', 'tests/'])


if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
