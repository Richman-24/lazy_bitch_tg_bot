from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from aiogram.utils.media_group import MediaGroupBuilder

from keyboards.keyboards import tastes_keyboard, type_of_wine
from database.db import ask_data_base, draw_image
from config import AVIALABLE_USERS
from states import Wine,  aviable_taste_wine, aviable_type_wine

router = Router()
router.message.filter(F.from_user.id.in_(AVIALABLE_USERS))
router.callback_query.filter(F.from_user.id.in_(AVIALABLE_USERS))





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
    try:
        data = ask_data_base(callback.data, user_data["chosen_mark"])
        if data:
            cnt = 0
            album_builder = MediaGroupBuilder(
                    caption=user_data["chosen_mark"]+" "+callback.data)
            for i in data:
                album_builder.add(
                        type="photo",
                        media=BufferedInputFile(draw_image(i[0], i[1]), "image.jpeg"))
                cnt +=1
                if cnt < 10: #контролирует, чтобы не посадить больше, чем есть мест
                    pass
                else: 
                    await callback.message.answer_media_group(
                        media=album_builder.build())
                    album_builder = MediaGroupBuilder(
                        caption=user_data["chosen_mark"]+" "+callback.data)
                    cnt = 0            
            try:
                await callback.message.answer_media_group(
                        media=album_builder.build())
            except Exception as err: 
                print(f"Ошибка в cmd_album - пустой альбом", err)
        else:
            await callback.message.answer("Такого вина вы ещё не пивали.\n\n{} {}.".format(user_data["chosen_mark"], callback.data))

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
