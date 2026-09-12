import os

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