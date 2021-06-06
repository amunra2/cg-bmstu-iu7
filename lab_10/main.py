from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, Radiobutton, LEFT, RIGHT, IntVar, PhotoImage, Spinbox
from tkinter import messagebox
from math import sqrt, acos, degrees, pi, sin, cos, radians, floor, fabs
import copy
from tkinter.constants import Y
import numpy as np
import matplotlib.pyplot as plt
from numpy import arange

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

X_DOT = 0
Y_DOT = 1
Z_DOT = 2

FROM = 0
TO = 1
STEP = 2

# For rectangle
is_set_rect = False


def check_option(option):
    messagebox.showinfo("Выбран", "Выбрана опция %d" %(option))


def clear_canvas():
    canvas_win.delete("all")


def get_fill_check_color(collor_fill):
    return (int(collor_fill[1:3], 16), int(collor_fill[3:5], 16), int(collor_fill[5:7], 16))


def reboot_prog():

    canvas_win.delete("all")


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


def parse_funcs(func_num):
    func = lambda x, z: sin(x) * cos(z)

    if (func_num == 1):
        func = lambda x, z: sin(x) * sin(z)
    elif (func_num == 2):
        func = lambda x, z: sin(cos(x)) * sin(z)
    elif (func_num == 3):
        func = lambda x, z: cos(x) * z / 3

    return func


def read_limits():
    try:
        x_from = float(x_from_entry.get())
        x_to = float(x_to_entry.get())
        x_step = float(x_step_entry.get())

        x_limits = [x_from, x_to, x_step]

        z_from = float(z_from_entry.get())
        z_to = float(z_to_entry.get())
        z_step = float(z_step_entry.get())

        z_limits = [z_from, z_to, z_step]
    
        return x_limits, z_limits
    except:
        return


def read_scale():
    try:
        scale_param = float(scale_entry.get())

        return scale_param
    except:
        return


trans_matrix = [[int(i == j) for i in range(4)] for j in range(4)]


def trans_dot(dot):
    dot.append(1) 

    print(dot)

    res_dot = [0, 0, 0, 0]

    for i in range(4):
        for j in range(4):
            res_dot[i] += dot[j] * trans_matrix[j][i]

    print(res_dot)

    scale_param = read_scale()

    for i in range(3):
        res_dot[i] *= scale_param

    res_dot[0] += CV_WIDE // 2
    res_dot[1] += CV_HEIGHT // 2

    return res_dot[:3]


def is_visible(dot):
    return (0 <= dot[X_DOT] <= CV_WIDE) and \
            (0 <= dot[Y_DOT] <= CV_HEIGHT)


def draw_pixel(x, y):
    color = parse_color(option_color_graph.get())

    canvas_win.create_line(x, y, x + 1, y + 1, fill = color)


def draw_dot(x, y, high_horizon, low_horizon):
    if (not is_visible([x, y])):
        return False

    if (y > high_horizon[x]):
        high_horizon[x] = y
        draw_pixel(x, y)
    elif (y < low_horizon[x]):
        low_horizon[x] = y
        draw_pixel(x, y)

    return True


def draw_horizon_part(dot1, dot2, high_horizon, low_horizon):
    if (dot1[X_DOT] > dot2[X_DOT]):
        dot1, dot2 = dot2, dot1

    #print(dot1, dot2)

    dx = dot2[X_DOT] - dot1[X_DOT]
    dy = dot2[Y_DOT] - dot1[Y_DOT]

    if (dx > dy):
        l = dx
    else:
        l = dy

    #print(dx, dy, l)

    dx /= l
    dy /= l

    x = dot1[X_DOT]
    y = dot1[Y_DOT]

    for _ in range(int(l) + 1):
        if (not draw_dot(round(x), y, high_horizon, low_horizon)):
            return

        x += dx
        y += dy


