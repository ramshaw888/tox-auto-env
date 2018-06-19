import pluggy

hookimpl = pluggy.HookimplMarker("tox")


@hookimpl
def tox_addoption(parser):
    print('toxaddoption')
    """Add command line option to display fireworks on request."""


@hookimpl
def tox_configure(config):
    print('tox_configure')
    """Post process config after parsing."""


@hookimpl
def tox_runenvreport(config):
    print('tox_runenvreport')
    """Display fireworks if all was fine and requested."""
