from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize


class menu_button(QPushButton):
    def __init__(self, icon_paths=["",  ""] , *args, **kwargs): # [active_icon_path, inactive_icon_path]  
        super().__init__(*args, **kwargs)
        self.default_style = "color: rgba(190,190,190,255); font-size: 18px; background-color: transparent; border: none; text-align: left"
        self.hover_style = "color: rgba(255,255,255,255); font-size: 18px; background-color: transparent; border-radius: 5px; text-align: left;"
        self.setStyleSheet(self.default_style)

        self.icon_paths = icon_paths

        self.setIcon(QIcon(icon_paths[1]))
        self.setIconSize(QSize(32, 32))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        # Animation for hover effect
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.setIcon(QIcon(self.icon_paths[0]))
        self.setIconSize(QSize(32, 32))
        self.setStyleSheet(self.hover_style)
        event.accept()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.setIcon(QIcon(self.icon_paths[1]))
        self.setIconSize(QSize(32, 32))
        self.setStyleSheet(self.default_style)
        event.accept()