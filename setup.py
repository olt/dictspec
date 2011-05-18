from setuptools import setup, find_packages

import dictspec

setup(
    name = "dictspec",
    version = dictspec.__version__,
    description='validator for JSON/YAML/dict data',
    long_description=open('README.md').read(),
    author = "Oliver Tonnhofer",
    author_email = "olt@omniscale.de",
    url='http://github.org/olt/dictspec/',
    license='MIT License',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)
