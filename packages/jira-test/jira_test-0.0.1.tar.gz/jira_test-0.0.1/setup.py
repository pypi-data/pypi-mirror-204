#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='jira_test',
    version='0.0.1',
    description='API 2.0',
    author='prijen.khokhani@netskope.com',
    packages=find_packages(),
    license = 'Proprietary',
    classifiers=['Development Status :: 3 - Alpha'],
    install_requires=[
        'numpy',
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'jira_test_sum=src.sum:main',
            'jira_test_minus=src.minus:main'
        ]
    }
)