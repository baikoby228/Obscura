import os

from .driver import get_driver
from config import ACCOUNTS_DIR

def list_accounts():
    """Возвращает список созданных папок аккаунтов"""
    if not os.path.exists(ACCOUNTS_DIR):
        return []
    return [d for d in os.listdir(ACCOUNTS_DIR) if os.path.isdir(os.path.join(ACCOUNTS_DIR, d))]

def get_account():
    """Выбор аккаунта и запуск шума в фоне"""
    accounts = list_accounts()

    if not accounts:
        print("\n[!] Нет добавленных аккаунтов. Сначала добавьте аккаунт (пункт 1).")
        return

    print("\nДоступные аккаунты:")
    for i, name in enumerate(accounts, 1):
        print(f"{i}. {name}")

    try:
        choice = int(input("\nВыберите номер аккаунта для запуска шума: "))
        selected_name = accounts[choice - 1]
    except (ValueError, IndexError):
        print("Неверный выбор.")
        return

    return selected_name

def add_account():
    """Регистрация нового профиля (видимое окно)"""
    name = input("\nВведите имя для этого аккаунта (например, 'personal' или 'mail1'): ").strip()
    if not name:
        print("Имя не может быть пустым.")
        return

    print(f"\n[ВХОД] Открываю окно для аккаунта '{name}'...")
    driver = get_driver(name, headless=False)

    try:
        driver.get("https://accounts.google.com/ServiceLogin")
        print(f"ВНИМАНИЕ: Войдите в Google аккаунт для профиля '{name}'.")
        input("После входа нажмите ENTER здесь, чтобы сохранить и закрыть...")
    finally:
        driver.quit()
        print(f"Аккаунт '{name}' успешно добавлен.")