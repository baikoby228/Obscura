import os
import undetected_chromedriver as uc

from config import ACCOUNTS_DIR

def get_driver(account_name, headless=False):
    """Запуск браузера с папкой конкретного аккаунта"""
    profile_path = os.path.join(ACCOUNTS_DIR, account_name)

    options = uc.ChromeOptions()
    options.add_argument(f'--user-data-dir={profile_path}')

    if headless:
        driver = uc.Chrome(options=options, headless=True, use_headless=True, version_main=152)
    else:
        driver = uc.Chrome(options=options, version_main=152)

    return driver