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
    global rect

    canvas_win.delete("all")

    lines = [[]]
    rect = [-1, -1, -1, -1]


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


def add_rect_click1(event):
    global is_set_rect

    is_set_rect = False


def add_rect_click(event):
    global rect
    global is_set_rect

    cutter_color = parse_color(option_color_cutter.get())

    if (is_set_rect == False):
        rect[X_MIN] = event.x
        rect[Y_MAX] = event.y

        is_set_rect = True
    else:
        x_first = rect[X_MIN]
        y_first = rect[Y_MAX]

        x = event.x
        y = event.y

        #canvas_win.create_rectangle(x_first, y_first, x_old, y_old, outline = "white")
        canvas_win.delete("all")
        canvas_win.create_rectangle(x_first, y_first, x, y, outline = cutter_color)

        rect[X_MAX] = x
        rect[Y_MIN] = y

        draw_lines()

    
def add_rect():
    global rect

    try:
        x_min = int(xleft_cutter_entry.get())
        y_max = int(yleft_cutter_entry.get())
        x_max = int(xright_cutter_entry.get())
        y_min = int(yright_cutter_entry.get())
    except:
        messagebox.showinfo("Ошибка", "Неверно введены координаты")
        return

    cutter_color = parse_color(option_color_cutter.get())

    canvas_win.delete("all")
    canvas_win.create_rectangle(x_min, y_max, x_max, y_min, outline = cutter_color)

    rect = [x_min, x_max, y_min, y_max]

    draw_lines()


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


def add_vert_horiz_lines():
    global lines
    global rect

    if (rect[0] == -1):
        messagebox.showerror("Ошибка", "Отсекатель не задан")
        return

    line_color = parse_color(option_color_line.get())

    x1 = rect[X_MIN]
    y1 = rect[Y_MAX]
    x2 = rect[X_MAX]
    y2 = rect[Y_MIN]

    dy = y2 - y1
    dx = x2 - x1

    lines.append([[x1, y1 + 0.1 * dy], [x1, y2 - 0.1 * dy], line_color]) # vertical line on cutter
    lines.append([[x1 + 0.1 * dx, y1], [x2 - 0.1 * dx, y1], line_color]) # horizontal line on cutter

    canvas_win.create_line(x1, y1 + 0.1 * dy, x1, y2 - 0.1 * dy, fill = line_color)
    canvas_win.create_line(x1 + 0.1 * dx, y1, x2 - 0.1 * dx, y1, fill = line_color)

    lines.append(list())


def add_line_click(event):

    line_color = parse_color(option_color_line.get())
    
    x = event.x
    y = event.y

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


def add_line():
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

def get_dot_bits(rect, dot):
    bits = 0b0000

    #print(rect, dot)

    if (dot[X_DOT] < rect[X_MIN]):
        bits += 0b0001

    if (dot[X_DOT] > rect[X_MAX]):
        bits += 0b0010
    
    if (dot[Y_DOT] > rect[Y_MIN]): # из-за экранной системы координат поменены
        bits += 0b0100
        
    if (dot[Y_DOT] < rect[Y_MAX]): # из-за экранной системы координат поменены
        bits += 0b1000

    return bits


def check_visible(dot1_bits, dot2_bits):

    vision = 0 # частично видимый

    if (dot1_bits == 0 and dot2_bits == 0):
        vision = 1 # видим
    elif (dot1_bits & dot2_bits):
        vision = -1 # не видим

    return vision


def get_bit(dot_bits, i):
    return (dot_bits >> i) & 1


def are_bits_equal(dot1_bits, dot2_bits, i):

    if get_bit(dot1_bits, i) == get_bit(dot2_bits, i):
        return True

    return False


