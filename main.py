#pip install -r requirements.txt
#pip freeze > requirements.txt

from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
from config import dp, bot, db
from texts import*
from keyboard import kb_client
from user import*
from admin import*
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import callbacks

storage = MemoryStorage()


async def on_startup(_):
    print('bot online')
    
    
async def add_user(message):
    user_dict = {
        'id': message.from_user.id,
        'username': message.from_user.id,
        'firstname': message.from_user.first_name,
        'orders': 0
    }
    db.users.insert_one(user_dict)
    


@dp.message_handler(lambda message: "bot" in message.text)
async def ping(message: types.Message):
    await message.answer('i working')


@dp.message_handler(commands='start')
async def start_cmnd(message: types.Message):
    await bot.send_message(message.chat.id, text=start_text, reply_markup = kb_client)
    await add_user(message)
    

@dp.message_handler(commands='id')
async def start_cmnd(message: types.Message):
    await bot.send_message(message.from_user.id, text=f'{message.from_user.id}\n {message.chat.id}', reply_markup = kb_client)
    await add_user(message)
    



if __name__ == '__main__':
    
    executor.start_polling(dp, skip_updates = False, on_startup=on_startup)
    