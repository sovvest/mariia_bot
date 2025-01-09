import random

from datetime import datetime

from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.utils.scheduler import schedule_periodic_message
from app.utils.state import save_state

from app.info import fixed_date, compliments, questions, trivias

import app.keyboards as kb


router = Router()

game_state = {}

class QuizState(StatesGroup):
    waiting_for_answer = State()
    next_question = State()

@router.message(CommandStart())
async def handle_message(message: Message):
    await message.answer("Привет, ты Мария?", reply_markup=kb.main)

@router.message(Command("trivia"))
async def ask_trivia(message: Message):
    trivia = random.choice(trivias)
    await message.answer(f"{trivia}")

@router.message(Command("time"))
async def time(message: Message):
    current_date = datetime.now()
    delta = (current_date - fixed_date).days
    await message.answer(f"С {fixed_date.strftime('%d.%m.%Y')} прошло {delta} дней. А это значит, что Владик тебя любит {delta} день!")

@router.message(Command("love"))
async def love(message: Message):
    await message.answer("Мария, ты самая прекрасная! ❤️")

@router.message(Command("id"))
async def get_user_id(message: Message):
    user_id = message.from_user.id  # Получаем ID пользователя
    await message.answer(f"Твой ID: {user_id}")

@router.message(Command("compliment"))
async def compliment(message: Message):
    compliment = random.choice(compliments)
    await message.answer(compliment)

@router.message(Command("guess"))
async def start_guess_game(message: Message):
    secret_number = random.randint(1, 100)
    game_state[message.from_user.id] = secret_number
    await message.answer(
        "Я загадал число от 1 до 100. Попробуй угадать! Напиши своё число."
    )

@router.message(Command("quiz"))
async def start_quiz(message: Message, state: FSMContext):
    await state.set_data({"index": 0, "correct_answers": 0})
    question = questions[0]["question"]
    await message.answer(f"Начинаем игру! Вот первый вопрос:\n{question}")
    await state.set_state(QuizState.waiting_for_answer)


@router.message(F.text == "Список команд")
async def handle_message(message: Message):
    await message.answer("Я пока только учусь. Список команд будет доступен ниже. Хозяин тебя любит!")
    await message.answer("/time - узнать сколько дней вы с хозяином вместе!")
    await message.answer("/love - порадовать саму себя!")
    await message.answer("/compliment - получить комплимент!")
    await message.answer("/guess - сыграть в игру 'Угадай число'!")
    await message.answer("/quiz - сыграть в игру 'Что ты знаешь о Владике!'")
    await message.answer("/trivia - получить вопрос!(Не смотри, что команда связана с фруктами!)")

@router.message(F.text == "Что я знаю о тебе!")
async def handle_message(message: Message):
    await message.answer("Ты любишь Владика! А он любит тебя!")

@router.message(F.text == "Заглушка")
async def handle_message(message: Message):
    await message.answer("пук пук пук...")

@router.message(F.text == "Отправка напоминалок 💌")
async def handle_message(message: Message):
    await message.answer("Ты попросила не отключать напоминалки. Так что это просто напоминалка, что я тебя люблЮ! ❤️")


@router.message(lambda message: "грустн" in message.text.lower())
async def cheer_up(message: Message):
    await message.answer("Не грусти, я всегда рядом, чтобы тебя поддержать! Ведь я для этого создан❤️")

@router.message(lambda message: "да" in message.text.lower())
async def cheer_up(message: Message):
    await message.answer("Пизда)")

@router.message(lambda message: message.from_user.id in game_state)
async def guess_number(message: Message):
    try:
        secret_number = game_state[message.from_user.id]
        user_guess = int(message.text)

        if user_guess < secret_number:
            await message.answer("Я загадал число побольше! Мария, попробуй ещё раз.")
        elif user_guess > secret_number:
            await message.answer("Я загадал число поменьше! Маричка, ещё разок!")
        else:
            await message.answer(
                f"Поздравляю, Мария! Ты угадала число: {secret_number} 🎉"
            )
            del game_state[message.from_user.id]
    except ValueError:
        await message.answer("Пожалуйста, введи целое число.")


@router.message(QuizState.waiting_for_answer)
async def check_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    correct_answers = data["correct_answers"]

    user_answer = message.text.lower().strip()
    correct_answer = questions[index]["answer"].lower()

    if user_answer == correct_answer:
        correct_answers += 1
        await message.answer("Правильно! 🎉")
    else:
        await message.answer(f"Неправильно. Правильный ответ: {questions[index]['answer']}")

    index += 1

    if index < len(questions):
        await state.update_data(index=index, correct_answers=correct_answers)

        next_question = questions[index]["question"]
        await message.answer(f"Следующий вопрос:\n\n{next_question}")
    else:
        await message.answer(f"Игра окончена! Ты ответила правильно на {correct_answers} из {len(questions)} вопросов.")
        await state.clear()
