import asyncio
from datetime import datetime

import pytest
from discord import Message

from src.bot.message_crafter import MessageCrafter
from src.core.notifications.model import Notification, NotificationStatus
from src.core.transactions.model import Transaction, TransactionType


def timestamp_to_round_datetime(timestamp: str) -> datetime:
    dt = datetime.fromisoformat(timestamp)
    dt = dt.replace(microsecond=0)
    return dt


def message_has_notification_embed(message_with_embed: Message, notification: Notification, author) -> bool:
    try:
        assert message_with_embed.author == author
        expected_embed = MessageCrafter(notification).to_card().to_dict()
        expected_thumbnail = expected_embed.pop("thumbnail")
        expected_timestamp = expected_embed.pop("timestamp")
        assert len(message_with_embed.embeds) == 1
        embed = message_with_embed.embeds[0].to_dict()
        thumbnail = embed.pop("thumbnail")
        timestamp = embed.pop("timestamp")
        print(f"found timestamp of embed == {timestamp}")
        print(f"comparing it to expected timestamp == {expected_timestamp}")
        print(f"Rounded timestamp == {timestamp_to_round_datetime(timestamp)}")
        print(f"Rounded expected_timestamp == {timestamp_to_round_datetime(expected_timestamp)}")

        assert timestamp_to_round_datetime(
            timestamp
        ) == timestamp_to_round_datetime(expected_timestamp)
        assert thumbnail["url"] == expected_thumbnail["url"]
        assert expected_embed == embed
        return True
    except AssertionError:
        return False



@pytest.mark.parametrize("tx_type", [tx_type for tx_type in TransactionType])
@pytest.mark.asyncio
async def test_notification_sent(populate_db, discord_bot, tx_type, discord_bot_config):
    transaction1 = Transaction.select().where(Transaction.type == tx_type.value).first()
    notification = Notification.create(
        transaction=transaction1, status=NotificationStatus.PENDING.value
    )
    print(f"my transaction timestamp == {transaction1.timestamp}")

    # Wait for the bot to send the notification
    # Adjust the sleep time to give the bot enough time to send the notification
    await asyncio.sleep(discord_bot_config.FREQUENCY + 1)
    # Fetch the channel by its ID
    async for client in discord_bot:
        channel = await client.fetch_channel(discord_bot_config.CHANNEL_ID)

        messages = channel.history(limit=10)
        async for message in messages:
            found = 0
            if message_has_notification_embed(message, notification, client.user):
                found = 1
            assert found == 1

        messages = channel.history(limit=10)
        assert any([message_has_notification_embed(message, notification, discord_bot.user) async for message in messages])