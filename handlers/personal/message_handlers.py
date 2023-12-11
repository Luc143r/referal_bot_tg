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
            await bot.send_message(message.chat.id, f'Привет! Вот твоя реферальная ссылочка, '
                                                    f'надеюсь ты пригласишь много людей:)\n{invite_link}', reply_markup=main_menu_markup)
        else:
            invite_link = db.select_link(user_id)[0]
            await bot.send_message(message.chat.id, f'Привет, кажется ты уже получал у меня ссылку. '
                                                    f'Кстати вот она: {invite_link}', reply_markup=main_menu_markup)
    else:
        await bot.send_message(message.chat.id, 'Привет. Укажи пожалуйста свой username в настройках телеграма, '
                                                'чтобы я мог привязать к тебе твою реферальную ссылку :)', reply_markup=main_menu_markup)


@dp.message_handler(Text(equals='Магазин'))
async def response_shop(message: types.Message):
    user_id = message.from_id
    ref_balance = db.select_ref_balance(user_id)[0]
    await bot.send_message(message.chat.id, f'Ваш баланс: {ref_balance} рефералов\nФильм/серия '
                                            '- 10 рефералов\nРеклама на канале - 200 рефералов\n\n'
                                            'Вывести деньги на карту - 200RU', reply_markup=markup_shop)

    #db.update_ref_balance(user_id, 205)


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
    top = []
    today = datetime.today().strftime('%d-%m-%Y')
    users = db.select_all_users_today(today)
    if not users:
        await bot.send_message(message.chat.id, 'Сегодня пока никто еще никого не пригласил :(')
    else:
        result = db.select_count_ref_today(today)
        hash_ref = sorted(result, key=lambda d: d[1], reverse=True)
        top_ref = []
        for i in range(len(hash_ref)):
            if i <= 9:
                top_ref.append(f'{i+1}. @{hash_ref[i][0]}: {hash_ref[i][1]}')
            else:
                return
        top_ref = '\n'.join(top_ref)
        await bot.send_message(message.chat.id, f'Топ 10 сегодня по приглашениям:\n{top_ref}')


@dp.message_handler(Text(equals='Инфо'))
async def response_info(message: types.Message):
    await bot.send_message(message.chat.id, 'Рефералы - это люди, которых вы пригласили в наш канал по своей реферальной ссылке'
                                            'и они подписались. За приглашенных рефералов можно покупать различные привелегии.')


@dp.chat_join_request_handler()
async def on_user_joined(update: types.ChatJoinRequest):
    invite_link = update['invite_link']['invite_link']
    user_id = update['from']['id']
    username = update['from']['username']
    id_partner = db.get_partner(invite_link)[0]
    name_partner = db.get_partner(invite_link)[1]
    ref_balance = db.select_ref_balance(id_partner)[0]
    all_ref = db.select_all_ref(id_partner)[0]

    await update.approve()

    is_instance = db.select_user(user_id)
    if not is_instance:
        today_date = datetime.today().strftime('%d-%m-%Y')
        db.insert_user(user_id, id_partner, name_partner, today_date)
        db.update_ref_balance(id_partner, ref_balance+1)
        db.update_all_ref(id_partner, all_ref+1)
    else:
        pass


@dp.callback_query_handler(lambda call: call.data == '/films_button')
async def films_response(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    print(user_id)
    ref_balance = db.select_ref_balance(user_id)[0]
    if ref_balance >= 10:
        await bot.send_message(callback_query.message.chat.id, f'Напишите информацию по заказу.', reply_markup=markup_cancel)
        await Buy_films().films.set()
    else:
        await bot.send_message(callback_query.message.chat.id, 'У вас пока не хватает на покупку. Приглашайте больше людей', reply_markup=markup_shop)
    await callback_query.answer()


@dp.callback_query_handler(lambda call: call.data == '/cancel_button', state='*')
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    ref_balance = db.select_ref_balance(user_id)[0]
    await bot.send_message(callback_query.message.chat.id, f'Ваш баланс: {ref_balance} рефералов\nФильм/серия '
                                            '- 10 рефералов\nРеклама на канале - 200 рефералов\n\n'
                                            'Вывести деньги на карту - 200RU', reply_markup=markup_shop)
    await state.reset_data()
    await state.reset_state()
    await state.finish()
    await callback_query.answer()


@dp.message_handler(state=Buy_films.films)
async def info_buy_films(message: types.Message, state: FSMContext):
    await state.update_data(films=message.text)
    await bot.send_message(message.chat.id, 'Спасибо за информацию, передал ее для оформления покупки')
    user_id = message.from_user.id
    username = message.from_user.username
    info = await state.get_data()
    print(user_id)
    ref_balance = db.select_ref_balance(user_id)[0]
    db.update_ref_balance(user_id, ref_balance-10)
    await bot.send_message(6770023877, f'Новый заказ от @{username}\n\n{info["films"]}')
    await state.finish()


@dp.callback_query_handler(lambda call: call.data == '/adv_button')
async def adv_response(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    print(user_id)
    ref_balance = db.select_ref_balance(user_id)[0]
    if ref_balance >= 200:
        await bot.send_message(callback_query.message.chat.id, f'Напишите информацию по заказу.', reply_markup=markup_cancel)
        await Buy_adv().adv.set()
    else:
        await bot.send_message(callback_query.message.chat.id, 'У вас пока не хватает на покупку. Приглашайте больше людей', reply_markup=markup_shop)
    await callback_query.answer()


@dp.message_handler(state=Buy_adv.adv)
async def info_buy_films(message: types.Message, state: FSMContext):
    await state.update_data(adv=message.text)
    await bot.send_message(message.chat.id, 'Спасибо за информацию, передал ее для оформления покупки')
    user_id = message.from_user.id
    username = message.from_user.username
    info = await state.get_data()
    print(user_id)
    ref_balance = db.select_ref_balance(user_id)[0]
    db.update_ref_balance(user_id, ref_balance-200)
    await bot.send_message(6770023877, f'Новый заказ от @{username}\n\n{info["adv"]}')
    await state.finish()


@dp.callback_query_handler(lambda call: call.data == '/payment_button')
async def payment_response(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    balance = db.select_balance(user_id)[0]
    if balance < 200:
        await bot.send_message(callback_query.message.chat.id, 'Вам пока не хватает на вывод. Вывод от 200')
    elif balance >= 200:
        await bot.send_message(callback_query.message.chat.id, 'Отлично, зафиксировал запрос на вывод. Ожидайте, пока с вами свяжутся')
        await bot.send_message(6770023877, f'Новый запрос на вывод средств от @{username}')
    await callback_query.answer()