def method_sazerland_kohen(rect, line):
    dot1 = [line[0][X_DOT], line[0][Y_DOT]]
    dot2 = [line[1][X_DOT], line[1][Y_DOT]]

    fl = 0

    if (dot1[X_DOT] == dot2[X_DOT]):
        fl = -1 # вертикальный
    else:
        m = (dot2[Y_DOT] - dot1[Y_DOT]) / (dot2[X_DOT] - dot1[X_DOT])

        if (m == 0):
            fl = 1 # горизонтальный

    for i in range(4):
        dot1_bits = get_dot_bits(rect, dot1)
        dot2_bits = get_dot_bits(rect, dot2)

        vision = check_visible(dot1_bits, dot2_bits)

        if (vision == -1):
            return # выйти и не рисовать
        elif (vision == 1):
            break # нарисовать и выйти

        if (are_bits_equal(dot1_bits, dot2_bits, i)):
            continue

        if get_bit(dot1_bits, i) == 0:
            tmp = dot1
            dot1 = dot2
            dot2 = tmp

        if (fl != -1):
            if (i < 2):
                dot1[Y_DOT] = m * (rect[i] - dot1[X_DOT]) + dot1[Y_DOT]
                dot1[X_DOT] = rect[i]
                continue
            else:
                dot1[X_DOT] = (1 / m) * (rect[i] - dot1[Y_DOT]) + dot1[X_DOT]

        dot1[Y_DOT] = rect[i]

    res_color = parse_color(option_color_cut_line.get())

    canvas_win.create_line(dot1[X_DOT], dot1[Y_DOT], dot2[X_DOT], dot2[Y_DOT], fill = res_color)
            

def cut_area():
    global rect

    if (rect[0] == -1):
        messagebox.showinfo("Ошибка", "Не задан отсекатель")

    rect = [min(rect[0], rect[1]), max(rect[0], rect[1]), max(rect[2], rect[3]), min(rect[2], rect[3])]

    canvas_win.create_rectangle(rect[X_MIN] + 1, rect[Y_MAX] + 1, rect[X_MAX] - 1, rect[Y_MIN] - 1, fill = "white", outline = "white")
    
    for line in lines:
        if (line):
            method_sazerland_kohen(rect, line)




