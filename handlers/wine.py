from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from keyboards.keyboards import tastes_keyboard, type_of_wine
from database_commands import ask_data_base, draw_image

flag = '>'
router = Router()
aviable_taste_wine = ('taste', 'not_taste')
aviable_type_wine = ('red', 'white', 'pink', 'champaign', 'fruit')

#кнопка /wine - запускает инлайн клавиатуру !Вкусное-невкусное
@router.message(Command("wine"))
async def cmd_alcho_lib(message: types.Message):
    
    await message.answer(
        "Какое вино вам показать?",
        reply_markup=tastes_keyboard().as_markup())


#Кнопка на инлайн ВКУСНОЕ|Невкусное, убирает старую инлайн и запускает новую с выбором типа вина
@router.callback_query(F.data.in_(aviable_taste_wine))
async def cmd_taste(callback: types.CallbackQuery):
    global flag
    flag = (">" if callback.data == 'taste' else "<")
    #print(callback.data)
    await callback.message.answer(
        "Какое вино вам показать?", 
        reply_markup=type_of_wine().as_markup())
    await callback.answer()


#кнопка посылает тип вина, который потом вставляется в запрос к БД
@router.callback_query(F.data.in_(aviable_type_wine))
async def cmd_album(callback: types.CallbackQuery):
    type_vine = "Вкусное" if flag == ">" else "Невкусное"
    album_builder = MediaGroupBuilder(
        caption=type_vine+" "+callback.data)
    try:
        for i in ask_data_base(callback.data, flag):
            album_builder.add(
                type="photo",
                media=BufferedInputFile(draw_image(i[0], i[1]), "image.jpeg"))    
        if album_builder._media == []:
            await callback.message.answer("Такого вина вы ещё не пивали.\n\n"+ type_vine+" "+callback.data)
        else: 
            await callback.message.answer_media_group(
            media=album_builder.build())
    except Exception as err:
        print("Ошибка в функции cmd_album:",err)