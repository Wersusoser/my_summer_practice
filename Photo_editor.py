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