import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher,  types
from aiogram.filters import CommandStart, Command

from config import TOKEN, EDAMAM_API_ID,EDAMAM_API_KEY
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я могу предложить тебе рецепты блюд. Введи ингредиенты, которые у тебя есть.")

@dp.message()
async def get_recipes(message: types.Message):
    ingredients = message.text
    url = f'https://api.edamam.com/search?q={ingredients}&app_id={EDAMAM_API_ID}&app_key={EDAMAM_API_KEY}'
    response = requests.get(url)
    recipes_data = response.json()

    if 'hits' in recipes_data:
        recipes = recipes_data['hits']
        for recipe in recipes[:5]:  # Отправляем только первые 5 рецептов
            recipe_title = recipe['recipe']['label']
            recipe_url = recipe['recipe']['url']
            await message.reply(f"{recipe_title}\n{recipe_url}")
    else:
        await message.reply("Извините, не удалось найти рецепты с такими ингредиентами. Попробуйте другие.")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())