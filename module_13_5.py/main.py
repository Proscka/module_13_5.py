from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
import asyncio

api = "7527901227:AAF9qrgQGQ8EItHrb1HACw2Q5sK6ons9_VM"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb=ReplyKeyboardMarkup()
button = KeyboardButton(text="Расчитать")
button2 = KeyboardButton(text="Информация")
kb.add(button)
kb.add(button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands= ['Привет'])
async def start(message):
    await message.answer(text="Введите команду/start чтобы начать общение")
@dp.message_handler(commands= ['start'])
async def start(message):
    await message.answer(text="Привет! Я бот помогающий твоему здоровью",reply_markup=kb)

@dp.message_handler(text = "Информация")
async def inform(message):
    await message.answer("Информация")

@dp.message_handler(text = ["Расчитать"])
async def set_age(message):
    await message.answer("Введите свой возраст")
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message,state):
    await state.update_data(age=message.text)
    await message.answer(f"Введите свой рост")
    await UserState.growth.set()
@dp.message_handler(state=UserState.growth)
async def set_weight(message,state):
    await state.update_data(growth=message.text)
    await message.answer(f"Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message,state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories_wom = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f"Ваша норма калорий {calories_wom}")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)