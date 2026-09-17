import os
import shutil

from .driver import get_driver
from config import ACCOUNTS_DIR


def list_accounts():
    """Возвращает список созданных папок аккаунтов"""
    if not os.path.exists(ACCOUNTS_DIR):
        return []
    return [d for d in os.listdir(ACCOUNTS_DIR) if os.path.isdir(os.path.join(ACCOUNTS_DIR, d))]


def launch_account_login(name):
    """
    Открывает окно браузера для авторизации.
    Возвращает объект драйвера.
    GUI должен сохранить его и вызвать driver.quit() по нажатию кнопки "Готово/Сохранить".
    """
    if not name or not name.strip():
        raise ValueError("Имя аккаунта не может быть пустым.")

    name = name.strip()
    driver = get_driver(name, headless=False)

    try:
        driver.get("https://accounts.google.com/ServiceLogin")
        return driver
    except Exception as e:
        driver.quit()
        raise RuntimeError(f"Ошибка при открытии страницы входа: {e}")


def remove_account(name):
    """
    Удаляет существующий профиль.
    GUI должен сам запрашивать подтверждение (например, через MessageBox)
    до вызова этой функции.
    """
    if not name or not name.strip():
        raise ValueError("Имя аккаунта не указано.")

    name = name.strip()
    account_path = os.path.join(ACCOUNTS_DIR, name)

    if not os.path.exists(account_path):
        raise FileNotFoundError(f"Аккаунт '{name}' не найден.")

    try:
        shutil.rmtree(account_path)
    except Exception as e:
        raise RuntimeError(f"Не удалось удалить аккаунт '{name}': {e}")