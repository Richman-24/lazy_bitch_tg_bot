from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from keyboards.keyboards import tastes_keyboard, type_of_wine
from database_commands import ask_data_base, draw_image

router = Router()