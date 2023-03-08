import click
from flask.cli import with_appcontext

from api.notifications.service import NotificationService
from api.synchronization.service import SynchronizationService
from api.transactions.model import TransactionType, Transaction
from api.transactions.service import TransactionService


@click.command(name='synchronize')
@click.argument('address')
@click.option(
    '--tx-type',
    '-t',
    'tx_types',
    multiple=True,
    type=click.Choice([t.value.lower() for t in TransactionType]),
    help='Transaction type(s) to synchronize'
)
@click.option(
    '--notify',
    is_flag=True,
    type=bool,
    help='To notify upon new transactions'
)
@with_appcontext
def synchronize(address: str, tx_types: list[str], notify: bool):
    if not tx_types:
        tx_types = [tx_type.value for tx_type in TransactionType]
    for tx_type in tx_types:
        SynchronizationService(address).synchronize_by_type(getattr(TransactionType, tx_type.upper()), notify)


@click.command(name='wipe')
@click.option(
    '--tx-type',
    '-t',
    'tx_types',
    multiple=True,
    type=click.Choice([t.value.lower() for t in TransactionType]),
    help='Transaction type(s) to wipe'
)
@click.option('--from-offset', type=int, default=0, help='Wipe all transactions from offset')
def wipe(tx_types: list[str], from_offset: int):
    if not tx_types:
        tx_types = [tx_type.value for tx_type in TransactionType]
    for tx_type in tx_types:

        TransactionService().delete_transactions(getattr(TransactionType, tx_type.upper()), from_offset)


@click.command(name='notify')
@click.option(
    '--tx-id',
    '-t',
    'tx_ids',
    multiple=True,
    type=int,
    help='Transaction id to create a notification for'
)
def notify(tx_ids: list[int]):
    NotificationService().new_notifications_for_tx_ids(tx_ids)
