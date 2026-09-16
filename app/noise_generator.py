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
from config import NOISE_HEADLESS, RUSSIAN_ALPHABET
from utils import stoppable_sleep

keep_running = True


def monitor_for_stop():
    global keep_running
    while keep_running:
        command = input()
        if command.strip().lower() in ['q', 'stop', 'exit']:
            print("\n[!] Получена команда на остановку. Завершаем работу...")
            keep_running = False
            break


def simulate_reading(driver):
    """Имитирует чтение страницы со случайным скроллингом"""
    read_time = random.randint(20, 50)
    print(f"    - 'Читаем' сайт {read_time} сек...")

    end_read_time = time.time() + read_time
    while keep_running and time.time() < end_read_time:
        driver.execute_script(f"window.scrollBy(0, {random.randint(100, 400)});")
        stoppable_sleep(random.uniform(2, 6), lambda: keep_running)

        if random.random() < 0.2:
            driver.execute_script(f"window.scrollBy(0, -{random.randint(50, 200)});")
            stoppable_sleep(random.uniform(1, 3), lambda: keep_running)


def start_noise_for_account():
    global keep_running

    selected_name = get_account()
    if not selected_name:
        return

    print(f"\n[ШУМ] Запуск '{selected_name}' в ФОНОВОМ режиме...")
    print(">>> Введите 'q', 'stop' или 'exit' и нажмите Enter для остановки <<<")

    listener_thread = threading.Thread(target=monitor_for_stop, daemon=True)
    listener_thread.start()

    driver = get_driver(selected_name, headless=NOISE_HEADLESS)

    try:
        #print("Типо шум")
        while keep_running:

            while len(driver.window_handles) > 2:
                driver.switch_to.window(driver.window_handles[0])
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])

            query = get_query()
            print(f"[{selected_name} | {time.strftime('%H:%M:%S')}] Ищу: {query}")

            driver.get("https://www.google.com")
            stoppable_sleep(random.uniform(1.5, 3.5), lambda: keep_running)
            if not keep_running: break

            try:
                elements = driver.find_elements(By.NAME, "q")
                count = len(elements)
                print(f'count = {count}!!!')

                #search_box = driver.find_element(By.NAME, "q")
                try:
                    search_box = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.NAME, "q"))
                    )
                    search_box.click()
                    print("Успешно: Элемент найден и клик совершен!")

                except TimeoutException:
                    print("Ошибка: Элемент не появился за 10 секунд.")
                except ElementClickInterceptedException:
                    print("Ошибка: Элемент виден, но его перекрывает другой объект (например, баннер).")
                except Exception as e:
                    print(f"Произошла другая ошибка при клике: {e}")

                stoppable_sleep(random.uniform(0.5, 1.0), lambda: keep_running)
                driver.save_screenshot(f"screen_google_{int(time.time())}.png")

                search_box = driver.find_element(By.NAME, "q")
                search_box.clear()

                for char in query:
                    if not keep_running: break

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

                if not keep_running: break

                stoppable_sleep(random.uniform(0.5, 1.5), lambda: keep_running)
                search_box.send_keys(Keys.RETURN)

                stoppable_sleep(random.uniform(3, 5), lambda: keep_running)
                if not keep_running: break

                scrolls = random.randint(2, 4)
                for _ in range(scrolls):
                    if not keep_running: break
                    driver.execute_script(f"window.scrollBy(0, {random.randint(150, 250)});")
                    stoppable_sleep(random.uniform(1.0, 3.0), lambda: keep_running)

                if random.random() < 0.4:
                    driver.execute_script(f"window.scrollBy(0, -{random.randint(150, 400)});")
                    stoppable_sleep(random.uniform(1.0, 2.0), lambda: keep_running)

                if not keep_running: break

                results = driver.find_elements(By.CSS_SELECTOR, "h3.LC20lb.MBeuO.DKV0Md")

                if results:
                    target = random.choice(results[:3]) if len(
                        results) > 3 and random.random() < 0.7 else random.choice(results)

                    open_in_new_tab = (random.random() < 0.2)

                    if open_in_new_tab:
                        print("    - Открываем сайт в НОВОЙ вкладке...")
                        driver.execute_script("arguments[0].closest('a').setAttribute('target', '_blank');", target)

                    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", target)
                    stoppable_sleep(random.uniform(0.5, 1.5), lambda: keep_running)

                    target.click()

                    if open_in_new_tab:
                        driver.switch_to.window(driver.window_handles[-1])

                    simulate_reading(driver)

                    max_returns = 3
                    returns_count = 0

                    while keep_running and returns_count < max_returns:
                        if random.random() > 0.4:
                            break

                        print(
                            f"    - Не понравилось, возвращаемся к результатам (возврат {returns_count + 1}/{max_returns})...")

                        if open_in_new_tab:
                            driver.close()
                            driver.switch_to.window(driver.window_handles[-1])
                        else:
                            driver.back()

                        stoppable_sleep(random.uniform(2, 4), lambda: keep_running)
                        if not keep_running: break

                        results = driver.find_elements(By.CSS_SELECTOR, "h3.LC20lb.MBeuO.DKV0Md")
                        if not results:
                            print("    - Результаты пропали, переходим к следующему запросу.")
                            break

                        clicked_successfully = False
                        for _ in range(3):
                            try:
                                target2 = random.choice(results)
                                open_in_new_tab = (random.random() < 0.2)
                                if open_in_new_tab:
                                    driver.execute_script("arguments[0].closest('a').setAttribute('target', '_blank');",
                                                          target2)

                                driver.execute_script(
                                    "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", target2)
                                stoppable_sleep(1, lambda: keep_running)

                                target2.click()

                                if open_in_new_tab:
                                    driver.switch_to.window(driver.window_handles[-1])

                                clicked_successfully = True
                                break
                            except:
                                stoppable_sleep(1, lambda: keep_running)

                        if clicked_successfully:
                            returns_count += 1
                            simulate_reading(driver)
                        else:
                            print("    - Не удалось перейти ни на один другой сайт. Завершаем текущий запрос.")
                            break

                else:
                    print("!!!!!!! NO results")
                    driver.save_screenshot(f"error_google_{int(time.time())}.png")

            except Exception as e:
                print(f"    ! Ошибка: {e}")

            if not keep_running: break

            wait = random.randint(45, 120)
            print(f"    - Отдых перед следующим запросом: {wait} сек.")
            stoppable_sleep(wait, lambda: keep_running)

    except KeyboardInterrupt:
        print(f"\n[ШУМ] Аккаунт '{selected_name}' остановлен (Ctrl+C).")
        keep_running = False
    finally:
        print(f"\n[ШУМ] Закрытие браузера для '{selected_name}'...")
        driver.quit()