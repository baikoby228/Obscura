from app import add_account, remove_account
from app import start_noise_for_account
from config import change_headless

def main():
    while True:
        from config import HEADLESS_MODE
        print("\n" + "=" * 30)
        print(" МЕНЕДЖЕР ЦИФРОВОГО ШУМА")
        print("=" * 30)
        print("1. Добавить новый Google аккаунт")
        print("2. Удалить аккаунт")
        print(f"3. Изменить режим (в текущий момент - {"скрытый" if HEADLESS_MODE else "видимый"})")
        print("4. Список аккаунтов и запуск шума (ФОН)")
        print("5. Выход")

        choice = input("\nВыберите действие: ")

        if choice == "1":
            add_account()
        elif choice == "2":
            remove_account()
        elif choice == "3":
            change_headless()
        elif choice == "4":
            start_noise_for_account()
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод.")


if __name__ == "__main__":
    main()