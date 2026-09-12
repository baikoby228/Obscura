from .driver import get_driver

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