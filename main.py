import asyncio
import os

from aiogram import Bot, Dispatcher, types
from mysql.connector import connect, Error, errorcode
from dotenv import dotenv_values

#Создал файл специально, что бы можно было работать с личными данными.
#Необходимосоздать свой .env и туда закинуть все необходимы переменные с у которых стоит приписка "config"
#================================================================
config = dotenv_values()

#Бот aiogram
#================================================================
chat_id = 1002001934089
bot = Bot(config["TOKEN"])
dp = Dispatcher()

async def send_photo():
    try:
        connection = connect(host=config["HOST"],
                             user=config["USER"],
                             password=config["PASSWORD"],
                             db=config["DATABASES"], )
        cursor = connection.cursor()

        # Получаем изображение из базы данных
        cursor.execute("SELECT imag FROM membot WHERE id = %s", (1,))
        image = cursor.fetchone()[0]

        # Отправляем изображение в чат
        await bot.send_photo(chat_id=chat_id, photo=image)

    except Error as e:
        print(f"Ошибка при работе с MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Запуск бота
if __name__ == '__main__':
    asyncio.run(send_photo())