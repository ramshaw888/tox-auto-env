import py
import pytest
import tox_auto_env


class MockEnvConfig:
    def __init__(self, env_name, deps):
        self.envdir = py.path.local(env_name)
        self.deps = deps


def test_deps_hash():
    reqs = ['pip', 'python', 'tox']
    result_a = tox_auto_env.deps_hash(reqs)
    result_b = tox_auto_env.deps_hash(reqs)
    assert result_a == result_b


def test_envdir_for_envconfigs():
    """Test that the envdir value is set correctly"""

    test_env_name = 'env_a'
    envconfig = MockEnvConfig(
        test_env_name, ['requests==2.1.0', 'marshmallow>=1.2.3', 'random']
    )
    pre_env_dir = envconfig.envdir
    tox_auto_env.set_envdir_for_envconfigs({test_env_name: envconfig})
    assert envconfig.envdir != pre_env_dir

    # Should be the same as the original envdir, but with the hash appended
    assert str(envconfig.envdir).startswith(str(pre_env_dir))
