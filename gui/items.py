# This file includes all items that will be used to draw the ERD
# as well as lines to connect them. They are all subclasses of QGraphicItems
# entity : QGraphicsRect
# relation : QGraphicsPolygon // there is no diamond in pyqt :(
# attribute: QGraphicsEclipse

# Imports
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsRectItem, QGraphicsPolygonItem
from PyQt6.QtCore import Qt, QPointF, QRectF, QLineF
from PyQt6.QtGui import QPen, QBrush, QColor, QPolygon, QPolygonF
import conv_dict
import gui.settings as settings

class line(QGraphicsLineItem):
    def __init__(self, obejct1, object2):
        super().__init__()
        self.setZValue(-1)
        self.obj_1 = obejct1
        self.obj_2 = object2
        self.setPen(QPen(Qt.GlobalColor.white, 2))
        self.update_line()

    def update_line(self):
        # Get the center points of the rectangles
        rect1_center = self.obj_1.sceneBoundingRect().center()
        rect2_center = self.obj_2.sceneBoundingRect().center()
        self.setLine(rect1_center.x(), rect1_center.y(), rect2_center.x(), rect2_center.y())

class relation(QGraphicsPolygonItem):
    def __init__(self, text, parent, x = 100, y = 100, width = 120, height = 60, linked_entity_1 = False, linked_entity_2 = False, cap = 100):
        super().__init__()
        self.name = text
        # Start pos
        self.org_x = x 
        self.org_y = y
        # Current pos
        self.new_x = x
        self.new_y = y
        
        # Starting size
        self.width = width
        self.height = height
        # Current size
        self.new_width = width
        self.new_height = height

        self.canvas = parent
        
        # Fill Color
        self.setBrush(QBrush(QColor(50,50,50, 255)))
        # Border Color
        self.setPen(QPen(Qt.GlobalColor.white, 2))
        
        # Changable attributes
        self.cap = cap # Number of lines that will be generated
        self.linked_entity_1 = linked_entity_1 # will be obj not string
        self.linked_entity_2 = linked_entity_2 # ---"---
        self.size_mult = 1 # width, height = width * size, height * size

        self.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable | QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges)

        # Set points        
        self.setPolygon(QPolygonF(
            [QPointF(x, y + height // 2), # Bottom point 
             QPointF(x + width // 2, y), # Right point 
             QPointF(x, y - height // 2), # Top point
             QPointF(x - width // 2, y)] # Left point
             )
        )

        # Sync the item
        self.update_settings([self.name, self.size_mult, self.linked_entity_1, self.linked_entity_2, self.cap])

    def to_dict(self):
        return {
            'name': self.name,
            'x': self.new_x,
            'y': self.new_y,
            'width': self.rect().width(),
            'height': self.rect().height(),
            'linked_entity_1': self.linked_entity_1.name,
            'linked_entity_2': self.linked_entity_2.name,
            'cap': self.cap
        }

    def rect(self):
        # This returns the rectangular size of the diamond
        return QRectF(
            self.org_x - self.width // 2, 
            self.org_y - self.height // 2, 
            self.width, 
            self.height
        )

    def paint(self, painter, option, widget=None):
        # Draws the text manualy (there is no build in way 
        # as far as i can tell)
        super().paint(painter, option, widget)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.name)

    def itemChange(self, change, value):
        # Handels dragging: adjust position & updating lines
        self.canvas.update_lines()

        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemPositionHasChanged:
            self.new_x = value.x()
            self.new_y = value.y()
        
        return super().itemChange(change, value)

    def update_settings(self, updated_settings):
        if updated_settings != None:
            
            self.name = updated_settings[0]
            self.size_mult = updated_settings[1]
            self.linked_entity_1 = self.canvas.name_to_object(updated_settings[2]) if updated_settings[2] != "None" else False
            self.linked_entity_2 = self.canvas.name_to_object(updated_settings[3]) if updated_settings[3] != "None" else False
            self.cap = updated_settings[4]

            self.height = 60 * self.size_mult
            self.width  = 120 * self.size_mult

            self.setPolygon(QPolygonF(
                [
                    QPointF(self.org_x, self.org_y + self.height // 2), 
                    QPointF(self.org_x + self.width // 2, self.org_y), 
                    QPointF(self.org_x, self.org_y - self.height // 2), 
                    QPointF(self.org_x - self.width // 2, self.org_y)
                ]
            ))

            self.update()
        
            self.canvas.redraw_lines()
            self.canvas.update_lines()
    
    def mousePressEvent(self, event):
        mods = QApplication.keyboardModifiers()
        if event.button() == Qt.MouseButton.RightButton and mods & Qt.KeyboardModifier.ShiftModifier:
            self.canvas.scene.removeItem(self)
            self.canvas.relations.remove(self)
        elif event.button() == Qt.MouseButton.RightButton:
            settings.run_relation(self)
        else:
            super().mousePressEvent(event)

class entity(QGraphicsRectItem):
    def __init__(self, text, parent, x = 100, y = 100, width = 120, height = 60, cap=100):
        super().__init__()
        # Starting pos
        self.org_x = x
        self.org_y = y

        # Current pos
        self.new_x = x
        self.new_y = y

        # Changable attributes
        self.size_mult = 1 # Size factor
        self.name = text
        self.cap = cap # Number of lines

        self.canvas = parent

        # Fill(Brush) and Border(Pen) color
        self.setBrush(QBrush(QColor(50,50,50, 255)))
        self.setPen(QPen(Qt.GlobalColor.white, 2))

        # Sets Rect
        self.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable | QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setRect(x - width // 2, y - height // 2, width, height)

        # Sync settings
        self.update_settings([self.name, self.size_mult, self.cap])

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.name)
    
    def to_dict(self):
        return {
            'name': self.name,
            'x': self.new_x - self.rect().width() // 2,
            'y': self.new_y - self.rect().height() // 2,
            'width': self.rect().width(),
            'height': self.rect().height(),
            'cap': self.cap
        }

    def itemChange(self, change, value):
        self.canvas.update_lines()

        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemPositionHasChanged:
            self.new_x = value.x() + self.rect().width() // 2
            self.new_y = value.y() + self.rect().height() // 2
        
        return super().itemChange(change, value)
   
    def update_settings(self, updated_settings):
        if updated_settings != None:
            
            self.name = updated_settings[0]
            self.size_mult = updated_settings[1]
            self.cap = updated_settings[2]

            self.setRect(self.org_x, self.org_y, 120 * self.size_mult, 60 * self.size_mult)
            self.update()
        
            self.canvas.redraw_lines()
            self.canvas.update_lines()

    def mousePressEvent(self, event):
        mods = QApplication.keyboardModifiers()
        if event.button() == Qt.MouseButton.RightButton and mods & Qt.KeyboardModifier.ShiftModifier:
            self.canvas.scene.removeItem(self)
            self.canvas.entities.remove(self)
        elif event.button() == Qt.MouseButton.RightButton:
            settings.run_entity(self)
        else:
            super().mousePressEvent(event)

class attribute(QGraphicsEllipseItem):  
    def __init__(self, text, parent, x = 100, y = 100, width = 120, height = 60, linked_item = False, attribute = False):
        super().__init__()

        # All available attributes
        self.list = [item for item in conv_dict.get()]

        # Intitial pos
        self.org_x = x
        self.org_y = y

        # Current pos
        self.new_x = x
        self.new_y = y

        self.size_mult = 1
        self.name = text
        self.attribute = attribute # actual attribute: string from self.list
                                   # (will be decoded on export)
        self.linked_item = linked_item
        self.canvas = parent

        # Color stuff
        self.setBrush(QBrush(QColor(50,50,50, 255)))
        self.setPen(QPen(Qt.GlobalColor.white, 2))

        # Sets rect
        self.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable | QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setRect(x, y, width, height)

        # Sync settings
        self.update_settings([self.name, self.size_mult, self.attribute, self.linked_item])

        # Rest of code is mostly the same as in other items
        
    def to_dict(self):
        return {
            'name': self.name,
            'x': self.new_x - self.rect().width() // 2,
            'y': self.new_y - self.rect().height() // 2,
            'width': self.rect().width(),
            'height': self.rect().height(),
            'linked_item': self.linked_item.name,
            'attribute': self.attribute
        }

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.name)

    def itemChange(self, change, value):
        self.canvas.update_lines()
        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemPositionHasChanged:
            self.new_x = value.x() + self.rect().width() // 2
            self.new_y = value.y() + self.rect().height() // 2

        return super().itemChange(change, value)

    def update_settings(self, updated_settings):
        if updated_settings != None:
            
            self.name = updated_settings[0]
            self.size_mult = updated_settings[1]
            self.attribute = updated_settings[2] if updated_settings[2] != "None" else False
            self.linked_item = self.canvas.name_to_object(updated_settings[3]) if updated_settings[3] != "None" else False

            self.setRect(self.org_x, self.org_y, 120 * self.size_mult, 60 * self.size_mult)
            self.update()
        
            #self.setPos(self.new_x - self.rect().width() // 2, self.new_y - self.rect().height() // 2)

            self.canvas.redraw_lines()
            self.canvas.update_lines()
    
    def mousePressEvent(self, event):
        mods = QApplication.keyboardModifiers()
        if event.button() == Qt.MouseButton.RightButton and mods & Qt.KeyboardModifier.ShiftModifier:
            self.canvas.scene.removeItem(self)
            self.canvas.attributes.remove(self)
        elif event.button() == Qt.MouseButton.RightButton:
            settings.run_attribute(self)
        else:
            super().mousePressEvent(event)