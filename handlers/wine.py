from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import FSInputFile, BufferedInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from keyboards.wine_keyboards import tastes_keyboard, type_of_wine
from database_commands import ask_data_base, image_from_bytes

flag = '>'
router = Router()


#кнопка /wine - запускает инлайн клавиатуру !Вкусное-невкусное
@router.message(Command("wine"))
async def cmd_alcho_lib(message: types.Message):
    
    await message.answer(
        "Какое вино вам показать?",
        reply_markup=tastes_keyboard().as_markup()
    )


#Кнопка на инлайн ВКУСНОЕ|Невкусное, убирает старую инлайн и запускает новую с выбором типа вина
@router.callback_query(F.data == "taste")
@router.callback_query(F.data == "not_taste")
async def cmd_taste(callback: types.CallbackQuery):
    global flag
    flag = (">" if callback.data == 'taste' else "<")
    #print(callback.data)
    await callback.message.answer(
        "Какое вино вам показать?", 
        reply_markup=type_of_wine().as_markup())
    await callback.answer()

#кнопка посылает тип вина, который потом вставляется в запрос к БД
@router.callback_query(F.data == 'red')
@router.callback_query(F.data == 'white')
@router.callback_query(F.data == 'pink')
@router.callback_query(F.data == 'champaign')
@router.callback_query(F.data == 'fruit')
async def cmd_album(callback: types.CallbackQuery):
    album_builder = MediaGroupBuilder(
        caption="Общая подпись для будущего альбома")
    try:
        for i in ask_data_base(callback.data, flag):
            album_builder.add(
                type="photo",
                media=BufferedInputFile(i[0], "image.jpeg"))
            
        await callback.message.answer_media_group(
            media=album_builder.build())
    except Exception as err:
        print("Ошибка в функции cmd_album",err)

'''async def cmd_type_of_wine(callback: types.CallbackQuery):
    bd_querry = """SELECT photo 
    FROM ALCO_BD
    WHERE type = {} AND mark {} 5""".format(callback.data, flag)
    #await callback.message.answer(bd_querry)
    await callback.message.answer
    await callback.answer()
'''   

"""    image_from_pc = types.FSInputFile("C:\\Proj\\LB_BOT\\alcho-BD\\red-d-1.jpg")
await callback.message.answer_photo(
        image_from_pc,
        caption="Красное, сухое\n !!! ТУТ БУДЕТ АЛЬБОМ ВКУСНЫХ ВИН !!!\n 19 Crimes Cabernet Sauvignon\n\
            Сухое, плотное, мягкое, кислотность невысокая, послевкусие невыраженное\n\
                Оценка: 4/5, FLAG = 1", reply_markup=types.ReplyKeyboardRemove())"""



