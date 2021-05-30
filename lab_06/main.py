from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, Radiobutton, LEFT, RIGHT, IntVar, PhotoImage
from tkinter import messagebox
from math import sqrt, acos, degrees, pi, sin, cos, radians, floor, fabs
import copy
import numpy as np
import matplotlib.pyplot as plt

from time import time, sleep

import colorutils as cu


WIN_WIDTH = 1500
WIN_HEIGHT = 900
WIN_COLOR = "#bf80ff"

CV_WIDE = 900
CV_HEIGHT = 900
CV_COLOR = "#ffffff" #f3e6ff" #"#cce6ff"
MAIN_TEXT_COLOR = "#b566ff" #"lightblue" a94dff
TEXT_COLOR = "#ce99ff"

TEMP_SIDE_COLOR_CHECK = (255, 0, 255) # purple
TEMP_SIDE_COLOR = "#ff00ff"

BOX_COLOR = "#dab3ff"

COLOR_LINE = "#000002" #(0, 0, 0) # black
COLOR_LINE_CHECK = (0, 0, 2)

FILL_COLOR = "#ff6e41"


def check_option(option):
    messagebox.showinfo("Выбран", "Выбрана опция %d" %(option))


def clear_canvas():
    canvas_win.delete("all")


def draw_dot(x, y, color):
    # canvas_win.create_line(x, y, x + 1, y, fill = color)
    image_canvas.put(color, (x, y))
    
    # for dot in dots:
    #     canvas_win.create_line(dot[0], dot[1], dot[0] + 1, dot[1], fill = dot[2].hex)


def sign(difference):
    if (difference < 0):
        return -1
    elif (difference == 0):
        return 0
    else:
        return 1


def bresenham_int(p1, p2, color):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    if (x2 - x1 == 0) and (y2 - y1 == 0):
        return [[x1, y1, color]]

    x = x1
    y = y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    s1 = sign(x2 - x1)
    s2 = sign(y2 - y1)

    if (dy > dx):
        tmp = dx
        dx = dy
        dy = tmp
        swaped = 1
    else:
        swaped = 0

    e = 2 * dy - dx

    i = 1

    while (i <= dx + 1):

        draw_dot(x, y, color)

        # dot = [x, y, color]
        # dots.append(dot)

        while (e >= 0):
            if (swaped):
                x = x + s1
            else:
                y = y + s2

            e = e - 2 * dx

        if (swaped):
            y = y + s2
        else:
            x = x + s1

        e = e + 2 * dy

        i += 1


def read_dot():
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты точки")
        return

    add_dot(int(x), int(y))


def add_dot_click(event):
    x = event.x
    y = event.y

    add_dot(x, y)


def add_seed_dot_click(event):
    global seed_dot

    x = event.x
    y = event.y

    seed_dot = [x, y]

    x_seed_entry.delete(0, END)
    x_seed_entry.insert(END, "%d" %(x))
    y_seed_entry.delete(0, END)
    y_seed_entry.insert(END, "%d" %(y))



def add_dot(x, y, last = True):
    cur_figure = len(dots) - 1
    dots[cur_figure].append([x, y])

    cur_dot = len(dots[cur_figure]) - 1

    if (last):
        dotslist_box.insert(END, "%d. (%4d;%4d)" %(cur_dot + 1, x, y))

    if (len(dots[cur_figure]) > 1):
        bresenham_int(dots[cur_figure][cur_dot - 1], dots[cur_figure][cur_dot], COLOR_LINE)
        

def del_dot():
    cur_figure = len(dots) - 1
    cur_dot = len(dots[cur_figure]) - 1

    if (len(dots[cur_figure]) == 0):
        return

    if (len(dots[cur_figure]) > 1):
        bresenham_int(dots[cur_figure][cur_dot - 1], dots[cur_figure][cur_dot], "white")

    # Find index for a table

    index = 0

    for i in range(cur_figure + 1):
        index += len(dots[i])

    #index += cur_figure


    dotslist_box.delete(index - 1, END)

    dots[cur_figure].pop(len(dots[cur_figure]) - 1)


def make_figure():
    cur_figure = len(dots)
    cur_dot = len(dots[cur_figure - 1])

    if (cur_dot < 3):
        messagebox.showerror("Ошибка", "Недостаточно точек, чтобы замкнуть фигуру")

    add_dot(dots[cur_figure - 1][0][0], dots[cur_figure - 1][0][1], last = False)

    dots.append(list())

    dotslist_box.insert(END, "_______________________")


def get_fill_check_color(collor_fill):
    return (int(collor_fill[1:3], 16), int(collor_fill[3:5], 16), int(collor_fill[5:7], 16))


