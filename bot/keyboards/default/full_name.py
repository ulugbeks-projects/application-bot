from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def full_name_keyboard(full_name: str):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=full_name)
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard