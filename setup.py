#!/usr/bin/env python
# vim: set et sw=4 sts=4:

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
    )

import os
from setuptools import setup, find_packages
from utils import description, get_version, require_python

# Workaround <http://bugs.python.org/issue10945>
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)

require_python(0x020600f0)

REQUIRES = [
    'pyramid<1.4dev',
    'pyramid_debugtoolbar',
    'waitress',
    ]

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Science/Research',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Education',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
    ]

ENTRY_POINTS = """\
    [paste.app_factory]
    main = weather:main
    """

HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, 'README.txt')).read()
CHANGES = open(os.path.join(HERE, 'CHANGES.txt')).read()

setup(
    name                 = 'weather',
    version              = get_version(os.path.join(HERE, 'weather', '__init__.py')),
    description          = 'A web-based weather related education suite',
    long_description     = README + '\n\n' + CHANGES,
    classifiers          = CLASSIFIERS,
    author               = 'Dave Hughes',
    author_email         = 'dave@waveform.org.uk',
    url                  = 'http://www.waveform.org.uk/trac/weather/',
    keywords             = 'weather climate web pyramid pylons',
    packages             = find_packages(exclude=['distribute_setup', 'utils']),
    include_package_data = True,
    zip_safe             = False,
    install_requires     = REQUIRES,
    tests_require        = REQUIRES,
    test_suite           = 'weather',
    entry_points         = ENTRY_POINTS,
    )

