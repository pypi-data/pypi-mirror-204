#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='kmx',
    version='0.1.1',
    author='akvarats',

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    packages=find_packages(),
    install_requires=[
        'aiokafka>=0.8,<0.9',
        'pydantic>=1.10,<1.11',
        'beanie>=1.17,<1.18',
        'aioredis[hiredis]>=2.0,<2.1',
        'networkx>=3.0,<3.1'
    ],
    setup_requires=['wheel'],
    python_requires='>=3.10,<4'
)
