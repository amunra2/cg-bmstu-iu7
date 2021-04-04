from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, Radiobutton, LEFT, RIGHT, IntVar
from tkinter import messagebox
from math import sqrt, acos, degrees, pi, sin, cos, radians, floor, fabs
import copy
import numpy as np
import matplotlib.pyplot as plt

import time

import colorutils as cu


WIN_WIDTH = 1600
WIN_HEIGHT = 900
WIN_COLOR = "#80b3ff"

CV_WIDE = 900
CV_HEIGHT = 900
CV_COLOR = "#ffffff" 
MAIN_TEXT_COLOR = "#4d4dff" 
BTN_TEXT_COLOR = "#4d94ff"

BOX_COLOR = "#8080ff"
BOX_WIDTH = 50




def check_option(option):
    messagebox.showinfo("Выбран", "Выбрана опция %d" %(option))



# Methods

def parse_color(option_color):

    print("Color = ", option_color)

    color = cu.Color((0, 0, 0)) # "black"

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







def clear_canvas():
    canvas_win.delete("all")



def lib_method(p1, p2, color):
    canvas_win.create_line(p1[0], p1[1], p2[0], p2[1], fill = color.hex)
    

        

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









def choose_color(color, intens):
    return color + (intens, intens, intens)



def change_figure(opt_figure):

    if (opt_figure == 1):
        rad_a_elips_text.place_forget()
        rad_a_elips_entry.place_forget()

        rad_b_elips_text.place_forget()
        rad_b_elips_entry.place_forget()

        rad_circle_text.place(x = CV_WIDE + 250, y = 445)

        rad_circle_entry.place(x = CV_WIDE + 310, y = 445)

    else:
        rad_circle_text.place_forget()
        rad_circle_entry.place_forget()

        rad_a_elips_text.place(x = CV_WIDE + 70, y = 445)

        rad_a_elips_entry.place(x = CV_WIDE + 130, y = 445)

        rad_b_elips_text.place(x = CV_WIDE + 430, y = 445)

        rad_b_elips_entry.place(x = CV_WIDE + 490, y = 445)



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
    win.title("Лабораторная работа #4 (Цветков И.А. ИУ7-43Б)")
    win.resizable(False, False)

    canvas_win = Canvas(win, width = CV_WIDE, height = CV_HEIGHT, bg = CV_COLOR)
    canvas_win.place(x = 0, y = 0)


    # Method

    back_box_method = Label(text = "", font="-family {Consolas} -size 16", width = BOX_WIDTH, height = 5, bg = BOX_COLOR)
    back_box_method.place(x = CV_WIDE + 20, y = 20)

    method_text = Label(win, text = "Алгоритм построения окружности", width = BOX_WIDTH, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    method_text.place(x = CV_WIDE + 20, y = 20)

    option = IntVar()
    option.set(1)

    method_kanon = Radiobutton(text = "Каноническое уравнение", font="-family {Consolas} -size 14", variable = option, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_kanon.place(x = CV_WIDE + 25, y = 55)

    method_param = Radiobutton(text = "Параметрическое уравнение", font="-family {Consolas} -size 14", variable = option, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_param.place(x = CV_WIDE + 350, y = 55)

    method_brsenhem = Radiobutton(text = "Алгоритм Брезенхем", font="-family {Consolas} -size 14", variable = option, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_brsenhem.place(x = CV_WIDE + 25, y = 90)

    method_mid_dot = Radiobutton(text = "Алгоритм средней точки", font="-family {Consolas} -size 14", variable = option, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_mid_dot.place(x = CV_WIDE + 350, y = 90)

    method_lib = Radiobutton(text = "Библиотечный", font="-family {Consolas} -size 14", variable = option, value = 5, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_lib.place(x = CV_WIDE + 230, y = 125)



    # Color

    back_box_color = Label(text = "", font="-family {Consolas} -size 16", width = BOX_WIDTH, height = 4, bg = BOX_COLOR)
    back_box_color.place(x = CV_WIDE + 20, y = 160)

    color_text = Label(win, text = "Цвет окружности", width = BOX_WIDTH, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 160)


    option_color = IntVar()
    option_color.set(1)

    color_line_black = Radiobutton(text = "Черный", font="-family {Consolas} -size 14", variable = option_color, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_black.place(x = CV_WIDE + 25, y = 195)

    color_line_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_blue.place(x = CV_WIDE + 25, y = 230)


    color_line_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_red.place(x = CV_WIDE + 400, y = 195)

    color_line_background = Radiobutton(text = "Фоновый", font="-family {Consolas} -size 14", variable = option_color, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_background.place(x = CV_WIDE + 400, y = 230)


    # Choose figure

    back_box_figure = Label(text = "", font="-family {Consolas} -size 16", width = BOX_WIDTH, height = 3, bg = BOX_COLOR)
    back_box_figure.place(x = CV_WIDE + 20, y = 280)

    color_text = Label(win, text = "Выбрать фигуру", width = BOX_WIDTH, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 280)

    option_figure = IntVar()
    option_figure.set(1)

    figure_circle = Radiobutton(text = "Окружность", font="-family {Consolas} -size 14", variable = option_figure, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR, command = lambda: change_figure(option_figure.get()))
    figure_circle.place(x = CV_WIDE + 25, y = 315)

    figure_elips = Radiobutton(text = "Элипс", font="-family {Consolas} -size 14", variable = option_figure, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR, command = lambda: change_figure(option_figure.get()))
    figure_elips.place(x = CV_WIDE + 400, y = 315)


    # Line
    back_box_line = Label(text = "", font="-family {Consolas} -size 16", width = BOX_WIDTH, height = 6, bg = BOX_COLOR)
    back_box_line.place(x = CV_WIDE + 20, y = 370)

    line_text = Label(win, text = "Нарисовать фигуру", width = BOX_WIDTH, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    line_text.place(x = CV_WIDE + 20, y = 370)

    # Figure center
    xc_fig_text = Label(text = "x_с: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    xc_fig_text.place(x = CV_WIDE + 70, y = 405)

    xc_fig_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    xc_fig_entry.place(x = CV_WIDE + 130, y = 405)

    yc_fig_text = Label(text = "y_с: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    yc_fig_text.place(x = CV_WIDE + 430, y = 405)

    yc_fig_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    yc_fig_entry.place(x = CV_WIDE + 490, y = 405)


    # Radius

    rad_circle_text = Label(text = "R: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)

    rad_circle_entry = Entry(font="-family {Consolas} -size 14", width = 9)


    rad_a_elips_text = Label(text = "R_a: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    
    rad_a_elips_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    
    rad_b_elips_text = Label(text = "R_b: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    
    rad_b_elips_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    
    change_figure(1) # set circle


    draw_circle_btn = Button(win, text = "Нарисовать", font="-family {Consolas} -size 14", command = lambda: parse_line(option.get(), option_color.get()), width = 20, bg = BTN_TEXT_COLOR)
    draw_circle_btn.place(x = CV_WIDE + 210, y = 490)


    # Spektr
    back_box_spektr = Label(text = "", font="-family {Consolas} -size 16", width = BOX_WIDTH, height = 5, bg = BOX_COLOR)
    back_box_spektr.place(x = CV_WIDE + 20, y = 550)

    spektr_text = Label(win, text = "Нарисовать спектр", width = BOX_WIDTH, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    spektr_text.place(x = CV_WIDE + 20, y = 550)


    # Data
    rad_step_text = Label(text = "Шаг: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    rad_step_text.place(x = CV_WIDE + 70, y = 590)

    rad_step_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    rad_step_entry.place(x = CV_WIDE + 130, y = 590)

    amount_text = Label(text = "Количество: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    amount_text.place(x = CV_WIDE + 340, y = 590)

    amount_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    amount_entry.place(x = CV_WIDE + 480, y = 590)

    draw_spektr_btn = Button(win, text = "Нарисовать", font="-family {Consolas} -size 14", command = lambda: parse_spektr(option.get(), option_color.get()), width = 20, bg = BTN_TEXT_COLOR)
    draw_spektr_btn.place(x = CV_WIDE + 210, y = 640)


    # Control buttons

    compare_time_btn = Button(win, text = "Сравнить время", font="-family {Consolas} -size 15", command = lambda: time_measure(), width = 20, height = 2,  bg = BTN_TEXT_COLOR)
    compare_time_btn.place(x = CV_WIDE + 30, y = 770)


    clear_win_btn = Button(win, text = "Очистить экран", font="-family {Consolas} -size 15", command = lambda: clear_canvas(), width = 20, height = 2, bg = BTN_TEXT_COLOR)
    clear_win_btn.place(x = CV_WIDE + 400, y = 770)

    # Insert # TODO


    win.mainloop()