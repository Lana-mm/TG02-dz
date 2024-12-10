from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# Список для инлайн-кнопок
test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

# Асинхронная функция для создания инлайн-клавиатуры
async def test_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in test:
        keyboard.add(InlineKeyboardButton(text=key, callback_data=key))  # Используем InlineKeyboardButton
    return keyboard.adjust(2).as_markup()


# Создание обычной клавиатуры
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Тестовая кнопка 1")],
    [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
], resize_keyboard=True)



# Создание инлайн-клавиатуры с ссылкой
inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Видео", url='https://www.youtube.com/watch?v=HfaIcB4Ogxk')]
])