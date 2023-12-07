from aiogram import types
from aiogram.types import ChatMemberUpdated
from aiogram.dispatcher.filters import Text
from main import dp, bot
from fsm import *
from keyboard import *
import re
from data import db


########################################
# Callback handlers / Обрабочтики кнопок
########################################


@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    channel_id = -1002074971755
    username = message.from_user.username
    is_instance = db.select_partner(username)
    if not is_instance:
        object_link = await bot.create_chat_invite_link(chat_id=channel_id, name=username, creates_join_request=True)
        invite_link = object_link['invite_link']
        db.insert_partner(username, invite_link)
        await bot.send_message(message.chat.id, f'Привет! Вот твоя реферальная ссылочка, надеюсь ты пригласишь много людей:)\n{invite_link}', reply_markup=main_menu_markup)
    else:
        invite_link = db.select_link(username)[0]
        await bot.send_message(message.chat.id, f'Привет, кажется ты уже получал у меня ссылку. Кстати вот она: {invite_link}', reply_markup=main_menu_markup)


@dp.message_handler(Text(equals='Магазин'))
async def response_shop(message: types.Message):
    await bot.send_message(message.chat.id, 'Выбери, что хочешь приобрести, скорлупа ;)', reply_markup=markup_shop)


@dp.message_handler(Text(equals='Рефералы'))
async def response_ref(message: types.Message):
    await bot.send_message(message.chat.id, 'Ваш баланс __ рефералов\nВсего приглашённых рефералов __\n'
                                            'Приглашенных сегодня __\nВаша реферальная ссылка __')


@dp.message_handler(Text(equals='Топ'))
async def response_top(message: types.Message):
    await bot.send_message(message.chat.id, 'Здесь будет топчик по приглосам потом. Из бд подтянется')


@dp.message_handler(Text(equals='Инфо'))
async def response_info(message: types.Message):
    await bot.send_message(message.chat.id, 'Рефералы - это люди, которых вы пригласили в наш канал по своей реферальной ссылке'
                                            'и они подписались. За приглашенных рефералов можно покупать различные привелегии.')


@dp.callback_query_handler(lambda call: call.data == '/create_link')
async def start_test_one(callback_query: types.CallbackQuery, state: FSMContext):
    channel_id = -1002074971755
    object_link = await bot.create_chat_invite_link(chat_id=channel_id, name=f'{callback_query.from_user.username}', creates_join_request=True)
    invite_link = object_link['invite_link']
    await bot.send_message(callback_query.message.chat.id, f'Твоя пригласительная ссылка: {invite_link}', reply_markup=markup_link)
    await callback_query.answer()


@dp.chat_join_request_handler()
async def on_user_joined(update: types.ChatJoinRequest):
    invite_link = update['invite_link']['invite_link']
    name_user = update['from']['first_name']
    name_partner = db.get_partner(invite_link)[0]
    ref_balance = db.select_ref_balance(name_partner)[0]
    all_ref = db.select_all_ref(name_partner)[0]
    db.update_ref_balance(name_partner, ref_balance+1)
    db.update_all_ref(name_partner, all_ref+1)

    await update.approve()
    
    is_instance = db.select_user(name_user)
    if not is_instance:
        db.insert_user(name_user, name_partner, 1)
    else:
        pass

    print(ref_balance)
    print(all_ref)
