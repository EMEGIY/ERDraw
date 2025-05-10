from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QSlider, QFrame, QSpinBox
from PyQt6.QtCore import Qt
import customtkinter as ctk
import csv

button_style = """
        QPushButton {
            font-size: 18px;
            background-color: rgba(35,35,35,255);
            color: #ffffff;
            border: none;
            border-radius: 5px;
        }
        QPushButton:hover {
            font-size: 18px;
            color: #ffffff;
            border-radius: 5px;
            border: 2px solid #ffffff;
            background-color: rgba(35,35,35,255);
        }
        """

def extract_categories(csv_file_path):
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        categories = next(reader)  # Read the first row (headers)
    return categories

def setup(attribute):
    root = attribute.canvas.parent().parent()  

    window = QWidget(root)
    window.setGeometry(0, 0, root.width(), root.height())
    window.show()
    window.setStyleSheet("background-color: rgba(35,35,35,255); border-radius: 10px;")
    
    def fit_size(size):
        window.setFixedHeight(size.height())
        window.setFixedWidth(size.width())

    root.resizedConnect(fit_size)

    layout = QVBoxLayout(window)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    title_label = QLabel(window, text=f"Settings of {attribute.name}")
    title_label.setStyleSheet("color: #ffffff; font-size: 26px;")
    title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    layout.addWidget(title_label)

    layout.addStretch()

    frame = QFrame(window)
    frame.setStyleSheet("background-color: rgba(41,41,41,255); border-radius: 10px;")
    frame.setFixedHeight(root.height() // 2)
    frame.setFixedWidth(root.width() // 3)
    layout.addWidget(frame)

    frame_layout = QVBoxLayout(frame)
    frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    frame_layout.addSpacing(15)

    return root, frame, frame_layout, layout, window

def run_attribute(attribute):
    
    root, frame, frame_layout, layout, window = setup(attribute)

    name_label = QLabel(frame, text="Name:")
    name_label.setStyleSheet("color: #ffffff; font-size: 16px;")
    name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    name_label.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(name_label)

    name_entry = QLineEdit(frame, text=attribute.name, placeholderText="Name of the attribute", maxLength=20)
    name_entry.setStyleSheet("background-color: rgba(50,50,50,255); color: #ffffff; border-radius: 5px;")
    name_entry.setFixedHeight(30)
    name_entry.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(name_entry)

    frame_layout.addSpacing(15)

    size_label = QLabel(frame, text="Scale Factor:")
    size_label.setStyleSheet("color: #ffffff; font-size: 16px;")
    size_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    size_label.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(size_label)

    size_slider = QSlider(Qt.Orientation.Horizontal, frame)
    size_slider.setRange(1, 400)
    size_slider.setSingleStep(5)
    size_slider.setValue(int(attribute.size_mult * 100))
    size_slider.setStyleSheet("color: #ffffff; border-radius: 5px;")
    size_slider.setFixedHeight(20)
    size_slider.setFixedWidth(root.width() // 4)
    size_slider.setToolTip(str(size_slider.value()))
    size_slider.valueChanged.connect(lambda: size_slider.setToolTip(str(size_slider.value())))

    frame_layout.addWidget(size_slider)
    
    frame_layout.addSpacing(15)
    
    connection_label = QLabel(frame, text="Connections:")
    connection_label.setStyleSheet("color: #ffffff; font-size: 16px;")
    connection_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    connection_label.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(connection_label)
    connection_combo = QComboBox(frame)
    connection_combo.setStyleSheet("font-size: 14px; background-color: rgba(50,50,50,255); color: #ffffff; border-radius: 0px;")
    connection_combo.setFixedHeight(30)
    connection_combo.setFixedWidth(root.width() // 4)
    connection_combo.addItem("None")
    connection_combo.addItems([entity.name for entity in attribute.canvas.entities] + [relation.name for relation in attribute.canvas.relations])
    connection_combo.setCurrentText(attribute.linked_item.name if attribute.linked_item else "None")
    frame_layout.addWidget(connection_combo)

    frame_layout.addSpacing(15)

    attribute_label = QLabel(frame, text="Assigned Attribute:")
    attribute_label.setStyleSheet("color: #ffffff; font-size: 16px;")
    attribute_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    attribute_label.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(attribute_label)
    attribute_combo = QComboBox(frame)
    attribute_combo.setStyleSheet("font-size: 14px; background-color: rgba(50,50,50,255); color: #ffffff; border-radius: 0px;")
    attribute_combo.setFixedHeight(30)
    attribute_combo.setFixedWidth(root.width() // 4)
    attribute_combo.addItem("None")

    attribute_combo.addItems(attribute.list)

    attribute_combo.setCurrentText(attribute.attribute if attribute.attribute else "None")


    frame_layout.addWidget(attribute_combo)

    layout.addStretch()

    button_container = QWidget(window)
    button_container.setStyleSheet("background-color: rgba(35,35,35,255); border-radius: 10px; font-size: 16px; ")
    button_container.setFixedHeight(root.height() // 10)
    button_container.setFixedWidth(root.width() // 3)
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

    def save():
        root.setMinimumSize(0, 0)
        root.setMaximumSize(16777215, 16777215)
        
        attribute.update_settings(
            [
                name_entry.text(), 
                size_slider.value() / 100, 
                attribute_combo.currentText() if attribute_combo.currentText() != "None" else None, 
                connection_combo.currentText() if connection_combo.currentText() != "None" else None
                ]
            )
        window.close()

    submit_button.clicked.connect(save)
    cancel_button.clicked.connect(close)

    button_layout.addWidget(submit_button)

    #while window.isVisible(): pass


def run_entity(entity):
    root, frame, frame_layout, layout, window = setup(entity)

    name_label = QLabel(frame, text="Name:")
    name_label.setStyleSheet("color: #ffffff; font-size: 16px;")
    name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    name_label.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(name_label)

    name_entry = QLineEdit(frame, text=entity.name, placeholderText="Name of the entity:", maxLength=20)
    name_entry.setStyleSheet("background-color: rgba(50,50,50,255); color: #ffffff; border-radius: 5px;")
    name_entry.setFixedHeight(30)
    name_entry.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(name_entry)

    frame_layout.addSpacing(15)

    size_label = QLabel(frame, text="Scale Factor:")
    size_label.setStyleSheet("color: #ffffff; foNt-size: 16px;")
    size_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    size_label.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(size_label)

    size_slider = QSlider(Qt.Orientation.Horizontal, frame)
    size_slider.setRange(1, 400)
    size_slider.setSingleStep(5)
    size_slider.setValue(int(entity.size_mult * 100))
    size_slider.setStyleSheet("color: #ffffff; border-radius: 5px;")
    size_slider.setFixedHeight(20)
    size_slider.setFixedWidth(root.width() // 4)
    size_slider.setToolTip(str(size_slider.value()))
    size_slider.valueChanged.connect(lambda: size_slider.setToolTip(str(size_slider.value())))
    frame_layout.addWidget(size_slider)

    frame_layout.addSpacing(15)

    cap_label = QLabel(frame, text="Lines:")
    cap_label.setStyleSheet("color: #ffffff; font-size: 16px;")
    cap_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    cap_label.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(cap_label)

    cap_spin_box = QSpinBox()
    cap_spin_box.setMinimum(0)  # Set the minimum value
    cap_spin_box.setMaximum(10000)  # Set the maximum value
    cap_spin_box.setValue(entity.cap)  # Set the default value
    cap_spin_box.setSingleStep(1)  # Set the step size (increment/decrement)
    cap_spin_box.setStyleSheet("font-size: 16px; background: rgba(50,50,50,255)")  # Optional: Style the spin box
    frame_layout.addWidget(cap_spin_box)

    layout.addStretch()

    button_container = QWidget(window)
    button_container.setStyleSheet("background-color: rgba(35,35,35,255); border-radius: 10px; font-size: 16px; ")
    button_container.setFixedHeight(root.height() // 10)
    button_container.setFixedWidth(root.width() // 3)
    layout.addWidget(button_container)
    button_layout = QHBoxLayout(button_container)
    button_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

    cancel_button = QPushButton(button_container, text="Cancel")
    cancel_button.setFixedHeight(45)
    cancel_button.setContentsMargins(15, 15, 15, 15)
    cancel_button.setStyleSheet(button_style)
    cancel_button.clicked.connect(window.close)
    button_layout.addWidget(cancel_button)

    submit_button = QPushButton(button_container, text="Submit")
    submit_button.setFixedHeight(45)
    submit_button.setContentsMargins(15, 15, 15, 15)
    submit_button.setStyleSheet(button_style)
    
    def save():
        entity.update_settings(
            [
                name_entry.text(), 
                size_slider.value() / 100, 
                cap_spin_box.value()
                ]
            )
        window.close()

    submit_button.clicked.connect(save)

    button_layout.addWidget(submit_button)

def run_relation(relation):
    root = relation.canvas.parent().parent()  
    root.setFixedSize(root.width(), root.height())  

    window = QWidget(root)
    window.setGeometry(0, 0, root.width(), root.height())
    window.show()
    window.setStyleSheet("background-color: rgba(35,35,35,255); border-radius: 10px;")
    
    layout = QVBoxLayout(window)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    title_label = QLabel(window, text=f"Settings of {relation.name}")
    title_label.setStyleSheet("color: #ffffff; font-size: 26px;")
    title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    layout.addWidget(title_label)

    layout.addStretch()

    frame = QFrame(window)
    frame.setStyleSheet("background-color: rgba(41,41,41,255); border-radius: 10px;")
    frame.setFixedHeight(root.height() // 2)
    frame.setFixedWidth(root.width() // 3)
    layout.addWidget(frame)

    frame_layout = QVBoxLayout(frame)
    frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    frame_layout.addSpacing(15)

    name_label = QLabel(frame, text="Name:")
    name_label.setStyleSheet("color: #ffffff; font-size: 16px;")
    name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    name_label.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(name_label)

    name_entry = QLineEdit(frame, text=relation.name, placeholderText="Name of the relation:", maxLength=20)
    name_entry.setStyleSheet("background-color: rgba(50,50,50,255); color: #ffffff; border-radius: 5px;")
    name_entry.setFixedHeight(30)
    name_entry.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(name_entry)

    frame_layout.addSpacing(15)

    size_label = QLabel(frame, text="Scale Factor:")
    size_label.setStyleSheet("color: #ffffff; font-size: 16px;")
    size_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    size_label.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(size_label)

    size_slider = QSlider(Qt.Orientation.Horizontal, frame)
    size_slider.setRange(1, 400)
    size_slider.setSingleStep(5)
    size_slider.setValue(int(relation.size_mult * 100))
    size_slider.setStyleSheet("color: #ffffff; border-radius: 5px;")
    size_slider.setFixedHeight(20)
    size_slider.setFixedWidth(root.width() // 4)
    size_slider.setToolTip(str(size_slider.value()))
    size_slider.valueChanged.connect(lambda: size_slider.setToolTip(str(size_slider.value())))
    frame_layout.addWidget(size_slider)

    frame_layout.addSpacing(15)

    connection_label_1 = QLabel(frame, text="Entity 1:")
    connection_label_1.setStyleSheet("color: #ffffff; font-size: 16px;")
    connection_label_1.setAlignment(Qt.AlignmentFlag.AlignLeft)
    connection_label_1.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(connection_label_1)

    connection_combo_1 = QComboBox(frame)
    connection_combo_1.setStyleSheet("font-size: 14px; background-color: rgba(50,50,50,255); color: #ffffff; border-radius: 0px;")
    connection_combo_1.setFixedHeight(30)
    connection_combo_1.setFixedWidth(root.width() // 4)
    connection_combo_1.addItem("None")
    connection_combo_1.addItems([entity.name for entity in relation.canvas.entities])
    if relation.linked_entity_2: connection_combo_1.removeItem(connection_combo_1.findText(relation.linked_entity_2.name))
    if relation.linked_entity_1: connection_combo_1.setCurrentText(relation.linked_entity_1.name if relation.linked_entity_1 else "None")
    frame_layout.addWidget(connection_combo_1)

    frame_layout.addSpacing(15)

    connection_label_2 = QLabel(frame, text="Entity 2:")
    connection_label_2.setStyleSheet("color: #ffffff; font-size: 16px;")
    connection_label_2.setAlignment(Qt.AlignmentFlag.AlignLeft)
    connection_label_2.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(connection_label_2)

    connection_combo_2 = QComboBox(frame)
    connection_combo_2.setStyleSheet("font-size: 14px; background-color: rgba(50,50,50,255); color: #ffffff; border-radius: 0px;")
    connection_combo_2.setFixedHeight(30)
    connection_combo_2.setFixedWidth(root.width() // 4)
    connection_combo_2.addItem("None")
    connection_combo_2.addItems([entity.name for entity in relation.canvas.entities])
    if relation.linked_entity_1: connection_combo_2.removeItem(connection_combo_2.findText(relation.linked_entity_1.name))
    if relation.linked_entity_2: connection_combo_2.setCurrentText(relation.linked_entity_2.name if relation.linked_entity_2 else "None")
    frame_layout.addWidget(connection_combo_2)

    frame_layout.addSpacing(15)

    cap_label = QLabel(frame, text="Lines:")
    cap_label.setStyleSheet("color: #ffffff; font-size: 16px;")
    cap_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    cap_label.setFixedWidth(root.width() // 4)
    frame_layout.addWidget(cap_label)

    cap_spin_box = QSpinBox()
    cap_spin_box.setMinimum(0)  # Set the minimum value
    cap_spin_box.setMaximum(10000)  # Set the maximum value
    cap_spin_box.setValue(relation.cap)  # Set the default value
    cap_spin_box.setSingleStep(1)  # Set the step size (increment/decrement)
    cap_spin_box.setStyleSheet("font-size: 16px; background: rgba(50,50,50,255)")  # Optional: Style the spin box
    frame_layout.addWidget(cap_spin_box)

    layout.addStretch()

    button_container = QWidget(window)
    button_container.setStyleSheet("background-color: rgba(35,35,35,255); border-radius: 10px; font-size: 16px; ")
    button_container.setFixedHeight(root.height() // 10)
    button_container.setFixedWidth(root.width() // 3)
    layout.addWidget(button_container)
    button_layout = QHBoxLayout(button_container)
    button_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

    cancel_button = QPushButton(button_container, text="Cancel")
    cancel_button.setFixedHeight(45)
    cancel_button.setContentsMargins(15, 15, 15, 15)
    cancel_button.setStyleSheet(button_style)
    cancel_button.clicked.connect(window.close)
    button_layout.addWidget(cancel_button)

    submit_button = QPushButton(button_container, text="Submit")
    submit_button.setFixedHeight(45)
    submit_button.setContentsMargins(15, 15, 15, 15)
    submit_button.setStyleSheet(button_style)
    
    def save():
        print("Connection 1:", connection_combo_1.currentText())
        print("Connection 2:", connection_combo_2.currentText())

        relation.update_settings(
            [
                name_entry.text(), 
                size_slider.value() / 100, 
                connection_combo_1.currentText() if connection_combo_1.currentText() != "None" else None,
                connection_combo_2.currentText() if connection_combo_2.currentText() != "None" else None,
                cap_spin_box.value()
            ]
        )
        
        window.close()

    submit_button.clicked.connect(save)

    button_layout.addWidget(submit_button)

