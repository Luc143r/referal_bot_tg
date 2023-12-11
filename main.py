from datetime import datetime
import logging
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ChatMemberUpdated
from aiogram import Bot, types
from keyboard import *
from data import db
from fsm import *
from config import token_bot
import sys


bot = Bot(token=token_bot)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)


async def sheduler():
    print('Timer started')
    while True:
        current_date = str(datetime.now().time())[:5]
        if current_date != '00:00':
            await asyncio.sleep(60)
        elif current_date == '00:00':
            today = datetime.today().strftime('%d-%m-%Y')
            result = db.select_count_ref_today(today)
            hash_ref = sorted(result, key=lambda d: d[1], reverse=True)

            top_ref = []
            print('Пошла рассылка')
            for i in range(len(hash_ref)):
                if i == 0:
                    try:
                        top_ref.append(f'@{hash_ref[i][0]}: {hash_ref[i][1]}')
                        user_id = db.select_partner_id(hash_ref[i][0])[0]
                        print(hash_ref[i][0])
                        print(user_id)
                        await bot.send_message(user_id, 'Вам начислено RU за место в топе. Накопите 200 RU и сможете вывести их на карту')
                        balance = db.select_balance(user_id)
                        db.update_balance(user_id, balance[0]+40)
                    except:
                        print('Такого пользователя не было найдено в базе')
                elif i == 1:
                    try:
                        top_ref.append(f'@{hash_ref[i][0]}: {hash_ref[i][1]}')
                        user_id = db.select_partner_id(hash_ref[i][0])[0]
                        print(hash_ref[i][0])
                        print(user_id)
                        await bot.send_message(user_id, 'Вам начислено RU за место в топе. Накопите 200 RU и сможете вывести их на карту')
                        balance = db.select_balance(user_id)
                        db.update_balance(user_id, balance[0]+30)
                    except:
                        print('Такого пользователя не было найдено в базе')
                elif i >= 2 and i <= 6:
                    try:
                        top_ref.append(f'@{hash_ref[i][0]}: {hash_ref[i][1]}')
                        user_id = db.select_partner_id(hash_ref[i][0])[0]
                        print(hash_ref[i][0])
                        print(user_id)
                        await bot.send_message(user_id, 'Вам начислено RU за место в топе. Накопите 200 RU и сможете вывести их на карту')
                        balance = db.select_balance(user_id)
                        db.update_balance(user_id, balance[0]+20)
                    except:
                        print('Такого пользователя не было найдено в базе')
                elif i >= 7 and i <= 9:
                    try:
                        top_ref.append(f'@{hash_ref[i][0]}: {hash_ref[i][1]}')
                        user_id = db.select_partner_id(hash_ref[i][0])[0]
                        print(hash_ref[i][0])
                        print(user_id)
                        await bot.send_message(user_id, 'Вам начислено RU за место в топе. Накопите 200 RU и сможете вывести их на карту')
                        balance = db.select_balance(user_id)
                        db.update_balance(user_id, balance[0]+10)
                    except:
                        print('Такого пользователя не было найдено в базе')
                else:
                    break
            await asyncio.sleep(60)

if __name__ == '__main__':
    from handlers import dp
    loop = asyncio.get_event_loop()
    loop.create_task(sheduler())
    print("Bot pooling")
    executor.start_polling(dp)
