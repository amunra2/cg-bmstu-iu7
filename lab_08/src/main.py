from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, Radiobutton, LEFT, RIGHT, IntVar, PhotoImage
from tkinter import messagebox
from math import sqrt, acos, degrees, pi, sin, cos, radians, floor, fabs
import copy
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

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

    lines = [[]]
    cutter = []
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


def add_dot_click(event):
    x = event.x
    y = event.y

    add_dot(x, y)


def read_dot():
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты точки")
        return

    add_dot(int(x), int(y))


def is_maked():
    maked = False

    if (len(cutter) > 3):
        if ((cutter[0][0] == cutter[len(cutter) - 1][0]) and (cutter[0][1] == cutter[len(cutter) - 1][1])):
            maked = True

    return maked


def add_dot(x, y, last = True):
    if (is_maked()): # для задания нового отсекателя
        cutter.clear()
        canvas_win.delete("all")
        draw_lines()
        dotslist_box.delete(0, END)
            

    cutter_color = parse_color(option_color_cutter.get())

    cutter.append([x, y])
    cur_dot = len(cutter) - 1

    if (last):
        dotslist_box.insert(END, "%d. (%4d;%4d)" %(cur_dot + 1, x, y))

    if (len(cutter) > 1):
        canvas_win.create_line(cutter[cur_dot - 1], cutter[cur_dot], fill = cutter_color)
        # bresenham_int(dots[cur_figure][cur_dot - 1], dots[cur_figure][cur_dot], COLOR_LINE)
        

def del_dot():
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

    dotslist_box.delete(index - 1, END)

    cutter.pop(len(cutter) - 1)


def make_figure():
    cur_dot = len(cutter)

    if (cur_dot < 3):
        messagebox.showerror("Ошибка", "Недостаточно точек, чтобы замкнуть фигуру")

    add_dot(cutter[0][0], cutter[0][1], last = False)


def draw_lines():

    for line in lines:
        if (len(line) != 0):
            x1 = line[0][0]
            y1 = line[0][1]

            x2 = line[1][0]
            y2 = line[1][1]

            color_line = line[2]

            #bresenham_int([x1, y1], [x2, y2], line_color)

            canvas_win.create_line(x1, y1, x2, y2, fill = color_line)


def add_line_click(event):
    
    x = event.x
    y = event.y

    add_line(x, y)




def add_line(x, y):
    line_color = parse_color(option_color_line.get())

    cur_line = len(lines) - 1

    if (len(lines[cur_line]) == 0):
        lines[cur_line].append([x, y])
    else:
        lines[cur_line].append([x, y])
        lines[cur_line].append(line_color)
        lines.append(list())

        x1 = lines[cur_line][0][0]
        y1 = lines[cur_line][0][1]

        x2 = lines[cur_line][1][0]
        y2 = lines[cur_line][1][1]

        canvas_win.create_line(x1, y1, x2, y2, fill = line_color)



def read_line():
    global lines

    try:
        x1 = int(x_start_line_entry.get())
        y1 = int(y_start_line_entry.get())
        x2 = int(x_end_line_entry.get())
        y2 = int(y_end_line_entry.get())
    except:
        messagebox.showinfo("Ошибка", "Неверно введены координаты")
        return

    cur_line = len(lines) - 1
    line_color = parse_color(option_color_line.get())

    lines[cur_line].append([x1, y1])
    lines[cur_line].append([x2, y2])
    lines[cur_line].append(line_color)

    lines.append(list())
    
    canvas_win.create_line(x1, y1, x2, y2, fill = line_color)


# Algorithm

def get_vector(dot1, dot2):
    return [dot2[X_DOT] - dot1[X_DOT], dot2[Y_DOT] - dot1[Y_DOT]]


def vector_mul(vec1, vec2):
    return (vec1[0] * vec2[1] - vec1[1] * vec2[0])


def scalar_mul(vec1, vec2):
    return (vec1[0] * vec2[0] + vec1[1] * vec2[1])


