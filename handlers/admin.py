from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State

from keyboards.keyboards import admin_pannel, tastes_keyboard, type_of_wine
from database.database_commands import ask_data_base, draw_image
import config

router = Router()
#router.message.filter(F.from_user.id == config.ADMIN_ID)

class Admin(StatesGroup):
    wine_taste = State()
    wine_type = State()
    wine_mark = State()
    wine_desc = State()
    wine_photo = State()

@router.message(Command("admin_pannel"))
async def cmd_admin(message: Message):
    await message.answer("Что будем делать?", reply_markup=admin_pannel())

@router.message(F.text == 'Добавить вино')
async def cmd_add_wine(message: Message):
    await message.reply("Какое вино будем добавлять?", reply_markup=tastes_keyboard().as_markup())