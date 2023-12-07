from aiogram import types
from aiogram.types import ChatMemberUpdated
from main import dp, bot
from fsm import *
from keyboard import *
import re


########################################
# Callback handlers / Обрабочтики кнопок
########################################



@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    channel_id = -1002074971755
    await bot.send_message(message.chat.id, 'Привет! Можешь меня попросить о чем-нибудь :)', reply_markup=markup_link)


@dp.callback_query_handler(lambda call: call.data == '/create_link')
async def start_test_one(callback_query: types.CallbackQuery, state: FSMContext):
    channel_id = -1002074971755
    object_link = await bot.create_chat_invite_link(chat_id=channel_id, name=f'{callback_query.from_user.username}', creates_join_request=True)
    invite_link = object_link['invite_link']
    await bot.send_message(callback_query.message.chat.id, f'Твоя пригласительная ссылка: {invite_link}', reply_markup=markup_link)
    await callback_query.answer()




@dp.chat_join_request_handler()
async def on_user_joined(message: types.Message):
    print(message)
