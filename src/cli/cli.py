# flake8: noqa: E402

import os
import click
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.bot.discord_bot import DiscordBot
from src.core.notifications.service import NotificationService
from src.core.transactions.model import TransactionType
from src.core.transactions.service import TransactionService
from src.synchronizer.service import SynchronizationService
from src.synchronizer.scheduler import BackgroundTxSynchronizer


@click.group()
def cli():
    pass


@cli.command(name="synchronize")
@click.argument("address")
@click.option(
    "--tx-type",
    "-t",
    "tx_types",
    multiple=True,
    type=click.Choice([t.value.lower() for t in TransactionType]),
    help="Transaction type(s) to synchronize",
)
@click.option(
    "--notify", is_flag=True, type=bool, help="To notify upon new transactions"
)
def synchronize(address: str, tx_types: list[str], notify: bool):
    if not tx_types:
        tx_types = [tx_type.value for tx_type in TransactionType]
    for tx_type in tx_types:
        SynchronizationService(address).synchronize_by_type(
            getattr(TransactionType, tx_type.upper()), notify
        )


@cli.command(name="wipe")
@click.option(
    "--tx-type",
    "-t",
    "tx_types",
    multiple=True,
    type=click.Choice([t.value.lower() for t in TransactionType]),
    help="Transaction type(s) to wipe",
)
@click.option(
    "--from-offset", type=int, default=0, help="Wipe all transactions from offset"
)
def wipe(tx_types: list[str], from_offset: int):
    if not tx_types:
        tx_types = [tx_type.value for tx_type in TransactionType]
    for tx_type in tx_types:
        TransactionService().delete_transactions(
            getattr(TransactionType, tx_type.upper()), from_offset
        )


@cli.command(name="bot")
def bot():
    client = DiscordBot()
    client.run()


@cli.command(name="notify")
@click.option(
    "--tx-id",
    "-t",
    "tx_ids",
    multiple=True,
    type=int,
    help="Transaction id to create a notification for",
)
def notify(tx_ids: list[int]):
    NotificationService().new_notifications_for_tx_ids(tx_ids)


@cli.command(name="start_synchronizer")
def start_synchronizer():
    synchronizer = BackgroundTxSynchronizer()
    synchronizer.start()


if __name__ == "__main__":
    cli()
