from __future__ import unicode_literals
import os
import sys
import logging
import functools
from logging.config import fileConfig

import click
import venusian
from pyramid.paster import get_appsettings
from pyramid.paster import setup_logging

import hovercraft
from hovercraft import scripts
from hovercraft.settings import default_settings


LOG_MAPPING = {
    'd': logging.DEBUG,
    'debug': logging.DEBUG,
    'i': logging.INFO,
    'info': logging.INFO,
    'w': logging.WARNING,
    'warn': logging.WARNING,
    'e': logging.ERROR,
    'err': logging.ERROR,
    'error': logging.ERROR,
}

DEFAULT_CONFIG_FILE = '/etc/hovercraft/hovercraft.ini'

SCRIPTS_FOLDER = os.path.dirname(__file__)


class MasterCLI(click.MultiCommand):

    def __init__(self, *args, **kwargs):
        super(MasterCLI, self).__init__(*args, **kwargs)
        self.subcommands = self._scan_subcommands()

    def _scan_subcommands(self):
        subcommands = {}
        scanner = venusian.Scanner(subcommands=subcommands)
        scanner.scan(scripts, categories=('subcommands', ))
        return subcommands

    def list_commands(self, ctx):
        command_names = self.subcommands.keys()
        command_names.sort()
        return command_names

    def get_command(self, ctx, name):
        if name not in self.subcommands:
            return
        return self.subcommands[name]


@click.command(cls=MasterCLI, invoke_without_command=True)
@click.option(
    '-l', '--log-level',
    type=click.Choice(LOG_MAPPING.keys()),
    help='log LEVEL',
    default='info',
)
@click.option(
    '-c', '--conf-file',
    type=str,
    help='configuration FILE, defaults to HOVERCRAFT_CONF, use - for defaults',
    default=os.getenv('HOVERCRAFT_CONF', DEFAULT_CONFIG_FILE),
)
@click.option(
    '-v', '--version',
    is_flag=True,
    help='print hovercraft version',
)
@click.pass_context
def cli(ctx, log_level, conf_file, version):
    click.echo('Log level: {}'.format(log_level), err=True)
    click.echo('Configuration: {}'.format(conf_file), err=True)

    setup_logging(
        conf_file,
        functools.partial(fileConfig, disable_existing_loggers=False),
    )
    root = logging.getLogger('')
    root.setLevel(level=LOG_MAPPING[log_level])
    settings = default_settings.copy()
    cfg_settings = get_appsettings(conf_file, name='main')
    settings.update(cfg_settings)
    
    ctx.obj['log_level'] = log_level
    ctx.obj['conf_file'] = conf_file
    ctx.obj['settings'] = settings

    if version:
        click.echo(hovercraft.__version__)
        return
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help(), err=True)
        sys.exit(-1)


def main():
    cli(obj={})

if __name__ == '__main__':
    main()
