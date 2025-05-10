from PyQt6.QtGui import QAction
from gui.pages import editor

class menu_bar():
    def __init__(self, parent):
            
        # Get the menu bar
        self.menu_bar = parent.menuBar()

        # Add "File" menu
        self.file_menu = self.menu_bar.addMenu("File")
        self.new_action = QAction("New", parent)
        self.new_action.setShortcut("Ctrl+N")
        self.open_action = QAction("Open", parent)
        self.open_action.setShortcut("Ctrl+O")
        self.save_action = QAction("Save", parent)
        self.save_action.setShortcut("Ctrl+S")
        self.export_action = QAction("Export", parent)
        self.export_action.setShortcut("Ctrl+E")
        self.exit_action = QAction("Exit", parent)
        self.exit_action.setShortcut("Ctrl+Q")

        self.save_action.setEnabled(False)
        self.export_action.setEnabled(False)

        self.exit_action.triggered.connect(parent.close)  # Connect Exit action to close the app
        self.open_action.triggered.connect(lambda: editor(parent.main_container).open_file())
        self.new_action.triggered.connect(lambda: editor(parent.main_container).new_file())
        self.save_action.triggered.connect(lambda: parent.main_container.canvas.save_file())
        self.export_action.triggered.connect(lambda: parent.main_container.canvas.export_file())
        
        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.export_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        # Add "Edit" menu
        self.edit_menu = self.menu_bar.addMenu("Edit")
        self.create_relation_action = QAction("Create relation", parent)
        self.create_entity_action = QAction("Create entity", parent)
        self.create_attribute_action = QAction("Create attribute", parent)
        self.create_editor_action = QAction("Create assignment table", parent)

        self.create_editor_action.setShortcut("Ctrl+T")

        self.create_relation_action.triggered.connect(lambda: parent.main_container.canvas.add_relation("Relation "))
        self.create_entity_action.triggered.connect(lambda: parent.main_container.canvas.add_entity("Entity "))
        self.create_attribute_action.triggered.connect(lambda: parent.main_container.canvas.add_attribute("Attribute "))
        self.create_editor_action.triggered.connect(lambda: run_creator(parent.main_container.canvas))
        
        self.create_attribute_action.setEnabled(False)
        self.create_relation_action.setEnabled(False)
        self.create_entity_action.setEnabled(False)
        self.create_editor_action.setEnabled(False)

        self.edit_menu.addAction(self.create_relation_action)
        self.edit_menu.addAction(self.create_entity_action)
        self.edit_menu.addAction(self.create_attribute_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.create_editor_action)

        # Add "Help" menu
        help_menu = self.menu_bar.addMenu("Help")
        about_action = QAction("About", parent)
        help_menu.addAction(about_action)

    def editing_mode(self):
        self.save_action.setEnabled(True)
        self.export_action.setEnabled(True)
        self.new_action.setEnabled(False)
        self.open_action.setEnabled(False)
        self.create_relation_action.setEnabled(True)
        self.create_entity_action.setEnabled(True)
        self.create_attribute_action.setEnabled(True)
        self.create_editor_action.setEnabled(True)