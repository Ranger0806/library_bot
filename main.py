from aiogram import Bot, Dispatcher
import logging
import asyncio
from handlers import hello_handler, get_book_handler, admin_load_handler
from Config import *

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(hello_handler.router, get_book_handler.router, admin_load_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())