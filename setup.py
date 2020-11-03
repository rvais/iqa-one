# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

from setuptools import setup, find_packages

setup(
    name='iqa-one',
    version='0.1.2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license='Apache 2.0',
    description='Messaging testing project',
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=[
        'pytest',
        'pytest-docker',
        "pytest-cov",
        'pytest-asyncio',
        'mock',
        'pytest-mock',
        'nest_asyncio',
        'tox',
        "codecov",
        "asynctest",
        "mypy",
        "aiologger",
        "uvloop",
    ],

    install_require=[
        'asyncssh',
        'requests',
        'ansible',
        'PyYAML',
        'dpath',
        'CALM',
        'cython',
        'ansible',
        'python-qpid-proton',
        'git+git://github.com/rh-messaging-qe/yacfg@master#egg=yacfg',
        'dpath',
        'optconstruct',
        'docker',
        'docker-compose',
        'urllib3',
        "flake8",
        'kubernetes'
    ],
    url='https://github.com/enkeys/iqa-one',
    author='Dominik Lenoch',
    author_email='dlenoch@redhat.com',
    entry_points={
        'pytest11': [
            'pytest_iqa = pytest_iqa.plugin',
        ],
    },
)
