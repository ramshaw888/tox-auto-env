from setuptools import setup

setup(
    name="tox-hash",
    py_modules=["tox_hash"],
    entry_points={"tox": ["hash = tox_hash"]},
    classifiers=["Framework:: tox"],
)
