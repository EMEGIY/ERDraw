import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, QEvent, QObject
from PyQt6.QtGui import QIcon
from gui.window_setup import menu_bar
from gui.canvas import canvas
from gui.pages import welcome
import gui.action as action



class ResizeEventFilter(QObject):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Resize:
            self.callback(event.size())  # Call the callback with the new size
        return super().eventFilter(obj, event)

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


    def resizedConnect(self, callback):
        self.resize_event_filter = ResizeEventFilter(callback)
        self.installEventFilter(self.resize_event_filter)
    
    

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

