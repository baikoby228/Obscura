import os
import json
import random

from dotenv import load_dotenv
from openai import OpenAI

from config import _FALLBACK_QUERIES
from utils import get_base_dir, clean_json_string, load_json_file, save_json_file

env_path = os.path.join(get_base_dir(), ".env")
load_dotenv(dotenv_path=env_path)

AI_API_KEY = os.getenv("AI_API_KEY")
AI_BASE_URL = "https://openrouter.ai/api/v1"
AI_MODEL = "openrouter/auto"

HISTORY_FILE = "last_queries.json"
_query_buffer = []

SYSTEM_PROMPT_BASE = """
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

HISTORY_INSTRUCTION = """
ВАЖНО! В прошлую генерацию ты выдал следующий список:
{last_queries}

Твоя текущая задача — сделать новую генерацию непохожей на предыдущую по структуре, порядку тем и стилистике.
Если прошлый список начинался с быта — начни с науки или игр. Измени пропорции тем, длину запросов и формулировки. 
Полностью сломай предыдущий шаблон, чтобы казалось, что этот список сгенерирован абсолютно другим человеком в другом настроении.
"""

def _fetch_new_queries_from_ai(count=15) -> list[str]:
    try:
        client = OpenAI(
            api_key=AI_API_KEY,
            base_url=AI_BASE_URL
        )

        final_system_prompt = SYSTEM_PROMPT_BASE.format(count=count)

        last_queries = load_json_file(HISTORY_FILE, default=[])
        if last_queries:
            history_text = json.dumps(last_queries, ensure_ascii=False)
            final_system_prompt += "\n" + HISTORY_INSTRUCTION.format(last_queries=history_text)

        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": final_system_prompt},
                {"role": "user", "content": f"Сгенерируй {count} запросов в виде JSON-массива строк."}
            ],
            temperature=1.0,
            max_tokens = 20000
        )

        raw_text = response.choices[0].message.content
        cleaned_text = clean_json_string(raw_text)
        queries = json.loads(cleaned_text)

        if isinstance(queries, list) and len(queries) > 0:
            cleaned_queries = [str(q).strip() for q in queries]
            save_json_file(HISTORY_FILE, cleaned_queries)
            return cleaned_queries

    except json.JSONDecodeError as e:
        print(f"[AI Query] Ошибка парсинга JSON: {e}")
    except Exception as e:
        print(f"[AI Query] Ошибка API: {e}")

    return []


def get_query() -> str:
    """
    Основная функция: возвращает один запрос из очереди.
    Если очередь пуста — запрашивает у ИИ новую пачку.
    """
    global _query_buffer

    if not _query_buffer:
        _query_buffer = _fetch_new_queries_from_ai(count=15)

    if _query_buffer:
        return _query_buffer.pop(0)

    return random.choice(_FALLBACK_QUERIES)