import sys
import threading
import customtkinter as ctk
from tkinter import messagebox

from app import list_accounts, launch_account_login, remove_account, noise_worker
import config

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class TextRedirector:
    """Перенаправляет поток print() в текстовое окно CustomTkinter"""

    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", text)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def flush(self):
        pass


class ObscuraGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Obscura — Менеджер Цифрового Шума")
        self.geometry("900x580")
        self.minsize(800, 500)

        self.stop_event = None
        self.worker_thread = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_sidebar()
        self._build_main_area()

        # Перенаправляем stdout в логи GUI
        sys.stdout = TextRedirector(self.log_textbox)

        self.refresh_accounts_list()

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        sidebar.grid_rowconfigure(7, weight=1)

        # Логотип
        title = ctk.CTkLabel(sidebar, text="OBSCURA", font=ctk.CTkFont(size=22, weight="bold"))
        title.grid(row=0, column=0, padx=20, pady=(20, 10))

        subtitle = ctk.CTkLabel(sidebar, text="Traffic Obfuscation Tool", font=ctk.CTkFont(size=11), text_color="gray")
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Переключатель Headless
        self.headless_switch = ctk.CTkSwitch(
            sidebar,
            text="Скрытый режим",
            command=self._toggle_headless
        )
        self.headless_switch.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        if config.HEADLESS_MODE:
            self.headless_switch.select()

        # Разделитель
        ctk.CTkFrame(sidebar, height=2, fg_color="gray30").grid(row=3, column=0, padx=20, pady=15, sticky="ew")

        # Кнопки управления аккаунтами
        btn_add = ctk.CTkButton(sidebar, text="+ Добавить аккаунт", command=self._add_account_action)
        btn_add.grid(row=4, column=0, padx=20, pady=8)

        btn_remove = ctk.CTkButton(
            sidebar,
            text="- Удалить аккаунт",
            fg_color="#A32A2A",
            hover_color="#822121",
            command=self._remove_account_action
        )
        btn_remove.grid(row=5, column=0, padx=20, pady=8)

        # Статус индикатор
        self.status_label = ctk.CTkLabel(
            sidebar,
            text="● Статус: Готов",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2AAA8A"
        )
        self.status_label.grid(row=8, column=0, padx=20, pady=20)

    def _build_main_area(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Панель выбора и запуска
        control_card = ctk.CTkFrame(main_frame)
        control_card.grid(row=0, column=0, sticky="ew", pady=(0, 15), padx=0)
        control_card.grid_columnconfigure(1, weight=1)

        label_acc = ctk.CTkLabel(control_card, text="Профиль Google:", font=ctk.CTkFont(size=14))
        label_acc.grid(row=0, column=0, padx=15, pady=15)

        self.account_menu = ctk.CTkOptionMenu(control_card, values=["Загрузка..."])
        self.account_menu.grid(row=0, column=1, padx=10, pady=15, sticky="ew")

        self.btn_start = ctk.CTkButton(
            control_card,
            text="Запустить шум",
            fg_color="#1F6AA5",
            font=ctk.CTkFont(weight="bold"),
            command=self.start_noise
        )
        self.btn_start.grid(row=0, column=2, padx=15, pady=15)

        # Лог консоль
        log_label = ctk.CTkLabel(main_frame, text="Консоль активности:", font=ctk.CTkFont(size=13, weight="bold"))
        log_label.grid(row=1, column=0, sticky="w", pady=(0, 5))

        self.log_textbox = ctk.CTkTextbox(main_frame, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_textbox.grid(row=2, column=0, sticky="nsew")
        self.log_textbox.configure(state="disabled")

    def refresh_accounts_list(self):
        accounts = list_accounts()
        if accounts:
            self.account_menu.configure(values=accounts)
            self.account_menu.set(accounts[0])
        else:
            self.account_menu.configure(values=["Нет аккаунтов"])
            self.account_menu.set("Нет аккаунтов")

    def _toggle_headless(self):
        config.change_headless()
        mode_str = "скрытый" if config.HEADLESS_MODE else "видимый"
        print(f"[Система] Режим браузера изменён на: {mode_str}")

    def _add_account_action(self):
        dialog = ctk.CTkInputDialog(text="Введите имя нового профиля:", title="Добавление аккаунта")
        name = dialog.get_input()
        if name and name.strip():
            # Запускаем браузер в отдельном потоке, чтобы не заморозить GUI
            threading.Thread(target=self._run_add_account, args=(name.strip(),), daemon=True).start()

    def _run_add_account(self, name):
        try:
            print(f"\n[ВХОД] Запуск браузера для авторизации '{name}'...")
            driver = launch_account_login(name)

            # После успешного запуска браузера вызываем окно подтверждения в главном потоке
            self.after(0, self._show_login_complete_dialog, name, driver)
        except Exception as e:
            print(f"[ОШИБКА] Не удалось открыть окно входа: {e}")

    def _show_login_complete_dialog(self, name, driver):
        """Окно, которое висит поверх остальных и ждет окончания авторизации"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Авторизация Google")
        dialog.geometry("400x150")
        dialog.attributes("-topmost", True)
        dialog.grab_set()  # Блокирует основное окно до закрытия диалога

        lbl = ctk.CTkLabel(
            dialog,
            text=f"Браузер открыт.\nВойдите в аккаунт для профиля '{name}'.\nПосле успешного входа нажмите кнопку ниже."
        )
        lbl.pack(pady=20, padx=20)

        def on_complete():
            print(f"[ВХОД] Сохранение профиля '{name}'...")
            try:
                driver.quit()
            except Exception:
                pass
            dialog.destroy()
            self.refresh_accounts_list()
            print(f"[УСПЕХ] Профиль '{name}' добавлен и готов к работе.")

        btn = ctk.CTkButton(dialog, text="Вход выполнен (Закрыть браузер)", fg_color="#2AAA8A", hover_color="#208068",
                            command=on_complete)
        btn.pack(pady=10)

    def _remove_account_action(self):
        selected = self.account_menu.get()
        if not selected or selected == "Нет аккаунтов":
            return

        if messagebox.askyesno("Удаление", f"Удалить профиль '{selected}' со всеми данными?"):
            try:
                # Теперь передаем selected как аргумент
                remove_account(selected)
                print(f"[УСПЕХ] Аккаунт '{selected}' удален.")
            except Exception as e:
                print(f"[ОШИБКА] {e}")
                messagebox.showerror("Ошибка", str(e))

            self.refresh_accounts_list()

    def start_noise(self):
        selected_account = self.account_menu.get()
        if not selected_account or selected_account == "Нет аккаунтов":
            messagebox.showwarning("Ошибка", "Сначала выберите или добавьте аккаунт.")
            return

        if self.worker_thread and self.worker_thread.is_alive():
            # Остановка текущей сессии
            self.stop_event.set()
            self.btn_start.configure(text="Останавливаю...", state="disabled")
            self.status_label.configure(text="● Остановка...", text_color="#E59866")
        else:
            # Запуск новой сессии
            self.stop_event = threading.Event()
            self.worker_thread = threading.Thread(
                target=self._run_noise_thread,
                args=(selected_account, self.stop_event),
                daemon=True
            )
            self.worker_thread.start()

            self.btn_start.configure(text="Остановить шум", fg_color="#A32A2A", hover_color="#822121")
            self.status_label.configure(text="● Шум активен", text_color="#2AAA8A")
            self.account_menu.configure(state="disabled")

    def _run_noise_thread(self, account_name, stop_event):
        noise_worker(account_name, stop_event)

        # Сброс UI элементов после завершения потока
        self.after(0, self._on_noise_stopped)

    def _on_noise_stopped(self):
        self.btn_start.configure(text="Запустить шум", fg_color="#1F6AA5", hover_color="#144D79", state="normal")
        self.status_label.configure(text="● Статус: Готов", text_color="#2AAA8A")
        self.account_menu.configure(state="normal")
        print("[Система] Поток генерации шума полностью остановлен.")


if __name__ == "__main__":
    app = ObscuraGUI()
    app.mainloop()