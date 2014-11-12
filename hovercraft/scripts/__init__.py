from __future__ import unicode_literals

import venusian


def subcommand(wrapped):
    """This decorator makes a function becomes a subcommand

    """
    def callback(scanner, name, ob):
        scanner.subcommands[ob.name] = ob
    venusian.attach(wrapped, callback, category='subcommands')
    return wrapped
