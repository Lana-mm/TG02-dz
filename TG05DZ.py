import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import requests
from googletrans import Translator
from config import TOKEN, WEATHER_API_KEY, API_FACTS_URL

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()
CITY_NAME = 'Екатеринбург'

# Функция для получения погоды
async def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return f"Погода в {city}: {data['weather'][0]['description']}, температура: {data['main']['temp']}°C"
            else:
                return "Не удалось получить данные о погоде."

# Функция для получения интересного факта о сегодняшней дате
def get_fact():
    response = requests.get(API_FACTS_URL)
    if response.status_code == 200:
        return response.text
    else:
        return 'Не удалось получить факт.'

@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer(
        "Привет! Я бот, который может сообщить тебе погоду на сегодня и интересный факт о какой-либо дате. "
        "Используй /weather для получения погоды или /today для факта."
    )

@dp.message(Command("today"))
async def today_command(message: Message):
    fact = get_fact()
    # Перевод факта на русский
    translated_fact = translator.translate(fact, dest='ru').text
    await message.reply(f"Интересный факт: {translated_fact}")

@dp.message(Command("weather"))
async def weather_command(message: Message):
    weather = await get_weather(CITY_NAME)
    await message.reply(weather)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())