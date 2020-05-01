import datetime
from typing import List
import asyncio

import jinja2
from aiogram import Bot
from fastapi import FastAPI, Header, Response

from starlette.background import BackgroundTasks
from starlette.config import Config
from aioprometheus import render, Counter, Registry, Gauge

from models import Event, Health
from notifications import TelegramNotificationChannel, notifier

config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=False)
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', cast=str, default='')
TEMPLATES_DIR = config('TEMPLATES_DIR', cast=str, default='templates')
DESTINATION_CHAT_ID = config('DESTINATION_CHAT_ID', cast=str, default='')

app = FastAPI(debug=DEBUG)
app.registry = Registry()

app.request_counter = Counter("amtg_total_requests", "Number of requests to endpoints")
app.bot_activity = Gauge("amtg_telegram_bot_active", "Flag that indicates is bot active or not")

app.registry.register(app.request_counter)
app.registry.register(app.bot_activity)


jinja_loader = jinja2.FileSystemLoader(TEMPLATES_DIR)
jinjaenv = jinja2.Environment(loader=jinja_loader, autoescape=True, enable_async=True)


async def datetimeformat(value: str):
    dtms, tz = value.split('+')
    dt, _ = dtms.split('.')
    return datetime.datetime.fromisoformat(f'{dt}.000+{tz}').strftime('%Y-%m-%d %H:%M:%S')


jinjaenv.filters['datetimeformat'] = datetimeformat

bot = Bot(token=TELEGRAM_BOT_TOKEN)

notifier.add_channel(
    TelegramNotificationChannel(
        bot=bot,
        chat_id=DESTINATION_CHAT_ID
    )
)


async def update_bot_status():

    is_active = 1

    while True:
        try:
            user = await bot.get_me()
        except Exception:
            is_active = 0

        app.bot_activity.set({}, is_active)
        await asyncio.sleep(30)


@app.on_event("startup")
async def startup_event():

    loop = asyncio.get_event_loop()
    loop.create_task(update_bot_status())


async def prepare_message_text(event: Event) -> str:
    t = jinjaenv.get_template('alert.j2')
    return await t.render_async(event)


async def handle_event(event: Event) -> None:
    text = await prepare_message_text(event)
    await notifier.notify_all(text)


@app.post('/alert')
async def handle_alert_webhook(event: Event, background_tasks: BackgroundTasks):
    app.request_counter.inc({"path": "/alert"})
    background_tasks.add_task(handle_event, event)


@app.get('/__health', response_model=Health)
async def health_check():
    app.request_counter.inc({"path": "/__health"})
    return {
        'datetime': datetime.datetime.now(),
        'status': 'ok',
    }


@app.get("/metrics")
async def handle_metrics(accept: List[str] = Header(None)):
    content, http_headers = render(app.registry, accept)
    return Response(content=content, media_type=http_headers["Content-Type"])
