from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QPushButton, QLineEdit, QComboBox, QMessageBox)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from prefabs.buttons import menu_button
from settings import extract_categories, button_style

combo_style = '''
        QComboBox {
            background-color: rgba(50,50,50,255);
            color: #ffffff;
            font-size: 18px;
            border-radius: 4px;
            padding-right: 0px;  /* Remove space for the arrow */
        }
        QComboBox::drop-down {
            background: none;  /* Remove the dropdown button */
            border: none;
        }
    '''

def update(combo1, combo2, combo3, canvas):

    def do_nothing():
        pass

    # To Avoid a recursion error when the combo boxes are updated
    combo1.currentTextChanged.connect(do_nothing)
    combo2.currentTextChanged.connect(do_nothing)

    if (combo1.currentText() != "None" and combo1.currentText() != "") and (combo2.currentText() != "None" and combo2.currentText() != ""):
        print("Dataset1:", combo1.currentText())
        print("Dataset2:", combo2.currentText())

        combo3.setEnabled(True)
        combo3.clear()
        for dataset_1_categorie in extract_categories(__file__.replace("gui\\assignment.py", "csv_files\\" + combo1.currentText())):
            for dataset_2_categorie in extract_categories(__file__.replace("gui\\assignment.py", "csv_files\\" + combo2.currentText())):
                if dataset_1_categorie == dataset_2_categorie:
                    combo3.addItem(dataset_1_categorie)
    else:
        combo3.clear()
        combo3.setEnabled(False)
    
    if combo1.currentText() != "None" and combo1.currentText() != "":
        if combo2.currentText() == "None":
            next_text = "None"
        else:
            next_text = combo2.currentText()
        
        combo2.clear()
        combo2.addItem("None")
        
        for item in canvas.imported_data_sets:
            if item != combo1.currentText():
                combo2.addItem(item)    

        combo2.setCurrentText(next_text)

    if combo2.currentText() != "None" and combo2.currentText() != "":
        if combo1.currentText() == "None":
            next_text = "None"
        else:
            next_text = combo2.currentText()
        
        combo1.clear()
        combo1.addItem("None")
        
        for item in canvas.imported_data_sets:
            if item != combo2.currentText():
                combo1.addItem(item)    

        combo1.setCurrentText(next_text)

    combo1.currentTextChanged.connect(lambda e: update(combo1, combo2, combo3, canvas))
    combo2.currentTextChanged.connect(lambda e: update(combo1, combo2, combo3, canvas))


