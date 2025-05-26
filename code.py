import os
import logging
import asyncio
from openai import AsyncOpenAI
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import Message

# Настройки
TELEGRAM_TOKEN = "7967328415:AAHOjXfv8Oa8ChCTRTuJJ-gBUASpV5EfZHA"
OPENAI_API_KEY = "your-openai-api-key"  # Замените на реальный ключ
MAX_HISTORY = 10  # Максимальное количество сообщений для контекста

# Настройка прокси для работы из России (используем например, прокси Китая или других стран)
PROXY_URL = "http://proxy-provider.com:port"  # Замените на реальный прокси

# Проверка токенов
if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Не указаны TELEGRAM_TOKEN или OPENAI_API_KEY")

# Инициализация клиентов
bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()

# Инициализация OpenAI клиента с прокси
client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    http_client=AsyncOpenAI(proxies={"http": PROXY_URL, "https": PROXY_URL})
)

# Хранилище истории диалогов
user_chats = {}

# Персонализация JARVIS
JARVIS_PERSONALITY = """Ты — JARVIS, искусственный интеллект из вселенной Marvel. 
Твой стиль общения:
- Короткие, точные ответы
- Сарказм, но без грубости
- Вежливость с лёгким высокомерием
- Используешь обращения: "Сэр", "Разумеется", "Как вам угодно"
- На глупые вопросы отвечаешь с юмором
- Изображения анализируешь детально, как высокотехнологичный ИИ"""


def get_user_messages(user_id: int):
    """Получение или создание истории сообщений для пользователя"""
    if user_id not in user_chats:
        # Инициализируем с системным сообщением для установки личности
        user_chats[user_id] = [
            {"role": "system", "content": JARVIS_PERSONALITY}
        ]
    return user_chats[user_id]


async def generate_jarvis_response(user_id: int, text: str) -> str:
    """Генерация ответа через OpenAI"""
    messages = get_user_messages(user_id)

    # Добавляем новое сообщение пользователя
    messages.append({"role": "user", "content": text})

    # Ограничиваем историю сообщений
    if len(messages) > MAX_HISTORY + 1:  # +1 для системного сообщения
        messages = [messages[0]] + messages[-MAX_HISTORY:]

    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=0.7,
            max_tokens=2048
        )

        assistant_reply = response.choices[0].message.content

        # Добавляем ответ ассистента в историю
        messages.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    except Exception as e:
        logging.error(f"OpenAI error: {e}")
        return f"⚠ Произошла ошибка, сэр: {str(e)}"


async def analyze_image(user_id: int, image_url: str) -> str:
    """Анализ изображения через OpenAI"""
    prompt = "Детально опиши изображение как JARVIS. Будь технически точным."
    messages = get_user_messages(user_id)

    try:
        response = await client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                *messages,
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            max_tokens=2048
        )

        assistant_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    except Exception as e:
        logging.error(f"Vision error: {e}")
        return f"⚠ Не удалось проанализировать изображение, сэр: {str(e)}"


@dp.message(Command("start", "help"))
async def send_welcome(message: Message):
    await message.answer(
        "🔊 Добро пожаловать, сэр. Я — JARVIS.\n\n"
        "Просто напишите мне сообщение или отправьте изображение для анализа.\n\n"
        "Команды:\n"
        "/clear - очистить историю диалога"
    )


@dp.message(Command("clear"))
async def clear_history(message: Message):
    user_id = message.from_user.id
    if user_id in user_chats:
        del user_chats[user_id]
    await message.answer("🔄 История диалога очищена, сэр.")


@dp.message(F.photo)
async def handle_image(message: Message):
    user_id = message.from_user.id
    try:
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        image_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file.file_path}"

        await bot.send_chat_action(message.chat.id, "typing")
        analysis = await analyze_image(user_id, image_url)
        await message.answer(analysis)
    except Exception as e:
        logging.error(f"Image handling error: {e}")
        await message.answer(f"⚠ Произошла ошибка при анализе изображения, сэр: {str(e)}")


@dp.message(F.text)
async def handle_text(message: Message):
    user_id = message.from_user.id
    text = message.text

    try:
        await bot.send_chat_action(message.chat.id, "typing")
        response = await generate_jarvis_response(user_id, text)
        await message.answer(response)
    except Exception as e:
        logging.error(f"Text handling error: {e}")
        await message.answer(f"⚠ Произошла ошибка, сэр: {str(e)}")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())