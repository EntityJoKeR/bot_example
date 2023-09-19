from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = KeyboardButton('Режим работы')
b2 = KeyboardButton('Расположение')
b3 = KeyboardButton('Заказать')
b4 = KeyboardButton('Меню')
b5 = KeyboardButton('Главное меню')
b6 = KeyboardButton('Команды')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1,b2,b3,b4,b5,b6)


inline_kb_main_menu = InlineKeyboardMarkup(row_width=2)
but1 = InlineKeyboardButton(text='Меню', callback_data='menu')
but2 = InlineKeyboardButton(text='Команды', callback_data='commands')
but3 = InlineKeyboardButton(text='Расположение', callback_data='menu')
but4 = InlineKeyboardButton(text='Заказать', callback_data='commands')
but5 = InlineKeyboardButton(text='Режим работы', callback_data='working_time')

inline_kb_main_menu.add(but1,but4,but3,but5,but2)


