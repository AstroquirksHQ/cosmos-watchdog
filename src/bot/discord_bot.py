import asyncio
import os

from discord import Client, Intents
from discord.ext import tasks
import structlog

from src.bot.config.service import BotConfigService
from src.bot.message_crafter import MessageCrafter
from src.core.common.database.context import database_context
from src.core.notifications.service import NotificationService


@database_context
class DiscordBot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **dict(*kwargs, intents=Intents.default()))
        self.logger = structlog.get_logger(__name__).bind(
            service=self.__class__.__name__
        )
        self.notification_service = NotificationService()
        self.config = self.init_config()

    def init_config(self):
        env = os.environ.get("ENV", "PROD")
        config = BotConfigService(env, file="config.yml").get_config()
        self.logger.info("config", **config.to_dict())
        return config

    def run(self, **kwargs) -> None:
        return super().run(self.config.TOKEN, **kwargs)

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        self.logger.info("------")

    @tasks.loop()  # task runs every 3 seconds
    async def my_background_task(self):
        self.logger.info(f"Waiting {self.config.FREQUENCY} seconds ...")
        await asyncio.sleep(self.config.FREQUENCY)
        channel = self.get_channel(self.config.CHANNEL_ID)  # channel ID goes here
        notifications = self.notification_service.get_pending_notifications()
        for notification in notifications:
            card = MessageCrafter(notification).to_card()
            if card:
                await channel.send(embed=card)
                self.notification_service.mark_as_sent(notification)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in
