from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from aiogram.utils.media_group import MediaGroupBuilder

from keyboards.keyboards import admin_pannel, tastes_keyboard, type_of_wine, wine_name_keyboard
from database.database_commands import ask_data_base, draw_image
from config import ADMIN_ID, aviable_type_wine, aviable_taste_wine

router = Router()
router.message.filter(F.from_user.id == int(ADMIN_ID))

class Admin(StatesGroup):
    taste = State()
    type_of = State()
    name = State()
    desc = State()
    mark = State()
    photo = State()

@router.message(Command("admin_pannel"))
async def cmd_admin(message: Message):
    await message.answer("Что будем делать?", reply_markup=admin_pannel())


@router.message(F.text == 'Добавить вино')
async def cmd_add_wine(message: Message, state: FSMContext):
    await state.set(Admin.taste)
    await message.reply(
        "Какое вино будем добавлять?",
        reply_markup=tastes_keyboard().as_markup())
    

#Пользователь выбирает состояние - вкусное\невкусное
@router.callback_query(Admin.wine_taste, F.data.in_(aviable_taste_wine))
async def cmd_taste(callback: CallbackQuery, state: FSMContext):
    await state.update_data(taste = callback.data)
    await state.set_state(Admin.type_of)
    await callback.message.answer(
        "Добавьте параметры вина: *......", 
        reply_markup=type_of_wine().as_markup())
    
    await callback.message.delete()

#Если пользователь введёт что-то не (Вкусное\Невкусное)
@router.callback_query(StateFilter("Admin.wine_taste")) 
async def taste_incor(callback: CallbackQuery):
    await callback.message.answer(
        text="Давай попробуем ещё раз.\n\n"
             "Пожалуйста, выберите один вариант из списка ниже:",
        reply_markup=type_of_wine().as_markup())
    
#Пользователь выбирает состояние - красное\белое\игристое...
@router.callback_query(Admin.wine_type, F.data.in_(aviable_type_wine))
async def cmd_taste(callback: CallbackQuery, state: FSMContext):
    await state.update_data(type_of = callback.data)
    await callback.message.answer(
        "Добавьте параметры вина: **.....", 
        reply_markup=type_of_wine().as_markup())
    await state.set_state(Admin.wine_name)
    await callback.message.delete()

#Если пользователь введёт не красное\белое и т.д.)
@router.callback_query(StateFilter("Admin.wine_type")) 
async def taste_incor(callback: CallbackQuery):
    await callback.message.answer(
        text="Давай попробуем ещё раз.\n\n"
             "Пожалуйста, выберите один вариант из списка ниже:",
        reply_markup=type_of_wine().as_markup())    
    
@router.message(Admin.wine_name, F.text)
async def cmd_taste(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.message.answer(
        "Добавьте параметры вина: ***....\n\n Введите название вина")

@router.message(Admin.wine_name, F.text)
async def cmd_taste(message: Message, state: FSMContext):
    await state.update_data(desc = message.text)
    await message.message.answer(
        "Добавьте параметры вина: ****...\n\n Введите описание вина")

@router.message(Admin.wine_name, F.text)
async def cmd_taste(message: Message, state: FSMContext):
    await state.update_data(mark = message.text)
    await message.message.answer(
        "Добавьте параметры вина: *****..\n\n Введите оценку вина")
    await state.set_state(Admin.wine_photo)

@router.message(Admin.wine_photo, F.photo)
async def cmd_taste(message: Message, state: FSMContext):
    await state.update_data(photo = message.photo)
    await message.message.answer(
        "Добавьте параметры вина: ******.\n\n Отправьте фото вина")

@router.callback_query() #Эта функция примет кнопку "Добавить" и создаст запрос к базе данных
async def cmd_album(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    album_builder = MediaGroupBuilder(
        caption=user_data["chosen_mark"]+" "+callback.data)
    try:
        for i in ask_data_base(callback.data, user_data["chosen_mark"]):
            album_builder.add(
                type="photo",
                media=BufferedInputFile(draw_image(i[0], i[1]), "image.jpeg"))    
        if album_builder._media == []:
            await callback.message.answer("Такого вина вы ещё не пивали.\n\n{} {}.".format(user_data["chosen_mark"], callback.data))
        else: 
            await callback.message.answer_media_group(
            media=album_builder.build())
    except Exception as err:
        print("Ошибка в функции cmd_album:",err)
    finally:
        await callback.message.delete()
        await state.clear()