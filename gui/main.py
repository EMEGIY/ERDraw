import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from window_setup import menu_bar
from canvas import canvas
from pages import welcome
import action
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from prefabs.buttons import menu_button
import action
from canvas import canvas



class MainInstance(QMainWindow):
    def __init__(self):
        super().__init__()
        self.repo_path = __file__.replace("gui\\main.py", "")

        self.menu_bar = menu_bar(self)

        # Window Configuration
        self.setWindowTitle("ErdModeler")
        self.setGeometry(100, 100, 1100, 800)
        self.setWindowIcon(QIcon(self.repo_path + "icons\\logo.png")) 

        self.main_container = QWidget(self)
        self.setCentralWidget(self.main_container)

        welcome(self.main_container)


def listStyles():
    from PyQt6.QtWidgets import QApplication, QStyleFactory

    app = QApplication([])
    print(QStyleFactory.keys())  # List all available styles

def main():
    app = QApplication(sys.argv)
    app.setStyle("Macintosh")  # Set the style to "Fusion" or any other available style
    window = MainInstance()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

