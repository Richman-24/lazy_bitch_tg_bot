from aiogram import Router, F, types
from aiogram.filters import Command
from keyboards.wine_keyboards import tastes_keyboard, type_of_wine


flag = -1
router = Router()

mark_tuple = ('<', '>')
bd_querry = """SELECT photo 
FROM ALCO_BD
WHERE type = {} AND mark {} 5""".format(F.data, mark_tuple[flag])

#кнопка /wine - запускает инлайн клавиатуру !Вкусное-невкусное
@router.message(Command("wine"))
async def cmd_alcho_lib(message: types.Message):
    
    await message.answer(
        "Какое вино вам показать?",
        reply_markup=tastes_keyboard().as_markup()
    )


#Кнопка на инлайн ВКУСНОЕ, убирает старую инлайн и запускает новую с выбором типа вина
@router.callback_query(F.data == "taste")
async def cmd_taste(callback: types.CallbackQuery):
    global flag
    flag = 1
    await callback.message.answer(
        "Инлайн с типом вина, flag = 1", 
        reply_markup=type_of_wine().as_markup())
    #await callback.answer()


#Кнопка на инлайн НЕВКУСНОЕ, убирает старую инлайн и запускает новую с выбором типа вина
@router.callback_query(F.data == "not_taste")
async def cmd_not_taste(callback: types.CallbackQuery):
    global flag
    flag = 0
    await callback.message.answer(
        "Инлайн с типом вина, flag = 0",
        reply_markup=type_of_wine().as_markup())
    #await callback.answer()

#кнопка посылает тип вина, который потом вставляется в запрос к БД
@router.callback_query(F.data == 'red')
@router.callback_query(F.data == 'white')
@router.callback_query(F.data == 'pink')
@router.callback_query(F.data == 'champaign')
@router.callback_query(F.data == 'fruit')
async def cmd_type_of_wine(callback: types.CallbackQuery):
    await callback.message.answer(
        "ЗАПРОС К БД С ТИПОМ ВИНА," + str(callback.data) + "И ФЛАГОМ flag" + str(flag))
    await callback.answer()

"""    image_from_pc = types.FSInputFile("C:\\Proj\\LB_BOT\\alcho-BD\\red-d-1.jpg")
await callback.message.answer_photo(
        image_from_pc,
        caption="Красное, сухое\n !!! ТУТ БУДЕТ АЛЬБОМ ВКУСНЫХ ВИН !!!\n 19 Crimes Cabernet Sauvignon\n\
            Сухое, плотное, мягкое, кислотность невысокая, послевкусие невыраженное\n\
                Оценка: 4/5, FLAG = 1", reply_markup=types.ReplyKeyboardRemove())"""