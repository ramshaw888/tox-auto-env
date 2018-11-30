import pluggy
import hashlib
import py
import shutil
import os

try:
    from pip.download import PipSession
    from pip.req import parse_requirements
except ImportError:
    # Support for pip 10 - these have been moved to _internal
    from pip._internal.download import PipSession
    from pip._internal.req.req_file import parse_requirements


hookimpl = pluggy.HookimplMarker('tox')

req_option = '-r'

BOLD = '\033[1m'


@hookimpl
def tox_configure(config):
    set_envdir_for_envconfigs(config.envconfigs)


@hookimpl
def tox_runtest_pre(venv):
    print('{}{} virtualenv: {}{}'.format(BOLD, venv.name, venv.path, BOLD))
    create_virtualenv_symlink(
        str(venv.envconfig.original_envdir),
        str(venv.envconfig.envdir)
    )


def create_virtualenv_symlink(original_dir, new_dir):
    """Adds a symlink from the new "{envname}-{hash}" directory, to the
    original location. This makes it easier to use autocomplete/IDEs that
    expect the virtualenv in a predictable location"""

    try:
        # Remove old symlink
        os.remove(original_dir)
    except OSError:
        pass

    try:
        # Remove the old directory for previously created virtualenvs,
        # additionally, tox still creates this as an empty dir when running.
        shutil.rmtree(original_dir)
    except OSError:
        pass

    os.symlink(new_dir, original_dir)


def set_envdir_for_envconfigs(envconfigs):
    for env in envconfigs:
        original_envdir = envconfigs[env].envdir
        new_path = '{}-{}'.format(
            original_envdir, deps_hash(envconfigs[env].deps))
        local_new_envdir = py.path.local(new_path)
        envconfigs[env].envdir = local_new_envdir
        envconfigs[env].original_envdir = original_envdir


def deps_hash(env_deps):
    dependencies = []
    for dep in env_deps:
        dep_name = str(dep)
        if dep_name.startswith(req_option):
            dependencies += dependencies_from_requirements(dep_name)
        else:
            dependencies.append(dep_name)
    dependencies_str = ''.join(sorted(dependencies))
    return hashlib.sha1(dependencies_str.encode('utf-8')).hexdigest()


def dependencies_from_requirements(req_file_name):
    req_file_name = req_file_name[len(req_option):]
    requirements = parse_requirements(
        req_file_name,
        session=PipSession()
    )
    return [str(r.req) for r in requirements if r.req]
