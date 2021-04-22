from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, Radiobutton, LEFT, RIGHT, IntVar, DISABLED, NORMAL
from tkinter import messagebox
from math import sqrt, acos, degrees, pi, sin, cos, radians, floor, fabs
import numpy as np
import matplotlib.pyplot as plt
import time
import colorutils as cu

from bresenham_method import bresenham_circle, bresenham_ellipse
from mid_dot_method import mid_dot_circle, mid_dot_ellipse
from canon_method import canon_circle, canon_ellips
from parametric_method import parametric_circle, parametric_ellips



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

NUMBER_OF_RUNS = 20
MAX_RADIUS = 10000
STEP = 1000



def check_option(option):
    messagebox.showinfo("Выбран", "Выбрана опция %d" %(option))


# Methods
def parse_color(option_color):

    #print("Color = ", option_color)

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


def parse_spektr_ellips(option, option_color, option_figure):
    try:
        rad_step = float(rad_step_elps_entry.get())
        amount = int(amount_elps_entry.get())

        r_a = float(rad_a_elps_entry.get())
        r_b = float(rad_b_elps_entry.get())
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

    koef = r_b / r_a


    while (index < amount):
        rad = [r_a, r_b]

        parse_methods(dot_c, rad, option, option_color, option_figure)

        r_a += rad_step
        r_b = (r_a * koef)
        
        index += 1

    
