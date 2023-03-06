from datetime import datetime

import discord
import structlog

from api.notifications.model import Notification
from api.transactions.model import TransactionType


class MessageCrafter:
    def __init__(self, notification: Notification):
        self.notification = notification
        self.logger = structlog.get_logger(__name__)

        self.CARD_BUILDERS = {
            TransactionType.DELEGATE.value: self.to_delegation_card,
            TransactionType.UNDELEGATE.value: self.to_undelegation_card,
            TransactionType.REDELEGATE.value: self.to_redelegation_card,
            TransactionType.UNREDELEGATE.value: self.to_unredelegation_card,
            TransactionType.RESTAKE.value: self.to_restake_card,
        }

    def amount(self, amount: int) -> str:
        return f"**{amount/1000000} $OSMO**"

    def tx_hash_url(self, hash: str) -> str:
        return f"[{hash}](https://www.mintscan.io/osmosis/txs/{hash})"

    def title(self, title: str):
        return title

    def address_url(self, address: str) -> str:
        return f"[{address}](https://www.mintscan.io/osmosis/account/{address})"

    def timestamp(self, timestamp: str) -> datetime:
        return datetime.fromisoformat(timestamp[:-1])

    def to_delegation_card(self):
        tx = self.notification.transaction
        card = discord.Embed(colour=discord.Colour.brand_green(),
                             title=self.title(tx.type),
                             timestamp=self.timestamp(tx.timestamp)
                             )
        card.add_field(name='Delegator', value=self.address_url(tx.delegator), inline=True)
        card.add_field(name='Amount', value=self.amount(tx.amount), inline=True)
        if tx.memo:
            card.add_field(name='Memo', value=tx.memo, inline=False)
        card.add_field(name='Hash', value=self.tx_hash_url(tx.hash), inline=False)
        card.set_thumbnail(url="https://i.imgur.com/KDZDxG1.png")
        return card

    def to_undelegation_card(self):
        tx = self.notification.transaction
        card = discord.Embed(colour=discord.Colour.dark_red(),
                             title=self.title(tx.type),
                             timestamp=self.timestamp(tx.timestamp)
                             )
        card.add_field(name='Delegator', value=self.address_url(tx.delegator), inline=True)
        card.add_field(name='Amount', value=self.amount(-tx.amount), inline=True)
        if tx.memo:
            card.add_field(name='Memo', value=tx.memo, inline=False)
        card.add_field(name='Hash', value=self.tx_hash_url(tx.hash), inline=False)
        card.set_thumbnail(url="https://i.imgur.com/F62aKwZ.png")
        return card

    def to_redelegation_card(self):
        tx = self.notification.transaction
        card = discord.Embed(colour=discord.Colour.dark_green(),
                             title=self.title(tx.type),
                             timestamp=self.timestamp(tx.timestamp)
                             )
        card.add_field(name='Delegator', value=self.address_url(tx.delegator), inline=True)
        card.add_field(name='Amount', value=self.amount(tx.amount), inline=True)
        card.add_field(name='From Validator', value=self.address_url(tx.from_validator), inline=False)
        if tx.memo:
            card.add_field(name='Memo', value=tx.memo, inline=False)
        card.add_field(name='Hash', value=self.tx_hash_url(tx.hash), inline=False)
        card.set_thumbnail(url="https://i.imgur.com/LttJe60.png")
        return card

    def to_unredelegation_card(self):
        tx = self.notification.transaction
        card = discord.Embed(colour=discord.Colour.brand_red(),
                             title=self.title(tx.type),
                             timestamp=self.timestamp(tx.timestamp)
                             )
        card.add_field(name='Delegator', value=self.address_url(tx.delegator), inline=True)
        card.add_field(name='Amount', value=self.amount(tx.amount), inline=True)
        card.add_field(name='To Validator', value=self.address_url(tx.validator), inline=False)
        if tx.memo:
            card.add_field(name='Memo', value=tx.memo, inline=False)
        card.add_field(name='Hash', value=self.tx_hash_url(tx.hash), inline=False)
        card.set_thumbnail(url="https://i.imgur.com/q1rpP83.png")
        return card

    def to_restake_card(self):
        tx = self.notification.transaction
        card = discord.Embed(colour=discord.Colour.green(),
                             title=self.title(tx.type),
                             timestamp=self.timestamp(tx.timestamp)
                             )
        card.add_field(name='Delegator', value=self.address_url(tx.delegator), inline=True)
        card.add_field(name='Amount', value=self.amount(tx.amount), inline=True)
        card.add_field(name='By', value=self.address_url(tx.grantee), inline=False)
        if tx.memo:
            card.add_field(name='Memo', value=tx.memo, inline=False)
        card.add_field(name='Hash', value=self.tx_hash_url(tx.hash), inline=False)
        card.set_thumbnail(url="https://i.imgur.com/hHY9HID.png")
        return card

    def to_card(self):
        tx = self.notification.transaction
        builder = self.CARD_BUILDERS.get(tx.type)
        if builder:
            return builder()
        else:
            self.logger.error(f"Tx type {tx.type} not supported. Card builder not found.")
