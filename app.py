import datetime

import jinja2
from aiogram import Bot
from fastapi import FastAPI, HTTPException
from starlette.background import BackgroundTasks
from starlette.config import Config

from models import Event
from notifications import TelegramNotificationChannel, notifier


config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=False)
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', cast=str, default='')
TEMPLATES_DIR = config('TEMPLATES_DIR', cast=str, default='templates')
DESTINATION_CHAT_ID = config('DESTINATION_CHAT_ID', cast=str, default='templates')

app = FastAPI(debug=DEBUG)

jinja_loader = jinja2.FileSystemLoader(TEMPLATES_DIR)
jinjaenv = jinja2.Environment(loader=jinja_loader, autoescape=True, enable_async=True)


def iso8601_to_time(value):
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")


def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    return value.strftime(format)


jinjaenv.filters['iso8601_to_time'] = iso8601_to_time
jinjaenv.filters['datetimeformat'] = datetimeformat

bot = Bot(token=TELEGRAM_BOT_TOKEN)

notifier.add_channel(
    TelegramNotificationChannel(
        bot=bot,
        chat_id=DESTINATION_CHAT_ID
    )
)


async def prepare_message_text(event: Event) -> str:
    t = jinjaenv.get_template('alert.j2')
    return await t.render_async(event)


async def handle_event(event: Event) -> None:
    text = await prepare_message_text(event)
    await notifier.notify_all(text)


@app.post('/alert')
async def handle_alert_webhook(event: Event, background_tasks: BackgroundTasks):
    background_tasks.add_task(handle_event, event)
