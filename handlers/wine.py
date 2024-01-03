from aiogram import Router, F, types
from aiogram.filters import Command
#from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.alcho_lab import tastes_keyboard

router = Router()


@router.message(F.text.lower() == "да")
async def answer_yes(message: types.Message):
    await message.answer(
        "Это здорово!",
        reply_markup=types.ReplyKeyboardRemove()
    )

@router.message(F.text.lower() == "нет")
async def answer_no(message: types.Message):
    await message.answer(
        "Жаль...",
        reply_markup=types.ReplyKeyboardRemove()
    )
######################################################################
@router.message(Command("alcho_lib"))
async def cmd_alcho_lab(message: types.Message):
    await message.answer("Какое вино вам показать?",
        reply_markup=tastes_keyboard()
    )

@router.message(F.text.lower() == "вкусное")
async def with_puree(message: types.Message):
    image_from_pc = types.FSInputFile("C:\\Proj\\LB_BOT\\alcho-BD\\red-d-1.jpg")
    await message.answer_photo(
        image_from_pc,
        caption="Красное, сухое\n 19 Crimes Cabernet Sauvignon\n\
            Сухое, плотное, мягкое, кислотность невысокая, послевкусие невыраженное\n\
                Оценка: 4/5",
        reply_markup=types.ReplyKeyboardRemove())


@router.message(F.text.lower() == "не вкусное")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!", reply_markup=types.ReplyKeyboardRemove())
    