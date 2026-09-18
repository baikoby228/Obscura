import os
import sys

if getattr(sys, 'frozen', False):
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    os.environ['TCL_LIBRARY'] = os.path.join(base_dir, 'tcl8.6')
    os.environ['TK_LIBRARY'] = os.path.join(base_dir, 'tk8.6')
else:
    base_python = getattr(sys, 'base_prefix', sys.prefix)
    os.environ['TCL_LIBRARY'] = os.path.join(base_python, 'tcl', 'tcl8.6')
    os.environ['TK_LIBRARY'] = os.path.join(base_python, 'tcl', 'tk8.6')

from gui import ObscuraGUI

if __name__ == "__main__":
    app = ObscuraGUI()
    app.mainloop()