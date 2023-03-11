import asyncio
from datetime import datetime

import pytest

from src.bot.message_crafter import MessageCrafter
from src.core.notifications.model import Notification, NotificationStatus
from src.core.transactions.model import Transaction, TransactionType


def timestamp_to_round_datetime(timestamp: str) -> datetime:
    dt = datetime.fromisoformat(timestamp)
    dt = dt.replace(microsecond=0)
    return dt


@pytest.mark.parametrize("tx_type", [tx_type for tx_type in TransactionType])
@pytest.mark.asyncio
async def test_notification_sent(populate_db, discord_bot, tx_type, discord_bot_config):
    transaction1 = Transaction.select().where(Transaction.type == tx_type.value).first()
    notification = Notification.create(
        transaction=transaction1, status=NotificationStatus.PENDING.value
    )

    expected_embed = MessageCrafter(notification).to_card().to_dict()
    expected_thumbnail = expected_embed.pop("thumbnail")
    expected_timestamp = expected_embed.pop("timestamp")

    # Wait for the bot to send the notification
    # Adjust the sleep time to give the bot enough time to send the notification
    await asyncio.sleep(discord_bot_config.FREQUENCY + 1)
    # Fetch the channel by its ID
    async for client in discord_bot:
        channel = await client.fetch_channel(discord_bot_config.CHANNEL_ID)

        messages = channel.history(limit=1)
        async for message in messages:
            assert len(message.embeds) == 1
            embed = message.embeds[0].to_dict()
            thumbnail = embed.pop("thumbnail")
            timestamp = embed.pop("timestamp")
            assert message.author == client.user
            assert timestamp_to_round_datetime(
                timestamp
            ) == timestamp_to_round_datetime(expected_timestamp)
            assert thumbnail["url"] == expected_thumbnail["url"]
            assert expected_embed == embed