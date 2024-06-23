from PIL import Image, ImageDraw, ImageFont
import sqlite3
import io

flag_dict = {"Вкусное": ">", "Невкусное": "<"}
type_dict = {
    "красное": "red",
    "белое": "white",
    "розовое": "pink",
    "игристое": "champaign",
    "фруктовое": "fruit",
}


def draw_image(photo: str, mark: int):
    """Функция берёт картинку и оценку, рисует оценку на картинке и возвращает
    в BLOB формате для записи в БД"""
    with Image.open(io.BytesIO(photo)) as im:
        draw_text = ImageDraw.Draw(im)
        font = ImageFont.truetype("servises\MonaspaceXenon-Bold.otf", size=150)
        fill = (
            "#fa0000" if mark < 5 else "#00e600"
        )  # определяет цвет заполнителя, в зависимости от оценки

        draw_text.text(  # рисуем оценку на картинке
            (100, 50), str(mark) + "\\10", font=font, fill=fill
        )

    data = (
        io.BytesIO()
    )  # Используем io.BytesIO() как временное хранилище картинки, чтобы не сохранять на диск
    im.save(data, format="jpeg")  # Сохраняем во временном хранилище, в формате jpeg
    return data.getvalue()  # Получаем байтовый поток изображения


def insert_blob_to_db(type_wine, title, mark, description, photo):
    """Вставляет данные в SQL"""
    try:
        connection = sqlite3.connect("db.db")
        cursor = connection.cursor()

        insert_query = """INSERT INTO wine_db (type_wine, title, mark, description, photo)
                          VALUES(?, ?, ?, ?, ?)"""

        data_tuple = (type_wine, title, mark, description, photo)
        cursor.execute(insert_query, data_tuple)
        connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite - insert_blob_to_db", error)
    finally:
        if connection:
            connection.close()


def ask_data_base(wine: str, flag: str):
    """Готовит список из БЛОБ фото по типу вина и оценке (переданных в функцию) и рисует через PIL оценку"""
    try:
        connection = sqlite3.connect("db.db")
        cursor = connection.cursor()

        data = list(
            cursor.execute(
                'SELECT photo, mark FROM wine_db WHERE type_wine == "{}" AND mark {} 5 ORDER BY mark'.format(
                    type_dict[wine], flag_dict[flag]
                )
            )
        )
        print("Выполнен запрос к SQL /Wine")

        return data

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite - ask_data_base", error)
    finally:
        if connection:
            connection.close()
