import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.methods import DeleteWebhook

TOKEN = getenv("TOKEN")
dp = Dispatcher()

@dp.message(Command("help"))
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"""Приветствую, {hbold(message.from_user.full_name)}!\n
Это телеграм бот \"Ленивая Сучка\".\n
Он может помочь тебе избавиться от некоторой рутины,\
например поиска информации в АлкоБиблиотеке.
Например попробуем /alcho_lab""")

@dp.message(Command("alcho_lab"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Вкусное"),
            types.KeyboardButton(text="Не вкусное")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбирете тип вина"
    )
    await message.answer("Какое вино вам показать?", reply_markup=keyboard)

@dp.message(F.text.lower() == "вкусное")
async def with_puree(message: types.Message):
    file_ids = []
    image_from_pc = FSInputFile("C:\\Proj\\LB_BOT\\alcho-BD\\red-d-1.jpg")
    result = await message.answer_photo(
        image_from_pc,
        caption="Красное, сухое\n 19 Crimes Cabernet Sauvignon\n\
            Сухое, плотное, мягкое, кислотность невысокая, послевкусие невыраженное\n\
                Оценка: 4/5",
        reply_markup=types.ReplyKeyboardRemove())
    file_ids.append(result.photo[-1].file_id)


@dp.message(F.text.lower() == "не вкусное")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!", reply_markup=types.ReplyKeyboardRemove())
    
@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        await message.answer(f'Ты молодец!')
       # await message.reply(f'Вы написали {message.text}')
        #await bot.send_message(message.from_user.id, f'Вы написали {message.text}')
    except TypeError:
        await message.answer("Nice try!")

#################################################################################
async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await bot(DeleteWebhook(drop_pending_updates=True))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())