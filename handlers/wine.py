from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from aiogram.utils.media_group import MediaGroupBuilder

from keyboards.keyboards import tastes_keyboard, type_of_wine
from database.database_commands import ask_data_base, draw_image


router = Router()

aviable_taste_wine = ('Вкусное', 'Невкусное')
aviable_type_wine = ('красное', 'белое', 'розовое', 'игристое', 'фруктовое')

class Wine(StatesGroup):
    choosing_wine_mark = State()
    choosing_wine_type = State()

#кнопка /wine - запускает инлайн клавиатуру !Вкусное-невкусное
@router.message(Command("wine"))
async def cmd_wine(message: Message, state: FSMContext):
    
    await message.answer(
        "Какое вино вам показать?",
        reply_markup=tastes_keyboard().as_markup())
    
    await state.set_state(Wine.choosing_wine_mark)

#Кнопка на инлайн ВКУСНОЕ|Невкусное, убирает старую инлайн и запускает новую с выбором типа вина
@router.callback_query(Wine.choosing_wine_mark, F.data.in_(aviable_taste_wine))
async def cmd_taste(callback: CallbackQuery, state: FSMContext):
    await state.update_data(chosen_mark= callback.data)
    #print(callback.data)
    await callback.message.answer(
        "Какое вино вам показать?", 
        reply_markup=type_of_wine().as_markup())
    await state.set_state(Wine.choosing_wine_type)
    await callback.message.delete()

#Если пользователь введёт что-то не (Вкусное\Невкусное)
@router.callback_query(StateFilter("Wine:choosing_wine_mark")) 
async def mark_chosen_incorrectly(callback: CallbackQuery):
    await callback.message.answer(
        text="Давай попробуем ещё раз.\n\n"
             "Пожалуйста, выберите один вариант из списка ниже:",
        reply_markup=tastes_keyboard().as_markup())

#кнопка посылает тип вина, который потом вставляется в запрос к БД
@router.callback_query(Wine.choosing_wine_type, F.data.in_(aviable_type_wine))
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

@router.message(StateFilter("Wine:choosing_wine_type")) #Если пользователен введёт несуществующий тип.
async def type_wine_chosen_incorrectly(callback: CallbackQuery):
    await callback.message.answer(
        text="Я не знаю вида вина.\n\n"
             "Пожалуйста, выберите вариант из списка ниже:",
        reply_markup=tastes_keyboard().as_markup()
    )