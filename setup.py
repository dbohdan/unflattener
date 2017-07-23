from __future__ import print_function

from setuptools import setup

from unflattener import __version__ as VERSION

REQUIRES = [
    'numpy',
    'pillow >= 2.2.1'
]

setup(
    name='Unflattener',
    version=VERSION,
    description='Make normal maps for 2D art.',
    url='http://github.com/dbohdan/unflattener',
    author='dbohdan',
    author_email='dbohdan@dbohdan.com',
    license='BSD',
    packages=['unflattener'],
    package_dir='',
    data_files=[('', ['LICENSE', 'README.md'])],
    test_suite='unflattener.tests.suite',
    zip_safe=False,
    install_requires=REQUIRES,
    entry_points = {
        'console_scripts': [
            'unflatten = unflattener.unflatten:main',
        ],
    }
)
