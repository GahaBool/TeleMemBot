from aiogram import F, types, Router
from aiogram.filters import Command, or_f
from mysql.connector import connect, Error, errorcode

from MySQL_Query import show_image_from_db, last_id
from dotenv import dotenv_values
import random

#Создал файл специально, что бы можно было работать с личными данными.
#Необходимосоздать свой .env и туда закинуть все необходимы переменные с у которых стоит приписка "config"
#================================================================
config = dotenv_values()

user_group_router = Router()#Фильтрация чатов

#Подключегие к БД
#================================================================
def connection_db():
    try:
        connection = connect(host=config["HOST"],
                             user=config["USER"],
                             password=config["PASSWORD"],
                             db=config["DATABASES"],)
        print("successfully connected...")
        print("################################################################")
    except Error as err:
        print(f"The error '{err}' occurred")
    return connection

connection = connection_db()
CHAT_ID_USERS = 1001541543072

@user_group_router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Hello")


@user_group_router.message(or_f(Command("memes"), (F.text.lower().contains("memes"))))
async def start_cmd(message: types.Message):

    id_image = last_id(connection)
    number = random.randint(1, id_image)
    file_path, description = show_image_from_db(connection, number)

    await message.answer_photo(
        photo=types.FSInputFile(
            path=file_path
        ),
        caption=description
    )