def draw_horizon(function, high_horizon, low_horizon, limits, z):
    f = lambda x: function(x, z)

    prev = None

    for x in arange(limits[FROM], limits[TO] + limits[STEP], limits[STEP]):
        cur = trans_dot([x, f(x), z])

        if (prev):
            draw_horizon_part(prev, cur, high_horizon, low_horizon)

        prev = cur



def build_graph():
    reboot_prog()

    f = parse_funcs(option_function.get())

    x_limits, z_limits = read_limits()

    print(x_limits, z_limits)

    high_horizon = [0 for i in range(CV_WIDE)] # ???
    low_horizon = [CV_HEIGHT for i in range(CV_WIDE)]


    for z in arange(z_limits[FROM], z_limits[TO] + z_limits[STEP], z_limits[STEP]):
        draw_horizon(f, high_horizon, low_horizon, x_limits, z)

    color = parse_color(option_color_graph.get())

    for z in arange(z_limits[FROM], z_limits[TO] + z_limits[STEP], z_limits[STEP]):
        dot1 = trans_dot([x_limits[FROM], f(x_limits[FROM], z), z])
        dot2 = trans_dot([x_limits[FROM], f(x_limits[FROM], z + x_limits[STEP]), z + x_limits[STEP]])

        canvas_win.create_line(dot1[X_DOT], dot1[Y_DOT], dot2[X_DOT], dot2[Y_DOT], fill = color)

        dot1 = trans_dot([x_limits[TO], f(x_limits[TO], z), z])
        dot2 = trans_dot([x_limits[TO], f(x_limits[TO], z + x_limits[STEP]), z + x_limits[STEP]])

        canvas_win.create_line(dot1[X_DOT], dot1[Y_DOT], dot2[X_DOT], dot2[Y_DOT], fill = color)
    

    










