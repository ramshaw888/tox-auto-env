import pluggy
import hashlib
import py
import os

try:
    from pip.download import PipSession
    from pip.req import parse_requirements
except ImportError:
    # Support for pip 10 - these have been moved to _internal
    from pip._internal.download import PipSession
    from pip._internal.req.req_file import parse_requirements


ENV_LIST_FILE = '/tmp/tox_auto_env_list'

hookimpl = pluggy.HookimplMarker('tox')

req_option = '-r'

BOLD = '\033[1m'


@hookimpl
def tox_configure(config):
    basename = config.setupdir.basename
    set_envdir_for_envconfigs(config.envconfigs)
    write_env_list_file(basename, config.envconfigs)


@hookimpl
def tox_runtest_pre(venv):
    print('{}{} virtualenv: {}{}'.format(BOLD, venv.name, venv.path, BOLD))


def set_envdir_for_envconfigs(envconfigs):
    for env in envconfigs:
        new_path = '{}-{}'.format(
            envconfigs[env].envdir,
            deps_hash(envconfigs[env].deps)
        )
        new_py_path = py.path.local(new_path)
        envconfigs[env].envdir = new_py_path


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


def write_env_list_file(basename, envconfigs):
    env_dir_map = {}
    for envname, env in envconfigs.items():
        env_dir_map[envname] = str(env.envdir)

    stored_envs = {}

    with open(ENV_LIST_FILE, 'w+') as f:
        lines = f.readlines()
        for line in lines:
            kv = line.split('=')
            if len(kv) == 2:
                val = kv[1]
                stored_envs[kv[0]] = val.replace(os.linesep, '')

        stored_envs.update(env_dir_map)
        f.truncate(0)

        for envname, envdir in stored_envs.items():
            envline = '{}:{}={}{}'.format(
                basename, envname, envdir, os.linesep)
            f.write(envline)
