from pymongo import MongoClient
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

db = MongoClient("mongodb+srv://dimonmarin16:Wotankist2004@example.sgljbgi.mongodb.net/?retryWrites=true&w=majority").bot
#admins, market, bot


token = "6535003795:AAGbT6UbMPwjoPjtc1UV8WoNxLUYtQz7-DE"
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)