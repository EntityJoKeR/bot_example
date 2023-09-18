from config import dp, bot, db
from aiogram import types
from main import*




@dp.message_handler(lambda message: 'Главное меню' in message.text)
async def main_menu(message: types.Message):
    ...



@dp.message_handler(lambda message: 'Меню' in message.text)
async def menu(message: types.Message):
    menu_list = list(db.market.find())
    
    if len(menu_list) != 0 :
        for item in menu_list:
            await bot.send_photo(message.from_user.id, caption=f'Название: {item["name"]}\nОписание: {item["description"]}\nЦена: {item["price"]}', photo=item['photo'])
    else:
        await message.answer('вам нужно добавить продукцию в меню')
    

@dp.message_handler(lambda message: 'Команды' in message.text)
async def help_cmnd(message: types.Message):
    ...
    

@dp.message_handler(lambda message: 'Заказать' in message.text)
async def order(message: types.Message):
    ...
    
    
@dp.message_handler(lambda message: 'Режим работы' in message.text)
async def work_time(message: types.Message):
    await message.answer(text=time_work)
    
    
@dp.message_handler(lambda message: 'Расположение' in message.text)
async def coord(message: types.Message):
    ...