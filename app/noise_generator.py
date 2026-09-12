import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .driver import get_driver
from .account_manager import get_account
from .query_selector import get_query

def start_noise_for_account():
    selected_name = get_account()
    if not selected_name:
        return

    print(f"\n[ШУМ] Запуск '{selected_name}' в ФОНОВОМ режиме...")
    #driver = get_driver(selected_name, headless=True)
    driver = get_driver(selected_name, headless=False)

    try:
        print("Типо шум")
        while True:
            query = get_query()
            print(f"[{selected_name} | {time.strftime('%H:%M:%S')}] Ищу: {query}")

            driver.get("https://www.google.com")
            #time.sleep(random.uniform(5, 8))
            time.sleep(random.uniform(0.1, 1))

            try:
                search_box = driver.find_element(By.NAME, "q")
                for char in query:
                    search_box.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.2))
                search_box.send_keys(Keys.RETURN)

                #time.sleep(random.uniform(7, 12))
                time.sleep(random.uniform(5, 7))

                driver.execute_script(f"window.scrollBy(0, {random.randint(0, 1000)});")
                time.sleep(random.uniform(1, 2))

                print("!")
                results = driver.find_elements(By.CSS_SELECTOR, "h3.LC20lb.MBeuO.DKV0Md")
                if results:
                    print("Start to try click!")
                    #print("result = ", results)
                    while True:
                        try:
                            #!!!!!!!!!!!
                            random.choice(results).click()
                            print("OK!")
                            break
                        except:
                            print("Bad!")
                    #time.sleep(random.uniform(15, 40))
                    time.sleep(random.uniform(5, 10))
                else:
                    print("!!!!!!! NO results")


            except Exception as e:
                print(f"    ! Ошибка: {e}")

            #wait = random.randint(60, 200)
            wait = random.randint(5, 10)
            print(f"    - Пауза: {wait} сек.")
            time.sleep(wait)
            #break

    except KeyboardInterrupt:
        print(f"\n[ШУМ] Аккаунт '{selected_name}' остановлен.")
    finally:
        driver.quit()