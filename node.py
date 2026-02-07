from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Node(QGraphicsItem):
    def __init__(self, title="Node", content="Content", parent=None):
        super().__init__(parent)
        self.title = title
        self.content = content
        
        # Включаем флаги для перемещения и выделения
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
        # Размеры
        self.width = 200
        self.height = 150
        self.corner_radius = 10
        self.title_height = 30
        
        # Градиенты
        self.gradient = QLinearGradient(0, 0, 0, self.height)
        self.gradient.setColorAt(0, QColor(45, 45, 65))
        self.gradient.setColorAt(1, QColor(30, 30, 45))
        
        self.title_gradient = QLinearGradient(0, 0, 0, self.title_height)
        self.title_gradient.setColorAt(0, QColor(70, 70, 100))
        self.title_gradient.setColorAt(1, QColor(60, 60, 90))
        
        # Порт для соединений (центр нижней грани)
        self.port = QPointF(self.width / 2, self.height)
        
        # Список коннекторов
        self.connectors = []
        
        # Для hover эффекта
        self.hover = False
        
        # Разрешаем события наведения
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton | Qt.MouseButton.RightButton)
    
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)
    
    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Рисуем тень
        painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(2, 2, self.width, self.height, 
                               self.corner_radius, self.corner_radius)
        
        # Основной прямоугольник
        painter.setBrush(self.gradient)
        painter.setPen(QPen(QColor(80, 80, 120), 2))
        painter.drawRoundedRect(0, 0, self.width, self.height, 
                               self.corner_radius, self.corner_radius)
        
        # Заголовок
        header_rect = QRectF(0, 0, self.width, self.title_height)
        painter.setBrush(self.title_gradient)
        painter.setPen(QPen(QColor(100, 100, 140), 1))
        painter.drawRoundedRect(header_rect, self.corner_radius, self.corner_radius)
        
        # Текст заголовка
        painter.setPen(QColor(220, 220, 255))
        font = QFont("Arial", 11, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(header_rect.adjusted(10, 0, -10, 0), 
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, 
                        self.title)
        
        # Основной текст
        painter.setPen(QColor(180, 180, 220))
        font = QFont("Arial", 10)
        painter.setFont(font)
        text_rect = QRectF(10, self.title_height + 5, 
                          self.width - 20, self.height - self.title_height - 10)
        painter.drawText(text_rect, Qt.TextFlag.TextWordWrap, self.content)
        
        # Точка подключения (показываем при выделении или наведении)
        if self.isSelected() or self.hover:
            painter.setBrush(QColor(100, 150, 255))
            painter.setPen(QPen(QColor(200, 220, 255), 2))
            painter.drawEllipse(self.port, 6, 6)
    
    def hoverEnterEvent(self, event):
        self.hover = True
        self.update()
        super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        self.hover = False
        self.update()
        super().hoverLeaveEvent(event)
    
    def addConnector(self, connector):
        """Добавить коннектор к ноде"""
        self.connectors.append(connector)
    
    def removeConnector(self, connector):
        """Удалить коннектор из ноды"""
        if connector in self.connectors:
            self.connectors.remove(connector)
    
    def updateConnectors(self):
        """Обновить все коннекторы, прикрепленные к этой ноде"""
        for connector in self.connectors:
            connector.updatePosition()
    
    def itemChange(self, change, value):
        """Обработка изменений позиции ноды"""
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            self.updateConnectors()
        return super().itemChange(change, value)