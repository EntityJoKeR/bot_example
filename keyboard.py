from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('Режим работы')
b2 = KeyboardButton('Расположение')
b3 = KeyboardButton('Заказать')
b4 = KeyboardButton('Меню')
b5 = KeyboardButton('Главное меню')
b6 = KeyboardButton('Команды')

kb_client = ReplyKeyboardMarkup(resize_keyboard = True)
kb_client.add(b1,b2,b3,b4,b5,b6)