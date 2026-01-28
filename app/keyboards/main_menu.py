from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Внести вес")],
            [KeyboardButton(text="Шаги"), KeyboardButton(text="Тренировка")],
            [KeyboardButton(text="Синхронизировать FatSecret")],
            [KeyboardButton(text="Отчет недели"), KeyboardButton(text="Помощь")],
        ],
        resize_keyboard=True,
    )
