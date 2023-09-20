from main import*
from aiogram import*
from config import*
from pymongo import*
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State



class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
    

@dp.message_handler(lambda message: 'Добавить сотрудника' in message.text)
async def add_employee(message: types.Message):
    if int(message.from_user.id) == owner_id:
        if message.reply_to_message:
            db.admins.insert_one({'admin_id': int(message.reply_to_message.from_user.id), 'admin_name': message.reply_to_message.from_user.username})
            await message.answer(f'Сотрудник {message.reply_to_message.from_user.username} добавлен!')
        else:
            await message.reply('Данная команда должна быть отправлена на сообщение сотрудника которого вы хотите добавить в бота')
    else:
        await message.reply('Эта команда доступна только владельцу бота')
    await message.delete()
        
@dp.message_handler(lambda message: 'Удалить сотрудника' in message.text)
async def delete_admin(message: types.message):
    if int(message.from_user.id) == owner_id:
        if message.reply_to_message:
            db.admins.delete_one({'admin_id': int(message.reply_to_message.from_user.id)})
            await message.answer(f'Сотрудник {message.reply_to_message.from_user.username} удален!')
        else:
            await message.reply('Данная команда должна быть отправлена на сообщение сотрудника которого вы хотите удалить из бота')
    else:
        await message.reply('Эта команда доступна только владельцу бота')
    await message.delete()
    
@dp.message_handler(lambda message: 'Добавить товар' in message.text, state=None)
async def start_upload(message: types.Message):
    admins = list(db.admins.find())
    admins_id = []
    for item in admins:
        admins_id.append(item['admin_id'])
    
    if (message.from_user.id in admins_id) or (message.from_user.id == owner_id):
        await FSMAdmin.photo.set()
        await message.reply('Загрузите фото')
    else:
        await message.answer('Данная команда вам недоступна')
    await message.delete()

@dp.message_handler(lambda message: 'Удалить товар' in message.text)
async def delete_product(message: types.Message):
    admins = list(db.admins.find())
    admins_id = []
    product_name = str(message.text).split()
    for item in admins:
        admins_id.append(item['admin_id'])
    if int(message.from_user.id) == owner_id or int(message.from_user.id) in admins_id:
        if len(product_name) == 3:
            print(product_name)
            product = db.market.find_one({'name': product_name[2]})
            if product is not None:
                db.market.delete_one({'name': product_name[2]})
                await message.answer(f'Товар {product_name[2]} удален.')
            else:
                await message.answer(f'Товар {product_name[2]} не найден, возможно вы не указали название товара или указали его неправильно, попробуйте еще раз(название должно быть указано с учетом  регистра).')
        else:
            await message.answer(
                f'Товар не найден, вы не указали название товара, попробуйте еще раз c указанием названия товара.')
    else:
        await message.answer('У вас недостаточно прав для использования этой команды')

    await message.delete()


    
@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def add_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Теперь введите название')


@dp.message_handler(state=FSMAdmin.name)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Теперь введите описание')
    
    
@dp.message_handler(state=FSMAdmin.description)
async def add_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply('Теперь введите цену')


@dp.message_handler(state=FSMAdmin.price)
async def add_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = int(message.text)
        db.market.insert_one({'photo' : data['photo'], 'name' : data['name'], 'description': data['description'], 'price': data['price']})
    await state.finish()
    await message.reply('готово')
