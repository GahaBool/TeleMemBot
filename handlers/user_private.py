from aiogram import F, types, Router
from aiogram.filters import Command, or_f
from filters.chat_types import ChatTypesFilter

user_private_router = Router()#Фильтрация чатов

CHAT_ID_USERS = 1002001934089

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

from aiogram import F, types, Router
from aiogram.filters import Command, or_f
from mysql.connector import connect, Error, errorcode

from MySQL_Query import show_image_from_db
from dotenv import dotenv_values

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
CHAT_ID_USERS = 1002001934089

@user_private_router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Hello")

@user_private_router.message(or_f(Command("memes"), (F.text.lower().contains("memes"))))
async def start_cmd(message: types.Message):

    file_path, description = show_image_from_db(connection, 2)
    await message.answer_photo(
        photo=types.FSInputFile(
            path=file_path
        ),
        caption=description
    )