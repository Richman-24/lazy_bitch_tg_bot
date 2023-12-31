from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def tastes_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Вкусное",
        callback_data="taste"),
        types.InlineKeyboardButton(
        text="Не вкусное",
        callback_data="not_taste")
    )
    return builder

def type_of_wine() -> ReplyKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(
        text="Красное",
        callback_data="red"),

        types.InlineKeyboardButton(
        text="Белое",
        callback_data="white"),

        types.InlineKeyboardButton(
        text="Розовое",
        callback_data="pink"),

        types.InlineKeyboardButton(
        text="Игристое",
        callback_data="champaign"),

        types.InlineKeyboardButton(
        text="Фруктовое",
        callback_data="fruit"))
    return kb

def main_keyboards() -> ReplyKeyboardMarkup:
    kb = [[types.KeyboardButton(text = "/wine")]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Чем могу вам помочь?")
    return keyboard