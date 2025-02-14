from tkinter import *  # Импортируем все из библиотеки tkinter для создания графического интерфейса
from tkinter.colorchooser import askcolor  # Импортируем диалог выбора цвета

class Paint(object):
    pen_size = 5.0  # Размер пера по умолчанию
    color = 'black'  # Цвет по умолчанию

    def __init__(self):
        self.root = Tk()  # Создаем основное окно приложения

        # Создаем кнопки для различных инструментов рисования
        self.pen_button = Button(self.root, text='Ручка', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='Кисть', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='Цвет', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='Ластик', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.clear_button = Button(self.root, text='Очистить', command=self.clear_canvas)
        self.clear_button.grid(row=0, column=4)

        # Создаем ползунок для выбора размера пера/кисти
        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL, label='Размер')
        self.choose_size_button.grid(row=0, column=5)

        # Создаем холст для рисования
        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=1, columnspan=6)

        self.setup()  # Настраиваем начальные параметры
        self.root.mainloop()  # Запускаем главный цикл приложения

    def setup(self):
        self.old_x = None  # Хранит предыдущее значение координаты x
        self.old_y = None  # Хранит предыдущее значение координаты y
        self.line_width = self.choose_size_button.get()  # Получаем текущий размер линии
        self.color = self.color  # Устанавливаем текущий цвет
        self.eraser_on = False  # Ластик выключен по умолчанию
        self.active_button = self.pen_button  # Устанавливаем активную кнопку (по умолчанию ручка)
        # Привязываем события к холсту
        self.c.bind('<B1-Motion>', self.print)  # Обработка движения мыши при нажатой левой кнопке
        self.c.bind('<ButtonRelease-1>', self.reset)  # Обработка отпускания левой кнопки мыши

    def use_pen(self):
        self.activate_button(self.pen_button)  # Активируем режим ручки

    def use_brush(self):
        self.activate_button(self.brush_button)  # Активируем режим кисти

    def choose_color(self):
        self.eraser_on = False  # Выключаем режим ластика
        self.color = askcolor(color=self.color)[1]  # Открываем диалог выбора цвета

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)  # Активируем режим ластика

    def clear_canvas(self):
        self.c.delete("all")  # Удаляет все элементы на холсте

    def activate_button(self, some_button, eraser_mode=False):
        # Настраивает активные кнопки
        self.active_button.config(relief=RAISED)  # Убираем эффект нажатия с предыдущей кнопки
        some_button.config(relief=SUNKEN)  # Применяем эффект нажатия к текущей кнопке
        self.active_button = some_button  # Устанавливаем текущую активную кнопку
        self.eraser_on = eraser_mode  # Устанавливаем режим ластика

    def print(self, event):
        # Обрабатывает рисование на холсте
        self.line_width = self.choose_size_button.get()  # Получаем текущий размер линии
        paint_color = 'white' if self.eraser_on else self.color  # Устанавливаем цвет в зависимости от режима (ластик или не ластик)
        if self.old_x and self.old_y:  # Проверяем, если предыдущие координаты существуют
            # Рисуем линию на холсте
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=True, splinesteps=36)
        # Обновляем старые координаты
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        # Сбрасывает старые координаты после отпускания кнопки мыши
        self.old_x, self.old_y = None, None

# Запуск приложения
if __name__ == '__main__':
    Paint()
