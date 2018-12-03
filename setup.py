from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='tox-auto-env',
    version='0.0.8',
    py_modules=['tox_auto_env'],
    entry_points={'tox': ['tox-auto-env = tox_auto_env']},
    classifiers=['Framework :: tox'],
    description=(
        'Keeps your tox virtualenv always up to date with dependencies'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Aaron Ramshaw',
    url='https://github.com/ramshaw888/tox-auto-env'
)
