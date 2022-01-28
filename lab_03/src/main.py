from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, Radiobutton, LEFT, RIGHT, IntVar
from tkinter import messagebox
from math import sqrt, acos, degrees, pi, sin, cos, radians, floor, fabs
import copy
import numpy as np
import matplotlib.pyplot as plt

import time

import colorutils as cu


WIN_WIDTH = 1500
WIN_HEIGHT = 900
WIN_COLOR = "#bf80ff"

CV_WIDE = 900
CV_HEIGHT = 900
CV_COLOR = "#ffffff" #f3e6ff" #"#cce6ff"
MAIN_TEXT_COLOR = "#b566ff" #"lightblue" a94dff
TEXT_COLOR = "#ce99ff"

BOX_COLOR = "#dab3ff"




def check_option(option):
    messagebox.showinfo("Выбран", "Выбрана опция %d" %(option))



# Methods

def parse_color(option_color):

    print("Color = ", option_color)

    color = "black" # None

    if (option_color == 1):
        color = cu.Color((0, 0, 0)) # "black"
    elif (option_color == 2):
        color = cu.Color((255, 0, 0)) # "red"
    elif (option_color == 3):
        color = cu.Color((0, 0, 255)) # "blue"
    elif (option_color == 4):
        color = cu.Color((255, 255, 255)) # СV_COLOR

    return color


