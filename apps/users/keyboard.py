from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_keyboards = [
    InlineKeyboardButton('Идентификация', callback_data='identification')
]

identification_buttons = InlineKeyboardMarkup().add(*inline_keyboards)