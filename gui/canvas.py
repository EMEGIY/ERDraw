# This is one of the most important unit across the board,
# because it creates the canvas that holds attributes, relations and
# entities. For the sake of simplicity it also manages saving, exporting and 
# opening features, which are heavly working with the erd items in "gui/items.py" 


from PyQt6.QtWidgets import QApplication, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsRectItem, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt, QPointF, QDir
from PyQt6.QtGui import QPen
from gui.settings import extract_categories
import gui.items as items
import random
import generator
import os
import json

class canvas(QGraphicsView):
    def __init__(self, parent, file_path):
        super().__init__(parent)

        parent.canvas = self
        self.file_path = file_path

        # Sets the menubar to editing mode
        parent.parent().menu_bar.editing_mode()

        # Loads the json file
        # NOTE: Canvas can only be intialized with a valid file path
        #       New file is just opening example.json
        with open(self.file_path, "r") as f:
            self.file_data = json.load(f)

        # Creates the graphics scene (this will handle the visuals)
        self.scene = QGraphicsScene(self)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.setScene(self.scene)

        # Stores the items and connections
        # BUG: When an item gets removed, the
        #      line remains
        self.lines = []
        self.relations =[]
        self.entities = []
        self.attributes = []

        # To set a constant coord spawn point in scene
        test_rect = QGraphicsRectItem(0, 0, 5, 5)
        self.scene.addItem(test_rect)
        self.scene.removeItem(test_rect)

        # This will build data from json file
        self.build_from_data()

        # Updates the connections between items
        self.update_lines()

    def save_file(self):
        try:
            file_path = QFileDialog.getSaveFileName(self, "Save File", "", "Json Files (*.json)")

            with open(file_path[0], "w") as f:
                data = {
                    'entities': [entity.to_dict() for entity in self.entities],
                    'relations': [relation.to_dict() for relation in self.relations],
                    'attributes': [attribute.to_dict() for attribute in self.attributes]
                }
                print("Saving:", data)
                json.dump(data, f, indent=4)
        
                print("File saved successfully")
                
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("File Saved")
                msg_box.setText("Your file has been saved successfully! :)")
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.setStyleSheet("background-color: rgba(35,35,35,255); color: white; font-size: 16px;")
                msg_box.exec()

        except Exception as e:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Error during saving")
                msg_box.setText("Oh no! An error occurred while saving the file.")
                msg_box.setIcon(QMessageBox.Icon.Critical)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.setStyleSheet("background-color: rgba(35,35,35,255); color: white; font-size: 16px;")
                msg_box.exec()
        
    def build_from_data(self):
        # Actually self explaing building algorithm
        for entity in self.file_data['entities']:
            self.add_entity(
                name=entity['name'],
                x=entity['x'],
                y=entity['y'],
                width=entity['width'],
                height=entity['height'],
                dataset=entity['cap']
            )
        for relation in self.file_data['relations']:
            self.add_relation(
                name=relation['name'],
                x=relation['x'],
                y=relation['y'],
                width=relation['width'],
                height=relation['height'],
                dataset=relation['cap'],
                linked_entity_1=relation['linked_entity_1'],
                linked_entity_2=relation['linked_entity_2']
            )
        for attribute in self.file_data['attributes']:
            self.add_attribute(
                name=attribute['name'],
                x=attribute['x'],
                y=attribute['y'],
                width=attribute['width'],
                height=attribute['height'],
                linked_item=attribute['linked_item'],
                attribute=attribute['attribute']
            )
  
        self.redraw_lines()
        self.update_lines()            

    def update_lines(self):
        # goes through all connections and update it   
        for line in self.lines:
            line.update_line()
    
    def name_to_object(self, name):
        # Checks what object has the name
        # POTENTIAL_BUG:
        # There might be issues if name duplications appear
        # which is necassary for relations :/

        for attribute in self.attributes:
            if attribute.name == name:
                return attribute
        for entity in self.entities:
            if entity.name == name:
                return entity
        for relation in self.relations:
            if relation.name == name:
                return relation
    
    def redraw_lines(self):
        # This redraws all connections
        # to add new or remove un needed

        for line in self.lines:
            self.scene.removeItem(line)

        self.lines = []

        for attribute in self.attributes:
            if attribute.linked_item:
                self.lines.append(items.line(attribute, attribute.linked_item))
        for relation in self.relations:
            if relation.linked_entity_1:
                self.lines.append(items.line(relation, relation.linked_entity_1))
            if relation.linked_entity_2:
                self.lines.append(items.line(relation, relation.linked_entity_2))
        
        for line in self.lines:
            self.scene.addItem(line)
    
    # Functions to add items:
    # 1: creating the object
    # 2: adding object to scene
    # 3: move object to initial position
    # 4: append it object to object lists
    # 5: return object (not used, so optional)

    def add_relation(self, name="", x = 100, y = 100, width = 200, height = 100, linked_entity_1 = False, linked_entity_2 = False, dataset = False): # TODO
        relation = items.relation(name, self, 0, 0, width, height, linked_entity_1, linked_entity_2, dataset)
        self.scene.addItem(relation)
        relation.moveBy(x, y)
        self.relations.append(relation)

        return relation

    def add_entity(self, name="", x=100, y=100, width=200, height=100, dataset=False): # TODO
        entity = items.entity(name, self, 0, 0, width, height, dataset)
        self.scene.addItem(entity)
        entity.moveBy(x, y)
        self.entities.append(entity)

        return entity


    def add_attribute(self, name="", x=100, y=100, width=200, height=100, linked_item=False, attribute=False): # TODO
        attribute = items.attribute(name, self, 0, 0, width, height, linked_item, attribute)
        self.scene.addItem(attribute)
        attribute.moveBy(x, y)
        self.attributes.append(attribute)
        
        return attribute

    def export_file(self):
        # Open a QFileDialog to select a directory
        selected_directory = QFileDialog.getExistingDirectory(
            self, "Select Directory"
        )

        new_folder_path = None

        if selected_directory:
            # Ask the user for the new folder name
            folder_name, ok = QInputDialog.getText(self, "Create Folder", "Enter folder name:")

            if ok and folder_name:
                # Create the new folder
                new_folder_path = os.path.join(selected_directory, folder_name)
                try:
                    os.makedirs(new_folder_path, exist_ok=True)
                    QMessageBox.information(self, "Success", f"Folder created: {new_folder_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to create folder: {e}")
            else:
                QMessageBox.warning(self, "Cancelled", "Folder creation cancelled.")
        else:
            QMessageBox.warning(self, "Cancelled", "No directory selected.")
        
        if new_folder_path:
            # Generator Instance
            gen = generator.get()

            for entity in self.entities:
                current_entity_attributes = []

                # Collecting attributes for csv table
                for attribute in self.attributes:
                    if attribute.linked_item == entity:
                        current_entity_attributes.append(attribute)

                # Clearing the file
                with open(new_folder_path + f"\\{entity.name}.csv", "w", encoding='utf-8') as f: f.write("")
                with open(new_folder_path + f"\\{entity.name}.csv", "a", encoding='utf-8') as f: 
                    # Adding headline
                    line = ""
                    for attribute in current_entity_attributes:
                        line += attribute.name + ","
                    line = line[:-1] # remove last ,
                    f.write(line + "\n") # write headline

                with open(new_folder_path + f"\\{entity.name}.csv", "a", encoding='utf-8') as f: 
                    # Generating content line wise
                    for _ in range(entity.cap):
                        line = ""

                        for attribute in current_entity_attributes:

                            conversion_dict = {
                                "name": gen.name,
                                "first name": gen.first_name,
                                "last name": gen.last_name,
                                "prefix": gen.prefix,
                                "suffix": gen.suffix,
                                "address": gen.address,
                                "street adress": gen.street_address,
                                "book title": gen.book_title,
                                "cs_field": gen.cs_field,
                                "annual_salary": gen.annual_salary,
                                "date": gen.date
                            }
                            
                            line += (conversion_dict[attribute.attribute])().replace("\n", "") + ","

                        f.write(line[:-1] + "\n")

            for relation in self.relations:
                current_relation_attributes = []
                
                # Generator Instance
                gen = generator.get()

                # Collecting attributes for csv table
                for attribute in self.attributes:
                    if attribute.linked_item == relation:
                        current_relation_attributes.append(attribute)
                
                with open(new_folder_path + f"\\{relation.name}.csv", "w", encoding='utf-8') as f: f.write("")
                
                # In this step the attribute is going to link attrtibutes which are duplicating e.g:
                # Entity_1(Humans):
                #    first_name
                #    last_name
                #    age
                # Entity_2(Books):
                #    name
                #    book_id
                #    age
                #
                # If the relation now also got book_id, first_name and last_name as attributes
                # its going to:
                # 1: Get all book ids, first_names and so on
                # 2: assign every attribute value with a random other attribute value
                lines = [[] for _ in range(relation.cap)]
                

                print(extract_categories(new_folder_path + f"\\{relation.linked_entity_1.name}.csv") +
                    extract_categories(new_folder_path + f"\\{relation.linked_entity_2.name}.csv"))
                print([att.name for att in current_relation_attributes])
                for attribute in current_relation_attributes:
                    if attribute.name in (extract_categories(new_folder_path + f"\\{relation.linked_entity_1.name}.csv") +
                                    extract_categories(new_folder_path + f"\\{relation.linked_entity_2.name}.csv")):
                        if attribute.name in extract_categories(new_folder_path + f"\\{relation.linked_entity_1.name}.csv"):
                            index = extract_categories(new_folder_path + f"\\{relation.linked_entity_1.name}.csv").index(attribute.name) 
                            fp = new_folder_path + f"\\{relation.linked_entity_1.name}.csv"
                        else:
                            index = extract_categories(new_folder_path + f"\\{relation.linked_entity_2.name}.csv").index(attribute.name)
                            fp = new_folder_path + f"\\{relation.linked_entity_2.name}.csv"
                        
                        with open(fp, "r") as f:
                            for line, iteration in zip(f.readlines(), range(relation.cap)):
                                lines[iteration].append(
                                    line.replace("\n", "").split(",")[index]
                                )
                        
                    # # Shuffle the values
                        lines = [lines[0]] + random.sample(lines[1:], len(lines[1:]))
                    else:
                        for line in lines[1:]:
                            conversion_dict = {
                                "name": gen.name,
                                "first name": gen.first_name,
                                "last name": gen.last_name,
                                "prefix": gen.prefix,
                                "suffix": gen.suffix,
                                "address": gen.address,
                                "street adress": gen.street_address,
                                "book title": gen.book_title,
                                "cs_field": gen.cs_field,
                                "annual_salary": gen.annual_salary,
                                "date": gen.date
                            }
                            line.append(conversion_dict[attribute.attribute]())
                        lines[0].append(attribute.attribute)

                        
                with open(new_folder_path + f"\\{relation.name}.csv", "a", encoding='utf-8') as f: 
                    for line in lines:
                        komma_line = ""
                        for element in line:
                            komma_line += str(element) + "," 
                        f.write(komma_line[:-1] + "\n")