def add_seed_dot():
    global seed_dot

    try:
        x = float(x_seed_entry.get())
        y = float(y_seed_entry.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты точки")
        return

    seed_dot = [x, y]


def parse_fill():

    cur_figure = len(dots) - 1

    if (len(dots[cur_figure]) != 0):
        messagebox.showerror("Ошибка", "Крайняя фигура не замкнута")
        return

    if (len(seed_dot) == 0):
        messagebox.showerror("Ошибка", "Затравочный пиксель не установлен")
        return

    if (option_filling.get() == 1):
        delay = True
    else:
        delay = False

    color_fill = parse_color(option_color.get())

    fill_with_seed(seed_dot, color_fill, delay = delay)


def fill_with_seed(dot_seed, color_fill, delay = False):

    color_fill_check = get_fill_check_color(color_fill)

    start_time = time()

    stack = list()
    stack.append(dot_seed)

    while (stack):

        dot_seed = stack.pop()

        x = dot_seed[0]
        y = dot_seed[1]

        image_canvas.put(color_fill, (x, y))

        tmp_x = x
        tmp_y = y

        # Заполнение текущей строки право до ребра или уже закрашенного пикселя
        x = x + 1

        while (image_canvas.get(x, y) != COLOR_LINE_CHECK 
                and image_canvas.get(x, y) != color_fill_check):
            image_canvas.put(color_fill, (x, y))
            x = x + 1

        x_right = x - 1


        # Заполнение текущей строки влево до ребра или уже закрашенного пикселя
        x = tmp_x - 1

        while (image_canvas.get(x, y) != COLOR_LINE_CHECK 
                and image_canvas.get(x, y) != color_fill_check):
            image_canvas.put(color_fill, (x, y))
            x = x - 1

        x_left = x + 1

        # Сканирование верхней строки
        x = x_left

        y = tmp_y + 1

        while (x <= x_right):
            flag = False

            # Поиск, есть ли в строке незакрашенный пиксель
            while (image_canvas.get(x, y) != COLOR_LINE_CHECK 
                    and image_canvas.get(x, y) != color_fill_check 
                    and x <= x_right):
                flag = True

                x = x + 1

            if (flag == True):
                if (x == x_right 
                        and image_canvas.get(x, y) != COLOR_LINE_CHECK
                        and image_canvas.get(x, y) != color_fill_check):
                    stack.append([x, y])
                else:
                    stack.append([x - 1, y])
            
                flag = False

            x_begin = x

            while ((image_canvas.get(x, y) == COLOR_LINE_CHECK 
                    or image_canvas.get(x, y) == color_fill_check) 
                    and x < x_right):
                x = x + 1

            if (x == x_begin):
                x = x + 1

        # Сканирование нижней строки
        x = x_left

        y = tmp_y - 1

        while (x <= x_right):
            flag = False    

            # Поиск, есть ли в строке незакрашенный пиксель
            while (image_canvas.get(x, y) != COLOR_LINE_CHECK 
                    and image_canvas.get(x, y) != color_fill_check 
                    and x <= x_right):
                flag = True

                x = x + 1

            if (flag == True):
                if (x == x_right 
                        and image_canvas.get(x, y) != COLOR_LINE_CHECK 
                        and image_canvas.get(x, y) != color_fill_check):
                    stack.append([x, y])
                else:
                    stack.append([x - 1, y])

                flag = False

            x_begin = x

            while ((image_canvas.get(x, y) == COLOR_LINE_CHECK 
                    or image_canvas.get(x, y) == color_fill_check) 
                    and x < x_right):
                x = x + 1

            if (x == x_begin):
                x = x + 1

        if (delay):
            sleep(0.001)
            canvas_win.update()

    end_time = time()

    time_label = Label(text = "Время: %-3.2f с" %(end_time - start_time), font="-family {Consolas} -size 16", bg = "lightgrey")
    time_label.place(x = 20, y = CV_HEIGHT - 50)


def reboot_prog():
    global dots
    global image_canvas
    global seed_dot

    canvas_win.delete("all")

    image_canvas = PhotoImage(width = CV_WIDE, height = CV_HEIGHT)
    canvas_win.create_image((CV_WIDE / 2, CV_HEIGHT / 2), image = image_canvas, state = "normal")

    image_canvas.put("#ffffff", to = (0, 0, CV_WIDE, CV_HEIGHT))

    canvas_win.place(x = 0, y = 0)

    dots = [[]]
    seed_dot = []
    dotslist_box.delete(0, END)


def parse_color(num_color):
    color = "orange"

    if (num_color == 1):
        color = "#ff6e41" #"orange"
    elif (num_color == 2):
        color = "#ff5733" #"red"
    elif (num_color == 3):
        color = "#0055ff" #"blue"
    elif (num_color == 4):
        color = "#45ff00" #"green"

    return color


def show_info():
    messagebox.showinfo("Информация", "Программа, организующая заполнение \
        ограниченной замкнутой области через затравочный пиксель \
        \n\n\nЛевая кнопка мыши:\n  установить вершину многоугольника \
        \n\nПравая кнопка мыши:\n  установить затравочный пиксель", detail = "")



if __name__ == "__main__":
    '''
        Основной графический модуль
    '''

    win = Tk()
    win['bg'] = WIN_COLOR
    win.geometry("%dx%d" %(WIN_WIDTH, WIN_HEIGHT))
    win.title("Лабораторная работа #6 (Цветков И.А. ИУ7-43Б)")
    win.resizable(False, False)

    canvas_win = Canvas(win, width = CV_WIDE, height = CV_HEIGHT, bg = CV_COLOR)

    image_canvas = PhotoImage(width = CV_WIDE, height = CV_HEIGHT)
    canvas_win.create_image((CV_WIDE / 2, CV_HEIGHT / 2), image = image_canvas, state = "normal")

    image_canvas.put("#ffffff", to = (0, 0, CV_WIDE, CV_HEIGHT))
    canvas_win.place(x = 0, y = 0)

    # Add dot

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 3, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 10)

    add_dot_text = Label(win, text = "Добавить точку", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    add_dot_text.place(x = CV_WIDE + 20, y = 10)

    x_text = Label(text = "x: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x_text.place(x = CV_WIDE + 70, y = 50)

    x_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    x_entry.place(x = CV_WIDE + 130, y = 50)

    y_text = Label(text = "y: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    y_text.place(x = CV_WIDE + 330, y = 50)

    y_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    y_entry.place(x = CV_WIDE + 390, y = 50)

    add_dot_btn = Button(win, text = "Добавить точку", font="-family {Consolas} -size 14", command = lambda: read_dot())
    add_dot_btn.place(x = CV_WIDE + 110, y = 100)

    del_dot_btn = Button(win, text = "Удалить крайнюю", font="-family {Consolas} -size 14", command = lambda: del_dot())
    del_dot_btn.place(x = CV_WIDE + 310, y = 100)

    make_figure_btn = Button(win, text = "Замкнуть фигуру", font="-family {Consolas} -size 14", command = lambda: make_figure())
    make_figure_btn.place(x = CV_WIDE + 200, y = 145)


    # Dots list

    dots = [[]]
    seed_dot = []

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 7, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 190)

    dots_list_text = Label(win, text = "Список точек", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    dots_list_text.place(x = CV_WIDE + 20, y = 190)

    dotslist_box = Listbox(bg = "white")
    dotslist_box.configure(height = 5, width = 45)
    dotslist_box.configure(font="-family {Consolas} -size 14")
    dotslist_box.place(x = CV_WIDE + 55, y = 230)


    # Add seed dot

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 3, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 400)

    add_seed_dot_text = Label(win, text = "Установить затравочный пиксель", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    add_seed_dot_text.place(x = CV_WIDE + 20, y = 400)

    x_seed_text = Label(text = "x: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x_seed_text.place(x = CV_WIDE + 70, y = 440)

    x_seed_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    x_seed_entry.place(x = CV_WIDE + 130, y = 440)

    y_seed_text = Label(text = "y: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    y_seed_text.place(x = CV_WIDE + 330, y = 440)

    y_seed_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    y_seed_entry.place(x = CV_WIDE + 390, y = 440)

    add_seed_dot_btn = Button(win, text = "Установить затравочный пиксель", font="-family {Consolas} -size 14", command = lambda: read_dot())
    add_seed_dot_btn.place(x = CV_WIDE + 130, y = 490)


    # Fill figure

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 3, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 540)

    color_text = Label(win, text = "Выбрать тип закраски", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 540)

    option_filling = IntVar()
    option_filling.set(1)

    draw_delay = Radiobutton(text = "С задержкой", font="-family {Consolas} -size 14", variable = option_filling, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    draw_delay.place(x = CV_WIDE + 25, y = 575)

    draw_without_delay = Radiobutton(text = "Без задержки", font="-family {Consolas} -size 14", variable = option_filling, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    draw_without_delay.place(x = CV_WIDE + 350, y = 575)

    fill_figure_btn = Button(win, text = "Закрасить выбранную область", font="-family {Consolas} -size 14", command = lambda: parse_fill())
    fill_figure_btn.place(x = CV_WIDE + 150, y = 625)

    # Time, clear and info

    time_label = Label(text = "Время: %-3.2f с" %(0), font="-family {Consolas} -size 16", bg = "lightgrey")
    time_label.place(x = 20, y = CV_HEIGHT - 50)

    info_btn = Button(win, width = 20, height = 2, text = "Информация", font="-family {Consolas} -size 14", command = lambda: show_info())
    info_btn.place(x = CV_WIDE + 35, y = 830)

    clear_win_btn = Button(win, width = 20, height = 2, text = "Очистить экран", font="-family {Consolas} -size 14", command = lambda: reboot_prog())
    clear_win_btn.place(x = CV_WIDE + 315, y = 830)

    # Binds

    canvas_win.bind("<1>", add_dot_click)
    canvas_win.bind("<3>", add_seed_dot_click)

    # TODO Choose color 

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 5, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 680)

    color_text = Label(win, text = "Выбрать цвет заполнения", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 680)

    option_color = IntVar()
    option_color.set(1)

    color_orange = Radiobutton(text = "Оранжевый", font="-family {Consolas} -size 14", variable = option_color, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_orange.place(x = CV_WIDE + 25, y = 710)

    color_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_red.place(x = CV_WIDE + 400, y = 710)

    color_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_blue.place(x = CV_WIDE + 25, y = 750)

    color_green = Radiobutton(text = "Зеленый", font="-family {Consolas} -size 14", variable = option_color, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_green.place(x = CV_WIDE + 400, y = 750)



    win.mainloop()