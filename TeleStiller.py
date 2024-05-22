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

channel_id = 1002096895063
# Обработчик новых сообщений
@client.on(events.NewMessage(chats=channel_id))
async def handler(event):
    # Извлекаем текст сообщения
    message_text = event.message.message or "No text"

    # Проверяем, есть ли у сообщения медиа в виде фото
    if event.message.photo:
        # Скачиваем медиа-файл асинхронно в файл
        img = await event.message.download_media(file=bytes)
        # Получаем имя файла для сохранения
        img_name = f"{event.message.photo.id}.jpg"

        create_table(connection)#Создание таблицы MeSQL или проверка была ли она создана ранее
        add_new_mem(connection, img, img_name, message_text)#Добавление новой записи в MySQL

        print("Был опублекован новый пост!")#Стандартное термининальное оповищение.

# Запуск клиента
client.start(password=config["PASSOWORD_TG"])#Необходим пароль если у вас влюченеа двухфакторная аутентификация телеграм
client.run_until_disconnected()#Позволяет циклу идти бесконечно
