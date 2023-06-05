from django.conf import settings
from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from logging import basicConfig, INFO

from apps.users.models import TelegramUser
from apps.users.keyboard import identification_buttons, question_buttons, end_buttons, cancel_buttons
from apps.users.state import IdentificationState
from apps.questions.models import Question, Task

# Create your views here.
bot = Bot(settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)

@dp.callback_query_handler(lambda call: call)
async def identification_callback(call):
    if call.data == 'identification':
        await identification_user(call.message)
    elif call.data == 'get_questions':
        await get_user_questions(call.message)
    elif call.data == 'end_questions':
        await get_results(call.message)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    try:
        user = await sync_to_async(TelegramUser.objects.get)(user_id=message.from_user.id)
        await message.answer(f"Привет {message.from_user.full_name}. Твой код идентификации {user.code}")
    except:
        await message.answer(f"Привет {message.from_user.full_name}", reply_markup=identification_buttons)

@dp.message_handler(commands='identification')
async def identification_user(message:types.Message):
    await message.answer("Введите код идентификации")
    await IdentificationState.code.set()

@dp.message_handler(state=IdentificationState.code)
async def get_identification_code(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await start(message)
        await state.finish()
    else:
        await message.answer("Проверяем данные...")
        all_codes = await sync_to_async(list)(TelegramUser.objects.all())
        codes = [user.code for user in all_codes]
        for code in codes:
            if code == message.text:
                user = await sync_to_async(TelegramUser.objects.get)(code=code)
                user.user_id = message.from_user.id
                user.chat_id = message.chat.id
                user.username = message.from_user.username
                user.first_name = message.from_user.first_name
                user.last_name = message.from_user.last_name
                await sync_to_async(user.save)()
                await message.answer("Данные успешно записаны ожидайте начало собесодевания")
                await state.finish()
                break
        else:
            await message.answer("К сожалению данные не верные, введите еще раз", reply_markup=cancel_buttons)

async def send_mailing(user, title, mailing_type):
    all_users = await sync_to_async(list)(TelegramUser.objects.all())
    chats_id = [user.chat_id for user in all_users]
    print(chats_id)
    if mailing_type == "Simple" and user == None:
        for chat in chats_id:
            await bot.send_message(chat, title)
    elif mailing_type == "Start" and user != None:
        personal_user = await sync_to_async(TelegramUser.objects.get)(code=user)
        print(personal_user.chat_id)
        await bot.send_message(personal_user.chat_id, title, reply_markup=question_buttons)
    elif mailing_type == "Personal" and user != None:
        personal_user = await sync_to_async(TelegramUser.objects.get)(code=user)
        print(personal_user.chat_id)
        await bot.send_message(personal_user.chat_id, title)
    elif mailing_type == "End":
        for chat in chats_id:
            await bot.send_message(chat, title, reply_markup=end_buttons)

async def get_user_questions(message:types.Message):
    personal_user = await sync_to_async(TelegramUser.objects.get)(user_id=message.chat.id)
    questions = await sync_to_async(list)(Question.objects.filter(user=personal_user.id))
    tasks = await sync_to_async(list)(Task.objects.filter(user=personal_user.id))
    user_questions = [question.title for question in questions]
    user_tasks = [task.title for task in tasks]
    if user_questions and user_tasks:
        n = 0
        for question in user_questions:
            n += 1
            await bot.send_message(personal_user.chat_id, f"{n}) {question}")
        t = 0
        await bot.send_message(personal_user.chat_id, "А теперь задачи")
        for task in user_tasks:
            t += 1
            await bot.send_message(personal_user.chat_id, f"{t}) {task}")

@dp.message_handler(commands='result')
async def get_results(message:types.Message):
    personal_user = await sync_to_async(TelegramUser.objects.get)(user_id=message.chat.id)
    questions = await sync_to_async(list)(Question.objects.filter(user=personal_user.id))
    user_points = [question.point != None for question in questions]
    await message.answer(f"{sum(user_points)}")
    if sum(user_points) >= 6:
        await message.answer(f"Уважаемый {personal_user.code}, вы прошли тест!\nВаш итоговый балл {sum(user_points)}/11\nПоздравляем!")
    else:
        await message.answer(f"{personal_user.code} вы не прошли тест\nВаш итоговый балл {sum(user_points)}/11\nПроходной балл 6")

@dp.message_handler()
async def not_found(message:types.Message):
    await message.answer("Я вас не понял введите help")