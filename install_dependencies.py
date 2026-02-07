import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    print("Установка зависимостей...")
    
    dependencies = [
        "PyQt6",
        "Pillow"
    ]
    
    for dep in dependencies:
        print(f"Установка {dep}...")
        try:
            install(dep)
            print(f"✓ {dep} установлен")
        except Exception as e:
            print(f"✗ Ошибка установки {dep}: {e}")
    
    print("\nВсе зависимости установлены!")
    print("Запустите main.py для запуска программы.")