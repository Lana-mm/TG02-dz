import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import sqlite3
import logging


API_TOKEN = '7635278323:AAFC74i3wULah_Yv25EN-me8MYsO3KVJL-A'


bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
	name = State()
	age = State()
	klass = State()

def init_db():
	conn = sqlite3.connect('school_data.db')
	cur = conn.cursor()
	cur.execute('''
	CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	age INTEGER NOT NULL,
	klass TEXT NOT NULL)
	''')
	conn.commit()
	conn.close()

init_db()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет, как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
	await state.update_data(age=message.text)
	await message.answer("В каком ты классе учишься?")
	await state.set_state(Form.klass)

@dp.message(Form.klass)
async def klass(message: Message, state: FSMContext):
	await state.update_data(klass=message.text)
	data = await state.get_data()
	conn = sqlite3.connect('school_data.db')
	cur = conn.cursor()
	cur.execute('''
	   INSERT INTO users (name, age, klass) VALUES (?, ?, ?)''',
				(data['name'], data['age'], data['klass']))
	conn.commit()
	conn.close()
	await message.answer(f"Ты {data['name']}. Тебе {data['age']} лет. Твой класс - {data['klass']}.")
	await state.clear()



async def main():
	await dp.start_polling(bot)
if __name__ == '__main__':
	asyncio.run(main())