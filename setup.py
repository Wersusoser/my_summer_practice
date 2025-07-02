from setuptools import setup, find_packages
from pathlib import Path

# Чтение описания из README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")


# Чтение зависимостей
def get_requirements():
    requirements_path = this_directory / "requirements.txt"
    with open(requirements_path, encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]


setup(
    name="photo_editor",
    version="1.0.0",
    author="Гумбатов Кирилл",
    author_email="gum20006@yandex.ru",
    description="Фоторедатор изображений",
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Указание пакетов
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),

    # Указание скриптов
    py_modules=["photo_editor"],

    # Зависимости
    install_requires=get_requirements(),

    # Точки входа
    entry_points={
        "console_scripts": [
            "photo-editor=photo_editor:main",
        ],
    },

    # Метаданные
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics :: Editors",
    ],

    # Включение дополнительных файлов
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md"],
    },
)