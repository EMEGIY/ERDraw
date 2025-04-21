from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsRectItem, QGraphicsPolygonItem
from PyQt6.QtCore import Qt, QPointF, QRectF, QLineF
from PyQt6.QtGui import QPen, QBrush, QColor, QPolygon, QPolygonF
import settings

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
        print("Obj 1:", self.obj_1)
        print("Obj 2:", self.obj_2)
        rect1_center = self.obj_1.sceneBoundingRect().center()
        rect2_center = self.obj_2.sceneBoundingRect().center()
        self.setLine(rect1_center.x(), rect1_center.y(), rect2_center.x(), rect2_center.y())



class relation(QGraphicsPolygonItem):
    def __init__(self, text, parent, x = 100, y = 100, width = 120, height = 60, linked_entity_1 = False, linked_entity_2 = False, dataset = False):
        super().__init__()
        self.size_mult = 1

        self.name = text
        self.org_x = x
        self.org_y = y
        self.new_x = x
        self.new_y = y
        self.new_width = width
        self.new_height = height
        self.width = width
        self.height = height
        self.canvas = parent


        self.setBrush(QBrush(QColor(50,50,50, 255)))
        self.setPen(QPen(Qt.GlobalColor.white, 2))
        
        self.dataset = dataset
        self.linked_entity_1 = linked_entity_1
        self.linked_entity_2 = linked_entity_2

        self.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable | QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges)

        self.setPolygon(QPolygonF([QPointF(x, y + height // 2), QPointF(x+ width // 2, y), QPointF(x, y - height // 2), QPointF(x - width // 2, y)]))

    def to_dict(self):
        return {
            'name': self.name,
            'x': self.new_x,
            'y': self.new_y,
            'width': self.rect().width(),
            'height': self.rect().height(),
            'linked_entity_1': self.linked_entity_1.name,
            'linked_entity_2': self.linked_entity_2.name,
            'dataset': self.dataset
        }

    def rect(self):
        return QRectF(self.org_x - self.width // 2, self.org_y - self.height // 2, self.width, self.height)

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.name)

    def itemChange(self, change, value):
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
            self.dataset = updated_settings[4] if updated_settings[4] != "None" else False

            print("Saved settings:", updated_settings)

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
        if event.button() == Qt.MouseButton.RightButton:
            settings.run_relation(self)
        else:
            super().mousePressEvent(event)


class entity(QGraphicsRectItem):
    def __init__(self, text, parent, x = 100, y = 100, width = 120, height = 60, dataset = False):
        super().__init__()
        self.size_mult = 1

        self.name = text
        self.dataset = dataset
        self.org_x = x
        self.org_y = y
        self.new_x = x
        self.new_y = y

        self.canvas = parent

        self.setBrush(QBrush(QColor(50,50,50, 255)))
        self.setPen(QPen(Qt.GlobalColor.white, 2))

        self.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable | QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges)

        self.setRect(x - width // 2, y - height // 2, width, height)

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
            'dataset': self.dataset
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
            self.dataset = updated_settings[2] if updated_settings[2] != "None" else False

            print(self.dataset)

            self.setRect(self.org_x, self.org_y, 120 * self.size_mult, 60 * self.size_mult)
            self.update()
        
            self.canvas.redraw_lines()
            self.canvas.update_lines()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            settings.run_entity(self)
        else:
            super().mousePressEvent(event)


class attribute(QGraphicsEllipseItem):
    def __init__(self, text, parent, x = 100, y = 100, width = 120, height = 60, linked_item = False, attribute = False):
        super().__init__()
        self.size_mult = 1

        self.name = text
        self.attribute = attribute
        self.linked_item = linked_item
        self.canvas = parent

        self.org_x = x
        self.org_y = y

        self.new_x = x
        self.new_y = y

        self.setBrush(QBrush(QColor(50,50,50, 255)))
        self.setPen(QPen(Qt.GlobalColor.white, 2))

        self.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable | QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
        self.setRect(x, y, width, height)
    
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

            print(self.attribute)

            self.setRect(self.org_x, self.org_y, 120 * self.size_mult, 60 * self.size_mult)
            self.update()
        
            #self.setPos(self.new_x - self.rect().width() // 2, self.new_y - self.rect().height() // 2)

            self.canvas.redraw_lines()
            self.canvas.update_lines()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            settings.run_attribute(self)
        else:
            super().mousePressEvent(event)