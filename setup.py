from setuptools import setup

setup(
    name='tox-hash',
    version='0.0.1',
    py_modules=['tox_hash'],
    entry_points={'tox': ['tox-hash = tox_hash']},
    classifiers=['Framework:: tox'],
)
