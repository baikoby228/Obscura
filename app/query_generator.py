import os
import json
import random

from dotenv import load_dotenv
from openai import OpenAI

from config import _FALLBACK_QUERIES

load_dotenv()

AI_API_KEY = os.getenv("AI_API_KEY")
AI_BASE_URL = "https://openrouter.ai/api/v1"
AI_MODEL = "openrouter/auto"

_query_buffer = []

SYSTEM_PROMPT = """
Ты — генератор реалистичных поисковых запросов для Google на русском языке.
Твоя задача — генерировать естественный "цифровой шум" обычного интернет-пользователя.

Сгенерируй {count} совершенно разных, ненаправленных поисковых запросов.

Разнообразь темы:
- Быт, ремонт, уход за вещами, кулинария
- Покупки, сравнение товаров, отзывы
- Наука, история, случайные факты, география
- Развлечения, фильмы, игры, книги, музыка
- IT, софт, простые технические вопросы
- Авто, спорт, здоровье, путешествия

Требования к запросам:
1. Разная форма: короткие ключи (2-3 слова), вопросы ("как...", "почему..."), искать конкретные фразы.
2. Естественный язык человека, а не робота.
3. Верни ТОЛЬКО валидный JSON-массив строк без разметки markdown и пояснений.
Пример формата: ["запрос 1", "запрос 2", "запрос 3"]
"""

def _clean_json_string(text: str) -> str:
    """Очищает ответ ИИ от markdown-разметки, если модель ее все же добавила."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def _fetch_new_queries_from_ai(count=15) -> list[str]:
    """Запрашивает у ИИ пачку новых поисковых запросов."""
    try:
        # Инициализируем универсальный клиент
        client = OpenAI(
            api_key=AI_API_KEY,
            base_url=AI_BASE_URL
        )

        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.format(count=count)},
                {"role": "user", "content": f"Сгенерируй {count} запросов в виде JSON-массива строк."}
            ],
            temperature=1.0,  # Высокая температура для разнообразия
        )

        raw_text = response.choices[0].message.content
        cleaned_text = _clean_json_string(raw_text)

        queries = json.loads(cleaned_text)

        if isinstance(queries, list) and len(queries) > 0:
            return [str(q).strip() for q in queries]

    except json.JSONDecodeError as e:
        print(f"[AI Query] Ошибка парсинга JSON от ИИ: {e}\nТекст ответа:\n{raw_text}")
    except Exception as e:
        print(f"[AI Query] Ошибка генерации через API: {e}")

    return []


def get_query() -> str:
    """
    Основная функция: возвращает один запрос из очереди.
    Если очередь пуста — запрашивает у ИИ новую пачку.
    """
    global _query_buffer

    if not _query_buffer:
        _query_buffer = _fetch_new_queries_from_ai(count=15)
        print("query_buffer:")
        for x in _query_buffer:
            print(x)

    if _query_buffer:
        return _query_buffer.pop(0)

    # Если ИИ сломался/нет интернета, возвращаем случайный из резерва
    return random.choice(_FALLBACK_QUERIES)