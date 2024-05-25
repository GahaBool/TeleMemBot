from mysql.connector import connect, Error, errorcode
from PIL import Image

#Основная работа с бд и мемами
#================================================================
def create_table(connection):
    cursor = connection.cursor()
    table = """CREATE TABLE IF NOT EXISTS MEMES (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_path VARCHAR(255),
    image_name VARCHAR(255),
    format VARCHAR(255),
    description TEXT
);"""
    try:
        cursor.execute(table)
    except Error as err:
        print(f"The error '{err}' occurred")


def add_new_mem(connection, imag, image_name, format, text):
    cursor = connection.cursor()
    table = """INSERT INTO MEMES (file_path, image_name, format, description) VALUES (%s, %s, %s, %s);"""
    try:
        cursor.execute(table, (imag, image_name, format, text))
    except Error as err:
        print(f"The error '{err}' occurred")
    connection.commit()


# Функция для показа изображения из БД
def show_image_from_db(connection, img_int):
    try:
        cursor = connection.cursor()
        query_photo = """SELECT file_path, format, description FROM membot.memes WHERE id = (%s);"""
        # Выполняем запрос для поиска пути изображения по ID
        cursor.execute(query_photo, [img_int])
        record = cursor.fetchone()

        if record:
            file_path, format, description = record
            return file_path, format, description  # Возвращаем путь к изображению и описание
        else:
            return None

    except Error as err:
        print("Ошибка при подключении к базе данных: ", err)

def last_id(connection):
    try:
        cursor = connection.cursor()
        query_id = """SELECT MAX(id) FROM membot.memes;"""
        cursor.execute(query_id)
        id_image = cursor.fetchone()[0]

        return id_image

    except Error as e:
        print(f"Ошибка при подключении к MySQL: {e}")
        return None

