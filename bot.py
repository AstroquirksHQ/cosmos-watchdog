import structlog

from api.notifications.service import NotificationService
from common.BaseModel import database_proxy
from common.Database import Database
from config import Config
import os
from discord.ext import tasks

import discord
from discord.MessageCrafter import MessageCrafter

TOKEN = "xxxx"
CHANNEL_ID = 1082130614939025439


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = structlog.get_logger(__name__)
        self.init_config()
        self.init_db()
        self.notification_service = NotificationService()

    def init_db(self):
        self.db = Database(self.config.DB)
        database_proxy.initialize(self.db.db_instance)

    def init_config(self):
        env = os.environ.get("ENV", "PROD")
        self.config = Config(env)
        self.logger.info("config", config=self.config)

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        self.logger.info("------")

    @tasks.loop(seconds=3)  # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_channel(CHANNEL_ID)  # channel ID goes here
        notifications = self.notification_service.get_pending_notifications()
        for notification in notifications:
            await channel.send(embed=MessageCrafter(notification).to_card())
            self.notification_service.mark_as_sent(notification)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)
