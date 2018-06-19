import pluggy
import hashlib
import py

try:
    from pip.download import PipSession
    from pip.req import parse_requirements
except ImportError:
    # It is quick hack to support pip 10 that has changed its internal
    # structure of the modules.
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
        hash_l.append(_str_to_sha1hex(dep_str_repr))
    return _str_to_sha1hex(''.join(sorted(hash_l)))


def requirements_hash(req_file_name):
    req_file_name = req_file_name[len(req_option):]
    pip_reqs = parse_pip_requirements(req_file_name)
    return ''.join(pip_reqs)


def parse_pip_requirements(requirement_file_path):
    """
    Parses requirements using the pip API.

    :param str requirement_file_path: path of the requirement file to parse.
    :returns list: list of requirements
    """
    requirements = parse_requirements(
        requirement_file_path,
        session=PipSession()
    )
    return sorted(str(r.req) for r in requirements if r.req)


def _str_to_sha1hex(v):
    """ Turn string into a SHA1 hex-digest.

    >>> _str_to_sha1hex('abc')
    'a9993e364706816aba3e25717850c26c9cd0d89d'
    """
    return hashlib.sha1(v.encode('utf-8')).hexdigest()
