import os
import sys

base_python = getattr(sys, 'base_prefix', sys.prefix)

tcl_dir = os.path.join(base_python, 'tcl', 'tcl8.6')
tk_dir = os.path.join(base_python, 'tcl', 'tk8.6')

os.environ['TCL_LIBRARY'] = tcl_dir
os.environ['TK_LIBRARY'] = tk_dir

print(f"[ИНФО] Базовый Python: {base_python}")
print(f"[ИНФО] Используется Tcl: {tcl_dir}")
print(f"[ИНФО] Используется Tk: {tk_dir}")

if not os.path.exists(tcl_dir):
    print(f"\n[ОШИБКА] Папка Tcl не найдена по пути: {tcl_dir}")
    print("Убедитесь, что Python установлен корректно.")
    sys.exit(1)

import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--noconfirm',
    '--onedir',
    '--windowed',
    '--hidden-import', 'undetected_chromedriver',
    '--add-data', f'{tcl_dir};tcl8.6',
    '--add-data', f'{tk_dir};tk8.6',
    '--add-data', '.venv/Lib/site-packages/customtkinter;customtkinter/'
])