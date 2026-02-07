import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from node import Node
from connector import Connector

class GraphEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setupScene()
        self.setupConnections()
        
    def setupUI(self):
        """Настройка интерфейса"""
        self.setWindowTitle("Graph Builder - Редактор схем")
        self.setGeometry(100, 100, 1400, 900)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QHBoxLayout(central_widget)
        
        # Графическая сцена
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor(30, 30, 40))
        
        # Вид для отображения сцены
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        
        # Панель инструментов
        self.tool_panel = self.createToolPanel()
        
        # Добавляем вид и панель в layout
        main_layout.addWidget(self.view, 4)  # 80% ширины
        main_layout.addLayout(self.tool_panel, 1)  # 20% ширины
        
        # Статус бар
        self.statusBar().showMessage("Готово. Двойной клик по ноде для редактирования")
        
        # Переменные для создания связей
        self.connecting = False
        self.start_node = None
        
        # Для редактирования
        self.editing_node = None
        self.text_edit_dialog = None
        
    def createToolPanel(self):
        """Создание панели инструментов"""
        panel = QVBoxLayout()
        
        # Группа: Создание
        create_group = QGroupBox("Создание")
        create_layout = QVBoxLayout()
        
        self.btn_add_node = QPushButton("➕ Добавить ноду")
        self.btn_add_node.setMinimumHeight(40)
        create_layout.addWidget(self.btn_add_node)
        
        self.btn_connect = QPushButton("🔗 Создать связь")
        self.btn_connect.setMinimumHeight(40)
        create_layout.addWidget(self.btn_connect)
        
        create_group.setLayout(create_layout)
        panel.addWidget(create_group)
        
        # Группа: Редактирование
        edit_group = QGroupBox("Редактирование")
        edit_layout = QVBoxLayout()
        
        self.btn_edit_text = QPushButton("📝 Редактировать текст")
        self.btn_edit_text.setMinimumHeight(40)
        edit_layout.addWidget(self.btn_edit_text)
        
        edit_group.setLayout(edit_layout)
        panel.addWidget(edit_group)
        
        # Группа: Внешний вид
        style_group = QGroupBox("Внешний вид")
        style_layout = QVBoxLayout()
        
        self.btn_node_color = QPushButton("🎨 Цвет ноды")
        style_layout.addWidget(self.btn_node_color)
        
        self.btn_line_color = QPushButton("🌈 Цвет связи")
        style_layout.addWidget(self.btn_line_color)
        
        style_group.setLayout(style_layout)
        panel.addWidget(style_group)
        
        # Группа: Управление
        control_group = QGroupBox("Управление")
        control_layout = QVBoxLayout()
        
        self.btn_delete = QPushButton("🗑️ Удалить")
        control_layout.addWidget(self.btn_delete)
        
        self.btn_clear = QPushButton("🧹 Очистить всё")
        control_layout.addWidget(self.btn_clear)
        
        control_group.setLayout(control_layout)
        panel.addWidget(control_group)
        
        # Группа: Информация
        info_group = QGroupBox("Справка")
        info_layout = QVBoxLayout()
        
        info_text = QLabel("""
        <b>Управление:</b><br>
        • Двойной клик по ноде: редактировать<br>
        • Перетаскивание: ЛКМ<br>
        • Выделение: ЛКМ + Shift<br>
        • Удаление: Delete<br>
        • Отмена связи: Esc
        """)
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        info_group.setLayout(info_layout)
        panel.addWidget(info_group)
        
        # Растягиваемый элемент
        panel.addStretch()
        
        return panel
    
    def setupScene(self):
        """Настройка сцены и создание примеров"""
        # Устанавливаем размер сцены
        self.scene.setSceneRect(-500, -500, 1000, 1000)
        
        # Создаем примеры нод
        self.createSampleNodes()
    
    def createSampleNodes(self):
        """Создание примеров нод"""
        # Нода 1
        node1 = Node("Начало", "Стартовая точка процесса")
        node1.setPos(-200, -100)
        self.scene.addItem(node1)
        
        # Нода 2
        node2 = Node("Процесс", "Основная обработка данных\nВыполнение операций")
        node2.setPos(0, -100)
        self.scene.addItem(node2)
        
        # Нода 3
        node3 = Node("Конец", "Завершение процесса\nРезультат работы")
        node3.setPos(200, -100)
        self.scene.addItem(node3)
        
        # Нода 4
        node4 = Node("Дополнительно", "Побочный процесс\nАльтернативное решение")
        node4.setPos(0, 100)
        self.scene.addItem(node4)
        
        # Создаем связи
        conn1 = Connector(node1, node2)
        self.scene.addItem(conn1)
        
        conn2 = Connector(node2, node3)
        self.scene.addItem(conn2)
        
        conn3 = Connector(node2, node4)
        self.scene.addItem(conn3)
    
    def setupConnections(self):
        """Настройка сигналов и слотов"""
        # Кнопки
        self.btn_add_node.clicked.connect(self.addNewNode)
        self.btn_connect.clicked.connect(self.startConnectionMode)
        self.btn_edit_text.clicked.connect(self.editSelectedNode)
        self.btn_delete.clicked.connect(self.deleteSelected)
        self.btn_clear.clicked.connect(self.clearScene)
        self.btn_node_color.clicked.connect(self.changeNodeColor)
        self.btn_line_color.clicked.connect(self.changeLineColor)
        
        # Обработка кликов по сцене
        self.view.mousePressEvent = self.handleViewClick
        self.view.mouseDoubleClickEvent = self.handleDoubleClick
    
    def addNewNode(self):
        """Добавить новую ноду"""
        # Создаем простую ноду
        node = Node(f"Нода {len(self.scene.items()) + 1}", 
                   "Новая нода\nОтредактируйте текст")
        
        # Помещаем в центр видимой области
        center = self.view.mapToScene(self.view.viewport().rect().center())
        node.setPos(center)
        
        self.scene.addItem(node)
        self.statusBar().showMessage("Новая нода добавлена. Двойной клик для редактирования")
    
    def startConnectionMode(self):
        """Войти в режим создания связей"""
        self.connecting = True
        self.start_node = None
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.statusBar().showMessage("Режим создания связи: выберите первую ноду")
    
    def handleViewClick(self, event):
        """Обработка кликов по виду"""
        if event.button() == Qt.MouseButton.RightButton:
            # Для правой кнопки - передаем событие дальше
            QGraphicsView.mousePressEvent(self.view, event)
            return
            
        if self.connecting and event.button() == Qt.MouseButton.LeftButton:
            # Преобразуем координаты клика
            scene_pos = self.view.mapToScene(event.pos())
            
            # Ищем ноду под курсором
            items = self.scene.items(scene_pos)
            node = None
            for item in items:
                if isinstance(item, Node):
                    node = item
                    break
            
            if node:
                if self.start_node is None:
                    # Выбираем первую ноду
                    self.start_node = node
                    self.statusBar().showMessage("Теперь выберите вторую ноду")
                else:
                    # Создаем связь между нодами
                    if self.start_node != node:  # Нельзя соединить ноду с самой собой
                        connector = Connector(self.start_node, node)
                        self.scene.addItem(connector)
                        self.statusBar().showMessage("Связь создана")
                    
                    # Выходим из режима создания связей
                    self.connecting = False
                    self.start_node = None
                    self.setCursor(Qt.CursorShape.ArrowCursor)
            else:
                # Кликнули не по ноде - выходим из режима
                self.connecting = False
                self.start_node = None
                self.setCursor(Qt.CursorShape.ArrowCursor)
                self.statusBar().showMessage("Режим создания связи отменен")
            
            return  # Перехватываем событие
        
        # Если не в режиме создания связей, передаем событие дальше
        QGraphicsView.mousePressEvent(self.view, event)
    
    def handleDoubleClick(self, event):
        """Обработка двойного клика для редактирования"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Преобразуем координаты клика
            scene_pos = self.view.mapToScene(event.pos())
            
            # Ищем ноду под курсором
            items = self.scene.items(scene_pos)
            for item in items:
                if isinstance(item, Node):
                    self.editNode(item)
                    return
        
        # Если не попали по ноде, передаем событие дальше
        QGraphicsView.mouseDoubleClickEvent(self.view, event)
    
    def editSelectedNode(self):
        """Редактировать выбранную ноду"""
        items = self.scene.selectedItems()
        if items:
            for item in items:
                if isinstance(item, Node):
                    self.editNode(item)
                    break
        else:
            self.statusBar().showMessage("Выберите ноду для редактирования")
    
    def editNode(self, node):
        """Редактировать текст ноды через диалог"""
        self.editing_node = node
        
        # Создаем диалоговое окно
        dialog = QDialog(self)
        dialog.setWindowTitle("Редактирование ноды")
        dialog.setMinimumWidth(500)
        dialog.setMinimumHeight(300)
        
        layout = QVBoxLayout()
        
        # Заголовок
        title_label = QLabel("Заголовок:")
        title_edit = QLineEdit(node.title)
        title_edit.setPlaceholderText("Введите заголовок")
        layout.addWidget(title_label)
        layout.addWidget(title_edit)
        
        # Содержание
        content_label = QLabel("Содержание:")
        content_edit = QTextEdit(node.content)
        content_edit.setPlaceholderText("Введите содержание")
        content_edit.setAcceptRichText(False)
        layout.addWidget(content_label)
        layout.addWidget(content_edit)
        
        # Кнопки
        button_box = QDialogButtonBox()
        ok_button = button_box.addButton("Сохранить", QDialogButtonBox.ButtonRole.AcceptRole)
        cancel_button = button_box.addButton("Отмена", QDialogButtonBox.ButtonRole.RejectRole)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        # Обработчики
        def save_changes():
            node.title = title_edit.text()
            node.content = content_edit.toPlainText()
            node.update()  # Обновляем отображение
            dialog.accept()
            self.statusBar().showMessage("Текст ноды обновлен")
        
        def reset_changes():
            title_edit.setText(node.title)
            content_edit.setPlainText(node.content)
        
        ok_button.clicked.connect(save_changes)
        cancel_button.clicked.connect(dialog.reject)
        
        # Кнопка сброса
        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(reset_changes)
        button_box.addButton(reset_button, QDialogButtonBox.ButtonRole.ActionRole)
        
        # Показываем диалог
        dialog.exec()
        self.editing_node = None
    
    def deleteSelected(self):
        """Удалить выбранные элементы"""
        items = self.scene.selectedItems()
        if items:
            for item in items:
                self.scene.removeItem(item)
            self.statusBar().showMessage(f"Удалено {len(items)} элементов")
    
    def clearScene(self):
        """Очистить всю сцену"""
        reply = QMessageBox.question(self, "Очистка",
                                   "Вы уверены, что хотите удалить все элементы?",
                                   QMessageBox.StandardButton.Yes | 
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.scene.clear()
            self.statusBar().showMessage("Сцена очищена")
    
    def changeNodeColor(self):
        """Изменить цвет выбранной ноды"""
        items = self.scene.selectedItems()
        if items:
            for item in items:
                if isinstance(item, Node):
                    # Диалог выбора цвета
                    color = QColorDialog.getColor(initial=QColor(45, 45, 65), 
                                                  parent=self, 
                                                  title="Выберите цвет ноды")
                    if color.isValid():
                        # Создаем темнее версию для градиента
                        darker = color.darker(120)
                        
                        # Обновляем градиент ноды
                        item.gradient = QLinearGradient(0, 0, 0, item.height)
                        item.gradient.setColorAt(0, color)
                        item.gradient.setColorAt(1, darker)
                        
                        # Обновляем цвет заголовка
                        title_darker = color.darker(140)
                        item.title_gradient = QLinearGradient(0, 0, 0, item.title_height)
                        item.title_gradient.setColorAt(0, color.lighter(120))
                        item.title_gradient.setColorAt(1, title_darker)
                        
                        item.update()
                        self.statusBar().showMessage("Цвет ноды изменен")
        else:
            self.statusBar().showMessage("Выберите ноду для изменения цвета")
    
    def changeLineColor(self):
        """Изменить цвет выбранной связи"""
        items = self.scene.selectedItems()
        if items:
            for item in items:
                if isinstance(item, Connector):
                    # Диалог выбора первого цвета
                    color1 = QColorDialog.getColor(initial=QColor(100, 150, 255),
                                                  parent=self,
                                                  title="Выберите начальный цвет связи")
                    if color1.isValid():
                        # Диалог выбора второго цвета
                        color2 = QColorDialog.getColor(initial=QColor(150, 200, 255),
                                                      parent=self,
                                                      title="Выберите конечный цвет связи")
                        if color2.isValid():
                            color1.setAlpha(200)
                            color2.setAlpha(200)
                            item.setColors(color1, color2)
                            self.statusBar().showMessage("Цвет связи изменен")
        else:
            self.statusBar().showMessage("Выберите связь для изменения цвета")
    
    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        if event.key() == Qt.Key.Key_Escape:
            if self.connecting:
                self.connecting = False
                self.start_node = None
                self.setCursor(Qt.CursorShape.ArrowCursor)
                self.statusBar().showMessage("Создание связи отменено")
            elif self.text_edit_dialog and self.text_edit_dialog.isVisible():
                self.text_edit_dialog.reject()
        
        elif event.key() == Qt.Key.Key_Delete:
            self.deleteSelected()
        
        elif event.key() == Qt.Key.Key_F2:
            self.editSelectedNode()
        
        super().keyPressEvent(event)

def applyDarkTheme(app):
    """Применение темной темы"""
    app.setStyle("Fusion")
    
    # Темная палитра
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(35, 35, 45))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 35))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 55))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(60, 60, 80))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(100, 150, 255))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(100, 150, 255))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    
    app.setPalette(dark_palette)
    
    # Стилизация
    app.setStyleSheet("""
        QMainWindow {
            background-color: #23232d;
        }
        QGroupBox {
            font-weight: bold;
            color: #ccccff;
            border: 2px solid #555;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 12px;
            background-color: #2d2d3d;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px 0 8px;
            color: #8888ff;
        }
        QPushButton {
            background-color: #4a4a6a;
            color: #ffffff;
            border: 2px solid #555;
            border-radius: 6px;
            padding: 10px;
            margin: 4px;
            font-size: 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #5a5a8a;
            border: 2px solid #666;
        }
        QPushButton:pressed {
            background-color: #3a3a5a;
        }
        QLabel {
            color: #ddddff;
            font-size: 11px;
        }
        QGraphicsView {
            border: 2px solid #444;
            border-radius: 5px;
            background-color: #1a1a2a;
        }
        QDialog {
            background-color: #2d2d3d;
        }
        QLineEdit, QTextEdit {
            background-color: #3a3a4a;
            color: #ffffff;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 5px;
        }
        QLineEdit:focus, QTextEdit:focus {
            border: 1px solid #6688ff;
        }
    """)

def main():
    app = QApplication(sys.argv)
    
    # Применяем темную тему
    applyDarkTheme(app)
    
    # Создаем и показываем главное окно
    window = GraphEditor()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()