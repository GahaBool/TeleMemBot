from mysql.connector import connect, Error, errorcode

#Основная работа с бд и мемами
#================================================================
def create_databases(connection):
    cursor = connection.cursor()
    databeses = """CREATE DATABASE IF NOT EXISTS membot;"""
    try:
        cursor.execute(databeses)
    except Error as err:
        print(f"The error '{err}' occurred")

def create_table(connection):
    cursor = connection.cursor()
    table = """CREATE TABLE IF NOT EXISTS MEMES (
            id INT AUTO_INCREMENT PRIMARY KEY,
            group_id INT,
            file_path TEXT,
            image_name VARCHAR(255),
            format VARCHAR(255),
            description TEXT
        );"""
    try:
        cursor.execute(table)
    except Error as err:
        print(f"The error '{err}' occurred")


def delete_row(connection):
    cursor = connection.cursor()
    delete_query = """
        DELETE FROM MEMES
        WHERE TRIM(description) = '' AND format = 'group';
        """
    cursor.execute(delete_query)
    deleted_rows = cursor.rowcount  # Количество удаленных строк
    connection.commit()  # Необходимо подтвердить изменения
    cursor.close()


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


def get_random_row_id(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT id FROM memes ORDER BY RAND() LIMIT 1;"
        cursor.execute(query)

        # Получаем одну запись
        result = cursor.fetchone()
        cursor.close()

        # Возвращаем полученный id или None, если запись не найдена
        return result[0] if result else None
    except Error as e:
        print(f"Error: {e}")
        return None

