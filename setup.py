from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='caldwr',
    version='1.0dev',
    description=(
        'Tools for retrieving and parsing data from California DWR'),
    long_description=long_description,
    author='Matt Davis',
    author_email='jiffyclub@gmail.com',
    url='https://github.com/jiffyclub/caldwr',
    packages=find_packages(),
    install_requires=[
        'lxml >= 3.0',
        'pandas >= 0.15'
    ],
    tests_require=['pytest >= 2.4'],
    classifiers=[
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'])
