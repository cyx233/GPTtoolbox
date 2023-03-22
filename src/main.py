from PySide2.QtWidgets import QApplication
from gui import LauncherWindow
import sys

if __name__ == "__main__":
    app = QApplication()
    launcher_window = LauncherWindow()
    launcher_window.show()
    sys.exit(app.exec_())