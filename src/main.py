from PySide2.QtWidgets import QApplication
from gui import LauncherWindow
import sys

if __name__ == "__main__":
    try:
        app = QApplication()
        launcher_window = LauncherWindow()
        launcher_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e.with_traceback())
        sys.exit(1)

# from utils import env

# chunk_db = env.open_db(b'chunk_database')
# filename = "chat_gui.py"

# for index in range(4):
#     with env.begin(write=False) as txn:
#         text_key = f"{filename}:{index}".encode()
#         text = txn.get(text_key, db=chunk_db)
#         print(text)