# tox-auto-env

[![CircleCI](https://circleci.com/gh/ramshaw888/tox-auto-env/tree/develop.svg?style=svg&circle-token=c1a0297fa1cebad4607a1a74226f1c05619d6b24)](https://circleci.com/gh/ramshaw888/tox-auto-env/tree/develop)

The virtualenv behind your tox environments will always reflect the
dependencies at the time of running. Never use `tox --recreate` again.

### Why
When testing or developing you may be updating or adding dependencies in the
`tox.ini` or `requirements.txt` files. You may then be stashing those changes
because they were _bad_. You may be switching between branches that have
different dependencies. Each time you do this, you need to recreate the tox
virtualenv so that those dependencies are correctly installed. Running `tox
--recreate` does this by deleting that virtualenv and starting fresh.

### How it works
When `tox-auto-env` is installed, virtualenvs created by tox are identified by
a hash of the dependencies that are installed in it. i.e. if you have 2
branches with different dependencies, running tox on each of those branches
will create 2 separate virtualenvs that will be used for those 2 branches.

### How to use
`tox-auto-env` is a `tox` plugin. Use `pip install tox-auto-env` to install.
If installed correctly, it should show up when `tox --version` is run.


### Kudos
Inspired by [tox-battery](https://github.com/signalpillar/tox-battery)