def parse_spektr(option, option_color):
    try:
        line_len = float(len_line.get())
        angle_spin = float(angle.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
        return

    if (line_len <= 0):
        messagebox.showerror("Ошибка", "Длина линии должна быть выше нуля")
        return

    if (angle_spin <= 0):
        messagebox.showerror("Ошибка", "Угол должен быть больше нуля")
        return


    p1 = [CV_WIDE // 2, CV_HEIGHT // 2]

    spin = 0

    while (spin <= 2 * pi):
        x2 = CV_WIDE // 2 + cos(spin) * line_len
        y2 = CV_HEIGHT // 2 + sin(spin) * line_len

        p2 = [x2, y2]

        parse_methods(p1, p2, option, option_color)

        spin += radians(angle_spin)
    

def parse_line(option, option_color):
    try:
        x1 = int(x1_line.get())
        y1 = int(y1_line.get())
        x2 = int(x2_line.get())
        y2 = int(y2_line.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
        return

    p1 = [x1, y1]
    p2 = [x2, y2]

    parse_methods(p1, p2, option, option_color)


def parse_methods(p1, p2, option, option_color, draw = True):

    print("Method = ", option)

    color = parse_color(option_color)

    if (option == 1):
        dots = cda_method(p1, p2, color)
        
        if draw:
            draw_line(dots)

    elif (option == 2):
        dots = bresenham_int(p1, p2, color)

        if draw:
            draw_line(dots)

    elif (option == 3):
        dots = bresenham_float(p1, p2, color)
        
        if draw:
            draw_line(dots)

    elif (option == 4):
        dots = wu(p1, p2, color)
        
        if draw:
            draw_line(dots)

    elif (option == 5):
        dots = bresenham_smooth(p1, p2, color)
        
        if draw:
            draw_line(dots)

    elif (option == 6):
        lib_method(p1, p2, color)
    else:
        messagebox.showerror("Ошибка", "Неизвестный алгоритм")


def wu(p1, p2, color, step_count = False):

    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    if (x2 - x1 == 0) and (y2 - y1 == 0):
        return [[x1, y1, color]]


    dx = x2 - x1
    dy = y2 - y1

    m = 1
    step = 1
    intens = 255

    dots = []

    steps = 0

    if (fabs(dy) > fabs(dx)):
        if (dy != 0):
            m = dx / dy
        m1 = m

        if (y1 > y2):
            m1 *= -1
            step *= -1

        y_end = round(y2) - 1 if (dy < dx) else (round(y2) + 1)

        for y_cur in range(round(y1), y_end, step):
            d1 = x1 - floor(x1)
            d2 = 1 - d1

            dot1 = [int(x1) + 1, y_cur, choose_color(color, round(fabs(d2) * intens))]

            dot2 = [int(x1), y_cur, choose_color(color, round(fabs(d1) * intens))]

            if step_count and y_cur < y2:
                if (int(x1) != int(x1 + m)):
                    steps += 1

            dots.append(dot1)
            dots.append(dot2)

            x1 += m1
    
    else:
        if (dx != 0):
            m = dy / dx

        m1 = m

        if (x1 > x2):
            step *= -1
            m1 *= -1

        x_end = round(x2) - 1 if (dy > dx) else (round(x2) + 1)

        for x_cur in range(round(x1), x_end, step):
            d1 = y1 - floor(y1)
            d2 = 1 - d1

            dot1 = [x_cur, int(y1) + 1, choose_color(color, round(fabs(d2) * intens))]

            dot2 = [x_cur, int(y1), choose_color(color, round(fabs(d1) * intens))]

            if step_count and x_cur < x2:
                if (int(y1) != int(y1 + m)):
                    steps += 1

            dots.append(dot1)
            dots.append(dot2)

            y1 += m1

    if step_count:
        return steps
    else:
        return dots




def clear_canvas():
    canvas_win.delete("all")



def lib_method(p1, p2, color):
    canvas_win.create_line(p1[0], p1[1], p2[0], p2[1], fill = color.hex)
    
    
def cda_method(p1, p2, color, step_count = False):

    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    if (x2 - x1 == 0) and (y2 - y1 == 0):
        return [[x1, y1, color]]

    dx = x2 - x1
    dy = y2 - y1

    if (abs(dx) >= abs(dy)):
        l = abs(dx)
    else:
        l = abs(dy)

    dx /= l
    dy /= l

    x = round(x1)
    y = round(y1)

    dots = [[round(x), round(y), color]]

    i = 1

    steps = 0

    while (i < l):

        x += dx
        y += dy

        dot = [round(x), round(y), color]

        dots.append(dot)

        if step_count:
            if not((round(x + dx) == round(x) and 
                        round(y + dy) != round(y)) or 
                        (round(x + dx) != round(x) and 
                        round(y + dy) == round(y))):
                steps += 1

        i += 1

    if step_count:
        return steps
    else:
        return dots
        

def draw_line(dots):

    for dot in dots:
        canvas_win.create_line(dot[0], dot[1], dot[0] + 1, dot[1], fill = dot[2].hex)


def sign(difference):
    if (difference < 0):
        return -1
    elif (difference == 0):
        return 0
    else:
        return 1


def bresenham_float(p1, p2, color, step_count = False):
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

    m = dy / dx
    e = m - 0.5
    i = 1

    dots = []

    steps = 0

    while (i <= dx + 1):
        dot = [x, y, color]
        dots.append(dot)

        x_buf = x
        y_buf = y

        while (e >= 0):
            if (swaped):
                x = x + s1
            else:
                y = y + s2

            e = e - 1

        if (swaped):
            y = y + s2
        else:
            x = x + s1

        e = e + m

        if step_count:
            if not((x_buf == x and y_buf != y) or
                    (x_buf != x and y_buf == y)):
                steps += 1

        i += 1

    if step_count:
        return steps
    else:
        return dots


def bresenham_int(p1, p2, color, step_count = False):
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

    dots = []

    steps = 0

    while (i <= dx + 1):
        dot = [x, y, color]
        dots.append(dot)

        x_buf = x
        y_buf = y

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

        if step_count:
            if ((x_buf != x) and (y_buf != y)):
                steps += 1

        i += 1

    if step_count:
        return steps
    else:
        return dots


def choose_color(color, intens):
    return color + (intens, intens, intens)


def bresenham_smooth(p1, p2, color, step_count = False):
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

    intens = 255

    m = dy / dx
    e = intens / 2

    m *= intens
    w = intens - m

    dots = [[x, y, choose_color(color, round(e))]]

    i = 1

    steps = 0

    while (i <= dx):
        x_buf = x
        y_buf = y
        
        if (e < w):
            if (swaped):
                y += s2
            else:
                x += s1
            e += m
        else:
            x += s1
            y += s2

            e -= w

        dot = [x, y, choose_color(color, round(e))]

        dots.append(dot)

        if step_count:
            if not((x_buf == x and y_buf != y) or
                    (x_buf != x and y_buf == y)):
                steps += 1

        i += 1

    if step_count:
        return steps
    else:
        return dots


def time_measure():

    time_mes = []

    try:
        line_len = float(len_line.get())
        angle_spin = float(angle.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
        return

    if (line_len <= 0):
        messagebox.showerror("Ошибка", "Длина линии должна быть выше нуля")
        return

    if (angle_spin <= 0):
        messagebox.showerror("Ошибка", "Угол должен быть больше нуля")
        return


    for i in range(1, 7):
        res_time = 0

        for _ in range(20):
            time_start = 0
            time_end = 0

            p1 = [CV_WIDE // 2, CV_HEIGHT // 2]

            spin = 0

            while (spin <= 2 * pi):
                x2 = CV_WIDE // 2 + cos(spin) * line_len
                y2 = CV_HEIGHT // 2 + sin(spin) * line_len

                p2 = [x2, y2]
                
                time_start += time.time()
                parse_methods(p1, p2, i, 4, draw = False)
                time_end += time.time()

                spin += radians(angle_spin)

            res_time += (time_end - time_start)

            clear_canvas()


        time_mes.append(res_time / 20)


    plt.figure(figsize = (14, 6))

    plt.title("Замеры времени для различных методов")

    positions = np.arange(6)

    methods = ["ЦДА", "Брезенхем (float)", "Брезенхем (int)", "Ву", "Брезенхем (сглаживание)", "Библиотечная"]

    plt.xticks(positions, methods)
    plt.ylabel("Время")
    #time_mes[1] = 0.75 * time_mes[4]
    plt.bar(positions, time_mes, align = "center", alpha = 1)

    plt.show()

    print(time_mes)


def steps_measure():

    try:
        line_len = float(len_line.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
        return

    if (line_len <= 0):
        messagebox.showerror("Ошибка", "Длина линии должна быть выше нуля")
        return

    p1 = [CV_WIDE // 2, CV_HEIGHT // 2]

    spin = 0

    angle_spin = [i for i in range(0, 91, 2)]

    cda_steps = []
    wu_steps = []
    bres_int_steps = []
    bres_float_steps = []
    bres_smooth_steps = []

    while (spin <= pi / 2 + 0.01):
        x2 = CV_WIDE // 2 + cos(spin) * line_len
        y2 = CV_HEIGHT // 2 + sin(spin) * line_len

        p2 = [x2, y2]
        
        cda_steps.append(cda_method(p1, p2, (255, 255, 255), step_count = True))
        wu_steps.append(wu(p1, p2, (255, 255, 255), step_count = True))
        bres_int_steps.append(bresenham_int(p1, p2, (255, 255, 255), step_count = True))
        bres_float_steps.append(bresenham_float(p1, p2, (255, 255, 255), step_count = True))
        bres_smooth_steps.append(bresenham_smooth(p1, p2, (255, 255, 255), step_count = True))

        spin += radians(2)


    plt.figure(figsize = (15, 6))

    plt.title("Замеры ступенчатости для различных методов\n{0} - длина отрезка".format(line_len))

    plt.xlabel("Угол (в градусах)")
    plt.ylabel("Количество ступенек")

    plt.plot(angle_spin, cda_steps, label = "ЦДА")
    plt.plot(angle_spin, wu_steps, label = "Ву")
    plt.plot(angle_spin, bres_float_steps, "-.", label = "Брезенхем (float/int)")
    plt.plot(angle_spin, bres_smooth_steps, ":", label = "Брезенхем\n(сглаживание)")

    plt.xticks(np.arange(91, step = 5))

    plt.legend()

    plt.show()







if __name__ == "__main__":
    '''
        Основной графический модуль
    '''

    win = Tk()
    win['bg'] = WIN_COLOR
    win.geometry("%dx%d" %(WIN_WIDTH, WIN_HEIGHT))
    win.title("Лабораторная работа #3 (Цветков И.А. ИУ7-43Б)")
    win.resizable(False, False)

    canvas_win = Canvas(win, width = CV_WIDE, height = CV_HEIGHT, bg = CV_COLOR)
    canvas_win.place(x = 0, y = 0)


    # Method

    back_box_method = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 6, bg = BOX_COLOR)
    back_box_method.place(x = CV_WIDE + 20, y = 30)

    method_text = Label(win, text = "Алгоритм построения отрезка", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    method_text.place(x = CV_WIDE + 20, y = 30)

    option = IntVar()
    option.set(1)

    method_cda = Radiobutton(text = "ЦДА", font="-family {Consolas} -size 14", variable = option, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_cda.place(x = CV_WIDE + 400, y = 70)

    method_wu = Radiobutton(text = "Ву", font="-family {Consolas} -size 14", variable = option, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_wu.place(x = CV_WIDE + 400, y = 105)

    method_lib = Radiobutton(text = "Библиотечная", font="-family {Consolas} -size 14", variable = option, value = 6, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_lib.place(x = CV_WIDE + 400, y = 140)

    
    method_bresenhem_float = Radiobutton(text = "Брезенхем (float)", font="-family {Consolas} -size 14", variable = option, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_bresenhem_float.place(x = CV_WIDE + 25, y = 70)

    method_bresenhem_int = Radiobutton(text = "Брезенхем (int)", font="-family {Consolas} -size 14", variable = option, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_bresenhem_int.place(x = CV_WIDE + 25, y = 105)

    method_bresenhem_smooth = Radiobutton(text = "Брезенхем (сглаживание)", font="-family {Consolas} -size 14", variable = option, value = 5, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_bresenhem_smooth.place(x = CV_WIDE + 25, y = 140)

    # Color

    back_box_color = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 5, bg = BOX_COLOR)
    back_box_color.place(x = CV_WIDE + 20, y = 210)

    color_text = Label(win, text = "Цвет отрезка", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 210)


    option_color = IntVar()
    option_color.set(1)

    color_line_black = Radiobutton(text = "Черный", font="-family {Consolas} -size 14", variable = option_color, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_black.place(x = CV_WIDE + 25, y = 250)

    color_line_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_blue.place(x = CV_WIDE + 25, y = 285)


    color_line_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_red.place(x = CV_WIDE + 400, y = 250)

    color_line_background = Radiobutton(text = "Фоновый", font="-family {Consolas} -size 14", variable = option_color, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_background.place(x = CV_WIDE + 400, y = 285)


    # Line
    back_box_line = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 6, bg = BOX_COLOR)
    back_box_line.place(x = CV_WIDE + 20, y = 370)

    line_text = Label(win, text = "Нарисовать отрезок", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    line_text.place(x = CV_WIDE + 20, y = 370)

    # Point 1
    x1_line_text = Label(text = "x1: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x1_line_text.place(x = CV_WIDE + 70, y = 405)

    x1_line = Entry(font="-family {Consolas} -size 14", width = 9)
    x1_line.place(x = CV_WIDE + 130, y = 405)

    y1_line_text = Label(text = "y1: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    y1_line_text.place(x = CV_WIDE + 330, y = 405)

    y1_line = Entry(font="-family {Consolas} -size 14", width = 9)
    y1_line.place(x = CV_WIDE + 390, y = 405)


    # Point 2
    x2_line_text = Label(text = "x2: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x2_line_text.place(x = CV_WIDE + 70, y = 455)

    x2_line = Entry(font="-family {Consolas} -size 14", width = 9)
    x2_line.place(x = CV_WIDE + 130, y = 455)

    y2_line_text = Label(text = "y2: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    y2_line_text.place(x = CV_WIDE + 330, y = 455)

    y2_line = Entry(font="-family {Consolas} -size 14", width = 9)
    y2_line.place(x = CV_WIDE + 390, y = 455)


    draw_line_btn = Button(win, text = "Нарисовать", font="-family {Consolas} -size 14", command = lambda: parse_line(option.get(), option_color.get()), width = 15, bg = TEXT_COLOR)
    draw_line_btn.place(x = CV_WIDE + 210, y = 490)


    # Spektr
    back_box_spektr = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 5, bg = BOX_COLOR)
    back_box_spektr.place(x = CV_WIDE + 20, y = 550)

    line_text = Label(win, text = "Нарисовать спектр", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    line_text.place(x = CV_WIDE + 20, y = 550)

    # Data
    len_line_text = Label(text = "Длина отрезка: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    len_line_text.place(x = CV_WIDE + 30, y = 590)

    len_line = Entry(font="-family {Consolas} -size 14", width = 9)
    len_line.place(x = CV_WIDE + 190, y = 590)

    angle_text = Label(text = "Угол°: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    angle_text.place(x = CV_WIDE + 370, y = 590)

    angle = Entry(font="-family {Consolas} -size 14", width = 9)
    angle.place(x = CV_WIDE + 450, y = 590)


    draw_spektr_btn = Button(win, text = "Нарисовать", font="-family {Consolas} -size 14", command = lambda: parse_spektr(option.get(), option_color.get()), width = 15, bg = TEXT_COLOR)
    draw_spektr_btn.place(x = CV_WIDE + 210, y = 640)


    # Control buttons

    compare_time_btn = Button(win, text = "Сравнить\nвремя", font="-family {Consolas} -size 15", command = lambda: time_measure(), width = 15, height = 2,  bg = TEXT_COLOR)
    compare_time_btn.place(x = CV_WIDE + 70, y = 720)

    compare_steps_btn = Button(win, text = "Сравнить\nступенчатость", font="-family {Consolas} -size 15", command = lambda: steps_measure(), width = 15, height = 2, bg = TEXT_COLOR)
    compare_steps_btn.place(x = CV_WIDE + 330, y = 720)


    clear_win_btn = Button(win, text = "Очистить экран", font="-family {Consolas} -size 15", command = lambda: clear_canvas(), width = 25, height = 2, bg = TEXT_COLOR)
    clear_win_btn.place(x = CV_WIDE + 150, y = 800)

    # Insert

    len_line.insert(END, "350")
    angle.insert(END, "10")

    x1_line.insert(END, "150")
    y1_line.insert(END, "150")

    x2_line.insert(END, "500")
    y2_line.insert(END, "170")


    win.mainloop()