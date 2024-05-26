from aiogram import F, types, Router
from aiogram.filters import Command, or_f
from mysql.connector import connect, Error, errorcode

from MySQL_Query import show_image_from_db, get_random_row_id
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

#Начальная команда
#================================================================
@user_group_router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Hello")

#Обработка событий
#================================================================
@user_group_router.message(or_f(Command("memes"), (F.text.lower().contains("memes"))))
async def random_mem(message: types.Message):

    number = get_random_row_id(connection)
    file_path, format, description = show_image_from_db(connection, number)

    if format == "group":
        media_files = file_path.split(',')  # Пути к файлам
        media_group = []

        # Описание применяется только к первому элементу группы, другие элементы не получают описание
        first_element = True

        for file_path in media_files:
            if file_path.endswith('.mp4'):  # Для видеофайлов
                media = types.InputMediaPhoto(media=types.FSInputFile(file_path))
            else:  # Для фотографий (предполагается, что все остальное - фотографии)
                media = types.InputMediaPhoto(media=types.FSInputFile(file_path))

            # Добавляем описание только к первому элементу
            if first_element:
                media.caption = description
                first_element = False

            media_group.append(media)

        await message.answer_media_group(media=media_group)

    elif format == "video":
        print("Видео!")
        await message.answer_video(video=types.FSInputFile(path=file_path), caption=description)
    elif format == "gif":
        await message.answer_animation(gif=types.FSInputFile(path=file_path), caption=description)
    elif format == "jpg":
        await message.answer_photo(photo=types.FSInputFile(path=file_path),caption=description)
    else:
        print("Такого формат не поддерживается!")