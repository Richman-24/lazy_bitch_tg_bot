#from aiogram.filters import BaseFilter
#from aiogram.types import Message
#
#from config import ADMIN_ID


#class isAdmin(BaseFilter):
#    def __init__(self): ...
#
#    async def __call__(self, message: Message) -> bool: #Call - "магический" метод возвращающий булевое(логическое) значение пишем тип возвращаемого значения функции.
#            return message.from_user.id == ADMIN_ID #Если данные совпадают то возвращается True, если нет то False!