if __name__ == "__main__":
    '''
        Основной графический модуль
    '''

    win = Tk()
    win['bg'] = WIN_COLOR
    win.geometry("%dx%d" %(WIN_WIDTH, WIN_HEIGHT))
    win.title("Лабораторная работа #10 (Цветков И.А. ИУ7-43Б)")
    win.resizable(False, False)

    canvas_win = Canvas(win, width = CV_WIDE, height = CV_HEIGHT, bg = CV_COLOR)
    canvas_win.place(x = 0, y = 0)

    # Binds

    #canvas_win.bind("<1>", add_rect_click1)

    cutter = []
    figure = []

    lines = []

    # canvas_win.bind("<1>", add_dot_cutter_click)
    # canvas_win.bind("<3>", add_dot_figure_click)

    #canvas_win.bind('<B1-Motion>', add_rect_click)
    
    #canvas_win.bind('LeftCtrl', add_vert_horiz_lines)

    # Set function

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 8, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 10)

    add_dot_text = Label(win, text = "Функция", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    add_dot_text.place(x = CV_WIDE + 20, y = 10)

    option_function = IntVar()
    option_function.set(1)

    graph1_option = Radiobutton(text = "sin(x) * cos(x)", font="-family {Consolas} -size 14", variable = option_function, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    graph1_option.place(x = CV_WIDE + 180, y = 50)

    graph2_option = Radiobutton(text = "sin(x) * cos(x) * sqrt(x)", font="-family {Consolas} -size 14", variable = option_function, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    graph2_option.place(x = CV_WIDE + 140, y = 90)

    graph3_option = Radiobutton(text = "sqrt(x) * cos(z)", font="-family {Consolas} -size 14", variable = option_function, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    graph3_option.place(x = CV_WIDE + 180, y = 130)

    graph4_option = Radiobutton(text = "sin(cos(x)))", font="-family {Consolas} -size 14", variable = option_function, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    graph4_option.place(x = CV_WIDE + 200, y = 170)

    # Set limits for function

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 5, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 225)

    figure_add_dot_text = Label(win, text = "Пределы", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    figure_add_dot_text.place(x = CV_WIDE + 20, y = 225)

    # Axis OX

    x_limit_text = Label(text = "Ось X  -- ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x_limit_text.place(x = CV_WIDE + 30, y = 265)

    x_from_text = Label(text = "от: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x_from_text.place(x = CV_WIDE + 150, y = 265)
    x_from_entry = Spinbox(font="-family {Consolas} -size 14", from_=0.0, to=1000.0, increment=1.0, width = 6)
    # x_from_entry = Entry(font="-family {Consolas} -size 14", width = 6)
    x_from_entry.place(x = CV_WIDE + 190, y = 265)

    x_to_text = Label(text = "до: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x_to_text.place(x = CV_WIDE + 295, y = 265)
    x_to_entry = Spinbox(font="-family {Consolas} -size 14", from_=0.0, to=1000.0, increment=1.0, width = 6)
    # x_to_entry = Entry(font="-family {Consolas} -size 14", width = 6)
    x_to_entry.place(x = CV_WIDE + 330, y = 265)

    x_step_text = Label(text = "шаг: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x_step_text.place(x = CV_WIDE + 430, y = 265)
    x_step_entry = Spinbox(font="-family {Consolas} -size 14", from_=0.0, to=1000.0, increment=1.0, width = 6)
    # x_step_entry = Entry(font="-family {Consolas} -size 14", width = 6)
    x_step_entry.place(x = CV_WIDE + 480, y = 265)

    # Insert
    x_from_entry.delete(0, END)
    x_from_entry.insert(0, "-10")
    x_to_entry.delete(0, END)
    x_to_entry.insert(0, "10")
    x_step_entry.delete(0, END)
    x_step_entry.insert(0, "0.1")


    # Axis OZ
    z_limit_text = Label(text = "Ось Z  -- ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    z_limit_text.place(x = CV_WIDE + 30, y = 315)

    z_from_text = Label(text = "от: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    z_from_text.place(x = CV_WIDE + 150, y = 315)
    z_from_entry = Spinbox(font="-family {Consolas} -size 14", from_=0.0, to=1000.0, increment=1.0, width = 6)
    # z_from_entry = Entry(font="-family {Consolas} -size 14", width = 6)
    z_from_entry.place(x = CV_WIDE + 190, y = 315)

    z_to_text = Label(text = "до: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    z_to_text.place(x = CV_WIDE + 295, y = 315)
    z_to_entry = Spinbox(font="-family {Consolas} -size 14", from_=0.0, to=1000.0, increment=1.0, width = 6)
    # z_to_entry = Entry(font="-family {Consolas} -size 14", width = 6)
    z_to_entry.place(x = CV_WIDE + 330, y = 315)

    z_step_text = Label(text = "шаг: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    z_step_text.place(x = CV_WIDE + 430, y = 315)
    z_step_entry = Spinbox(font="-family {Consolas} -size 14", from_=0.0, to=1000.0, increment=1.0, width = 6)
    # z_step_entry = Entry(font="-family {Consolas} -size 14", width = 6)
    z_step_entry.place(x = CV_WIDE + 480, y = 315)

    # Insert
    z_from_entry.delete(0, END)
    z_from_entry.insert(0, "-10")
    z_to_entry.delete(0, END)
    z_to_entry.insert(0, "10")
    z_step_entry.delete(0, END)
    z_step_entry.insert(0, "0.1")


    # Set spin

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 7, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 380)

    figure_add_dot_text = Label(win, text = "Вращение", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    figure_add_dot_text.place(x = CV_WIDE + 20, y = 380)

    # Spin OX

    x_spin_text = Label(text = "OX: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x_spin_text.place(x = CV_WIDE + 120, y = 420)

    x_spin_entry = Spinbox(font="-family {Consolas} -size 14", from_=0.0, to=1000.0, increment=1.0, width = 6)
    # x_spin_entry = Entry(font="-family {Consolas} -size 14", width = 6)
    x_spin_entry.place(x = CV_WIDE + 190, y = 420)

    x_spin_btn = Button(win, text = "Повернуть", width = 12, height = 1, font="-family {Consolas} -size 14", command = lambda: cut_area())
    x_spin_btn.place(x = CV_WIDE + 330, y = 415)


    # Spin OY

    y_spin_text = Label(text = "OY: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    y_spin_text.place(x = CV_WIDE + 120, y = 465)

    y_spin_entry = Spinbox(font="-family {Consolas} -size 14", from_=0.0, to=1000.0, increment=1.0, width = 6)
    # y_spin_entry = Entry(font="-family {Consolas} -size 14", width = 6)
    y_spin_entry.place(x = CV_WIDE + 190, y = 465)

    y_spin_btn = Button(win, text = "Повернуть", width = 12, height = 1, font="-family {Consolas} -size 14", command = lambda: cut_area())
    y_spin_btn.place(x = CV_WIDE + 330, y = 460)


    # Spin OZ

    z_spin_text = Label(text = "OZ: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    z_spin_text.place(x = CV_WIDE + 120, y = 510)

    z_spin_entry = Spinbox(font="-family {Consolas} -size 14", from_=0.0, to=1000.0, increment=1.0, width = 6)
    # z_spin_entry = Entry(font="-family {Consolas} -size 14", width = 6)
    z_spin_entry.place(x = CV_WIDE + 190, y = 510)

    z_spin_btn = Button(win, text = "Повернуть", width = 12, height = 1, font="-family {Consolas} -size 14", command = lambda: cut_area())
    z_spin_btn.place(x = CV_WIDE + 330, y = 505)


    # Set scale

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 5, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 570)

    figure_add_dot_text = Label(win, text = "Масштабировать", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    figure_add_dot_text.place(x = CV_WIDE + 20, y = 570)

    # Scale k

    scale_text = Label(text = "Коэффициент k ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    scale_text.place(x = CV_WIDE + 120, y = 610)

    scale_entry = Spinbox(font="-family {Consolas} -size 14", from_=0.0, to=1000.0, increment=1.0, width = 7)
    # x_spin_entry = Entry(font="-family {Consolas} -size 14", width = 6)
    scale_entry.place(x = CV_WIDE + 330, y = 610)

    scale_btn = Button(win, text = "Масштабировать", width = 14, height = 1, font="-family {Consolas} -size 14", command = lambda: cut_area())
    scale_btn.place(x = CV_WIDE + 190, y = 655)

    # Insert
    scale_entry.delete(0, END)
    scale_entry.insert(0, "48")

    

    # TODO Choose cut line color 

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 4, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 710)

    color_text = Label(win, text = "Выбрать цвет графика", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 710)

    option_color_graph = IntVar()
    option_color_graph.set(3)

    color_graph_orange = Radiobutton(text = "Оранжевый", font="-family {Consolas} -size 14", variable = option_color_graph, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_graph_orange.place(x = CV_WIDE + 25, y = 750)

    color_graph_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color_graph, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_graph_red.place(x = CV_WIDE + 400, y = 750)

    color_graph_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color_graph, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_graph_blue.place(x = CV_WIDE + 25, y = 780)

    color_graph_green = Radiobutton(text = "Зеленый", font="-family {Consolas} -size 14", variable = option_color_graph, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_graph_green.place(x = CV_WIDE + 400, y = 780)


    cut_btn = Button(win, text = "Результат", width = 18, height = 2, font="-family {Consolas} -size 14", command = lambda: build_graph())
    cut_btn.place(x = CV_WIDE + 20, y = 830)

    clear_btn = Button(win, text = "Очистить экран", width = 18, height = 2, font="-family {Consolas} -size 14", command = lambda: reboot_prog())
    clear_btn.place(x = CV_WIDE + 350, y = 830)



    win.mainloop()
