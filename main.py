import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from googletrans import Translator

from config import TOKEN
import keyboards as kb

translator = Translator()

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Приветствие /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.answer(f"Приветики, я ваш бот", reply_markup=kb.inline_keyboard_test)

# Сохранинеи фотографий в папку img
@dp.message(F.photo)
async def handle_photo(message: Message):
    if not os.path.exists('img'):
        os.makedirs('img')
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    photo_path = f'img/{photo.file_id}.jpg'
    await bot.download_file(file_info.file_path, photo_path)
    await message.answer("Файл сохранен")

# Перевод на английский введенного текста
@dp.message(F.text)
async def handle_text(message: Message):
    text_to_translate = message.text
    translated_text = translator.translate(text_to_translate, src='auto', dest='en').text
    await message.answer(translated_text)

# Отправка голосового сообщения
@dp.message(Command(commands=['sendvoice']))
async def send_voice(message: Message):
    voice_path = 'path_to_voice_message.ogg'  # Путь к вашему голосовому сообщению
    with open(voice_path, 'rb') as voice:
        await message.answer_voice(voice)

# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)