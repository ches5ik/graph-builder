from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Connector(QGraphicsItem):
    def __init__(self, start_node, end_node):
        super().__init__()
        self.start_node = start_node
        self.end_node = end_node
        
        # Добавляем коннектор к нодам
        start_node.addConnector(self)
        end_node.addConnector(self)
        
        # Настройки линии
        self.line_width = 3
        self.color_start = QColor(100, 150, 255, 200)
        self.color_end = QColor(150, 200, 255, 200)
        
        # Размер стрелки
        self.arrow_size = 10
        
        # Обновляем начальную позицию
        self.updatePosition()
        
        # Устанавливаем низкий z-index, чтобы быть под нодами
        self.setZValue(-1)
    
    def boundingRect(self):
        """Определяем область, которую занимает коннектор"""
        # Создаем ограничивающий прямоугольник вокруг всей линии
        rect = QRectF(self.start_point, self.end_point).normalized()
        # Добавляем отступ для стрелки и толщины линии
        return rect.adjusted(-self.arrow_size - 5, -self.arrow_size - 5, 
                            self.arrow_size + 5, self.arrow_size + 5)
    
    def updatePosition(self):
        """Обновить позиции концов линии"""
        # Получаем позиции портов в координатах сцены
        self.start_point = self.start_node.mapToScene(self.start_node.port)
        self.end_point = self.end_node.mapToScene(self.end_node.port)
        
        # Обновляем отображение
        self.prepareGeometryChange()
        self.update()
    
    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Создаем градиент
        gradient = QLinearGradient(self.start_point, self.end_point)
        gradient.setColorAt(0, self.color_start)
        gradient.setColorAt(1, self.color_end)
        
        # Создаем плавную кривую
        path = QPainterPath()
        path.moveTo(self.start_point)
        
        # Вычисляем контрольные точки для кривой Безье
        mid_x = (self.start_point.x() + self.end_point.x()) / 2
        ctrl1 = QPointF(mid_x, self.start_point.y())
        ctrl2 = QPointF(mid_x, self.end_point.y())
        
        # Рисуем кривую Безье
        path.cubicTo(ctrl1, ctrl2, self.end_point)
        
        # Рисуем линию
        pen = QPen(gradient, self.line_width)
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # Рисуем стрелку на конце
        self.drawArrow(painter, path)
    
    def drawArrow(self, painter, path):
        """Нарисовать стрелку на конце линии"""
        # Получаем точку в конце пути (95% от длины)
        t = 0.95
        point = path.pointAtPercent(t)
        angle = path.angleAtPercent(t)
        
        painter.save()
        painter.translate(point)
        painter.rotate(-angle)  # Поворачиваем по касательной
        
        # Рисуем треугольник-стрелку
        arrow = QPolygonF()
        arrow.append(QPointF(0, 0))
        arrow.append(QPointF(-self.arrow_size, self.arrow_size / 2))
        arrow.append(QPointF(-self.arrow_size, -self.arrow_size / 2))
        
        painter.setBrush(self.color_end)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(arrow)
        
        painter.restore()
    
    def setColors(self, color1, color2):
        """Установить цвета градиента"""
        self.color_start = color1
        self.color_end = color2
        self.update()