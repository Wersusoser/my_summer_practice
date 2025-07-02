from tkinter import *
from tkinter import ttk, filedialog, Toplevel, Canvas, Scrollbar, Frame, NW
from tkinter.messagebox import showerror, showwarning, showinfo
import cv2
import numpy as np
from PIL import Image, ImageTk
from typing import Optional

img: Optional[np.ndarray] = None  # Текущее редактируемое изображение
original_photo: Optional[np.ndarray] = None  # Оригинальное изображение без изменений


def img_check(func):
    """Декоратор для проверки загружено ли изображение перед выполнением функции."""

    def wrapper(*args, **kwargs):
        global img
        if img is None:
            showwarning(
                title='Предупреждение',
                message='Фотография еще не выбрана')
            return None
        return func(*args, **kwargs)

    return wrapper


def change_path():
    """Загружает изображение из файла через диалоговое окно."""
    global img, original_photo
    filetypes = [('Изображения', ('*.png', '*.jpg'))]
    new_path = filedialog.askopenfilename(
        title='Выберите фотографию формата jpg или png:',
        filetypes=filetypes)
    if new_path:
        img = cv2.imread(new_path)
        original_photo = img.copy()
        showinfo(title='Успех', message='Фотография успешно выбрана')


def webcam_photo():
    """Открывает окно для захвата фото с веб-камеры."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        showerror("Ошибка",
                  "Не удалось подключиться к веб-камере. "
                  "Проверьте, что камера включена.")
        return

    webcam_window = Toplevel()
    webcam_window.title("Веб-камера")
    window_width = 650
    window_height = 550
    screen_width = webcam_window.winfo_screenwidth()
    screen_height = webcam_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    webcam_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    video_label = Label(webcam_window)
    video_label.pack()

    def update_frame():
        """Обновляет кадры с веб-камеры в окне."""
        ret, frame = cap.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img_pil)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
        else:
            showerror("Ошибка", "Проблема с получением изображения с камеры")
            cap.release()
            webcam_window.destroy()
            return
        video_label.after(10, update_frame)

    def take_photo():
        """Фиксирует текущий кадр с камеры и сохраняет его."""
        ret, frame = cap.read()
        if ret:
            global img, original_photo
            img = frame.copy()
            original_photo = frame.copy()
            cap.release()
            webcam_window.destroy()
            showinfo(title='Успех', message='Фотография успешно сделана')

    capture_btn = ttk.Button(webcam_window,
                             text="Сделать фото",
                             command=take_photo)
    capture_btn.pack(pady=10, ipadx=20, ipady=5)
    update_frame()


def photo_opening(name, image):
    """Открывает изображение с возможностью прокрутки в окне Tkinter."""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(image)
    photo_window = Toplevel()
    window_width = 500
    window_height = 500
    screen_width = photo_window.winfo_screenwidth()
    screen_height = photo_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    photo_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    photo_window.title(name)

    frame = Frame(photo_window)
    frame.pack(fill="both", expand=True)
    v_scroll = Scrollbar(frame)
    v_scroll.pack(side="right", fill="y")
    h_scroll = Scrollbar(frame, orient='horizontal')
    h_scroll.pack(side="bottom", fill="x")
    canvas = Canvas(frame,
                    yscrollcommand=v_scroll.set,
                    xscrollcommand=h_scroll.set)
    canvas.pack(side="left", fill="both", expand=True)
    v_scroll.config(command=canvas.yview)
    h_scroll.config(command=canvas.xview)
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas.create_image(0, 0, anchor=NW, image=img_tk)
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.image = img_tk


@img_check
def open_main_photo():
    """Отображает текущее изображение в отдельном окне."""
    global img
    photo_opening('Photo', img)


@img_check
def reset_changes():
    """Сбрасывает все изменения, восстанавливая оригинальное изображение."""
    global img, original_photo
    if np.array_equal(img, original_photo):
        showwarning(
            title='Предупреждение',
            message='Вы еще не изменяли фотографию')
        return
    img = original_photo.copy()
    showinfo(title='Успех', message='Изменения фотографии были сброшены')


@img_check
def convert_to_grayscale():
    """Преобразует изображение в оттенки серого."""
    global img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # Для сохранения 3 каналов
    showinfo(title='Успех', message='Изображение преобразовано в оттенки серого')


@img_check
def draw_rectangle():
    """Рисует прямоугольник на изображении по заданным координатам."""
    global img
    rect_window = Toplevel()
    rect_window.title('Рисование прямоугольника')
    rect_window.geometry("300x400")

    # Координаты
    ttk.Label(rect_window, text="Координата x1:").pack()
    x1_entry = ttk.Entry(rect_window)
    x1_entry.pack()

    ttk.Label(rect_window, text="Координата y1:").pack()
    y1_entry = ttk.Entry(rect_window)
    y1_entry.pack()

    ttk.Label(rect_window, text="Координата x2:").pack()
    x2_entry = ttk.Entry(rect_window)
    x2_entry.pack()

    ttk.Label(rect_window, text="Координата y2:").pack()
    y2_entry = ttk.Entry(rect_window)
    y2_entry.pack()

    # Цвет
    ttk.Label(rect_window, text="Цвет (B G R, 0-255):").pack()
    color_entries = []
    for i, color in enumerate(["Синий (B):", "Зеленый (G):", "Красный (R):"]):
        ttk.Label(rect_window, text=color).pack()
        entry = ttk.Entry(rect_window)
        entry.pack()
        color_entries.append(entry)

    # Толщина
    ttk.Label(rect_window, text="Толщина линии:").pack()
    thickness_entry = ttk.Entry(rect_window)
    thickness_entry.pack()

    def apply_rectangle():
        """Рисует прямоугольник с проверкой введенных параметров."""
        try:
            height, width = img.shape[:2]
            x1 = int(x1_entry.get())
            y1 = int(y1_entry.get())
            x2 = int(x2_entry.get())
            y2 = int(y2_entry.get())

            # Проверка координат
            if (x1 < 0 or y1 < 0 or x2 > width or y2 > height or
                    x1 >= x2 or y1 >= y2):
                showwarning('Ошибка', 'Некорректные координаты прямоугольника')
                return

            # Получение цвета
            color = []
            for entry in color_entries:
                val = int(entry.get())
                if val < 0 or val > 255:
                    showwarning('Ошибка', 'Значения цвета должны быть от 0 до 255')
                    return
                color.append(val)
            color = tuple(color)

            # Толщина
            thickness = int(thickness_entry.get())
            if thickness < -1:
                showwarning('Ошибка', 'Толщина должна быть >= -1')
                return

            # Рисование прямоугольника
            cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
            rect_window.destroy()
            showinfo('Успех', 'Прямоугольник успешно нарисован')

        except ValueError:
            showwarning('Ошибка', 'Пожалуйста, введите целые числа')

    ttk.Button(rect_window, text="Применить", command=apply_rectangle).pack(pady=10)
    rect_window.grab_set()


@img_check
def resize_image():
    """Изменяет размер изображения по введенным параметрам."""
    global img
    resize_window = Toplevel()
    resize_window.title('Изменение размера изображения')
    resize_window.geometry("300x200")

    ttk.Label(resize_window, text="Ширина").pack()
    width_entry = ttk.Entry(resize_window)
    width_entry.pack()

    ttk.Label(resize_window, text="Высота").pack()
    height_entry = ttk.Entry(resize_window)
    height_entry.pack()

    def apply_resize():
        """Применяет изменение размера с проверкой введенных значений."""
        global img
        try:
            width = int(width_entry.get())
            height = int(height_entry.get())

            if width <= 0 or height <= 0:
                showwarning('Ошибка', 'Размеры должны быть положительными числами')
                return

            img = cv2.resize(img, (width, height))
            resize_window.destroy()
            showinfo('Успех', 'Размер изображения изменен')

        except ValueError:
            showwarning('Ошибка', 'Пожалуйста, введите целые числа')

    ttk.Button(resize_window, text="Применить", command=apply_resize).pack(pady=10)
    resize_window.grab_set()


def main():
    """Инициализирует главное окно приложения."""
    main_window = Tk()
    window_width = 500
    window_height = 600
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    main_window.title("Фоторедактор")

    style = ttk.Style()
    style.configure("TButton", padding=8, font=('Segoe UI', 9), relief="flat")

    Label(main_window,
          text="Фоторедактор",
          font=('Segoe UI', 16, 'bold'),
          bg="#f5f5f5",
          pady=15).pack()

    main_frame = Frame(main_window, bg="#f5f5f5", padx=20, pady=10)
    main_frame.pack(fill="both", expand=True)

    buttons = [
        ("Выбрать изображение", change_path),
        ("Сделать фото с камеры", webcam_photo),
        ("Показать изображение", open_main_photo),
        ("Сбросить изменения", reset_changes),
        ("В оттенки серого", convert_to_grayscale),
        ("Нарисовать прямоугольник", draw_rectangle),
        ("Изменить размер", resize_image)
    ]

    for text, command in buttons:
        btn = ttk.Button(main_frame,
                         text=text,
                         command=command,
                         style="TButton")
        btn.pack(fill="x", pady=5, ipady=5)

    main_window.mainloop()


if __name__ == "__main__":
    main()