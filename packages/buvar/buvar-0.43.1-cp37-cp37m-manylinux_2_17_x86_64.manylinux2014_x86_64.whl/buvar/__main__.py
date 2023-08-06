"""CLI buvar bootstrapping."""
import select
import sys

import toml

from buvar import config, fork, plugin
from buvar.components import Components


# load config from stdin
def stdin_data(fd=sys.stdin):
    if select.select(
        [
            fd,
        ],
        [],
        [],
        0.0,
    )[0]:
        return fd.read()


# load module via module path
# fork.stage()


# load module via file


if __name__ == "__main__":
    components = Components()
    config_source = config.ConfigSource()
    config_data = stdin_data()
    if config_data:
        config_source.merge(toml.loads(config_data))

    print(config_source)
# config_source.load(components)


# create config source
# - import all marked dependencies
# - > collect whatever information
# - > apply

# we need a config phase before fork is run
# to enable DRY in terms of socket definition repetition


# breakpoint()  # XXX BREAKPOINT

# fork.stage(components=components)
