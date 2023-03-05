import click
from flask.cli import with_appcontext

from api.synchronization.service import SynchronizationService


@click.command(name='synchronize')
@click.argument('address')
@with_appcontext
def synchronize(address):
    SynchronizationService(address).synchronize_all()