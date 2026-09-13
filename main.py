from app import add_account, remove_account
from app import start_noise_for_account

def main():
    while True:
        print("\n" + "=" * 30)
        print(" МЕНЕДЖЕР ЦИФРОВОГО ШУМА")
        print("=" * 30)
        print("1. Добавить новый Google аккаунт")
        print("2. Удалить аккаунт")
        print("3. Список аккаунтов и запуск шума (ФОН)")
        print("4. Выход")

        choice = input("\nВыберите действие: ")

        if choice == "1":
            add_account()
        elif choice == "2":
            remove_account()
        elif choice == "3":
            start_noise_for_account()
        elif choice == "4":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод.")


if __name__ == "__main__":
    main()