def run_creator(canvas):
    root = canvas.parent().parent()
    root.setFixedSize(root.width(), root.height())  

    window = QWidget(root)
    window.setGeometry(0, 0, root.width(), root.height())
    window.show()
    window.setStyleSheet("background-color: rgba(35,35,35,255); border-radius: 5px;")
    
    layout = QVBoxLayout(window)
    layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    print(layout.alignment())

    title_label = QLabel(window, text=f"Assignment Table Creator")
    title_label.setStyleSheet("color: #ffffff; font-size: 24px;")
    title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    title_label.setFixedWidth(root.width() // 4)
    layout.addWidget(title_label)

    layout.addStretch()

    name_label = QLabel(window, text="Assignment Table Name:")
    name_label.setStyleSheet("color: #ffffff; font-size: 18px;")
    name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    name_label.setFixedHeight(30)
    name_label.setFixedWidth(root.width() // 4)
    layout.addWidget(name_label)

    name_entry = QLineEdit(window)
    name_entry.setStyleSheet("background-color: rgba(50,50,50,255); color: #ffffff; font-size: 18px; border-radius: 4px")
    name_entry.setFixedHeight(37)
    name_entry.setFixedWidth(root.width() // 4)
    name_entry.setPlaceholderText("Enter table name here")
    layout.addWidget(name_entry)
    layout.addSpacing(15)

    dataset_1_label = QLabel(window, text="Select first Dataset:")
    dataset_1_label.setStyleSheet("color: #ffffff; font-size: 18px;")
    dataset_1_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    dataset_1_label.setFixedHeight(30)
    dataset_1_label.setFixedWidth(root.width() // 4)
    layout.addWidget(dataset_1_label)

    dataset_1_combo_box = QComboBox(window)
    dataset_1_combo_box.setStyleSheet(combo_style)
    dataset_1_combo_box.setFixedHeight(37)
    dataset_1_combo_box.setFixedWidth(root.width() // 4)
    dataset_1_combo_box.setCursor(Qt.CursorShape.PointingHandCursor)
    dataset_1_combo_box.setPlaceholderText("No dataset selected...")
    dataset_1_combo_box.setContentsMargins(0, 0, 0, 0)
    dataset_1_combo_box.setCursor(Qt.CursorShape.PointingHandCursor)
    dataset_1_combo_box.setToolTip("Select first dataset")
    dataset_1_combo_box.addItem("None")
    dataset_1_combo_box.setCurrentText("None")
    

    for dataset in canvas.imported_data_sets:
        dataset_1_combo_box.addItem(dataset)
    
    layout.addWidget(dataset_1_combo_box)
    layout.addSpacing(15)

    dataset_2_label = QLabel(window, text="Select second Dataset:")
    dataset_2_label.setStyleSheet("color: #ffffff; font-size: 18px;")
    dataset_2_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    dataset_2_label.setFixedHeight(30)
    dataset_2_label.setFixedWidth(root.width() // 4)
    layout.addWidget(dataset_2_label)

    dataset_2_combo_box = QComboBox(window)
    dataset_2_combo_box.setStyleSheet(combo_style)
    dataset_2_combo_box.setFixedHeight(37)
    dataset_2_combo_box.setFixedWidth(root.width() // 4)
    dataset_2_combo_box.setCursor(Qt.CursorShape.PointingHandCursor)
    dataset_2_combo_box.setPlaceholderText("No dataset selected...")
    dataset_2_combo_box.setContentsMargins(0, 0, 0, 0)
    dataset_2_combo_box.setCursor(Qt.CursorShape.PointingHandCursor)
    dataset_2_combo_box.setToolTip("Select second dataset")
    dataset_2_combo_box.addItem("None")
    dataset_2_combo_box.setCurrentText("None")

    for dataset in canvas.imported_data_sets:
        dataset_2_combo_box.addItem(dataset)
    
    layout.addWidget(dataset_2_combo_box)
    layout.addSpacing(15)

    assignment_argument_label = QLabel(window, text="Select assignment argument:")
    assignment_argument_label.setStyleSheet("color: #ffffff; font-size: 18px;")
    assignment_argument_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    assignment_argument_label.setFixedHeight(30)
    assignment_argument_label.setFixedWidth(root.width() // 4)
    layout.addWidget(assignment_argument_label)

    assignment_argument_combo_box = QComboBox(window)
    assignment_argument_combo_box.setStyleSheet(combo_style)
    assignment_argument_combo_box.setFixedHeight(37)
    assignment_argument_combo_box.setFixedWidth(root.width() // 4)
    assignment_argument_combo_box.setCursor(Qt.CursorShape.PointingHandCursor)
    assignment_argument_combo_box.setPlaceholderText("No argument selected...")
    assignment_argument_combo_box.setContentsMargins(0, 0, 0, 0)
    assignment_argument_combo_box.setCursor(Qt.CursorShape.PointingHandCursor)
    assignment_argument_combo_box.setToolTip("Select assignment argument")
    assignment_argument_combo_box.addItem("None")
    assignment_argument_combo_box.setCurrentText("None")
    assignment_argument_combo_box.setEnabled(False)

    layout.addWidget(assignment_argument_combo_box)
    layout.addStretch()

    dataset_1_combo_box.currentTextChanged.connect(lambda e: update(dataset_1_combo_box, dataset_2_combo_box, assignment_argument_combo_box, canvas))
    dataset_2_combo_box.currentTextChanged.connect(lambda e: update(dataset_1_combo_box, dataset_2_combo_box, assignment_argument_combo_box, canvas))


"""
attribute_container = QWidget(window)
    attribute_container.setStyleSheet("background-color: rgba(35,35,35,255);")
    attribute_container.setFixedHeight(50)
    attribute_container.setContentsMargins(0, 0, 0, 0)
    attribute_container.setFixedWidth(root.width() // 4)

    attribute_layout = QHBoxLayout(attribute_container)
    attribute_layout.setContentsMargins(0, 0, 0, 0)

    attribute_label = QLabel(window, text="Attributes")
    attribute_label.setStyleSheet("color: #ffffff; font-size: 18px;")
    attribute_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    attribute_label.setFixedHeight(30)

    attribute_push_button = QPushButton(window, text="")
    attribute_push_button.setStyleSheet("background-color: rgba(35,35,35,255)")
    attribute_push_button.setIcon(QIcon(__file__.replace("gui\\assignment.py", "icons\\plus.png")))    
    attribute_push_button.setIconSize(QSize(30, 30))
    attribute_push_button.setFixedHeight(30)
    attribute_push_button.setFixedWidth(30)
    attribute_push_button.setCursor(Qt.CursorShape.PointingHandCursor)
    attribute_push_button.setToolTip("Add Attribute")
    
    attribute_layout.addWidget(attribute_label)
    attribute_layout.addStretch()
    attribute_layout.addWidget(attribute_push_button)
    layout.addWidget(attribute_container)


    attribute_collection = QWidget(window)
    attribute_collection.setStyleSheet("background-color: rgba(35,35,35,255);")
    attribute_collection.setFixedHeight(root.height() // 3)
    attribute_collection.setFixedWidth(root.width() // 4)
    layout.addWidget(attribute_collection)

    attribute_container_layout = QVBoxLayout(attribute_collection)
    attribute_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    attribute_container_layout.setContentsMargins(0, 0, 0, 0)

    widget_list = []


    def add_attribute():
        widget = QWidget(attribute_collection)
        widget_list.append(widget)

        widget.setStyleSheet("background-color: rgba(50,50,50,255);")
        widget.setFixedHeight(65)
        widget.setFixedWidth(root.width() // 4)
        attribute_container_layout.addWidget(widget)

        vertical_layout = QVBoxLayout(widget)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        vertical_layout.setContentsMargins(5, 0, 5, 0)

        attribute_layout = QHBoxLayout()
        attribute_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        widget.NameEntry = QLineEdit(widget)
        widget.NameEntry.setStyleSheet("background-color: rgba(50,50,50,255); color: #ffffff; font-size: 18px; border-radius: 4px")
        widget.NameEntry.setFixedHeight(30)
        widget.NameEntry.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        widget.NameEntry.setFixedWidth(root.width() // 4 - 40)
        widget.NameEntry.setPlaceholderText("Name...")
        attribute_layout.addWidget(widget.NameEntry)
        print(widget.NameEntry.text())

        attribute_push_button = QPushButton(widget, text="")
        attribute_push_button.setStyleSheet("background-color: rgba(50,50,50,255); border-radius: 4px;")
        attribute_push_button.setIcon(QIcon(__file__.replace("gui\\assignment.py", "icons\\delete.png")))
        attribute_push_button.setIconSize(QSize(20, 20))
        attribute_push_button.setFixedHeight(30)
        attribute_push_button.setFixedWidth(20)
        attribute_push_button.setCursor(Qt.CursorShape.PointingHandCursor)
        attribute_push_button.setToolTip("Delete Attribute")
        attribute_push_button.clicked.connect(lambda: widget.deleteLater())
        attribute_layout.addWidget(attribute_push_button)

        widget.combo_box = QComboBox(widget)
        widget.combo_box.setStyleSheet('''
            QComboBox {
                background-color: rgba(50,50,50,255);
                color: #ffffff;
                font-size: 18px;
                border-radius: 4px;
                padding-right: 0px;  /* Remove space for the arrow */
            }
            QComboBox::drop-down {
                background: none;  /* Remove the dropdown button */
                border: none;
            }
        ''')
        widget.combo_box.setFixedHeight(30)
        widget.combo_box.setFixedWidth(root.width() // 4 - 10)
        widget.combo_box.setCursor(Qt.CursorShape.PointingHandCursor)
        
        for dataset in canvas.imported_data_sets:
            for categorie in extract_categories(__file__.replace("gui\\assignment.py", "csv_files\\" + dataset)):
                widget.combo_box.addItem(categorie)

        widget.combo_box.setPlaceholderText("Select attribute...")
        
        vertical_layout.addLayout(attribute_layout)
        vertical_layout.addWidget(widget.combo_box)

    attribute_push_button.clicked.connect(add_attribute)

    layout.addStretch()
    
    button_container = QWidget(window)
    button_container.setStyleSheet("background-color: rgba(35,35,35,255); border-radius: 10px; font-size: 16px; ")
    button_container.setFixedHeight(root.height() // 10)
    button_container.setFixedWidth(root.width() // 4)
    layout.addWidget(button_container)
    button_layout = QHBoxLayout(button_container)
    button_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

    cancel_button = QPushButton(button_container, text="Cancel")
    cancel_button.setFixedHeight(45)
    cancel_button.setContentsMargins(15, 15, 15, 15)
    cancel_button.setStyleSheet(button_style)
    button_layout.addWidget(cancel_button)

    submit_button = QPushButton(button_container, text="Submit")
    submit_button.setFixedHeight(45)
    submit_button.setContentsMargins(15, 15, 15, 15)
    submit_button.setStyleSheet(button_style)
    
    def close():
        root.setMinimumSize(0, 0)
        root.setMaximumSize(16777215, 16777215)
        window.close()

    def error_box():
        error_box = QMessageBox(window)
        error_box.setWindowTitle("Error")
        error_box.setText("Please fill in all fields.")
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_box.setStyleSheet("background-color: rgba(35,35,35,255); color: white; font-size: 16px;")
        error_box.exec()

    def save():
        root.setMinimumSize(0, 0)
        root.setMaximumSize(16777215, 16777215)

        if name_entry.text() == "" or len(widget_list) == 0:
            error_box()
            return
        else:
            with open(__file__.replace("gui\\assignment.py", "csv_files\\" + name_entry.text() + ".csv"), "w") as f: f.write("")

            with open(__file__.replace("gui\\assignment.py", "csv_files\\" + name_entry.text() + ".csv"), "a") as f:
                f.write("".join([widget.NameEntry.text() + "," for widget in widget_list])+"\n")
                for widget in widget_list:
                    if widget.NameEntry.text() != "" and widget.combo_box.currentText() != "":
                        pass
                    else:
                        error_box()
                        return

    submit_button.clicked.connect(save)
    cancel_button.clicked.connect(close)

    button_layout.addWidget(submit_button)


"""