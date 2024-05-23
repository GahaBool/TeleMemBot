import os
from telethon import TelegramClient, events
from mysql.connector import connect, Error, errorcode
from MySQL_Query import create_table, add_new_mem
from dotenv import dotenv_values

#Создал файл специально, что бы можно было работать с личными данными.
#Необходимосоздать свой .env и туда закинуть все необходимы переменные с у которых стоит приписка "config"
#================================================================
config = dotenv_values()

#Подключение к базам MySQL
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

#Позволяет при получении новых сообщений сохранять карнтинки
#================================================================
#данные для подключения к API client
bot = 'MemBot'
api_id = config["API_ID"]
api_hash = config["API_HASH"]

client = TelegramClient(bot, api_id, api_hash)

channel_id = 1001541543072

SAVE_FOLDER = '\\Project_Python\\TelegramMem\\memes'

# Обработчик новых сообщений
@client.on(events.NewMessage(chats=channel_id))
async def handler(event):
    # Извлекаем текст сообщения
    message_text = event.message.message or "No text"

    # Проверяем, есть ли у сообщения медиа в виде фото
    if event.message.photo:
        # Даем уникальное имя для изображения на основании его ID в Telegram
        img_name = f"{event.message.photo.id}.jpg"
        # Путь, по которому будет сохранено изображение
        img_path = os.path.join(SAVE_FOLDER, img_name)

        # Скачиваем медиа-файл асинхронно и сохраняем на диск
        await event.message.download_media(file=img_path)

        # Вызываем функцию для создания таблицы в MySQL, если она еще не создана
        create_table(connection)
        # Добавляем новую запись в MySQL с путем до картинки, названием и текстом
        add_new_mem(connection, img_path, img_name, message_text)

        print("Был опублекован новый пост!")#Стандартное термининальное оповищение.

# Запуск клиента
client.start(password=config["PASSOWORD_TG"])#Необходим пароль если у вас влюченеа двухфакторная аутентификация телеграм
client.run_until_disconnected()#Позволяет циклу идти бесконечно
