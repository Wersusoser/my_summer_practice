from setuptools import setup, find_packages
from pathlib import Path


def parse_requirements():
    """Универсальное чтение requirements.txt с обработкой кодировок"""
    req_path = Path(__file__).parent / "requirements.txt"

    # Попробуем основные кодировки
    encodings = ['utf-8-sig', 'utf-16', 'cp1251']

    for enc in encodings:
        try:
            with open(req_path, encoding=enc) as f:
                return [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith("#")
                ]
        except UnicodeError:
            continue

    # Если ни одна кодировка не подошла - читаем как бинарный файл
    with open(req_path, 'rb') as f:
        content = f.read().decode('utf-8', errors='ignore')
        return [
            line.strip()
            for line in content.splitlines()
            if line.strip() and not line.startswith("#")
        ]


setup(
    name="photo_editor",
    version="1.0.0",
    packages=find_packages(),
    install_requires=parse_requirements(),

    # Базовые параметры (без long_description_content_type для Python 3.6)
    author="Кирилл Гумбатов",
    author_email="gum20006@yandex.ru",

    entry_points={
        'console_scripts': [
            'photo-editor=photo_editor:main',
        ],
    }
)