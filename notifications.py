from abc import ABCMeta, abstractmethod
from typing import Optional, Union, List

from aiogram import Bot


class NotificationChannel(metaclass=ABCMeta):

    @abstractmethod
    def notify(self, text):
        pass


class TelegramNotificationChannel(NotificationChannel):

    def __init__(self,
                 bot: Bot,
                 chat_id: str,
                 parsing_method: str = 'markdown',
                 disable_notification: Optional[bool] = None):
        self.bot = bot
        self.chat_id = chat_id
        self.parsing_method = parsing_method
        self.disable_notification = disable_notification

    async def notify(self, text: str):
        await self.bot.send_message(self.chat_id,
                                    text,
                                    parse_mode=self.parsing_method,
                                    disable_notification=self.disable_notification)


class AutomatedTelegramNotificationChannel(NotificationChannel):
    """
    todo: implement automatic chat id discovery via Chat Service
    """
    pass


class Notifier:
    def __init__(self):
        self.channels: Union[List[NotificationChannel], list] = []

    def add_channel(self, channel: NotificationChannel):
        self.channels.append(channel)

    async def notify_all(self, text):
        for ch in self.channels:
            await ch.notify(text)


notifier = Notifier()