def line_koefs(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1*y2 - x2*y1

    return a, b, c


def solve_lines_intersection(a1, b1, c1, a2, b2, c2):
    opr = a1*b2 - a2*b1
    opr1 = (-c1)*b2 - b1*(-c2)
    opr2 = a1*(-c2) - (-c1)*a2

    if (opr == 0):
        return -5, -5 # прямые параллельны

    x = opr1 / opr
    y = opr2 / opr

    return x, y


def is_coord_between(left_coord, right_coord, dot_coord):
    return (min(left_coord, right_coord) <= dot_coord) \
            and (max(left_coord, right_coord) >= dot_coord)


def is_dot_between(dot_left, dot_right, dot_intersec):
    return is_coord_between(dot_left[X_DOT], dot_right[X_DOT], dot_intersec[X_DOT]) \
            and is_coord_between(dot_left[Y_DOT], dot_right[Y_DOT], dot_intersec[Y_DOT])


def are_connected_sides(line1, line2):

    if ((line1[0][X_DOT] == line2[0][X_DOT]) and (line1[0][Y_DOT] == line2[0][Y_DOT])) \
            or ((line1[1][X_DOT] == line2[1][X_DOT]) and (line1[1][Y_DOT] == line2[1][Y_DOT])) \
            or ((line1[0][X_DOT] == line2[1][X_DOT]) and (line1[0][Y_DOT] == line2[1][Y_DOT])) \
            or ((line1[1][X_DOT] == line2[0][X_DOT]) and (line1[1][Y_DOT] == line2[0][Y_DOT])):
        return True

    return False



def extra_check(): # чтобы не было пересечений
    
    cutter_lines = []

    for i in range(len(cutter) - 1):
        cutter_lines.append([cutter[i], cutter[i + 1]]) # разбиваю отсекатель на линии

    combs_lines = list(combinations(cutter_lines, 2)) # все возможные комбинации сторон

    for i in range(len(combs_lines)):
        line1 = combs_lines[i][0]
        line2 = combs_lines[i][1]

        if (are_connected_sides(line1, line2)):
            print("Connected")
            continue

        a1, b1, c1 = line_koefs(line1[0][X_DOT], line1[0][Y_DOT], line1[1][X_DOT], line1[1][Y_DOT])
        a2, b2, c2 = line_koefs(line2[0][X_DOT], line2[0][Y_DOT], line2[1][X_DOT], line2[1][Y_DOT])

        dot_intersec = solve_lines_intersection(a1, b1, c1, a2, b2, c2)

        if (is_dot_between(line1[0], line1[1], dot_intersec)) \
                and (is_dot_between(line2[0], line2[1], dot_intersec)):
            return True

    return False


def check_polygon(): 
    if (len(cutter) < 3):
        return False

    sign = 0

    if (vector_mul(get_vector(cutter[1], cutter[2]), get_vector(cutter[0], cutter[1])) > 0):
        sign = 1
    else:
        sign = -1

    for i in range(3, len(cutter)):
        if sign * vector_mul(get_vector(cutter[i - 1], cutter[i]), get_vector(cutter[i - 2], cutter[i - 1])) < 0:
            return False

    check = extra_check()

    print("\n\nResult:", check, "\n\n")

    if (check):
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

    t_bottom = 0
    t_top = 1

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
                t_bottom = max(t_bottom, t)
            else:
                return
        elif (d_scalar < 0):
            if (t >= 0):
                t_top = min(t_top, t)
            else:
                return

        if (t_bottom > t_top):
            break
    

    dot1_res = [round(dot1[X_DOT] + d[X_DOT] * t_bottom), round(dot1[Y_DOT] + d[Y_DOT] * t_bottom)]
    dot2_res = [round(dot1[X_DOT] + d[X_DOT] * t_top), round(dot1[Y_DOT] + d[Y_DOT] * t_top)]
    
    res_color = parse_color(option_color_cut_line.get())

    if (t_bottom <= t_top):
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

    if (not is_maked()):
        messagebox.showinfo("Ошибка", "Отсекатель не замкнут")
        return

    if (len(cutter) < 3):
        messagebox.showinfo("Ошибка", "Не задан отсекатель")
        return

    if (not check_polygon()):
        messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником")
        return

    cutter_color = parse_color(option_color_cutter.get())
    canvas_win.create_polygon(cutter, outline = cutter_color, fill = "white")

    find_start_dot()

    dot = cutter.pop()

    for line in lines:
        if (line):
            cyrus_beck_algorithm(line, len(cutter))

    cutter.append(dot)



def add_paral_line_cutter(event):
    print("Pressed: Space", event.x, event.y)

    dif_x = abs(event.x - cutter[len(cutter) - 1][X_DOT])
    dif_y = abs(event.y - cutter[len(cutter) - 1][Y_DOT])

    if (dif_x > dif_y):
        add_dot(event.x, cutter[len(cutter) - 1][Y_DOT])
    else:
        add_dot(cutter[len(cutter) - 1][X_DOT], event.y)


def add_paral_line_line(event):
    print("Pressed: Control_L", event.x, event.y)

    cur_line = len(lines) - 1

    if (len(lines[cur_line]) > 0):
        dif_x = abs(event.x - lines[cur_line][0][X_DOT])
        dif_y = abs(event.y - lines[cur_line][0][Y_DOT])

        if (dif_x > dif_y):
            add_line(event.x, lines[cur_line][0][Y_DOT])
        else:
            add_line(lines[cur_line][0][X_DOT], event.y)


if __name__ == "__main__":
    '''
        Основной графический модуль
    '''

    win = Tk()
    win['bg'] = WIN_COLOR
    win.geometry("%dx%d" %(WIN_WIDTH, WIN_HEIGHT))
    win.title("Лабораторная работа #8 (Цветков И.А. ИУ7-43Б)")
    win.resizable(False, False)

    canvas_win = Canvas(win, width = CV_WIDE, height = CV_HEIGHT, bg = CV_COLOR)
    canvas_win.place(x = 0, y = 0)

    # Binds

    lines = [[]]
    canvas_win.bind("<3>", add_line_click)

    cutter = []
    canvas_win.bind("<1>", add_dot_click)

    canvas_win.bind('<space>', add_paral_line_cutter)
    canvas_win.bind('<Control_L>', add_paral_line_line)

    # Add cutter

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 8, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 10)

    add_dot_text = Label(win, text = "Добавить точку отсекателя", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    add_dot_text.place(x = CV_WIDE + 20, y = 10)

    x_text = Label(text = "x: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x_text.place(x = CV_WIDE + 30, y = 50)

    x_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    x_entry.place(x = CV_WIDE + 90, y = 50)

    y_text = Label(text = "y: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    y_text.place(x = CV_WIDE + 30, y = 90)

    y_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    y_entry.place(x = CV_WIDE + 90, y = 90)

    # Dots list

    dots_list_text = Label(win, text = "Список точек", width = 20, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    dots_list_text.place(x = CV_WIDE + 300, y = 55)

    dotslist_box = Listbox(bg = "white")
    dotslist_box.configure(height = 5, width = 23)
    dotslist_box.configure(font="-family {Consolas} -size 14")
    dotslist_box.place(x = CV_WIDE + 303, y = 88)

    # Buttons for cutter

    add_dot_btn = Button(win, text = "Добавить точку", font="-family {Consolas} -size 14", command = lambda: read_dot())
    add_dot_btn.place(x = CV_WIDE + 50, y = 140)

    del_dot_btn = Button(win, text = "Удалить крайнюю", font="-family {Consolas} -size 14", command = lambda: del_dot())
    del_dot_btn.place(x = CV_WIDE + 45, y = 180)

    make_figure_btn = Button(win, text = "Замкнуть отсекатель", font="-family {Consolas} -size 14", command = lambda: make_figure())
    make_figure_btn.place(x = CV_WIDE + 180, y = 235)


    # Add line

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 6, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 290)

    cutter_text = Label(win, text = "Добавить отрезок", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    cutter_text.place(x = CV_WIDE + 20, y = 290)


    x_start_line_text = Label(text = "Начало x: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x_start_line_text.place(x = CV_WIDE + 20, y = 330)

    x_start_line_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    x_start_line_entry.place(x = CV_WIDE + 130, y = 330)

    y_start_line_text = Label(text = "y: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    y_start_line_text.place(x = CV_WIDE + 360, y = 330)

    y_start_line_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    y_start_line_entry.place(x = CV_WIDE + 390, y = 330)


    x_end_line_text = Label(text = "Конец  x: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x_end_line_text.place(x = CV_WIDE + 20, y = 370)

    x_end_line_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    x_end_line_entry.place(x = CV_WIDE + 130, y = 370)

    y_end_line_text = Label(text = "y: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    y_end_line_text.place(x = CV_WIDE + 360, y = 370)

    y_end_line_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    y_end_line_entry.place(x = CV_WIDE + 390, y = 370)


    add_line_btn = Button(win, text = "Нарисовать отрезок", font="-family {Consolas} -size 14", command = lambda: add_line())
    add_line_btn.place(x = CV_WIDE + 190, y = 405)


    # TODO Choose cutter color 

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 4, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 475)

    color_text = Label(win, text = "Выбрать цвет отсекателя", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 475)

    option_color_cutter = IntVar()
    option_color_cutter.set(1)

    color_cutter_orange = Radiobutton(text = "Оранжевый", font="-family {Consolas} -size 14", variable = option_color_cutter, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cutter_orange.place(x = CV_WIDE + 25, y = 505)

    color_cutter_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color_cutter, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cutter_red.place(x = CV_WIDE + 400, y = 505)

    color_cutter_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color_cutter, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cutter_blue.place(x = CV_WIDE + 25, y = 545)

    color_cutter_green = Radiobutton(text = "Зеленый", font="-family {Consolas} -size 14", variable = option_color_cutter, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cutter_green.place(x = CV_WIDE + 400, y = 545)


    # TODO Choose line color 

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 4, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 590)

    color_text = Label(win, text = "Выбрать цвет отрезка", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 590)

    option_color_line = IntVar()
    option_color_line.set(3)

    color_line_orange = Radiobutton(text = "Оранжевый", font="-family {Consolas} -size 14", variable = option_color_line, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_orange.place(x = CV_WIDE + 25, y = 630)

    color_line_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color_line, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_red.place(x = CV_WIDE + 400, y = 630)

    color_line_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color_line, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_blue.place(x = CV_WIDE + 25, y = 660)

    color_line_green = Radiobutton(text = "Зеленый", font="-family {Consolas} -size 14", variable = option_color_line, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_green.place(x = CV_WIDE + 400, y = 660)


    # TODO Choose cut line color 

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 4, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 705)

    color_text = Label(win, text = "Выбрать цвет результата", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 705)

    option_color_cut_line = IntVar()
    option_color_cut_line.set(4)

    color_cut_line_orange = Radiobutton(text = "Оранжевый", font="-family {Consolas} -size 14", variable = option_color_cut_line, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cut_line_orange.place(x = CV_WIDE + 25, y = 745)

    color_cut_line_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color_cut_line, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cut_line_red.place(x = CV_WIDE + 400, y = 745)

    color_cut_line_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color_cut_line, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cut_line_blue.place(x = CV_WIDE + 25, y = 775)

    color_cut_line_green = Radiobutton(text = "Зеленый", font="-family {Consolas} -size 14", variable = option_color_cut_line, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cut_line_green.place(x = CV_WIDE + 400, y = 775)


    # add_vert_horiz_lines_btn = Button(win, text = "Добавить вертикальный и\nгоризонтальный отрезки", width = 35, height = 2, font="-family {Consolas} -size 14", command = lambda: add_vert_horiz_lines())
    # add_vert_horiz_lines_btn.place(x = CV_WIDE + 100, y = 750)

    cut_btn = Button(win, text = "Отсечь", width = 18, height = 2, font="-family {Consolas} -size 14", command = lambda: cut_area())
    cut_btn.place(x = CV_WIDE + 20, y = 830)

    clear_btn = Button(win, text = "Очистить экран", width = 18, height = 2, font="-family {Consolas} -size 14", command = lambda: reboot_prog())
    clear_btn.place(x = CV_WIDE + 350, y = 830)



    win.mainloop()
