#!/usr/bin/env python
from setuptools import setup
import re
import os
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

MODULE = 'syscohada_2018'
PREFIX = 'apsarl'
MODULE2PREFIX = {}


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

config = ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
major_version, minor_version, _ = info.get('version', '0.0.1').split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

requires = []
for dep in info.get('depends', []):
    if not re.match(r'(ir|res|webdav)(\W|$)', dep):
        prefix = MODULE2PREFIX.get(dep, 'trytond')
        requires.append('%s_%s >= %s.%s, < %s.%s' %
                (prefix, dep, major_version, minor_version,
                major_version, minor_version + 1))
requires.append('trytond >= %s.%s, < %s.%s' %
        (major_version, minor_version, major_version, minor_version + 1))

tests_require = ['proteus >= %s.%s, < %s.%s' %
    (major_version, minor_version, major_version, minor_version + 1)]

setup(name='%s_%s' % (PREFIX, MODULE),
    version=info.get('version', '0.0.1'),
    description='SYSCOHADA COA 2018 revision',
    long_description=read('README'),
    author='Richmond FIKO, Africa Performances',
    url='https://www.africaperformances-ci.com/',
    download_url=("http://downloads.tryton.org/" +
        info.get('version', '0.0.1').rsplit('.', 1)[0] + '/'),
    package_dir={'trytond.modules.%s' % MODULE: '.'},
    packages=[
        'trytond.modules.%s' % MODULE,
        'trytond.modules.%s.tests' % MODULE,
        ],
    package_data={
        'trytond.modules.%s' % MODULE: (info.get('xml', [])
            + ['tryton.cfg', 'locale/*.po', 'tests/*.rst']),
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: Bulgarian',
        'Natural Language :: Catalan',
        'Natural Language :: Czech',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'Natural Language :: French',
        'Natural Language :: German',
        'Natural Language :: Russian',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Financial :: Accounting',
        ],
    license='GPL-3',
    install_requires=requires,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    %s = trytond.modules.%s
    """ % (MODULE, MODULE),
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
    tests_require=tests_require,
    )
