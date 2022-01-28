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
    global figure
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
    if (is_maked(figure)): # для задания нового отсекаемого
            reboot_prog() # ???
            

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


def extra_check(object): # чтобы не было пересечений
    
    lines = []

    for i in range(len(object) - 1):
        lines.append([object[i], object[i + 1]]) # разбиваю многоугольник на линии

    combs_lines = list(combinations(lines, 2)) # все возможные комбинации сторон

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


def check_polygon(): # через проход по всем точкам, поворот которых должен быть все время в одну сторону
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

    check = extra_check(cutter)

    print("\n\nResult:", check, "\n\n")

    if (check):
        return False

    if (sign < 0):
        cutter.reverse()

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


def is_visible(dot, f_dot, s_dot):
    vec1 = get_vector(f_dot, s_dot)
    vec2 = get_vector(f_dot, dot)

    if (vector_mul(vec1, vec2) <= 0):
        return True
    else:
        return False


def get_lines_parametric_intersec(line1, line2, normal):
    d = get_vector(line1[0], line1[1])
    w = get_vector(line2[0], line1[0])

    d_scalar = scalar_mul(d, normal)
    w_scalar = scalar_mul(w, normal)

    t = -w_scalar / d_scalar

    dot_intersec = [line1[0][X_DOT] + d[0] * t, line1[0][Y_DOT] + d[1] * t]

    return dot_intersec


def sutherland_hodgman_algorythm(cutter_line, position, prev_result):
    cur_result = []

    dot1 = cutter_line[0]
    dot2 = cutter_line[1]

    normal = get_normal(dot1, dot2, position)

    prev_vision = is_visible(prev_result[-2], dot1, dot2)

    for cur_dot_index in range(-1, len(prev_result)):
        cur_vision = is_visible(prev_result[cur_dot_index], dot1, dot2)

        if (prev_vision):
            if (cur_vision):
                cur_result.append(prev_result[cur_dot_index])
            else:
                figure_line = [prev_result[cur_dot_index - 1], prev_result[cur_dot_index]]

                cur_result.append(get_lines_parametric_intersec(figure_line, cutter_line, normal))
        else:
            if (cur_vision):
                figure_line = [prev_result[cur_dot_index - 1], prev_result[cur_dot_index]]

                cur_result.append(get_lines_parametric_intersec(figure_line, cutter_line, normal))

                cur_result.append(prev_result[cur_dot_index])

        prev_vision = cur_vision

    return cur_result


# TODO

def cut_area():

    if (not is_maked(cutter)):
        messagebox.showinfo("Ошибка", "Отсекатель не замкнут")
        return

    if (not is_maked(figure)):
        messagebox.showinfo("Ошибка", "Отекаемый многоугольник не замкнут")
        return

    if (extra_check(figure)):
        messagebox.showinfo("Ошибка", "Отекаемое должно быть многоугольником")
        return

    if (len(cutter) < 3):
        messagebox.showinfo("Ошибка", "Не задан отсекатель")
        return

    if (not check_polygon()):
        messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником")
        return

    result = copy.deepcopy(figure)

    for cur_dot_ind in range(-1, len(cutter) - 1):
        line = [cutter[cur_dot_ind], cutter[cur_dot_ind + 1]]

        position_dot = cutter[cur_dot_ind + 1]

        result = sutherland_hodgman_algorythm(line, position_dot, result)

        if (len(result) <= 2):
            return

    draw_result_figure(result)


def draw_result_figure(figure_dots):
    fixed_figure = remove_odd_sides(figure_dots)

    res_color = parse_color(option_color_line.get())

    for line in fixed_figure:
        canvas_win.create_line(line[0], line[1], fill = res_color)


# Odd sides
def make_unique(sides):

    for side in sides:
        side.sort()

    return list(filter(lambda x: (sides.count(x) % 2) == 1, sides))


def is_dot_in_side(dot, side):
    if abs(vector_mul(get_vector(dot, side[0]), get_vector(side[1], side[0]))) <= 1e-6:
        if (side[0] < dot < side[1] or side[1] < dot < side[0]):
            return True
    return False


def get_sides(side, rest_dots):
    dots_list = [side[0], side[1]]

    for dot in rest_dots:
        if is_dot_in_side(dot, side):
            dots_list.append(dot)

    dots_list.sort()

    sections_list = list()

    for i in range(len(dots_list) - 1):
        sections_list.append([dots_list[i], dots_list[i + 1]])

    return sections_list


def remove_odd_sides(figure_dots):
    all_sides = list()
    rest_dots = figure_dots[2:]

    for i in range(len(figure_dots)):
        cur_side = [figure_dots[i], figure_dots[(i + 1) % len(figure_dots)]]

        all_sides.extend(get_sides(cur_side, rest_dots))

        rest_dots.pop(0)
        rest_dots.append(figure_dots[i])

    return make_unique(all_sides)



def add_paral_line_cutter(event):
    print("Pressed: Space", event.x, event.y)

    if (len(cutter) < 1):
        return

    dif_x = abs(event.x - cutter[len(cutter) - 1][X_DOT])
    dif_y = abs(event.y - cutter[len(cutter) - 1][Y_DOT])

    if (dif_x > dif_y):
        add_dot_cutter(event.x, cutter[len(cutter) - 1][Y_DOT])
    else:
        add_dot_cutter(cutter[len(cutter) - 1][X_DOT], event.y)


def add_paral_line_figure(event):
    print("Pressed: Control_L", event.x, event.y)

    if (len(figure) < 1):
        return

    dif_x = abs(event.x - figure[len(figure) - 1][X_DOT])
    dif_y = abs(event.y - figure[len(figure) - 1][Y_DOT])

    if (dif_x > dif_y):
        add_dot_figure(event.x, figure[len(figure) - 1][Y_DOT])
    else:
        add_dot_figure(figure[len(figure) - 1][X_DOT], event.y)




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

    cutter = []
    figure = []

    lines = []

    canvas_win.bind("<1>", add_dot_cutter_click)
    canvas_win.bind("<3>", add_dot_figure_click)

    canvas_win.bind('<space>', add_paral_line_cutter)
    canvas_win.bind('<Control_L>', add_paral_line_figure)

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
