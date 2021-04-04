from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, Radiobutton, LEFT, RIGHT, IntVar
from tkinter import messagebox
from math import sqrt, acos, degrees, pi, sin, cos, radians, floor, fabs
import copy
import numpy as np
import matplotlib.pyplot as plt
import time
import colorutils as cu

from bresenham_method import bresenham_circle, bresenham_ellipse


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


def parse_spektr(option, option_color, option_figure):
    try:
        rad_step = float(rad_step_entry.get())
        amount = int(amount_entry.get())

        if (option_figure == 1):
            r_a = int(rad_circle_entry.get())
            r_b = r_a
        else:
            r_a = int(rad_a_ellips_entry.get())
            r_b = int(rad_b_ellips_entry.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
        return

    if (rad_step <= 0):
        messagebox.showerror("Ошибка", "Шаг радиуса должен быть выше нуля")
        return

    if (amount <= 0):
        messagebox.showerror("Ошибка", "Количество должно быть больше нуля")
        return

    dot_c = [CV_WIDE // 2, CV_HEIGHT // 2]

    index = 0

    while (index < amount):
        rad = [r_a, r_b]

        parse_methods(dot_c, rad, option, option_color, option_figure)

        r_a += rad_step
        r_b += rad_step
        
        index += 1


def parse_figure(option, option_color, option_figure):
    try:
        x_c = float(xc_fig_entry.get())
        y_c = int(yc_fig_entry.get())

        if (option_figure == 1):
            r_a = int(rad_circle_entry.get())
            r_b = r_a
        else:
            r_a = int(rad_a_ellips_entry.get())
            r_b = int(rad_b_ellips_entry.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
        return

    dot_c = [x_c, y_c]
    rad = [r_a, r_b]

    parse_methods(dot_c, rad, option, option_color, option_figure)



def parse_methods(dot_c, rad, option, option_color, option_figure, draw = True):

    print("Method = ", option)

    color = parse_color(option_color)

    if (option == 1): # kanon
        check_option(option)
        
        # if draw:
        #     draw_line(dots)

    elif (option == 2): # param
        check_option(option)

        # if draw:
        #     draw_line(dots)

    elif (option == 3): # bres
        if (option_figure == 1):
            dots = bresenham_circle(dot_c, rad[0], color)
        elif (option_figure == 2):
            dots = bresenham_ellipse(dot_c, rad, color)
        
        if draw:
            draw_line(dots)

    elif (option == 4): # mid point
        check_option(option)
        
        # if draw:
        #     draw_line(dots)

    elif (option == 5):
        lib_method(dot_c, rad, color)
    else:
        messagebox.showerror("Ошибка", "Неизвестный алгоритм")


def clear_canvas():
    canvas_win.delete("all")



def lib_method(dot_c, rad, color):
    canvas_win.create_oval(dot_c[0] - rad[0], dot_c[1] - rad[1], dot_c[0] + rad[0], dot_c[1] + rad[1], outline = color.hex) 
    

        

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
        rad_a_ellips_text.place_forget()
        rad_a_ellips_entry.place_forget()

        rad_b_ellips_text.place_forget()
        rad_b_ellips_entry.place_forget()

        rad_circle_text.place(x = CV_WIDE + 250, y = 445)

        rad_circle_entry.place(x = CV_WIDE + 310, y = 445)

    else:
        rad_circle_text.place_forget()
        rad_circle_entry.place_forget()

        rad_a_ellips_text.place(x = CV_WIDE + 100, y = 445)

        rad_a_ellips_entry.place(x = CV_WIDE + 160, y = 445)

        rad_b_ellips_text.place(x = CV_WIDE + 400, y = 445)

        rad_b_ellips_entry.place(x = CV_WIDE + 460, y = 445)



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

    figure_ellips = Radiobutton(text = "Эллипс", font="-family {Consolas} -size 14", variable = option_figure, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR, command = lambda: change_figure(option_figure.get()))
    figure_ellips.place(x = CV_WIDE + 400, y = 315)


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


    rad_a_ellips_text = Label(text = "R_a: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    
    rad_a_ellips_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    
    rad_b_ellips_text = Label(text = "R_b: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    
    rad_b_ellips_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    
    change_figure(1) # set circle


    draw_circle_btn = Button(win, text = "Нарисовать", font="-family {Consolas} -size 14", command = lambda: parse_figure(option.get(), option_color.get(), option_figure.get()), width = 20, bg = BTN_TEXT_COLOR)
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

    draw_spektr_btn = Button(win, text = "Нарисовать", font="-family {Consolas} -size 14", command = lambda: parse_spektr(option.get(), option_color.get(), option_figure.get()), width = 20, bg = BTN_TEXT_COLOR)
    draw_spektr_btn.place(x = CV_WIDE + 210, y = 640)


    # Control buttons

    compare_time_btn = Button(win, text = "Сравнить время", font="-family {Consolas} -size 15", command = lambda: time_measure(), width = 20, height = 2,  bg = BTN_TEXT_COLOR)
    compare_time_btn.place(x = CV_WIDE + 30, y = 770)


    clear_win_btn = Button(win, text = "Очистить экран", font="-family {Consolas} -size 15", command = lambda: clear_canvas(), width = 20, height = 2, bg = BTN_TEXT_COLOR)
    clear_win_btn.place(x = CV_WIDE + 400, y = 770)

    # Insert # TODO

    xc_fig_entry.insert(END, "450")
    yc_fig_entry.insert(END, "450")

    rad_a_ellips_entry.insert(END, "10")
    rad_b_ellips_entry.insert(END, "50")

    rad_circle_entry.insert(END, "30")

    amount_entry.insert(END, "50")
    rad_step_entry.insert(END, "5")

    win.mainloop()