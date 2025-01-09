from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.utils.state import load_state
import asyncio

scheduler = AsyncIOScheduler()

async def send_daily_message(bot, chat_id: int, message: str):
    """Отправляет запланированное сообщение."""
    await bot.send_message(chat_id, message)

def schedule_periodic_message(bot, chat_id: int):
    """Настраивает периодические задачи."""

    # Проверка состояния
    if load_state():
        scheduler.add_job(
            lambda: asyncio.run_coroutine_threadsafe(
                send_daily_message(bot, chat_id, "Доброе утро! Обязательно улыбнись разок! 🌞"),
                asyncio.get_event_loop(),
            ),
            CronTrigger(hour=9, minute=0),
        )

        scheduler.add_job(
            lambda: asyncio.run_coroutine_threadsafe(
                send_daily_message(bot, chat_id, "Доброй ночи! Если волчонок не рядом, то не забывай, что он тебя любит! 🌙"),
                asyncio.get_event_loop(),
            ),
            CronTrigger(hour=22, minute=0),
        )

        scheduler.add_job(
            lambda: asyncio.run_coroutine_threadsafe(
                send_daily_message(bot, chat_id, "Напоминаю, скоро пора спать. У тебя самые красивые глаза!🌙"),
                asyncio.get_event_loop(),
            ),
            CronTrigger(hour=20, minute=0),
        )

        scheduler.add_job(
            lambda: asyncio.run_coroutine_threadsafe(
                send_daily_message(bot, chat_id, "Добрый день! Не забывай пить воду! 🌞"),
                asyncio.get_event_loop(),
            ),
            CronTrigger(hour=13, minute=0),
        )

        scheduler.add_job(
            lambda: asyncio.run_coroutine_threadsafe(
                send_daily_message(bot, chat_id, "День почти закончился! Не забудь попить чаю! 🌞"),
                asyncio.get_event_loop(),
            ),
            CronTrigger(hour=18, minute=0),
        )

    scheduler.start()
