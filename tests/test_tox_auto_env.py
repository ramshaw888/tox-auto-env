import py
import pytest
import tox_auto_env

try:
    from unittest.mock import mock_open, patch
except ImportError:
    from mock import mock_open, patch


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


def test_write_env_list_to_file():
    test_env_name = 'env_a'
    envconfig = MockEnvConfig(
        test_env_name, ['requests==2.1.0', 'marshmallow>=1.2.3', 'random']
    )
    envconfigs = {test_env_name: envconfig}
    tox_auto_env.set_envdir_for_envconfigs(envconfigs)

    m = mock_open(read_data='abcd=12345\nenv_a=toreplace\n')
    with patch('tox_auto_env.open', m, create=True):
        tox_auto_env.write_env_list_file(envconfigs)

    handle = m()
    # Should clear the file
    handle.truncate.assert_called_once_with(0)

    lines = set([call_arg[0][0] for call_arg in handle.write.call_args_list])

    # should not remove unrelated envs
    assert 'abcd=12345\n' in lines

    # Should update `env_a` with new envdir
    expected_line = '{}={}\n'.format(test_env_name, envconfig.envdir)
    assert expected_line in lines

    # Old value for `env_a` should not exist
    assert 'env_a=toreplace\n' not in lines
