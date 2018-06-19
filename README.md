# tox-env-hash

Never use `tox --recreate` again. Virtualenvs created by tox are identified by
the dependencies that are installed in it.

### Why
When testing or developing you may be updating or adding dependencies in the
`tox.ini` or `requirements.txt` files. You may then be stashing those changes
because they were _bad_. You may be switching between branches that have
different dependencies. Each time you do this, you need to recreate the tox
virtualenv so that those dependencies are correctly installed. Running `tox
--recreate` does this by deleting that virtualenv and starting fresh.

### How it works
When `tox-env-hash` is installed, virtualenvs created by tox are id'd by a hash
of the dependencies that are installed in it. i.e. if you have 2 branches with
different dependencies, running tox on each of those branches will create 2
separate virtualenvs that will be used for those 2 branches.


### Kudos
Inspired by [tox-battery](https://github.com/signalpillar/tox-battery)
