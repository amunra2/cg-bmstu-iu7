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

# Define

X_MIN = 0
X_MAX = 1
Y_MIN = 2
Y_MAX = 3

X_DOT = 0
Y_DOT = 1

# For rectangle
is_set_rect = False


def check_option(option):
    messagebox.showinfo("Выбран", "Выбрана опция %d" %(option))


def clear_canvas():
    canvas_win.delete("all")


def get_fill_check_color(collor_fill):
    return (int(collor_fill[1:3], 16), int(collor_fill[3:5], 16), int(collor_fill[5:7], 16))


def reboot_prog():
    global lines
    global cutter

    canvas_win.delete("all")

    cutter = []
    figure = []
    cutter_dotslist_box.delete(0, END)
    figure_dotslist_box.delete(0, END)


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


def is_maked(object):
    maked = False

    if (len(object) > 3):
        if ((object[0][0] == object[len(object) - 1][0]) and (object[0][1] == object[len(object) - 1][1])):
            maked = True

    return maked



def add_dot_cutter_click(event):
    x = event.x
    y = event.y

    add_dot_cutter(x, y)


def read_dot_cutter():
    try:
        x = float(cutter_x_entry.get())
        y = float(cutter_y_entry.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты точки")
        return

    add_dot_cutter(int(x), int(y))


def add_dot_cutter(x, y, last = True):
    if (is_maked(cutter)): # для задания нового отсекателя
            cutter.clear()
            canvas_win.delete("all")
            draw_figure()
            cutter_dotslist_box.delete(0, END)
            

    cutter_color = parse_color(option_color_cutter.get())

    cutter.append([x, y])
    cur_dot = len(cutter) - 1

    if (last):
        cutter_dotslist_box.insert(END, "%d. (%4d;%4d)" %(cur_dot + 1, x, y))

    if (len(cutter) > 1):
        canvas_win.create_line(cutter[cur_dot - 1], cutter[cur_dot], fill = cutter_color)
        # bresenham_int(dots[cur_figure][cur_dot - 1], dots[cur_figure][cur_dot], COLOR_LINE)
        

def del_dot_cutter():
    if (is_maked()):
        return

    cur_dot = len(cutter) - 1

    if (len(cutter) == 0):
        return

    if (len(cutter) > 1):
        canvas_win.create_line(cutter[cur_dot - 1], cutter[cur_dot], fill = "white")
        #bresenham_int(dots[cur_figure][cur_dot - 1], dots[cur_figure][cur_dot], "white")

    # Find index for a table

    index = len(cutter)

    cutter_dotslist_box.delete(index - 1, END)

    cutter.pop(len(cutter) - 1)


def make_cutter():
    if (is_maked(cutter)):
        messagebox.showerror("Ошибка", "Фигура уже замкнута")
        return

    cur_dot = len(cutter)

    if (cur_dot < 3):
        messagebox.showerror("Ошибка", "Недостаточно точек, чтобы замкнуть фигуру")
        return

    add_dot_cutter(cutter[0][0], cutter[0][1], last = False)


# Figure

def add_dot_figure_click(event):
    x = event.x
    y = event.y

    add_dot_figure(x, y)


def read_dot_figure():
    try:
        x = float(figure_x_entry.get())
        y = float(figure_y_entry.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты точки")
        return

    add_dot_figure(int(x), int(y))


def add_dot_figure(x, y, last = True):
    if (is_maked(figure)): # для задания нового отсекателя
            figure.clear()
            #draw_lines()
            figure_dotslist_box.delete(0, END)
            

    figure_color = parse_color(option_color_cut_line.get())

    figure.append([x, y])
    cur_dot = len(figure) - 1

    if (last):
        figure_dotslist_box.insert(END, "%d. (%4d;%4d)" %(cur_dot + 1, x, y))

    if (len(figure) > 1):
        canvas_win.create_line(figure[cur_dot - 1], figure[cur_dot], fill = figure_color)
        # bresenham_int(dots[cur_figure][cur_dot - 1], dots[cur_figure][cur_dot], COLOR_LINE)
        

def del_dot_figure():
    if (is_maked(figure)):
        return

    cur_dot = len(figure) - 1

    if (len(figure) == 0):
        return

    if (len(figure) > 1):
        canvas_win.create_line(figure[cur_dot - 1], figure[cur_dot], fill = "white")
        #bresenham_int(dots[cur_figure][cur_dot - 1], dots[cur_figure][cur_dot], "white")

    # Find index for a table

    index = len(figure)

    figure_dotslist_box.delete(index - 1, END)

    figure.pop(len(figure) - 1)


def make_figure():
    if (is_maked(figure)):
        messagebox.showerror("Ошибка", "Фигура уже замкнута")
        return

    cur_dot = len(figure)

    if (cur_dot < 3):
        messagebox.showerror("Ошибка", "Недостаточно точек, чтобы замкнуть фигуру")
        return

    add_dot_figure(figure[0][0], figure[0][1], last = False)


def draw_figure():
    figure_color = parse_color(option_color_cut_line.get())

    canvas_win.create_polygon(figure, outline = figure_color, fill = "white")


# Algorithm

def get_vector(dot1, dot2):
    return [dot2[X_DOT] - dot1[X_DOT], dot2[Y_DOT] - dot1[Y_DOT]]


def vector_mul(vec1, vec2):
    return (vec1[0] * vec2[1] - vec1[1] * vec2[0])


def scalar_mul(vec1, vec2):
    return (vec1[0] * vec2[0] + vec1[1] * vec2[1])


def check_polygon(): # через проход по всем точкам, поворот которых должен быть все время в одну сторону
    if (len(cutter) < 3):
        return False

    sign = 0

    if (vector_mul(get_vector(cutter[1], cutter[2]), get_vector(cutter[0], cutter[1])) > 0):
        sign = 1 # по часовой стрелке
    else:
        sign = -1 # против часовой стрелки

    for i in range(3, len(cutter)):
        if sign * vector_mul(get_vector(cutter[i - 1], cutter[i]), get_vector(cutter[i - 2], cutter[i - 1])) < 0:
            return False

    return True



def get_normal(dot1, dot2, pos):
    f_vect = get_vector(dot1, dot2)
    pos_vect = get_vector(dot2, pos)

    if (f_vect[1]):
        normal = [1, -f_vect[0] / f_vect[1]]
    else:
        normal = [0, 1]

    if (scalar_mul(pos_vect, normal) < 0):
        normal[0] = -normal[0]
        normal[1] = -normal[1]

    return normal


def cyrus_beck_algorithm(line, count):
    dot1 = line[0]
    dot2 = line[1]

    d = [dot2[X_DOT] - dot1[X_DOT], dot2[Y_DOT] - dot1[Y_DOT]]

    t_top = 0
    t_bottom = 1

    for i in range(-2, count - 2):
        normal = get_normal(cutter[i], cutter[i + 1], cutter[i + 2])

        w = [dot1[X_DOT] - cutter[i][X_DOT], dot1[Y_DOT] - cutter[i][Y_DOT]]

        d_scalar = scalar_mul(d, normal)
        w_scalar = scalar_mul(w, normal)

        if (d_scalar == 0):
            if (w_scalar < 0):
                return
            else:
                continue

        t = -w_scalar / d_scalar

        if (d_scalar > 0):
            if (t <= 1):
                t_top = max(t_top, t)
            else:
                return
        elif (d_scalar < 0):
            if (t >= 0):
                t_bottom = min(t_bottom, t)
            else:
                return

        if (t_top > t_bottom):
            break
    

    dot1_res = [round(dot1[X_DOT] + d[X_DOT] * t_top), round(dot1[Y_DOT] + d[Y_DOT] * t_top)]
    dot2_res = [round(dot1[X_DOT] + d[X_DOT] * t_bottom), round(dot1[Y_DOT] + d[Y_DOT] * t_bottom)]
    
    res_color = parse_color(option_color_cut_line.get())

    if (t_top <= t_bottom):
        canvas_win.create_line(dot1_res, dot2_res, fill = res_color)



# TODO


def find_start_dot():
    y_max = cutter[0][Y_DOT]
    dot_index = 0

    for i in range(len(cutter)):
        if (cutter[i][Y_DOT] > y_max):
            y_max = cutter[i][Y_DOT]
            dot_index = i

    cutter.pop()

    for _ in range(dot_index):
        cutter.append(cutter.pop(0))

    cutter.append(cutter[0])

    if (cutter[-2][0] > cutter[1][0]):
        cutter.reverse()


def cut_area():

    if (len(cutter) < 3):
        messagebox.showinfo("Ошибка", "Не задан отсекатель")
        return

    if (not check_polygon()):
        messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником")
        return

    cutter_color = parse_color(option_color_cutter.get())

    canvas_win.create_polygon(cutter, outline = cutter_color, fill = "white")

    find_start_dot()

    for line in lines:
        if (line):
            cyrus_beck_algorithm(line, len(cutter))



if __name__ == "__main__":
    '''
        Основной графический модуль
    '''

    win = Tk()
    win['bg'] = WIN_COLOR
    win.geometry("%dx%d" %(WIN_WIDTH, WIN_HEIGHT))
    win.title("Лабораторная работа #9 (Цветков И.А. ИУ7-43Б)")
    win.resizable(False, False)

    canvas_win = Canvas(win, width = CV_WIDE, height = CV_HEIGHT, bg = CV_COLOR)
    canvas_win.place(x = 0, y = 0)

    # Binds

    #canvas_win.bind("<1>", add_rect_click1)

    cutter = []
    figure = []

    lines = []

    canvas_win.bind("<1>", add_dot_cutter_click)
    canvas_win.bind("<3>", add_dot_figure_click)

    #canvas_win.bind('<B1-Motion>', add_rect_click)
    
    #canvas_win.bind('LeftCtrl', add_vert_horiz_lines)

    # Add cutter

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 8, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 10)

    add_dot_text = Label(win, text = "Добавить точку отсекателя", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    add_dot_text.place(x = CV_WIDE + 20, y = 10)

    cutter_x_text = Label(text = "x: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    cutter_x_text.place(x = CV_WIDE + 30, y = 50)

    cutter_x_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    cutter_x_entry.place(x = CV_WIDE + 90, y = 50)

    cutter_y_text = Label(text = "y: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    cutter_y_text.place(x = CV_WIDE + 30, y = 90)

    cutter_y_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    cutter_y_entry.place(x = CV_WIDE + 90, y = 90)

    # Dots list

    cutter_dots_list_text = Label(win, text = "Список точек", width = 20, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    cutter_dots_list_text.place(x = CV_WIDE + 300, y = 55)

    cutter_dotslist_box = Listbox(bg = "white")
    cutter_dotslist_box.configure(height = 5, width = 23)
    cutter_dotslist_box.configure(font="-family {Consolas} -size 14")
    cutter_dotslist_box.place(x = CV_WIDE + 303, y = 88)

    # Buttons for cutter

    cutter_add_dot_btn = Button(win, text = "Добавить точку", font="-family {Consolas} -size 14", command = lambda: read_dot_cutter())
    cutter_add_dot_btn.place(x = CV_WIDE + 50, y = 140)

    cutter_del_dot_btn = Button(win, text = "Удалить крайнюю", font="-family {Consolas} -size 14", command = lambda: del_dot_cutter())
    cutter_del_dot_btn.place(x = CV_WIDE + 45, y = 180)

    make_cutter_btn = Button(win, text = "Замкнуть отсекатель", font="-family {Consolas} -size 14", command = lambda: make_cutter())
    make_cutter_btn.place(x = CV_WIDE + 330, y = 440)


    # Add polygonal

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 8, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 225)

    figure_add_dot_text = Label(win, text = "Добавить точку многоугольника", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    figure_add_dot_text.place(x = CV_WIDE + 20, y = 225)

    figure_x_text = Label(text = "x: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    figure_x_text.place(x = CV_WIDE + 30, y = 265)

    figure_x_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    figure_x_entry.place(x = CV_WIDE + 90, y = 265)

    figure_y_text = Label(text = "y: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    figure_y_text.place(x = CV_WIDE + 30, y = 305)

    figure_y_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    figure_y_entry.place(x = CV_WIDE + 90, y = 305)

    # Dots list

    figure_dots_list_text = Label(win, text = "Список точек", width = 20, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    figure_dots_list_text.place(x = CV_WIDE + 300, y = 265)

    figure_dotslist_box = Listbox(bg = "white")
    figure_dotslist_box.configure(height = 5, width = 23)
    figure_dotslist_box.configure(font="-family {Consolas} -size 14")
    figure_dotslist_box.place(x = CV_WIDE + 303, y = 296)

    # Buttons for cutter

    figure_add_dot_btn = Button(win, text = "Добавить точку", font="-family {Consolas} -size 14", command = lambda: read_dot_figure())
    figure_add_dot_btn.place(x = CV_WIDE + 50, y = 355)

    figure_del_dot_btn = Button(win, text = "Удалить крайнюю", font="-family {Consolas} -size 14", command = lambda: del_dot_figure())
    figure_del_dot_btn.place(x = CV_WIDE + 45, y = 395)

    make_figure_btn = Button(win, text = "Замкнуть многоугольник", font="-family {Consolas} -size 14", command = lambda: make_figure())
    make_figure_btn.place(x = CV_WIDE + 30, y = 440)

    # TODO Choose cutter color 

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 4, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 480)

    color_text = Label(win, text = "Выбрать цвет отсекателя", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 480)

    option_color_cutter = IntVar()
    option_color_cutter.set(1)

    color_cutter_orange = Radiobutton(text = "Оранжевый", font="-family {Consolas} -size 14", variable = option_color_cutter, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cutter_orange.place(x = CV_WIDE + 25, y = 510)

    color_cutter_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color_cutter, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cutter_red.place(x = CV_WIDE + 400, y = 510)

    color_cutter_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color_cutter, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cutter_blue.place(x = CV_WIDE + 25, y = 550)

    color_cutter_green = Radiobutton(text = "Зеленый", font="-family {Consolas} -size 14", variable = option_color_cutter, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cutter_green.place(x = CV_WIDE + 400, y = 550)


    # TODO Choose line color 

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 4, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 595)

    color_text = Label(win, text = "Выбрать цвет отрезка", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 595)

    option_color_line = IntVar()
    option_color_line.set(3)

    color_line_orange = Radiobutton(text = "Оранжевый", font="-family {Consolas} -size 14", variable = option_color_line, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_orange.place(x = CV_WIDE + 25, y = 635)

    color_line_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color_line, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_red.place(x = CV_WIDE + 400, y = 635)

    color_line_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color_line, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_blue.place(x = CV_WIDE + 25, y = 665)

    color_line_green = Radiobutton(text = "Зеленый", font="-family {Consolas} -size 14", variable = option_color_line, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_green.place(x = CV_WIDE + 400, y = 665)


    # TODO Choose cut line color 

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 4, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 710)

    color_text = Label(win, text = "Выбрать цвет результата", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 710)

    option_color_cut_line = IntVar()
    option_color_cut_line.set(4)

    color_cut_line_orange = Radiobutton(text = "Оранжевый", font="-family {Consolas} -size 14", variable = option_color_cut_line, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cut_line_orange.place(x = CV_WIDE + 25, y = 750)

    color_cut_line_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color_cut_line, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cut_line_red.place(x = CV_WIDE + 400, y = 750)

    color_cut_line_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color_cut_line, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cut_line_blue.place(x = CV_WIDE + 25, y = 780)

    color_cut_line_green = Radiobutton(text = "Зеленый", font="-family {Consolas} -size 14", variable = option_color_cut_line, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cut_line_green.place(x = CV_WIDE + 400, y = 780)


    cut_btn = Button(win, text = "Отсечь", width = 18, height = 2, font="-family {Consolas} -size 14", command = lambda: cut_area())
    cut_btn.place(x = CV_WIDE + 20, y = 830)

    clear_btn = Button(win, text = "Очистить экран", width = 18, height = 2, font="-family {Consolas} -size 14", command = lambda: reboot_prog())
    clear_btn.place(x = CV_WIDE + 350, y = 830)



    win.mainloop()
