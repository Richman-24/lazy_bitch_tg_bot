from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def tastes_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Вкусное",
        callback_data="Вкусное"),
        types.InlineKeyboardButton(
        text="Невкусное",
        callback_data="Невкусное")
    )
    return builder

def type_of_wine() -> ReplyKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(
        text="Красное",
        callback_data="красное"),

        types.InlineKeyboardButton(
        text="Белое",
        callback_data="белое"))

    kb.row(types.InlineKeyboardButton(
        text="Розовое",
        callback_data="розовое"),

        types.InlineKeyboardButton(
        text="Игристое",
        callback_data="игристое"),

        types.InlineKeyboardButton(
        text="Фруктовое",
        callback_data="фруктовое"))
    return kb

#def type_of_wine() -> ReplyKeyboardMarkup:
#    kb = ReplyKeyboardMarkup.row()




def main_keyboards() -> ReplyKeyboardMarkup:
    kb = [[types.KeyboardButton(text = "/wine")], [types.KeyboardButton(text = "/food")]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Чем могу вам помочь?")
    return keyboard

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)