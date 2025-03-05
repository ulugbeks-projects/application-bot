from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

submit_application_callback = CallbackData("submit_application", "action")

submit_application_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ha, barchasi to'g'ri✅", callback_data=submit_application_callback.new(action="submit"))
        ],
        [
            InlineKeyboardButton(text="Yo'q, xatolik mavjud❌", callback_data=submit_application_callback.new(action="cancel"))
        ]
    ]
)