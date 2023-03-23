from PySide2.QtWidgets import QApplication
from gui import LauncherWindow
import utils
import sys

def main():
    try:
        app = QApplication()
        launcher_window = LauncherWindow()
        launcher_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e.with_traceback())
        sys.exit(1)


if __name__ == "__main__":
    main()