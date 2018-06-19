from setuptools import setup

setup(
    name='tox-env-hash',
    version='0.0.1',
    py_modules=['tox_env_hash'],
    entry_points={'tox': ['tox-env-hash = tox_env_hash']},
    classifiers=['Framework:: tox'],
)
