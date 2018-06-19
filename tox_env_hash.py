import pluggy
import hashlib
import py

try:
    from pip.download import PipSession
    from pip.req import parse_requirements
except ImportError:
    # Support for pip 10 - these have been moved to _internal
    from pip._internal.download import PipSession
    from pip._internal.req.req_file import parse_requirements


hookimpl = pluggy.HookimplMarker('tox')

req_option = '-r'


@hookimpl
def tox_configure(config):
    set_envdir_for_envconfigs(config.envconfigs)


def set_envdir_for_envconfigs(envconfigs):
    for env in envconfigs:
        new_path = '{}-{}'.format(
            envconfigs[env].envdir,
            deps_hash(envconfigs[env].deps)
        )
        envconfigs[env].envdir = py.path.local(new_path)


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
