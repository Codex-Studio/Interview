from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

inline_keyboards = [
    InlineKeyboardButton('Идентификация', callback_data='identification')
]

identification_buttons = InlineKeyboardMarkup().add(*inline_keyboards)
#####################
question_keyboards = [
    InlineKeyboardButton('Получить вопросы', callback_data='get_questions')
]
question_buttons = InlineKeyboardMarkup().add(*question_keyboards)
#################################
end_keyboards = [
    InlineKeyboardButton('Узнать ответы', callback_data='end_questions')
]
end_buttons = InlineKeyboardMarkup().add(*end_keyboards)
##################################
cancel_keyboards = [
    KeyboardButton('Отменить')
]

cancel_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*cancel_keyboards)