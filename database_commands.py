from PIL import Image, ImageDraw, ImageFont
import sqlite3
import io

def draw_image(photo: str, mark: int):
    """Функция берёт картинку и оценку, рисует оценку на картинке и возвращает 
    в BLOB формате для записи в БД"""
    b_img = io.BytesIO(photo)
    with Image.open(b_img) as im:
        draw_text = ImageDraw.Draw(im)
        font = ImageFont.truetype("servises\MonaspaceXenon-Bold.otf", size=150)
        fill = '#fa0000' if mark < 5 else '#00e600' #определяет цвет заполнителя, в зависимости от оценки 
        
        draw_text.text( #рисуем оценку на картинке
            (100, 50),
            str(mark)+'\\10',
            font=font,
            fill = fill)
    
    
    data = io.BytesIO() #Используем io.BytesIO() как временное хранилище картинки, чтобы не сохранять на диск
    im.save(data, format='jpeg') #Сохраняем в локальном хранилище, в формате jpeg
    return data.getvalue() #Получаем байтовый поток изображения


def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def insert_blob_to_db(type_wine, title, mark, description, path_photo):
    """Вставляет данные в SQL"""
    try:
        connection = sqlite3.connect('database\\alcho_db.db')
        cursor = connection.cursor()
        #print("Подключен к SQLite")

        insert_query = """INSERT INTO wine_db (type_wine, title, mark, description, photo)
                          VALUES(?, ?, ?, ?, ?)"""
        photo = convert_to_binary_data(path_photo)
        # Преобразование данных в формат кортежа
        data_tuple = (type_wine, title, mark, description, photo)
        cursor.execute(insert_query, data_tuple)
        connection.commit()
        #print("Изображение и файл успешно вставлены как BLOB в таблицу")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite - insert_blob_to_db", error)
    finally:
        if connection:
            connection.close()
            #print("Соединение с SQLite закрыто")

def ask_data_base(wine: str, flag: str):
    """Готовит список из БЛОБ фото по типу вина и оценке (переданных в функцию) и рисует через PIL оценку"""
    try:
        connection = sqlite3.connect('database\\alcho_db.db')
        cursor = connection.cursor()
        #print("Подключен к alcho_db")
        
        data = list(cursor.execute('SELECT photo, mark FROM wine_db WHERE type_wine == "{}" AND mark {} 5 ORDER BY mark'.format(wine, flag)))
        print("Выполнен запрос к SQL /Wine")

        return data


    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite - ask_data_base", error)
    finally:
        if connection:
            connection.close()
            #print("Соединение с SQLite закрыто")
