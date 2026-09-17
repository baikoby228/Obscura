import os
import sys
import json
import threading


def stoppable_sleep(seconds: float, stop_event: threading.Event) -> bool:
    """
    Засыпает на seconds секунд или просыпается раньше, если установлен stop_event.
    Возвращает True, если пауза прошла полностью, и False, если получена команда остановки.
    """
    return not stop_event.wait(timeout=seconds)


def get_base_dir() -> str:
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def clean_json_string(text: str) -> str:
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def load_json_file(filename: str, default=None):
    if default is None:
        default = []
    file_path = os.path.join(get_base_dir(), filename)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Utils] Ошибка чтения {filename}: {e}")
    return default


def save_json_file(filename: str, data) -> bool:
    file_path = os.path.join(get_base_dir(), filename)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[Utils] Ошибка сохранения {filename}: {e}")
        return False