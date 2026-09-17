import time
import random
import threading

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

from .driver import get_driver
from .account_manager import get_account
from .query_generator import get_query
from config import RUSSIAN_ALPHABET, HEADLESS_MODE
from utils import stoppable_sleep


def simulate_reading(driver, stop_event: threading.Event):
    """Имитирует чтение страницы со случайным скроллингом"""
    read_time = random.randint(20, 50)
    print(f"    - 'Читаем' сайт {read_time} сек...")

    end_read_time = time.time() + read_time
    while not stop_event.is_set() and time.time() < end_read_time:
        driver.execute_script(f"window.scrollBy(0, {random.randint(100, 400)});")
        if not stoppable_sleep(random.uniform(2, 6), stop_event):
            break

        if random.random() < 0.2:
            driver.execute_script(f"window.scrollBy(0, -{random.randint(50, 200)});\n")
            if not stoppable_sleep(random.uniform(1, 3), stop_event):
                break


def noise_worker(selected_name: str, stop_event: threading.Event):
    """Изолированный фоновый поток для выполнения сценария автокликкера"""
    driver = get_driver(selected_name, headless=HEADLESS_MODE)

    try:
        while not stop_event.is_set():
            while len(driver.window_handles) > 2:
                driver.switch_to.window(driver.window_handles[0])
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])

            query = get_query()
            print(f"[{selected_name} | {time.strftime('%H:%M:%S')}] Ищу: {query}")

            driver.get("https://www.google.com")
            if not stoppable_sleep(random.uniform(1.5, 3.5), stop_event):
                break

            try:
                try:
                    search_box = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.NAME, "q"))
                    )
                    search_box.click()
                except TimeoutException:
                    print("Ошибка: Элемент не появился за 10 секунд.")
                except ElementClickInterceptedException:
                    print("Ошибка: Элемент перекрыт другим объектом.")
                except Exception as e:
                    print(f"Ошибка при клике: {e}")

                if not stoppable_sleep(random.uniform(0.5, 1.0), stop_event):
                    break

                search_box = driver.find_element(By.NAME, "q")
                search_box.clear()

                for char in query:
                    if stop_event.is_set():
                        break

                    if char.isalpha() and random.random() < 0.07:
                        wrong_char = random.choice(RUSSIAN_ALPHABET)
                        search_box.send_keys(wrong_char)
                        time.sleep(random.uniform(0.15, 0.35))
                        search_box.send_keys(Keys.BACK_SPACE)
                        time.sleep(random.uniform(0.1, 0.25))

                    search_box.send_keys(char)

                    if random.random() < 0.05:
                        time.sleep(random.uniform(0.5, 1.2))
                    else:
                        time.sleep(random.uniform(0.05, 0.2))

                if stop_event.is_set():
                    break

                if not stoppable_sleep(random.uniform(0.5, 1.5), stop_event):
                    break

                search_box.send_keys(Keys.RETURN)

                if not stoppable_sleep(random.uniform(3, 5), stop_event):
                    break

                scrolls = random.randint(2, 4)
                for _ in range(scrolls):
                    if stop_event.is_set():
                        break
                    driver.execute_script(f"window.scrollBy(0, {random.randint(150, 250)});\n")
                    if not stoppable_sleep(random.uniform(1.0, 3.0), stop_event):
                        break

                if random.random() < 0.4 and not stop_event.is_set():
                    driver.execute_script(f"window.scrollBy(0, -{random.randint(150, 400)});\n")
                    if not stoppable_sleep(random.uniform(1.0, 2.0), stop_event):
                        break

                if stop_event.is_set():
                    break

                results = driver.find_elements(By.CSS_SELECTOR, "h3.LC20lb.MBeuO.DKV0Md")

                if results:
                    target = random.choice(results[:3]) if len(results) > 3 and random.random() < 0.7 else random.choice(results)
                    open_in_new_tab = (random.random() < 0.2)

                    if open_in_new_tab:
                        print("    - Открываем сайт в НОВОЙ вкладке...")
                        driver.execute_script("arguments[0].closest('a').setAttribute('target', '_blank');", target)

                    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", target)
                    if not stoppable_sleep(random.uniform(0.5, 1.5), stop_event):
                        break

                    target.click()

                    if open_in_new_tab:
                        driver.switch_to.window(driver.window_handles[-1])

                    simulate_reading(driver, stop_event)

                    max_returns = 3
                    returns_count = 0

                    while not stop_event.is_set() and returns_count < max_returns:
                        if random.random() > 0.4:
                            break

                        print(f"    - Возвращаемся к результатам (возврат {returns_count + 1}/{max_returns})...")

                        if open_in_new_tab:
                            driver.close()
                            driver.switch_to.window(driver.window_handles[-1])
                        else:
                            driver.back()

                        if not stoppable_sleep(random.uniform(2, 4), stop_event):
                            break

                        results = driver.find_elements(By.CSS_SELECTOR, "h3.LC20lb.MBeuO.DKV0Md")
                        if not results:
                            break

                        clicked_successfully = False
                        for _ in range(3):
                            if stop_event.is_set():
                                break
                            try:
                                target2 = random.choice(results)
                                open_in_new_tab = (random.random() < 0.2)
                                if open_in_new_tab:
                                    driver.execute_script("arguments[0].closest('a').setAttribute('target', '_blank');", target2)

                                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", target2)
                                if not stoppable_sleep(1, stop_event):
                                    break

                                target2.click()

                                if open_in_new_tab:
                                    driver.switch_to.window(driver.window_handles[-1])

                                clicked_successfully = True
                                break
                            except:
                                if not stoppable_sleep(1, stop_event):
                                    break

                        if clicked_successfully:
                            returns_count += 1
                            simulate_reading(driver, stop_event)
                        else:
                            break

            except Exception as e:
                print(f"    ! Ошибка в цикле: {e}")

            if stop_event.is_set():
                break

            wait = random.randint(45, 120)
            print(f"    - Отдых перед следующим запросом: {wait} сек.")
            if not stoppable_sleep(wait, stop_event):
                break

    except KeyboardInterrupt:
        print(f"\n[ШУМ] Остановлено вручную.")
    finally:
        print(f"\n[ШУМ] Закрытие браузера для '{selected_name}'...")
        driver.quit()


def start_noise_for_account():
    """CLI-обёртка для запуска воркера с отслеживанием консольного ввода"""
    selected_name = get_account()
    if not selected_name:
        return

    stop_event = threading.Event()

    worker_thread = threading.Thread(
        target=noise_worker,
        args=(selected_name, stop_event),
        daemon=True
    )

    print(f"\n[ШУМ] Запуск '{selected_name}' в фоновом режиме...")
    print(">>> Введите 'q', 'stop' или 'exit' и нажмите Enter для остановки <<<")

    worker_thread.start()

    while worker_thread.is_alive():
        try:
            cmd = input()
            if cmd.strip().lower() in ['q', 'stop', 'exit']:
                print("\n[!] Получена команда на остановку. Завершаем работу...")
                stop_event.set()
                break
        except (KeyboardInterrupt, EOFError):
            stop_event.set()
            break

    worker_thread.join()