if __name__ == "__main__":
    '''
        Основной графический модуль
    '''

    win = Tk()
    win['bg'] = WIN_COLOR
    win.geometry("%dx%d" %(WIN_WIDTH, WIN_HEIGHT))
    win.title("Лабораторная работа #7 (Цветков И.А. ИУ7-43Б)")
    win.resizable(False, False)

    canvas_win = Canvas(win, width = CV_WIDE, height = CV_HEIGHT, bg = CV_COLOR)
    canvas_win.place(x = 0, y = 0)

    # Binds

    lines = [[]]
    canvas_win.bind("<3>", add_line_click)

    rect = [-1, -1, -1, -1]
    canvas_win.bind("<1>", add_rect_click1)
    canvas_win.bind('<B1-Motion>', add_rect_click)
    
    canvas_win.bind('LeftCtrl', add_vert_horiz_lines)

    # Add cutter

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 6, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 10)

    cutter_text = Label(win, text = "Координаты отсекателя", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    cutter_text.place(x = CV_WIDE + 20, y = 10)

    xleft_cutter_text = Label(text = "Левый верхний  x: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    xleft_cutter_text.place(x = CV_WIDE + 20, y = 50)

    xleft_cutter_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    xleft_cutter_entry.place(x = CV_WIDE + 210, y = 50)

    yleft_cutter_text = Label(text = "y: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    yleft_cutter_text.place(x = CV_WIDE + 360, y = 50)

    yleft_cutter_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    yleft_cutter_entry.place(x = CV_WIDE + 390, y = 50)


    xright_cutter_text = Label(text = "Правый нижний  x: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    xright_cutter_text.place(x = CV_WIDE + 20, y = 90)

    xright_cutter_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    xright_cutter_entry.place(x = CV_WIDE + 210, y = 90)

    yright_cutter_text = Label(text = "y: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    yright_cutter_text.place(x = CV_WIDE + 360, y = 90)

    yright_cutter_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    yright_cutter_entry.place(x = CV_WIDE + 390, y = 90)


    add_cutter_btn = Button(win, text = "Нарисовать отсекатель", font="-family {Consolas} -size 14", command = lambda: add_rect())
    add_cutter_btn.place(x = CV_WIDE + 170, y = 130)


    # Add line

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 6, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 190)

    cutter_text = Label(win, text = "Добавить отрезок", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    cutter_text.place(x = CV_WIDE + 20, y = 190)


    x_start_line_text = Label(text = "Начало x: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x_start_line_text.place(x = CV_WIDE + 20, y = 230)

    x_start_line_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    x_start_line_entry.place(x = CV_WIDE + 130, y = 230)

    y_start_line_text = Label(text = "y: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    y_start_line_text.place(x = CV_WIDE + 360, y = 230)

    y_start_line_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    y_start_line_entry.place(x = CV_WIDE + 390, y = 230)


    x_end_line_text = Label(text = "Конец  x: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x_end_line_text.place(x = CV_WIDE + 20, y = 270)

    x_end_line_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    x_end_line_entry.place(x = CV_WIDE + 130, y = 270)

    y_end_line_text = Label(text = "y: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    y_end_line_text.place(x = CV_WIDE + 360, y = 270)

    y_end_line_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    y_end_line_entry.place(x = CV_WIDE + 390, y = 270)


    add_line_btn = Button(win, text = "Нарисовать отрезок", font="-family {Consolas} -size 14", command = lambda: add_line())
    add_line_btn.place(x = CV_WIDE + 190, y = 305)


    # TODO Choose cutter color 

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 4, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 375)

    color_text = Label(win, text = "Выбрать цвет отсекателя", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 375)

    option_color_cutter = IntVar()
    option_color_cutter.set(1)

    color_cutter_orange = Radiobutton(text = "Оранжевый", font="-family {Consolas} -size 14", variable = option_color_cutter, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cutter_orange.place(x = CV_WIDE + 25, y = 405)

    color_cutter_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color_cutter, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cutter_red.place(x = CV_WIDE + 400, y = 405)

    color_cutter_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color_cutter, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cutter_blue.place(x = CV_WIDE + 25, y = 445)

    color_cutter_green = Radiobutton(text = "Зеленый", font="-family {Consolas} -size 14", variable = option_color_cutter, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cutter_green.place(x = CV_WIDE + 400, y = 445)


    # TODO Choose line color 

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 4, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 495)

    color_text = Label(win, text = "Выбрать цвет отрезка", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 495)

    option_color_line = IntVar()
    option_color_line.set(3)

    color_line_orange = Radiobutton(text = "Оранжевый", font="-family {Consolas} -size 14", variable = option_color_line, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_orange.place(x = CV_WIDE + 25, y = 535)

    color_line_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color_line, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_red.place(x = CV_WIDE + 400, y = 535)

    color_line_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color_line, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_blue.place(x = CV_WIDE + 25, y = 565)

    color_line_green = Radiobutton(text = "Зеленый", font="-family {Consolas} -size 14", variable = option_color_line, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_green.place(x = CV_WIDE + 400, y = 565)


    # TODO Choose cut line color 

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 4, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 615)

    color_text = Label(win, text = "Выбрать цвет результата", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 615)

    option_color_cut_line = IntVar()
    option_color_cut_line.set(4)

    color_cut_line_orange = Radiobutton(text = "Оранжевый", font="-family {Consolas} -size 14", variable = option_color_cut_line, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cut_line_orange.place(x = CV_WIDE + 25, y = 655)

    color_cut_line_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color_cut_line, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cut_line_red.place(x = CV_WIDE + 400, y = 655)

    color_cut_line_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color_cut_line, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cut_line_blue.place(x = CV_WIDE + 25, y = 685)

    color_cut_line_green = Radiobutton(text = "Зеленый", font="-family {Consolas} -size 14", variable = option_color_cut_line, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_cut_line_green.place(x = CV_WIDE + 400, y = 685)


    add_vert_horiz_lines_btn = Button(win, text = "Добавить вертикальный и\nгоризонтальный отрезки", width = 35, height = 2, font="-family {Consolas} -size 14", command = lambda: add_vert_horiz_lines())
    add_vert_horiz_lines_btn.place(x = CV_WIDE + 100, y = 750)

    cut_btn = Button(win, text = "Отсечь", width = 18, height = 2, font="-family {Consolas} -size 14", command = lambda: cut_area())
    cut_btn.place(x = CV_WIDE + 20, y = 830)

    clear_btn = Button(win, text = "Очистить экран", width = 18, height = 2, font="-family {Consolas} -size 14", command = lambda: reboot_prog())
    clear_btn.place(x = CV_WIDE + 350, y = 830)



    win.mainloop()