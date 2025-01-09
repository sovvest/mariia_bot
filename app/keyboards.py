from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Список команд")],
                                     [KeyboardButton(text="Что я знаю о тебе!"), KeyboardButton(text="Заглушка")],
                                     [KeyboardButton(text="Отправка напоминалок 💌")]],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите пункт меню")