from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


###############
# Кнопка link
###############


create_link_button = InlineKeyboardButton('Link', callback_data='/create_link')
markup_link = InlineKeyboardMarkup()
markup_link.row(create_link_button)


main_menu_shop = KeyboardButton(text='Магазин')
main_menu_ref = KeyboardButton(text='Рефералы')
main_menu_top = KeyboardButton(text='Топ')
main_menu_info = KeyboardButton(text='Инфо')
main_menu_markup = ReplyKeyboardMarkup()
main_menu_markup.add(main_menu_shop, main_menu_ref, main_menu_top, main_menu_info)


films_button_shop = InlineKeyboardButton('Фильм/Серия', callback_data='/films_button')
adv_button_shop = InlineKeyboardButton('Реклама', callback_data='/adv_button')
out_money_shop = InlineKeyboardButton('Вывести деньги на карту', callback_data='/payment_button')
markup_shop = InlineKeyboardMarkup()
markup_shop.row(films_button_shop, adv_button_shop, out_money_shop)


accept_button_shop = InlineKeyboardButton('Подтверждаю', callback_data='/accept_button')
decline_button_shop = InlineKeyboardButton('Отказываюсь', callback_data='/decline_button')
markup_accept_shop = InlineKeyboardMarkup()
markup_accept_shop.row(accept_button_shop, decline_button_shop)