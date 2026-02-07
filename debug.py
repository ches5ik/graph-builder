import sys
print("Python version:", sys.version)

try:
    from PyQt6.QtWidgets import QApplication
    print("PyQt6 импортируется успешно!")
    
    # Проверяем все модули
    from node import Node
    print("Модуль node загружен")
    
    from connector import Connector
    print("Модуль connector загружен")
    
    print("\n✅ Все модули загружены успешно!")
    print("Запускайте main.py")
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()