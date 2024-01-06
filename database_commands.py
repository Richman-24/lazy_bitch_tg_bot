from PIL import Image, ImageDraw, ImageFont
import sqlite3
import io

def draw_image(path: str, mark: int):
    """Функция берёт картинку и оценку, рисует оценку на картинке и возвращает 
    в BLOB формате для записи в БД"""
    with Image.open(path) as im:
        draw_text = ImageDraw.Draw(im)
        font = ImageFont.truetype("C:\Proj\LB_BOT\spaceranger-rus.otf", size=200)
        fill = '#fa0000' if mark < 5 else '#00e600' #определяет цвет заполнителя, в зависимости от оценки 
        
        draw_text.text( #рисуем оценку на картинке
            (50, 50),
            str(mark)+'\\10',
            font=font,
            fill = fill)
    
    
    data = io.BytesIO() #Используем io.BytesIO() как временное хранилище картинки, чтобы не сохранять на диск
    im.save(data, format='jpeg') #Сохраняем в локальном хранилище, в формате jpeg
    return data.getvalue() #Получаем байтовый поток изображения


def insert_blob_to_db(type_wine, title, mark, description, path_photo):
    """Вставляет данные в SQL"""
    try:
        connection = sqlite3.connect('AL_BD\\alcho_db.db')
        cursor = connection.cursor()
        print("Подключен к SQLite")

        insert_query = """INSERT INTO wine_db (type_wine, title, mark, description, photo)
                          VALUES(?, ?, ?, ?, ?)"""

        photo = draw_image(path_photo, mark) #
        # Преобразование данных в формат кортежа
        data_tuple = (type_wine, title, mark, description, photo)
        cursor.execute(insert_query, data_tuple)
        connection.commit()
        print("Изображение и файл успешно вставлены как BLOB в таблицу")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if connection:
            connection.close()
            print("Соединение с SQLite закрыто")

def ask_data_base(wine: str, flag: str):
    """Готовит список из БЛОБ фото по типу вина и оценке (переданных в функцию)"""
    try:
        connection = sqlite3.connect('AL_BD\\alcho_db.db')
        cursor = connection.cursor()
        print("Подключен к alcho_db")
        
        data = list(cursor.execute('SELECT photo FROM wine_db WHERE type_wine == "{}" AND mark {} 5 ORDER BY mark'.format(wine, flag)))
        print("Выполнен запрос")

        return data


    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if connection:
            connection.close()
            print("Соединение с SQLite закрыто")
