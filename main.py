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

storage = MemoryStorage()
async def on_startup(_):
    print('bot online')


@dp.message_handler(lambda message: "bot" in message.text)
async def ping(message: types.Message):
    await message.answer('i working')


@dp.message_handler(commands='start')
async def start_cmnd(message: types.Message):
    await bot.send_message(message.from_user.id, text=start_text, reply_markup = kb_client)
    



if __name__ == '__main__':
    
    executor.start_polling(dp, skip_updates = False, on_startup=on_startup)
    