from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def tastes_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Вкусное",
        callback_data="Вкусное"),
        InlineKeyboardButton(
        text="Невкусное",
        callback_data="Невкусное")
    )
    return builder

def type_of_wine() -> ReplyKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(
        text="Красное",
        callback_data="красное"),

        InlineKeyboardButton(
        text="Белое",
        callback_data="белое"))

    kb.row(InlineKeyboardButton(
        text="Розовое",
        callback_data="розовое"),

        InlineKeyboardButton(
        text="Игристое",
        callback_data="игристое"),

        InlineKeyboardButton(
        text="Фруктовое",
        callback_data="фруктовое")
        )
    return kb

#def type_of_wine() -> ReplyKeyboardMarkup:
#    kb = ReplyKeyboardMarkup.row()


def main_keyboards() -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text = "/wine")], [KeyboardButton(text = "/food")]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Чем могу вам помочь?")
    return keyboard

def admin_pannel() -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text = "Добавить вино")]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Чем могу вам помочь?")
    return keyboard

def wine_name_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Запомнить имя",
        callback_data="set_name")
    )
    return builder

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)