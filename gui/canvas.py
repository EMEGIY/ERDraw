from PyQt6.QtWidgets import QApplication, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsRectItem, QMessageBox
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPen
import os
import items
import json


class canvas(QGraphicsView):
    def __init__(self, parent, file_path):
        super().__init__(parent)

        parent.canvas = self
        self.file_path = file_path

        parent.parent().menu_bar.editing_mode()

        with open(self.file_path, "r") as f:
            self.file_data = json.load(f)

        self.scene = QGraphicsScene(self)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        #self.setSceneRect(0, 0, parent.width(), parent.height())
        self.setScene(self.scene)

        self.lines = []
        self.relations =[]
        self.entities = []
        self.attributes = []

        test_rect = QGraphicsRectItem(0, 0, 5, 5)
        self.scene.addItem(test_rect)
        self.scene.removeItem(test_rect)

        self.build_from_data()

        directory = __file__.replace("gui\\canvas.py", "csv_files")

        self.imported_data_sets = [f for f in os.listdir(directory) if f.endswith(".csv") and os.path.isfile(os.path.join(directory, f))]

        print("Imported datasets:", self.imported_data_sets)

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
        print("Building canvas from file")
        
        for entity in self.file_data['entities']:
            self.add_entity(
                name=entity['name'],
                x=entity['x'],
                y=entity['y'],
                width=entity['width'],
                height=entity['height'],
                dataset=entity['dataset']
            )
        for relation in self.file_data['relations']:
            self.add_relation(
                name=relation['name'],
                x=relation['x'],
                y=relation['y'],
                width=relation['width'],
                height=relation['height'],
                dataset=relation['dataset'],
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

        for relation in self.relations:
            relation.linked_entity_1 = self.name_to_object(relation.linked_entity_1) if relation.linked_entity_1 != "None" else False
            relation.linked_entity_2 = self.name_to_object(relation.linked_entity_2) if relation.linked_entity_2 != "None" else False
        for attribute in self.attributes:
            attribute.linked_item = self.name_to_object(attribute.linked_item) if attribute.linked_item != "None" else False
        
        self.redraw_lines()
        self.update_lines()            

    def add_relation(self, name="", x = 100, y = 100, width = 200, height = 100, linked_entity_1 = False, linked_entity_2 = False, dataset = False): # TODO
        while name in [relation.name for relation in self.relations]:
            name += str(len(self.relations) + 1) # Makes sure, there are no duplicates

        print("Adding relation:", x, y)
        
        relation = items.relation(name, self, 0, 0, width, height, linked_entity_1, linked_entity_2, dataset)
        self.scene.addItem(relation)
        relation.moveBy(x, y)

        self.relations.append(relation)

        return relation

    def add_entity(self, name="", x=100, y=100, width=200, height=100, dataset=False): # TODO
        while name in [entity.name for entity in self.entities]:
            name += str(len(self.entities) + 1) # Makes sure, there are no duplicates
        
        print("Adding entity:", x, y)

        entity = items.entity(name, self, 0, 0, width, height, dataset)
        self.scene.addItem(entity)
        entity.moveBy(x, y)

        
        self.entities.append(entity)

        return entity


    def add_attribute(self, name="", x=100, y=100, width=200, height=100, linked_item=False, attribute=False): # TODO
        while name in [attribute.name for attribute in self.attributes]:
            name += str(len(self.attributes) + 1) # Makes sure, there are no duplicates
        
        print("Adding entity:", x, y)

        attribute = items.attribute(name, self, 0, 0, width, height, linked_item, attribute)
        self.scene.addItem(attribute)
        attribute.moveBy(x, y)
        
        self.attributes.append(attribute)

        return attribute

    def update_lines(self):   
        for line in self.lines:
            line.update_line()
    
    def name_to_object(self, name):
        for attribute in self.attributes:
            if attribute.name == name:
                return attribute
        for entity in self.entities:
            if entity.name == name:
                return entity
        for relation in self.relations:
            if relation.name == name:
                return relation
        print("Could not find object with name:", name, " class: ", type(name))
    
    def redraw_lines(self):
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