from config import bot, dp, db
from aiogram import types
from main import add_user

@dp.callback_query_handler(lambda callback: 'order_' in callback.data)
async def order(callback: types.CallbackQuery):
    params = callback.data.split('_')
    user_id = int(params[1])
    product_name = str(params[2])
    user = db.users.find_one({'id': user_id})
    if user is not None:
        ...
    else:
        await add_user(callback)
    