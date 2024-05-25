import asyncio
import os

from aiogram import Bot, Dispatcher, types
from mysql.connector import connect, Error, errorcode

from dotenv import dotenv_values

from handlers.user_group import user_group_router

#Создал файл специально, что бы можно было работать с личными данными.
#Необходимосоздать свой .env и туда закинуть все необходимы переменные с у которых стоит приписка "config"
#================================================================
config = dotenv_values()

#Бот aiogram
#================================================================
chat_id = 1002001934089
bot = Bot(config["TOKEN"])
dp = Dispatcher()

dp.include_router(user_group_router)

async def telebot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(telebot())