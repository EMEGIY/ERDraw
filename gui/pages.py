from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from prefabs.buttons import menu_button
import action
from canvas import canvas

def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)  # Remove the first item in the layout
        if item.widget():
            item.widget().deleteLater()  # Delete the widget
        elif item.layout():
            clear_layout(item.layout())  # Recursively clear nested layouts

class welcome(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.setParent(parent)
        self.root = parent

        for child in parent.children():
            if isinstance(child, QWidget):
                child.deleteLater()


        parent.setLayout(None)

        self.widget_layout = QVBoxLayout() 
        parent.setLayout(self.widget_layout)
        
        welcome_label = QLabel(self, text="Welcome to the ErdModeler!")
        welcome_label.setStyleSheet("font-size: 35px;")
     
        getting_started_label = QLabel(self, text="How to get started:")
        getting_started_label.setStyleSheet("color: rgba(170,170,170,255); font-size: 18px;")

        create_file_button = menu_button(parent=self, text="create a new erd", icon_paths=[self.root.parent().repo_path + "icons\\add_database_active.png", self.root.parent().repo_path + "icons\\add_database_inactive.png"])
        open_file_button = menu_button(parent=self, text="open an existing erd", icon_paths=[self.root.parent().repo_path + "icons\\open_database_active.png", self.root.parent().repo_path + "icons\\open_database_inactive.png"])
        csv_file_button = menu_button(parent=self, text="extend the csv collection", icon_paths=[self.root.parent().repo_path + "icons\\add_csv_active.png", self.root.parent().repo_path + "icons\\add_csv_inactive.png"])

        open_file_button.clicked.connect(lambda: editor(parent).open_file())
        create_file_button.clicked.connect(lambda: editor(parent).new_file())

        self.widget_layout.addStretch()

        self.widget_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.widget_layout.addWidget(welcome_label)
        self.widget_layout.addSpacing(2)
        self.widget_layout.addWidget(getting_started_label)
        self.widget_layout.addSpacing(20)
        self.widget_layout.addWidget(create_file_button)
        self.widget_layout.addWidget(open_file_button)
        self.widget_layout.addWidget(csv_file_button)

        self.widget_layout.addStretch()

class editor(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.root = parent



    def setup_root(self):
        for child in self.root.children():
            if isinstance(child, QWidget):
                child.deleteLater()

        clear_layout(self.root.layout())

        self.canvas_layout = QVBoxLayout()
        self.root.layout().addLayout(self.canvas_layout)


        title_label = QLabel(self.root, text="Editor")
        title_label.setStyleSheet("color: #ffffff; font-size: 26px;")
        

    def open_file(self):
        file_path = action.open_file_dialog()        

        if file_path != None:
            try:
                self.setup_root()
                self.canvas = canvas(self.root, file_path)
                #self.canvas.setSceneRect(0,0,self.root.width(),self.root.width())
                self.canvas.setStyleSheet("background-color: rgba(35,35,35,255); border-radius: 10px;")
                self.canvas_layout.addWidget(self.canvas)

            except Exception as e:
                print("Error loading file:", e)
                msg_box = QMessageBox(self.root)
                msg_box.setWindowTitle("Error")
                msg_box.setText("Oh no! An error occurred while loading the file.\n\nError details: \n" + str(e))
                msg_box.setIcon(QMessageBox.Icon.Critical)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.setStyleSheet("background-color: rgba(35,35,35,255); color: white; font-size: 16px;")
                msg_box.exec()

                welcome(self.root)

        else:
            msg_box = QMessageBox(self.root)
            msg_box.setWindowTitle("No file has been opened")
            msg_box.setText("Please select a valid file path to open.")
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.setStyleSheet("background-color: rgba(35,35,35,255); color: white; font-size: 16px;")
            msg_box.exec()

    def new_file(self):
        file_path = __file__.replace("gui\\pages.py", "example.json")

        if file_path != None:
            self.setup_root()
            self.canvas = canvas(self.root, file_path)
            self.canvas.setSceneRect(0,0,self.root.width(),self.root.width())
            self.canvas.setStyleSheet("background-color: rgba(35,35,35,255); border-radius: 10px;")
            self.canvas_layout.addWidget(self.canvas)

class welcome(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.setParent(parent)
        self.root = parent

        for child in parent.children():
            if isinstance(child, QWidget):
                child.deleteLater()

        self.widget_layout = QVBoxLayout() 
        parent.setLayout(self.widget_layout)
        
        welcome_label = QLabel(self, text="Welcome to the ErdModeler!")
        welcome_label.setStyleSheet("font-size: 35px;")
     
        getting_started_label = QLabel(self, text="How to get started:")
        getting_started_label.setStyleSheet("color: rgba(170,170,170,255); font-size: 18px;")

        create_file_button = menu_button(parent=self, text="create a new erd", icon_paths=[self.root.parent().repo_path + "icons\\add_database_active.png", self.root.parent().repo_path + "icons\\add_database_inactive.png"])
        open_file_button = menu_button(parent=self, text="open an existing erd", icon_paths=[self.root.parent().repo_path + "icons\\open_database_active.png", self.root.parent().repo_path + "icons\\open_database_inactive.png"])
        csv_file_button = menu_button(parent=self, text="extend the csv collection", icon_paths=[self.root.parent().repo_path + "icons\\add_csv_active.png", self.root.parent().repo_path + "icons\\add_csv_inactive.png"])

        open_file_button.clicked.connect(lambda: editor(parent).open_file())
        create_file_button.clicked.connect(lambda: editor(parent).new_file())

        self.widget_layout.addStretch()

        self.widget_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.widget_layout.addWidget(welcome_label)
        self.widget_layout.addSpacing(2)
        self.widget_layout.addWidget(getting_started_label)
        self.widget_layout.addSpacing(20)
        self.widget_layout.addWidget(create_file_button)
        self.widget_layout.addWidget(open_file_button)
        self.widget_layout.addWidget(csv_file_button)

        self.widget_layout.addStretch()
