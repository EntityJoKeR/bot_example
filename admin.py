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
    
    
@dp.message_handler(lambda message: 'Добавить товар' in message.text, state=None)
async def start_upload(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply('Загрузите фото')
    
    
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
