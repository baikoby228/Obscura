import time
import random
import threading

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .driver import get_driver
from .account_manager import get_account
from .query_selector import get_query
from config import NOISE_HEADLESS
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

def start_noise_for_account():
    selected_name = get_account()
    if not selected_name:
        return

    print(f"\n[ШУМ] Запуск '{selected_name}' в ФОНОВОМ режиме...")
    print(">>> Введите 'q', 'stop' или 'exit' и нажмите Enter для остановки <<<")

    listener_thread = threading.Thread(target=monitor_for_stop, daemon=True)
    listener_thread.start()

    driver = get_driver(selected_name, headless=NOISE_HEADLESS)

    try:
        print("Типо шум")
        while keep_running:
            query = get_query()
            print(f"[{selected_name} | {time.strftime('%H:%M:%S')}] Ищу: {query}")

            driver.get("https://www.google.com")
            #time.sleep(random.uniform(5, 8))
            stoppable_sleep(random.uniform(0.1, 1), lambda: keep_running)
            if not keep_running: break

            try:
                search_box = driver.find_element(By.NAME, "q")
                for char in query:
                    search_box.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.2))
                search_box.send_keys(Keys.RETURN)

                #time.sleep(random.uniform(7, 12))
                stoppable_sleep(random.uniform(5, 7), lambda: keep_running)
                if not keep_running: break

                driver.execute_script(f"window.scrollBy(0, {random.randint(0, 1000)});")

                #time.sleep(random.uniform(1, 2))
                stoppable_sleep(random.uniform(1, 2), lambda: keep_running)
                if not keep_running: break

                print("!")
                results = driver.find_elements(By.CSS_SELECTOR, "h3.LC20lb.MBeuO.DKV0Md")
                if results:
                    print("Start to try click!")
                    #print("result = ", results)
                    for _ in range(5):
                        try:
                            #!!!!!!!!!!!
                            random.choice(results).click()
                            print("OK!")
                            break
                        except:
                            print("Bad!")
                    #time.sleep(random.uniform(15, 40))
                    stoppable_sleep(random.uniform(5, 10), lambda: keep_running)
                else:
                    print("!!!!!!! NO results")
                    #driver.save_screenshot(f"error_google_{int(time.time())}.png")

            except Exception as e:
                print(f"    ! Ошибка: {e}")

            if not keep_running: break

            #wait = random.randint(60, 200)
            wait = random.randint(5, 10)
            print(f"    - Пауза: {wait} сек.")
            stoppable_sleep(wait, lambda: keep_running)
            #break

    except KeyboardInterrupt:
        print(f"\n[ШУМ] Аккаунт '{selected_name}' остановлен.")
    finally:
        driver.quit()