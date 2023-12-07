import datetime
from time import sleep
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
from fsm import *
from config import token_bot
import sys


bot = Bot(token=token_bot)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    from handlers import dp
    print("Bot pooling")
    executor.start_polling(dp)
