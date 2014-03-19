from setuptools import setup

execfile('unflattener/__init__.py')

setup(
    name='Unflattener',
    version=__version__,
    description='Make normal maps for 2D art.',
    url='http://github.com/dbohdan/unflattener',
    author='Danyil Bohdan',
    author_email='danyil.bohdan@gmail.com',
    license='BSD',
    packages=['unflattener'],
    package_dir = {'': '.'},
    data_files=['LICENSE', 'README.md'],
    test_suite='unflattener.tests.suite',
    zip_safe=False,
    install_requires=[
            "numpy",
            "pillow",
        ],
    entry_points = {
        'console_scripts': [
            'unflatten = unflattener.unflatten:main',
        ],
    }
)
