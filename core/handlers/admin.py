from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile, CallbackQuery, Message, ReplyKeyboardRemove

from keyboards.keyboards import admin_pannel, type_of_wine, add_wine_confirm
from database.db import insert_blob_to_db, type_dict
from config import ADMIN_ID, AVIALABLE_USERS
from states import Admin, aviable_type_wine 
import io

router = Router()
router.message.filter(F.from_user.id == int(ADMIN_ID))



@router.message(Command("admin_pannel"))
async def cmd_admin(message: Message):
    await message.answer("Что будем делать?", reply_markup=admin_pannel())

@router.message(Command("add_wine"))
async def cmd_add_wine(message: Message, state: FSMContext):
    await state.set_state(Admin.type_of)
    await message.reply(
        "Какое вино будем добавлять?",
        reply_markup=type_of_wine().as_markup())

#Пользователь выбирает состояние - красное\белое\игристое...
@router.callback_query(Admin.type_of, F.data.in_(aviable_type_wine))
async def cmd_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(type_of = callback.data)
    await state.set_state(Admin.name)
    await callback.message.answer(
        "Добавьте параметры вина:\nВведите название:\n *....", reply_markup = ReplyKeyboardRemove())

#Если пользователь введёт не красное\белое и т.д.)
@router.callback_query(StateFilter("Admin.wine_type")) 
async def type_incor(callback: CallbackQuery):
    await callback.message.answer(
        text="Давай попробуем ещё раз.\n\n"
             "Пожалуйста, выберите один вариант из списка ниже:",
        reply_markup=type_of_wine().as_markup())  
      
#Пользователь ПИШЕТ название    
@router.message(Admin.name, F.text)
async def cmd_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Admin.desc)
    await message.answer(
        "Добавьте параметры вина:\n Введите описание вина\n  **...")


@router.message(Admin.desc, F.text)
async def cmd_desc(message: Message, state: FSMContext):
    await state.update_data(desc = message.text)
    await state.set_state(Admin.mark)
    await message.answer(
        "Добавьте параметры вина:\n Введите оценку вина (1-10)\n  ***..")


@router.message(Admin.mark, F.text)
async def cmd_mark(message: Message, state: FSMContext):
    await state.update_data(mark = int(message.text))
    await state.set_state(Admin.photo)
    await message.answer(
        "Добавьте параметры вина:\n Отправьте фото вина\n ****.")
    await message.delete()

@router.message(Admin.photo, F.photo)
async def cmd_photo(message: Message, state: FSMContext):
    await state.update_data(photo = message.photo)
    data = await state.get_data()
    await message.answer_photo(photo=message.photo[-1].file_id, caption=f"""
Добавляем {data['type_of']} вино\n
Названние: {data['name']}\n
Описание: {data['desc']}\n
Оценка: {data['mark']}""",
    reply_markup=add_wine_confirm().as_markup())

@router.callback_query(Admin.photo, F.data == "all_right")
async def cmd_summary(callback: CallbackQuery, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        photo = io.BytesIO()
        await bot.download(data["photo"][-1], destination= photo)
        
        insert_blob_to_db(type_dict[data['type_of']], data['name'], data['mark'],  data['desc'], photo.getvalue())
        await callback.message.answer("Вино добавлено в алко-библиотеку")
    except Exception as err:
        print("Ошибка cmd_summary ", err)
    finally:
        await state.clear()
        photo.close()
        await callback.message.delete()

@router.callback_query(Admin.photo, F.data == "cancel")
async def cmd_summary(callback: CallbackQuery, state: FSMContext, bot: Bot):
        await state.clear()
        await callback.message.delete()
        await callback.message.answer("Добавление фото отменено! \n Что будем делать теперь?",
                                       reply_markup=admin_pannel())