def parse_spektr_circle(option, option_color, option_figure, option_spektr_crcl):
    try:
        rad_step = float(rad_step_crcl_entry.get())
        amount = int(amount_crcl_entry.get())

        rad_begin = float(rad_begin_crcl_entry.get())
        rad_end = float(rad_end_crcl_entry.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
        return

    # Choose combination

    if (option_spektr_crcl == 1):
        rad_step = int((rad_end - rad_begin) / amount)
    elif (option_spektr_crcl == 2):
        amount = int((rad_end - rad_begin) / rad_step)
    elif (option_spektr_crcl == 3):
        rad_begin = float(rad_end - rad_step * amount)
    elif (option_spektr_crcl == 4):
        rad_end = float(rad_begin + rad_step * amount)

    if (rad_begin > rad_end):
        messagebox.showerror("Ошибка", "Начальный радиус не может быть больше конечного")
        return

    if (rad_step <= 0):
        messagebox.showerror("Ошибка", "Шаг радиуса должен быть выше нуля")
        return

    if (amount <= 0):
        messagebox.showerror("Ошибка", "Количество должно быть больше нуля")
        return



    r_a = rad_begin
    r_b = rad_begin

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


def choose_spektr(option, option_color, option_figure, option_spektr_crcl):
    if (option_figure == 1):
        parse_spektr_circle(option, option_color, option_figure, option_spektr_crcl)
    elif (option_figure == 2):
        parse_spektr_ellips(option, option_color, option_figure)



def parse_methods(dot_c, rad, option, option_color, option_figure, draw = True):

    color = parse_color(option_color)

    if (option == 1): # canon
        if (option_figure == 1):
            canon_circle(canvas_win, dot_c, rad[0], color, draw)
        elif (option_figure == 2):
            canon_ellips(canvas_win, dot_c, rad, color, draw)

    elif (option == 2): # param
        if (option_figure == 1):
            parametric_circle(canvas_win, dot_c, rad[0], color, draw)
        elif (option_figure == 2):
            parametric_ellips(canvas_win, dot_c, rad, color, draw)

    elif (option == 3): # bres
        if (option_figure == 1):
            bresenham_circle(canvas_win, dot_c, rad[0], color, draw)
        elif (option_figure == 2):
            bresenham_ellipse(canvas_win, dot_c, rad, color, draw)
        

    elif (option == 4): # mid point
        if (option_figure == 1):
            mid_dot_circle(canvas_win, dot_c, rad[0], color, draw)
        elif (option_figure == 2):
            mid_dot_ellipse(canvas_win, dot_c, rad, color, draw)
        

    elif (option == 5):
        lib_method(dot_c, rad, color)
    else:
        messagebox.showerror("Ошибка", "Неизвестный алгоритм")


def clear_canvas():
    canvas_win.delete("all")


def lib_method(dot_c, rad, color):
    canvas_win.create_oval(dot_c[0] - rad[0], dot_c[1] - rad[1], dot_c[0] + rad[0], dot_c[1] + rad[1], outline = color.hex) 
    


def change_figure(opt_figure):
    if (opt_figure == 1):
        rad_a_ellips_text.place_forget()
        rad_a_ellips_entry.place_forget()

        rad_b_ellips_text.place_forget()
        rad_b_ellips_entry.place_forget()

        rad_circle_text.place(x = CV_WIDE + 250, y = 445)

        rad_circle_entry.place(x = CV_WIDE + 310, y = 445)

        # Spektr

        #Elps

        rad_step_elps_text.place_forget()

        rad_step_elps_entry.place_forget()

        amount_elps_text.place_forget()

        amount_elps_entry.place_forget()

        rad_a_elps_text.place_forget()

        rad_a_elps_entry.place_forget()

        rad_b_elps_text.place_forget()

        rad_b_elps_entry.place_forget()

        # Circle

        rad_step_crcl_text.place(x = CV_WIDE + 60, y = 590)

        rad_step_crcl_entry.place(x = CV_WIDE + 110, y = 590)

        amount_crcl_text.place(x = CV_WIDE + 190, y = 590)
        amount_crcl_entry.place(x = CV_WIDE + 220, y = 590)

        rad_begin_crcl_text.place(x = CV_WIDE + 310, y = 590)
        rad_begin_crcl_entry.place(x = CV_WIDE + 380, y = 590)

        rad_end_crcl_text.place(x = CV_WIDE + 460, y = 590)
        rad_end_crcl_entry.place(x = CV_WIDE + 530, y = 590)

        # Radio button for hide

        remove_txt.place(x = CV_WIDE + 25, y = 630)

        spektr_crcl_remove_step.place(x = CV_WIDE + 25, y = 660)

        spektr_crcl_remove_amount.place(x = CV_WIDE + 25, y = 685)

        spektr_crcl_remove_rad_begin.place(x = CV_WIDE + 400, y = 660)

        spektr_crcl_remove_rad_end.place(x = CV_WIDE + 400, y = 685)

    else:
        rad_circle_text.place_forget()
        rad_circle_entry.place_forget()

        rad_a_ellips_text.place(x = CV_WIDE + 100, y = 445)

        rad_a_ellips_entry.place(x = CV_WIDE + 160, y = 445)

        rad_b_ellips_text.place(x = CV_WIDE + 400, y = 445)

        rad_b_ellips_entry.place(x = CV_WIDE + 460, y = 445)

        # Spektr

        # Elps

        rad_step_elps_text.place(x = CV_WIDE + 70, y = 590)

        rad_step_elps_entry.place(x = CV_WIDE + 130, y = 590)

        amount_elps_text.place(x = CV_WIDE + 340, y = 590)

        amount_elps_entry.place(x = CV_WIDE + 480, y = 590)

        rad_a_elps_text.place(x = CV_WIDE + 100, y = 640)

        rad_a_elps_entry.place(x = CV_WIDE + 160, y = 640)

        rad_b_elps_text.place(x = CV_WIDE + 400, y = 640)

        rad_b_elps_entry.place(x = CV_WIDE + 460, y = 640)

        # Crcl

        rad_step_crcl_text.place_forget()

        rad_step_crcl_entry.place_forget()

        amount_crcl_text.place_forget()
        amount_crcl_entry.place_forget()

        rad_begin_crcl_text.place_forget()
        rad_begin_crcl_entry.place_forget()

        rad_end_crcl_text.place_forget()
        rad_end_crcl_entry.place_forget()

        # Radio button for hide

        remove_txt.place_forget()

        spektr_crcl_remove_step.place_forget()

        spektr_crcl_remove_amount.place_forget()

        spektr_crcl_remove_rad_begin.place_forget()

        spektr_crcl_remove_rad_end.place_forget()


def remove_btn_spektr_cicle(option_spektr_crcl):
    rad_step_crcl_entry.configure(state = NORMAL)
    amount_crcl_entry.configure(state = NORMAL)
    rad_begin_crcl_entry.configure(state = NORMAL)
    rad_end_crcl_entry.configure(state = NORMAL)

    if (option_spektr_crcl == 1):
        rad_step_crcl_entry.configure(state = DISABLED)
    elif (option_spektr_crcl == 2):
        amount_crcl_entry.configure(state = DISABLED)
    elif (option_spektr_crcl == 3):
        rad_begin_crcl_entry.configure(state = DISABLED)
    elif (option_spektr_crcl == 4):
        rad_end_crcl_entry.configure(state = DISABLED)

def time_measure(option_figure):

    time_mes = []

    if (option_figure == 1):
        r_a = STEP
        r_b = r_a
        name = "окружность"
    else:
        r_a = STEP
        r_b = STEP
        name = "эллипс"

    dot_c = [CV_WIDE // 2, CV_HEIGHT // 2]

    for i in range(1, 5):

        time_start = [0] * (MAX_RADIUS // STEP)
        time_end = [0] * (MAX_RADIUS // STEP)

        for _ in range(NUMBER_OF_RUNS):

            r_a = STEP
            r_b = STEP

            for k in range(MAX_RADIUS // STEP):
                rad = [r_a, r_b]
                
                time_start[k] += time.time()

                parse_methods(dot_c, rad, i, 4, option_figure, draw = False)

                time_end[k] += time.time()

                r_a += STEP
                r_b += STEP

        size = len(time_start)

        res_time = list((time_end[j] - time_start[j]) / NUMBER_OF_RUNS for j in range(size))

        time_mes.append(res_time)

        # clear_canvas()

    rad_arr = list(i for i in range(0, MAX_RADIUS, STEP))
    plt.figure(figsize = (14, 6))

    plt.title("Замеры времени для различных методов\nФигура: " + name)


    plt.plot(rad_arr, time_mes[0], label = "Каноническое\nуравнеие")

    plt.plot(rad_arr, time_mes[1], label = "Параметрическое\nуравнение")

    plt.plot(rad_arr, time_mes[2], label = "Брезенхем")

    plt.plot(rad_arr, time_mes[3], label = "Алгоритм\nсредней точки")


    plt.xticks(np.arange(STEP, MAX_RADIUS, STEP))
    plt.legend()

    plt.ylabel("Время")
    plt.xlabel("Величина радиуса")

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


    draw_circle_btn = Button(win, text = "Нарисовать", font="-family {Consolas} -size 14", command = lambda: parse_figure(option.get(), option_color.get(), option_figure.get()), width = 20, bg = BTN_TEXT_COLOR)
    draw_circle_btn.place(x = CV_WIDE + 210, y = 490)


    # Spektr
    back_box_spektr = Label(text = "", font="-family {Consolas} -size 16", width = BOX_WIDTH, height = 8, bg = BOX_COLOR)
    back_box_spektr.place(x = CV_WIDE + 20, y = 550)

    spektr_text = Label(win, text = "Нарисовать спектр", width = BOX_WIDTH, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    spektr_text.place(x = CV_WIDE + 20, y = 550)


    # Data

    # Elips
    rad_step_elps_text = Label(text = "Шаг: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    rad_step_elps_entry = Entry(font="-family {Consolas} -size 14", width = 9)

    rad_a_elps_text = Label(text = "R_a: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    rad_a_elps_entry = Entry(font="-family {Consolas} -size 14", width = 9)

    rad_b_elps_text = Label(text = "R_b: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    rad_b_elps_entry = Entry(font="-family {Consolas} -size 14", width = 9)

    amount_elps_text = Label(text = "Количество: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    amount_elps_entry = Entry(font="-family {Consolas} -size 14", width = 9)

    # Circle

    rad_step_crcl_text = Label(text = "Шаг: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    rad_step_crcl_entry = Entry(font="-family {Consolas} -size 14", width = 5)

    amount_crcl_text = Label(text = "N:", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    amount_crcl_entry = Entry(font="-family {Consolas} -size 14", width = 5)

    rad_begin_crcl_text = Label(text = "R нач:", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    rad_begin_crcl_entry = Entry(font="-family {Consolas} -size 14", width = 5)

    rad_end_crcl_text = Label(text = "R кон:", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    rad_end_crcl_entry = Entry(font="-family {Consolas} -size 14", width = 5)

    # Radio button for hide

    remove_txt = Label(text = "Скрыть:", font="-family {Consolas} -size 16", bg = BOX_COLOR)
    remove_txt.place(x = CV_WIDE + 25, y = 630)

    option_spektr_crcl = IntVar()
    option_spektr_crcl.set(4)

    spektr_crcl_remove_step = Radiobutton(text = "Шаг", font="-family {Consolas} -size 14", variable = option_spektr_crcl, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR, command = lambda : remove_btn_spektr_cicle(option_spektr_crcl.get()))

    spektr_crcl_remove_amount = Radiobutton(text = "N", font="-family {Consolas} -size 14", variable = option_spektr_crcl, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR, command = lambda : remove_btn_spektr_cicle(option_spektr_crcl.get()))

    spektr_crcl_remove_rad_begin = Radiobutton(text = "R нач", font="-family {Consolas} -size 14", variable = option_spektr_crcl, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR, command = lambda : remove_btn_spektr_cicle(option_spektr_crcl.get()))

    spektr_crcl_remove_rad_end = Radiobutton(text = "R кон", font="-family {Consolas} -size 14", variable = option_spektr_crcl, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR, command = lambda : remove_btn_spektr_cicle(option_spektr_crcl.get()))




    draw_spektr_btn = Button(win, text = "Нарисовать", font="-family {Consolas} -size 14", command = lambda: choose_spektr(option.get(), option_color.get(), option_figure.get(), option_spektr_crcl.get()), width = 20, bg = BTN_TEXT_COLOR)
    draw_spektr_btn.place(x = CV_WIDE + 210, y = 720)


    # Control buttons

    compare_time_btn = Button(win, text = "Сравнить время", font="-family {Consolas} -size 15", command = lambda: time_measure(option_figure.get()), width = 20, height = 2,  bg = BTN_TEXT_COLOR)
    compare_time_btn.place(x = CV_WIDE + 30, y = 770)


    clear_win_btn = Button(win, text = "Очистить экран", font="-family {Consolas} -size 15", command = lambda: clear_canvas(), width = 20, height = 2, bg = BTN_TEXT_COLOR)
    clear_win_btn.place(x = CV_WIDE + 400, y = 770)

    # Insert # TODO

    xc_fig_entry.insert(END, "450")
    yc_fig_entry.insert(END, "450")

    rad_a_ellips_entry.insert(END, "10")
    rad_b_ellips_entry.insert(END, "50")

    rad_circle_entry.insert(END, "30")

    amount_elps_entry.insert(END, "30")
    rad_step_elps_entry.insert(END, "10")

    rad_a_elps_entry.insert(END, "40")
    rad_b_elps_entry.insert(END, "20")

    rad_begin_crcl_entry.insert(END, "30")
    rad_end_crcl_entry.insert(END, "90")

    rad_step_crcl_entry.insert(END, "5")

    amount_crcl_entry.insert(END, "50")

    remove_btn_spektr_cicle(4) # set remove step
    change_figure(1) # set circle

    win.mainloop()