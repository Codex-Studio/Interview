from django.conf import settings
from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from logging import basicConfig, INFO

from apps.users.models import TelegramUser
from apps.users.keyboard import identification_buttons
from apps.users.state import IdentificationState

# Create your views here.
bot = Bot(settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}", reply_markup=identification_buttons)

@dp.callback_query_handler(lambda call: call)
async def identification_callback(call):
    if call.data == 'identification':
        await identification_user(call.message)

@dp.message_handler(commands='identification')
async def identification_user(message:types.Message):
    await message.answer("Введите код идентификации")
    await IdentificationState.code.set()

@dp.message_handler(state=IdentificationState.code)
async def get_identification_code(message:types.Message, state:FSMContext):
    await message.answer("PON")