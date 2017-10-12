import os
import sys
from setuptools import setup, Extension

try:
    from Cython.Build import cythonize
    ext = '.pyx'
except ImportError:
    def cythonize(extensions): return extensions
    ext = '.cpp'

MIN_PYTHON = (2, 7)
if sys.version_info < MIN_PYTHON:
    sys.stderr.write("Python {}.{} or later is required\n".format(*MIN_PYTHON))
    sys.exit(1)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

extensions = cythonize([
    Extension(
        '_morton', ['_morton' + ext],
        language="c++",
    ),
])


setup(
    name='morton-py',
    version='1.2',
    author='Andrew Kirilenko',
    author_email='iced@gojuno.com',
    maintainer='Alexander Verbitsky',
    maintainer_email='averbitsky@gojuno.com',
    description='Morton code pack/unpack library',
    long_description=read('README.rst'),
    keywords='z-order, morton coding, hashing',
    url='https://github.com/gojuno/morton-py',
    py_modules=['morton'],
    ext_modules = extensions,
    test_suite='test',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
    ],
)
