import os
import undetected_chromedriver as uc
from config import ACCOUNTS_DIR


def get_driver(account_name, headless=False):
    """Запуск браузера с папкой конкретного аккаунта"""

    profile_path = os.path.abspath(os.path.join(ACCOUNTS_DIR, account_name))
    os.makedirs(profile_path, exist_ok=True)

    options = uc.ChromeOptions()

    if headless:
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        options.add_argument(f"--user-agent={ua}")

    driver = uc.Chrome(
        options=options,
        user_data_dir=profile_path,
        headless=headless,
        version_main=152
    )

    return driver