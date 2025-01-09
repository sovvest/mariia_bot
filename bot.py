import asyncio
from aiogram import Bot, Dispatcher

from app.handliers import router
from app.utils.scheduler import schedule_periodic_message
from app.utils.state import load_state

async def main():
    bot = Bot(token='7565139059:AAGxtTacith93d_OXumn9FB1tH8c5HhexVg')
    dp = Dispatcher()
    print("Бот запущен...")
    
    dp.include_router(router)

    chat_id = 5840918859  # Ваш ID пользователя

    schedule_periodic_message(bot, chat_id)

    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен')
