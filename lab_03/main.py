from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, Radiobutton, LEFT, RIGHT, IntVar
from tkinter import messagebox
from math import sqrt, acos, degrees, pi, sin, cos, radians
import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


WIN_WIDTH = 1500
WIN_HEIGHT = 900
WIN_COLOR = "#bf80ff"

CV_WIDE = 900
CV_HEIGHT = 900
CV_COLOR = "#f3e6ff" #"#cce6ff"
#CV_COLOR
#СV_COLOR
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
        color = "blue"
    elif (option_color == 2):
        color = "orange"
    elif (option_color == 3):
        color = "black"
    elif (option_color == 4):
        color = CV_COLOR
    # else:
    #     messagebox.showerror("Ошибка", "Нет такого цвета")

    return color


def parse_spektr(option, option_color):
    try:
        line_len = float(len_line.get()) # float?
        angle_spin = float(angle.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
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
        x1 = float(x1_line.get()) # float?
        y1 = float(y1_line.get())
        x2 = float(x2_line.get())
        y2 = float(y2_line.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
        return

    p1 = [x1, y1]
    p2 = [x2, y2]

    parse_methods(p1, p2, option, option_color)


def parse_methods(p1, p2, option, option_color):

    print("Method = ", option)

    color = parse_color(option_color)

    if (option == 1):
        messagebox.showinfo("Метод", "Брезенхем (int)")
    elif (option == 2):
        messagebox.showinfo("Метод", "Брезенхем (float)")
    elif (option == 3):
        messagebox.showinfo("Метод", "Брезенхем (smooth)")
    elif (option == 4):
        messagebox.showinfo("Метод", "ЦДА")
    elif (option == 5):
        messagebox.showinfo("Метод", "Ву")
    elif (option == 6):
        #messagebox.showinfo("Метод", "Библиотечная")
        lib_method(p1, p2, color)
    else:
        messagebox.showerror("Ошибка", "Неизвестный алгоритм")


def lib_method(p1, p2, color):

    canvas_win.create_line(p1[0], p1[1], p2[0], p2[1], fill = color)
    
    

















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
    option.set(0)

    method_cda = Radiobutton(text = "ЦДА", font="-family {Consolas} -size 14", variable = option, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_cda.place(x = CV_WIDE + 400, y = 70)

    method_wu = Radiobutton(text = "Ву", font="-family {Consolas} -size 14", variable = option, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_wu.place(x = CV_WIDE + 400, y = 105)

    method_lib = Radiobutton(text = "Библиотечная", font="-family {Consolas} -size 14", variable = option, value = 6, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_lib.place(x = CV_WIDE + 400, y = 140)

    

    method_bresenhem_float = Radiobutton(text = "Брезенхем (float)", font="-family {Consolas} -size 14", variable = option, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_bresenhem_float.place(x = CV_WIDE + 25, y = 70)

    method_bresenhem_int = Radiobutton(text = "Брезенхем (int)", font="-family {Consolas} -size 14", variable = option, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_bresenhem_int.place(x = CV_WIDE + 25, y = 105)

    method_bresenhem_smooth = Radiobutton(text = "Брезенхем (сглаживание)", font="-family {Consolas} -size 14", variable = option, value = 5, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    method_bresenhem_smooth.place(x = CV_WIDE + 25, y = 140)


    # check_btn = Button(win, text = "Проверить", font="-family {Consolas} -size 14", command = lambda: check_option(option.get()), width = 15, height = 2, bg = TEXT_COLOR)
    # check_btn.place(x = CV_WIDE + 200, y = 180)



    # Color

    back_box_color = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 5, bg = BOX_COLOR)
    back_box_color.place(x = CV_WIDE + 20, y = 210)

    color_text = Label(win, text = "Цвет отрезка", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 210)


    option_color = IntVar()
    option_color.set(0)

    color_line_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_blue.place(x = CV_WIDE + 25, y = 250)

    color_line_black = Radiobutton(text = "Черный", font="-family {Consolas} -size 14", variable = option_color, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_black.place(x = CV_WIDE + 25, y = 285)


    color_line_orange = Radiobutton(text = "Оранжевый", font="-family {Consolas} -size 14", variable = option_color, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_line_orange.place(x = CV_WIDE + 400, y = 250)

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

    compare_time_btn = Button(win, text = "Сравнить\nвремя", font="-family {Consolas} -size 15", command = lambda: check_option(option.get()), width = 15, height = 2,  bg = TEXT_COLOR)
    compare_time_btn.place(x = CV_WIDE + 70, y = 720)

    compare_steps_btn = Button(win, text = "Сравнить\nступенчатость", font="-family {Consolas} -size 15", command = lambda: check_option(option.get()), width = 15, height = 2, bg = TEXT_COLOR)
    compare_steps_btn.place(x = CV_WIDE + 330, y = 720)


    clear_win_btn = Button(win, text = "Очистить экран", font="-family {Consolas} -size 15", command = lambda: check_option(option.get()), width = 25, height = 2, bg = TEXT_COLOR)
    clear_win_btn.place(x = CV_WIDE + 150, y = 800)





    # # Figure center
    # figure_c = Label(win, text = "Центр фигуры: (%3.2f;%3.2f)" %(x_all[0][0], y_all[0][0]), width = 36, font="-family {Consolas} -size 17", bg = TEXT_COLOR)
    # figure_c.place(x = CV_WIDE + 1, y = 850)

    # # Center
    # center_label = Label(win, text = "Центр(для масштабирования и поворота)", font="-family {Consolas} -size 16", bg = WIN_COLOR)
    # center_label.place (x = CV_WIDE + 15, y = 20)

    # center_x_label = Label(win, text = "X:", font="-family {Consolas} -size 14", bg = WIN_COLOR)
    # center_x_label.place(x = CV_WIDE + 70, y = 50)
    # center_x = Entry(win, font="-family {Consolas} -size 14", width = 9)
    # center_x.insert(END, "0")
    # center_x.place (x = CV_WIDE + 100, y = 50)

    # center_y_label = Label(win, text = "Y:", font="-family {Consolas} -size 14", bg = WIN_COLOR)
    # center_y_label.place(x = CV_WIDE + 270, y = 50)
    # center_y = Entry(win, font="-family {Consolas} -size 14", width = 9)
    # center_y.insert(END, "0")
    # center_y.place (x = CV_WIDE + 300, y = 50)

    # # Spin
    # spin_label = Label(win, text = "Поворот", width = 36, font="-family {Consolas} -size 18", bg = TEXT_COLOR)
    # spin_label.place(x = CV_WIDE + 1, y = 110)

    # spin_angle_label = Label(win, text = "Угол°: ", font="-family {Consolas} -size 16", bg = WIN_COLOR)
    # spin_angle_label.place(x = CV_WIDE + 160, y = 155)
    # spin_angle = Entry(win, font="-family {Consolas} -size 16", width = 9)
    # spin_angle.insert(END, "0")
    # spin_angle.place (x = CV_WIDE + 240, y = 155)

    # spin_btn = Button(win, text = "Повернуть", font="-family {Consolas} -size 14", command = lambda: parse_spin(), width = 15, height = 2, bg = TEXT_COLOR)
    # spin_btn.place(x = CV_WIDE + 160, y = 200)

    # # Scale
    # scale_label = Label(win, text = "Масштабирование", width = 36, font="-family {Consolas} -size 18", bg = TEXT_COLOR)
    # scale_label.place(x = CV_WIDE + 1, y = 300)

    # scale_x_label = Label(win, text = "kx: ", font="-family {Consolas} -size 16", bg = WIN_COLOR)
    # scale_x_label.place(x = CV_WIDE + 100, y = 360)
    # scale_x = Entry(win, font="-family {Consolas} -size 14", width = 9)
    # scale_x.insert(END, "1")
    # scale_x.place (x = CV_WIDE + 140, y = 360)

    # scale_y_label = Label(win, text = "ky: ", font="-family {Consolas} -size 16", bg = WIN_COLOR)
    # scale_y_label.place(x = CV_WIDE + 270, y = 360)
    # scale_y = Entry(win, font="-family {Consolas} -size 14", width = 9)
    # scale_y.insert(END, "1")
    # scale_y.place (x = CV_WIDE + 310, y = 360)

    # scale_btn = Button(win, text = "Масштабировать", font="-family {Consolas} -size 14", command = lambda: parse_scale(), width = 15, height = 2, bg = TEXT_COLOR)
    # scale_btn.place(x = CV_WIDE + 160, y = 420)

    # # Move
    # move_label = Label(win, text = "Перемещение", width = 36, font="-family {Consolas} -size 18", bg = TEXT_COLOR)
    # move_label.place(x = CV_WIDE + 1, y = 520)

    # move_x_label = Label(win, text = "dx: ", font="-family {Consolas} -size 16", bg = WIN_COLOR)
    # move_x_label.place(x = CV_WIDE + 100, y = 580)
    # move_x = Entry(win, font="-family {Consolas} -size 14", width = 9)
    # move_x.insert(END, "0")
    # move_x.place (x = CV_WIDE + 140, y = 580)

    # move_y_label = Label(win, text = "dy: ", font="-family {Consolas} -size 16", bg = WIN_COLOR)
    # move_y_label.place(x = CV_WIDE + 270, y = 580)
    # move_y = Entry(win, font="-family {Consolas} -size 14", width = 9)
    # move_y.insert(END, "0")
    # move_y.place (x = CV_WIDE + 310, y = 580)

    # move_btn = Button(win, text = "Передвинуть", font="-family {Consolas} -size 14", command = lambda: parse_move(), width = 15, height = 2, bg = TEXT_COLOR)
    # move_btn.place(x = CV_WIDE + 160, y = 640)

    # line = Label(win, text = "", width = 36, font="-family {Consolas} -size 18", bg = TEXT_COLOR)
    # line.place(x = CV_WIDE + 1, y = 710)

    # stab_back = Button(win, text = "Шаг назад", font="-family {Consolas} -size 14", command = lambda: step_backing(), width = 15, height = 2, bg = TEXT_COLOR)
    # stab_back.place(x = CV_WIDE + 25, y = 760)

    # clear = Button(win, text = "Сбросить", font="-family {Consolas} -size 14", command = lambda: reset(), width = 15, height = 2, bg = TEXT_COLOR)
    # clear.place(x = CV_WIDE + 300, y = 760)

    win.mainloop()