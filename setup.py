from setuptools import setup

setup(
    name='tox-auto-env',
    version='0.0.1a',
    py_modules=['tox_auto_env'],
    entry_points={'tox': ['tox-auto-env = tox_auto_env']},
    classifiers=['Framework :: tox'],
    description='Keeps your tox virtualenv always up to date with dependencies',
    author='Aaron Ramshaw'
)
