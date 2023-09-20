from config import bot, dp, db, channel_id
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from texts import*

product_name = []


async def add_user(message):
    user_dict = {
        'id': message.from_user.id,
        'username': message.from_user.id,
        'firstname': message.from_user.first_name,
        'orders': 0
    }
    db.users.insert_one(user_dict)


class FSMOrder(StatesGroup):
    product_name = State()
    name = State()
    number = State()
    quantity = State()
    payment_method = State()
    adress = State()

@dp.callback_query_handler(lambda callback: 'order_' in callback.data, state=None)
async def order(callback: types.CallbackQuery):
    params = callback.data.split('_')
    user_id = int(params[1])
    product_name.append(str(params[2]))
    user = db.users.find_one({'id': user_id})
    if user is not None:
        await bot.send_message(callback.from_user.id, text=f'Отлично! Теперь укажите пожалуйса ваше имя')
        await FSMOrder.name.set()
        db.users.update_one({'id': callback.from_user.id}, {'$set': {'orders':user['orders'] + 1}})
        
    else:
        await add_user(callback)
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
        await bot.send_message(chat_id=channel_id, text=f"Заказ пользователя: @{message.from_user.username}\n"
                                                                                    f"Название продукта: {product_name[0]}\n"
                                                                                    f"Количество: {data_order['quantity']}\n"
                                                                                    f"Номер телефона: {data_order['number']}\n"
                                                                                    f"Способ оплаты: {data_order['payment_method']}\n"
                                                                                    f"Адрес: {data_order['adress']}\n")
    await state.finish()
    await message.reply('Отлично, ваш заказ будет отправлен менеджеру после чего он с вами свяжется.')
    product_name.clear()



@dp.callback_query_handler(lambda callback: 'menu' in  callback.data)
async def inline_menu(callback: types.CallbackQuery):
    menu_list = list(db.market.find())
    if len(menu_list) != 0:
        for item in menu_list:
            inline_kb_menu = InlineKeyboardMarkup(row_width=1)
            menu_but1 = InlineKeyboardButton(text='Заказать товар',
                                             callback_data=f'order_{callback.from_user.id}_{item["name"]}')
            inline_kb_menu.add(menu_but1)
            await bot.send_photo(callback.from_user.id,
                                 caption=f'\nНазвание:{item["name"]}\nОписание: {item["description"]}\nЦена: {item["price"]}',
                                 photo=item['photo'], reply_markup=inline_kb_menu)
    else:
        await callback.answer('вам нужно добавить продукцию в меню')
    

@dp.callback_query_handler(lambda callback: 'commands' in  callback.data)
async def inline_menu(callback: types.CallbackQuery):
    await callback.message.answer(help_text)
    

@dp.callback_query_handler(lambda callback: 'location' in  callback.data)
async def inline_menu(callback: types.CallbackQuery):
    await callback.message.answer(location)

    
    
@dp.callback_query_handler(lambda callback: 'working_time' in  callback.data)
async def working_time(callback: types.CallbackQuery):
    await callback.message.answer(time_work)


