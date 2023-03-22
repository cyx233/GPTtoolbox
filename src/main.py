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
        print(f"An error occurred: {e}")
        sys.exit(1)