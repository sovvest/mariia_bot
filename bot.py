import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiohttp import web
from flask import Flask, request

from app.handliers import router
from app.utils.scheduler import schedule_periodic_message
from app.utils.state import load_state

# Flask приложение для webhook
app = Flask(__name__)

BOT_TOKEN = '7565139059:AAGxtTacith93d_OXumn9FB1tH8c5HhexVg'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

dp.include_router(router)

# Ваш ID пользователя
chat_id = 5840918859  
schedule_periodic_message(bot, chat_id)

# Функция обработки вебхуков
@app.route('/webhook/' + BOT_TOKEN, methods=['POST'])
async def handle_webhook():
    json_str = await request.get_data()
    update = Update.de_json(json_str, bot)
    await dp.process_update(update)
    return 'OK'

# Функция для старта вебхуков
async def on_start(request):
    return web.Response(text="Webhook server is running")

async def main():
    # Настройка webhook в Telegram
    await bot.set_webhook('https://your-domain.com/webhook/' + BOT_TOKEN)

    # Запуск Flask-сервера
    app.run(host='0.0.0.0', port=5000)

    # Запуск polling (если необходимо)
    await dp.start_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен')
