from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def tastes_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Вкусное")
    kb.button(text="Невкусное")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def red_or_white_key() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Красное")
    kb.button(text="Белое")
    kb.button(text="Розовое")
    kb.button(text="Игристое")
    kb.button(text="Фруктовое")
    kb.adjust(5)
    return kb.as_markup(resize_keyboard=True)

