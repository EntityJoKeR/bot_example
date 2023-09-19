from config import bot, dp, db, channel_id
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


async def add_user(message):
    user_dict = {
        'id': message.from_user.id,
        'username': message.from_user.id,
        'firstname': message.from_user.first_name,
        'orders': 0
    }
    db.users.insert_one(user_dict)


class FSMOrder(StatesGroup):
    name = State()
    number = State()
    quantity = State()
    payment_method = State()
    adress = State()

@dp.callback_query_handler(lambda callback: 'order_' in callback.data, state=None)
async def order(callback: types.CallbackQuery):
    print('hdhdh')
    params = callback.data.split('_')
    user_id = int(params[1])
    product_name = str(params[2])
    user = db.users.find_one({'id': user_id})
    if user is not None:
        await bot.send_message(callback.from_user.id, text='Отлично! Теперь напишите ваше имя.') 
        await FSMOrder.name.set()
        #db.users.update_one({'id': callback.from_user.id}, {'$set': {'orders':user['orders'] + 1}})
        
    else:
        await add_user(callback)
        await bot.send_message(message.from_user.id, text='Отлично! Теперь напишите ваше имя.') 
        await FSMOrder.name.set()
        
        
@dp.message_handler(state=FSMOrder.name)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data_order:
        data_order['name'] = message.text
    await FSMOrder.next()
    await message.reply('Теперь укажите ваш номер.')
    
        
@dp.message_handler(state=FSMOrder.number)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data_order:
        data_order['number'] = message.text
    await FSMOrder.next()
    await message.reply('Теперь укажите количество.')
    
    
@dp.message_handler(state=FSMOrder.quantity)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data_order:
        data_order['quantity'] = message.text
    await FSMOrder.next()
    await message.reply('Теперь укажите способ оплаты (неличная, безналичная)')
    
    
@dp.message_handler(state=FSMOrder.payment_method)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data_order:
        data_order['payment_method'] = message.text
    await FSMOrder.next()
    await message.reply('Теперь введите ваш адрес.')
    
    
@dp.message_handler(state=FSMOrder.adress)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data_order:
        data_order['adress'] = message.text
        await bot.send_message(chat_id=channel_id, text=f"xxx")
    await FSMOrder.next()
    await message.reply('Отлично, ваш заказ будет отправлен менеджеру после чего он с вами свяжется.')
    

    

    
    
    
    
    