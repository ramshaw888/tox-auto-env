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
    for env in config.envconfigs:
        new_path = '{}-{}'.format(
            config.envconfigs[env].envdir,
            deps_hash(config.envconfigs[env].deps)
        )
        config.envconfigs[env].envdir = py.path.local(new_path)


def deps_hash(deps):
    hash_l = []
    for dep in deps:
        dep_name = str(dep)
        if dep_name.startswith(req_option):
            dep_str_repr = requirements_hash(dep_name)
        else:
            dep_str_repr = dep_name
        hash_l.append(str_to_sha1hex(dep_str_repr))
    return str_to_sha1hex(''.join(sorted(hash_l)))


def requirements_hash(req_file_name):
    req_file_name = req_file_name[len(req_option):]
    pip_reqs = parse_pip_requirements(req_file_name)
    return ''.join(pip_reqs)


def parse_pip_requirements(requirement_file_path):
    requirements = parse_requirements(
        requirement_file_path,
        session=PipSession()
    )
    return sorted(str(r.req) for r in requirements if r.req)


def str_to_sha1hex(v):
    return hashlib.sha1(v.encode('utf-8')).hexdigest()
