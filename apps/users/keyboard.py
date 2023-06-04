from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_keyboards = [
    InlineKeyboardButton('Идентификация', callback_data='identification')
]

identification_buttons = InlineKeyboardMarkup().add(*inline_keyboards)

question_keyboards = [
    InlineKeyboardButton('Получить вопросы', callback_data='get_questions')
]
question_buttons = InlineKeyboardMarkup().add(*question_keyboards)