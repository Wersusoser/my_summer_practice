# Редактор избражений

![Python](https://img.shields.io/badge/python-3.6%2B-red)
![OpenCV](https://img.shields.io/badge/opencv-4.6.0.66-blue)

Графическое приложение для обработки изображений с поддержкой:
- Загрузки изображений
- Съемки с камеры
- Базовых операций редактирования


## 🛠 Полная инструкция по сборке и распространению

## Первый способ сборки
### 1. Подготовка окружения
```bash
# Убедитесь что установлены wheel и setuptools
pip install wheel setuptools
```

### 2. Сборка дистрибутивов
``` bash
python setup.py sdist bdist_wheel
```

## Второй способ сборки

### 1. Подготовка окружения
Перед сборкой убедитесь, что у вас установлены необходимые инструменты:

```bash
# Установка build tools (если ещё не установлены)
python -m pip install --upgrade pip wheel setuptools build
```

### 2. Сборка дистрибутивов
Выполните в корне проекта следующую команду:

```bash
python -m build
```

---
После успешной сборки в папке `dist/` появятся два файла:
- `image_redactor-1.0.0.tar.gz` - архив с исходным кодом
- `image_redactor-1.0.0-py3-none-any.whl` - бинарный wheel-пакет

### 3. Проверка содержимого пакета
Убедитесь, что все необходимые файлы включены:

```bash
# Для проверки .tar.gz:
tar -tf dist/image_redactor-1.0.0.tar.gz

# Для проверки .whl:
unzip -l dist/image_redactor-1.0.0-py3-none-any.whl
```

Должны отобразиться все ключевые файлы:
- `photo_editor.py`
- `setup.py`
- `requirements.txt`
- `MANIFEST.in`
- `README.md`

### 4. Установка из собранного пакета
Для тестирования установки:

```bash
pip install dist/image_redactor-1.0.0-py3-none-any.whl
```

Или альтернативный вариант:
```bash
pip install dist/image_redactor-1.0.0.tar.gz
```


## 📦 Установка

1. **Клонирование репозитория**:
   ```bash
   git clone https://github.com/ваш-репозиторий.git
   cd image-redactor
   ```

2. **Создание виртуального окружения**:
   ```bash
   python -m venv venv
   # Активация:
   # Windows: venv\Scripts\activate
   # Linux/Mac: source venv/bin/activate
   ```

3. **Установка зависимостей**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Установка пакета** (опционально для разработки):
   ```bash
   pip install -e .
   ```

## 🚀 Запуск приложения
```bash
photo_editor
```

## 🛠 Основные функции
- **Файл**:
  - Загрузка изображений (JPG, PNG)
- **Камера**:
  - Захват фото с веб-камеры
- **Редактирование**:
  - Перевод изображения в оттенки серого
  - Рисование прямоугольников
  - Выделение цветовых каналов (R/G/B)
  - Изменение размеров изображения
## 📂 Структура проекта
```
├── photo_editor.py          # Главный скрипт
├── requirements.txt         # Зависимости
├── setup.py                 # Конфигурация пакета
├── MANIFEST.in              # Список включаемых файлов
└── README.md                # Эта инструкция
```

## ⚠️ Системные требования
- Python 3.6 или новее
- OpenCV 4.6.0.66
- Pytorch 2.7.1
