from mysql.connector import connect, Error, errorcode

#Основная работа с бд и мемами
#================================================================
def create_table(connection):
    cursor = connection.cursor()
    table = """CREATE TABLE IF NOT EXISTS MEMES (
    id INT AUTO_INCREMENT PRIMARY KEY,
    imag LONGBLOB,
    image_name VARCHAR(255),
    description TEXT);"""
    try:
        cursor.execute(table)
    except Error as err:
        print(f"The error '{err}' occurred")

def add_new_mem(connection, imag, image_name, text):
    cursor = connection.cursor()
    table = """INSERT INTO MEMES (imag, image_name, description) VALUES (%s, %s, %s);"""
    try:
        cursor.execute(table, (imag, image_name, text))
    except Error as err:
        print(f"The error '{err}' occurred")
    connection.commit()

