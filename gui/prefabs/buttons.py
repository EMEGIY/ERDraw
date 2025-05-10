# This unit stores some widget subclasses that will be used often
# in other units

# Imports
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize

class menu_button(QPushButton):
    def __init__(self, icon_paths=["",  ""] , *args, **kwargs): # [active_icon_path, inactive_icon_path]  
        super().__init__(*args, **kwargs)

        # This button will be used for the menu options
        self.default_style = "color: rgba(190,190,190,255); font-size: 18px; background-color: transparent; border: none; text-align: left"
        self.hover_style = "color: rgba(255,255,255,255); font-size: 18px; background-color: transparent; border-radius: 5px; text-align: left;"
        self.setStyleSheet(self.default_style)
        
        # That should be full paths
        self.icon_paths = icon_paths

        self.setIcon(QIcon(icon_paths[1]))
        self.setIconSize(QSize(32, 32))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.setIcon(QIcon(self.icon_paths[0]))
        self.setIconSize(QSize(32, 32))
        self.setStyleSheet(self.hover_style)
        event.accept() # Continues the event

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.setIcon(QIcon(self.icon_paths[1]))
        self.setIconSize(QSize(32, 32))
        self.setStyleSheet(self.default_style)
        event.accept() # Continues the event