from aiogram.fsm.state import StatesGroup, State


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()

class Admin(StatesGroup):
    type_of = State()
    name = State()
    desc = State()
    mark = State()
    photo = State()

class Wine(StatesGroup):
    choosing_wine_mark = State()
    choosing_wine_type = State()
    
aviable_taste_wine = ('Вкусное', 'Невкусное')
aviable_type_wine = ('красное', 'белое', 'розовое', 'игристое', 'фруктовое')