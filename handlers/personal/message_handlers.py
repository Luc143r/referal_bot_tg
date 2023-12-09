from aiogram import types
from aiogram.types import ChatMemberUpdated
from aiogram.dispatcher.filters import Text
from main import dp, bot
from fsm import *
from keyboard import *
import re
from data import db
from datetime import datetime


########################################
# Callback handlers / Обрабочтики кнопок
########################################


@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    print(message.from_id)
    channel_id = -1002074971755
    username = message.from_user.username
    user_id = message.from_id
    if user_id:
        is_instance = db.select_partner(user_id)
        if not is_instance:
            object_link = await bot.create_chat_invite_link(chat_id=channel_id, name=username, creates_join_request=True)
            invite_link = object_link['invite_link']
            db.insert_partner(user_id, username, invite_link)
            await bot.send_message(message.chat.id, f'Привет! Вот твоя реферальная ссылочка, надеюсь ты пригласишь много людей:)\n{invite_link}', reply_markup=main_menu_markup)
        else:
            invite_link = db.select_link(user_id)[0]
            await bot.send_message(message.chat.id, f'Привет, кажется ты уже получал у меня ссылку. Кстати вот она: {invite_link}', reply_markup=main_menu_markup)
    else:
        await bot.send_message(message.chat.id, 'Привет. Укажи пожалуйста свой username в настройках телеграма, чтобы я мог привязать к тебе твою реферальную ссылку :)', reply_markup=main_menu_markup)


@dp.message_handler(Text(equals='Магазин'))
async def response_shop(message: types.Message):
    await bot.send_message(message.chat.id, 'Выбери, что хочешь приобрести, скорлупа ;)', reply_markup=markup_shop)


@dp.message_handler(Text(equals='Рефералы'))
async def response_ref(message: types.Message):
    username = message.from_user.username
    user_id = message.from_id
    today_date = datetime.today().strftime('%d-%m-%Y')
    if user_id:
        is_instance = db.select_partner(user_id)
        if is_instance:
            ref_balance = db.select_ref_balance(user_id)[0]
            all_ref = db.select_all_ref(user_id)[0]
            ref_today = db.select_user_on_date(user_id, today_date)
            ref_link = db.select_link(user_id)[0]
            await bot.send_message(message.chat.id, f'Ваш баланс - {ref_balance} рефералов\nВсего приглашённых рефералов - {all_ref}\n'
                                                    f'Приглашенных сегодня - {ref_today}\nВаша реферальная ссылка - {ref_link}')
        else:
            pass
    else:
        pass


@dp.message_handler(Text(equals='Топ'))
async def response_top(message: types.Message):
    await bot.send_message(message.chat.id, 'Здесь будет топчик по приглосам потом. Из бд подтянется')


@dp.message_handler(Text(equals='Инфо'))
async def response_info(message: types.Message):
    await bot.send_message(message.chat.id, 'Рефералы - это люди, которых вы пригласили в наш канал по своей реферальной ссылке'
                                            'и они подписались. За приглашенных рефералов можно покупать различные привелегии.')


'''@dp.callback_query_handler(lambda call: call.data == '/create_link')
async def start_test_one(callback_query: types.CallbackQuery, state: FSMContext):
    channel_id = -1002074971755
    object_link = await bot.create_chat_invite_link(chat_id=channel_id, name=f'{callback_query.from_user.username}', creates_join_request=True)
    invite_link = object_link['invite_link']
    await bot.send_message(callback_query.message.chat.id, f'Твоя пригласительная ссылка: {invite_link}', reply_markup=markup_link)
    await callback_query.answer()'''


@dp.chat_join_request_handler()
async def on_user_joined(update: types.ChatJoinRequest):
    invite_link = update['invite_link']['invite_link']
    user_id = update['from']['id']
    username = update['from']['username']
    id_partner = db.get_partner(invite_link)[0]
    ref_balance = db.select_ref_balance(id_partner)[0]
    all_ref = db.select_all_ref(id_partner)[0]

    await update.approve()

    is_instance = db.select_user(user_id)
    if not is_instance:
        today_date = datetime.today().strftime('%d-%m-%Y')
        db.insert_user(user_id, id_partner, today_date)
        db.update_ref_balance(id_partner, ref_balance+1)
        db.update_all_ref(id_partner, all_ref+1)
    else:
        pass

    print(ref_balance)
    print(all_ref)
