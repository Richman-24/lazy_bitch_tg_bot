import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.methods import DeleteWebhook

from handlers import difirent_types,  ordering_food, wine
from keyboards.keyboards import main_keyboards

dp = Dispatcher()
dp.include_routers(wine.router, difirent_types.router, ordering_food.router)

@dp.message(Command("help"))
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` and '/help' command
    """
    
    await message.answer(f"""Приветствую, {hbold(message.from_user.full_name)}!\n
Это телеграм бот \"Ленивая Сучка\".\n
Он может помочь тебе избавиться от некоторой рутины,\
например поиска информации в АлкоБиблиотеке.
Например попробуем /wine""",
reply_markup=main_keyboards())
#################################################################################
async def main() -> None:

    bot = Bot(getenv("TOKEN"), parse_mode=ParseMode.HTML)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())