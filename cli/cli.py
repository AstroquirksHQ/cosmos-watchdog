from typing import Optional

import click
from flask.cli import with_appcontext

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
@with_appcontext
def synchronize(address: str, tx_types: list[str]):
    if not tx_types:
        tx_types = [tx_type.value for tx_type in TransactionType]
    for tx_type in tx_types:
        SynchronizationService(address).synchronize_by_type(getattr(TransactionType, tx_type.upper()))


@click.command(name='wipe')
@click.option(
    '--tx-type',
    '-t',
    'tx_types',
    multiple=True,
    type=click.Choice([t.value.lower() for t in TransactionType]),
    help='Transaction type(s) to wipe'
)
@click.option('--from-offset', type=int, help='Wipe all transactions from offset')
def wipe(tx_types: list[str], from_offset: Optional[int]):
    if not tx_types:
        tx_types = [tx_type.value for tx_type in TransactionType]
    for tx_type in tx_types:
        TransactionService().delete_transactions(getattr(TransactionType, tx_type.upper()), from_offset)
