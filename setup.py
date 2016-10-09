from __future__ import print_function

from setuptools import setup

from unflattener import __version__ as VERSION

PIL_DEP = 'pil >= 1.1.7'
PILLOW_DEP = 'pillow >= 2.2.1'

REQUIRES = [
    'numpy',
]

try:
    import PIL
    # Use the original PIL if is it installed. Since v1.1.7 is the first
    # version compatible with Python 2.7 the PIL version shouldn't be a
    # problem.
    if not hasattr(PIL, 'PILLOW_VERSION'):
        REQUIRES.append(PIL_DEP)
    else:
        REQUIRES.append(PILLOW_DEP)
except:
    print('Module PIL not found. Depending on Pillow by default.')
    REQUIRES.append(PILLOW_DEP)

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
