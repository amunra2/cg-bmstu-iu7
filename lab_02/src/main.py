from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas
from tkinter import messagebox
from math import sqrt, acos, degrees, pi, sin, cos
import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


WIN_WIDTH = 1400
WIN_HEIGHT = 900
WIN_COLOR = "#66b3ff"

CV_WIDE = 900
CV_HEIGHT = 900
СV_COLOR = "#cce6ff"

GRAPH_WIDE = 60
GRAPH_HEIGHT = 60

TEXT_COLOR = "lightblue"

# Cicloid
NUMB_POINTS = 300
A_KOEF = 2
B_KOEF = 3

# Rectangle
LEFT_UP_X = -18
LEFT_UP_Y = 10
RIGHT_DOWN_X = 18
RIGHT_DOWN_Y = -10


EPS = 0.14#0.1973

X_CENTER = 0
Y_CENTER = 0



def cicloid(t):
    '''
        Функция для получения координат точки циклоиды при параметре t
    '''
    x = (A_KOEF + B_KOEF) * np.cos(t) - A_KOEF * np.cos((A_KOEF + B_KOEF) * t / A_KOEF)
    y = (A_KOEF + B_KOEF) * np.sin(t) - A_KOEF * np.sin((A_KOEF + B_KOEF) * t / A_KOEF)

    return x + X_CENTER, y + Y_CENTER


def check_intersection(x_graph, y_graph, x, y):
    '''
       Функция для нахождения пересечения между линией штриховки прямоугольника и циклоидой 
    '''
    for i in range (len(x_graph)):
        if (abs(x_graph[i] - x) < EPS) and (abs(y_graph[i] - y) < EPS):
            return 1

    return 0


def init_lines_rect(x_graph, y_graph):
    '''
        Функция для нахождения линий штриховки
    '''

    x_all = []
    y_all = []

    for i in range(LEFT_UP_X + X_CENTER, RIGHT_DOWN_X + X_CENTER, 5):
        y_b = RIGHT_DOWN_Y + Y_CENTER
        y_e = LEFT_UP_Y + Y_CENTER

        x_e = LEFT_UP_X + X_CENTER
        x_b = i

        x_line = []
        y_line = []

        while (y_b <= y_e):

            if (check_intersection(x_graph, y_graph, x_b, y_b) == 1):
                break

            if (x_b < x_e):
                break

            x_line.append(x_b)
            y_line.append(y_b)
            
            x_b -= 0.01
            y_b += 0.01

        x_all.append(x_line)
        y_all.append(y_line)


    for i in range(LEFT_UP_X + X_CENTER, RIGHT_DOWN_X + X_CENTER, 5):
        y_b = LEFT_UP_Y + Y_CENTER
        y_e = RIGHT_DOWN_Y + Y_CENTER

        x_e = RIGHT_DOWN_X + X_CENTER
        x_b = i

        x_line = []
        y_line = []

        while (y_b >= y_e):

            if (check_intersection(x_graph, y_graph, x_b, y_b) == 1):
                break

            if (x_b > x_e):
                break

            x_line.append(x_b)
            y_line.append(y_b)
            x_b += 0.01
            y_b -= 0.01

        x_all.append(x_line)
        y_all.append(y_line)

    return x_all, y_all


def draw_lines_rect(x_lines, y_lines):
    '''
       Функция для отрисовки линий штриховки 
    '''
    for line in range(3, len(x_lines)):
        plt.plot(x_lines[line], y_lines[line], 'b')


def init_rectangle():
    '''
        Функция для нахождения координат вершин прямоугольника
    '''
    x_rect = [LEFT_UP_X + X_CENTER, RIGHT_DOWN_X + X_CENTER, RIGHT_DOWN_X + X_CENTER, LEFT_UP_X + X_CENTER, LEFT_UP_X + X_CENTER]
    y_rect = [RIGHT_DOWN_Y + Y_CENTER, RIGHT_DOWN_Y + Y_CENTER, LEFT_UP_Y + Y_CENTER, LEFT_UP_Y + Y_CENTER, RIGHT_DOWN_Y + Y_CENTER]

    return x_rect, y_rect


def draw_rectangle(x_rect, y_rect):
    '''
       Функция для отрисовки прямоугльника 
    '''
    plt.plot(x_rect, y_rect, linewidth = 3)


def init_graph():
    '''
        Функция для вычисления координат циклоиды для ее последующего построения
    '''
    x_arr = []
    y_arr = []

    arr = np.linspace(0, 4 * pi, NUMB_POINTS)

    for i in arr:
        x, y = cicloid(i)

        x_arr.append(x)
        y_arr.append(y)

    return x_arr, y_arr


def draw_graph(x_graph, y_graph):
    '''
        Функция для отрисовки графика циклоиды
    '''
    plt.plot(x_graph, y_graph, linewidth = 3)


def draw_picrure(x_all, y_all):
    '''
        Функция для отрисовки всей картины
    '''
    build_empty_figure()

    draw_lines_rect(x_all, y_all)
    draw_rectangle(x_all[2], y_all[2])
    draw_graph(x_all[1], y_all[1])

    canvas.draw()


def init_all():
    '''
        Функция для вычисления координат всех необходимых объектов
    '''
    x_graph, y_graph = init_graph()
    x_lines, y_lines = init_lines_rect(x_graph, y_graph)
    x_rect, y_rect = init_rectangle()   

    x_all = [[X_CENTER], x_graph, x_rect]
    y_all = [[Y_CENTER], y_graph, y_rect]

    for i in range(len(x_lines)):
        x_all.append(x_lines[i])
        y_all.append(y_lines[i])

    draw_picrure(x_all, y_all)

    return x_all, y_all


def move(x_all, y_all, dx, dy):
    '''
        Функция для вычисления координат всех нужных точек при перемещении
    '''

    for i in range(len(x_all)):
        for j in range(len(x_all[i])):
            x_all[i][j] += dx
            y_all[i][j] += dy

    set_figure_center(x_all[0][0], y_all[0][0])

    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))
            
    draw_picrure(x_history[len(x_history) - 1], y_history[len(y_history) - 1])  


def spin(x_all, y_all, angle, x_c, y_c):
    '''
        Функция для вычисления координат всех нужных точек при повороте
    '''

    angle = (angle * pi) / 180

    matrix_spin = np.array([[cos(angle) , -sin(angle)], [sin(angle), cos(angle)]])

    for i in range(len(x_all)):
        for j in range(len(x_all[i])):
            x_all[i][j] -= x_c
            y_all[i][j] -= y_c

            coords = np.dot(matrix_spin, [x_all[i][j], y_all[i][j]])

            x_all[i][j] = coords[0] + x_c
            y_all[i][j] = coords[1] + y_c

    set_figure_center(x_all[0][0], y_all[0][0])

    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))

    draw_picrure(x_history[len(x_history) - 1], y_history[len(y_history) - 1])



def scale(x_all, y_all, x_c, y_c, kx, ky):
    '''
        Функция для вычисления координат всех нужных точек при масштабировании
    '''

    for i in range(len(x_all)):
        for j in range(len(x_all[i])):
            x_all[i][j] = kx * (x_all[i][j] - x_c) + x_c
            y_all[i][j] = ky * (y_all[i][j] - y_c) + y_c

    set_figure_center(x_all[0][0], y_all[0][0])

    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))

    draw_picrure(x_history[len(x_history) - 1], y_history[len(y_history) - 1])


def build_empty_figure():
    '''
        Функция для очистки поля для последующего построения на нем фигуры
    '''
    global ax

    fig.clear()

    ax = fig.add_subplot(111)

    ax.set_xlim([-GRAPH_WIDE, GRAPH_WIDE])
    ax.set_ylim([-GRAPH_HEIGHT, GRAPH_HEIGHT])
    ax.grid()

    fig.subplots_adjust(right = 0.97, left = 0.06, bottom = 0.06, top = 0.97)

    canvas.draw()


def reset():
    '''
        Функция для сброса всех преобразований и возврата к начальному состояни фигуры
    '''
    global x_all, y_all, x_history, y_history

    set_figure_center(0, 0)

    x_all, y_all = init_all()

    x_history.clear()
    y_history.clear()

    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))


def step_backing():
    '''
        Функция для возврата к предыдущему состоянию фигуры
    '''

    if (len(x_history) == 1):
        messagebox.showerror("Стоп", "Вы дошли до начального изображения")
        return

    x_history.pop()
    y_history.pop()

    set_figure_center(x_history[len(x_history) - 1][0][0], y_history[len(y_history) - 1][0][0])

    draw_picrure(x_history[len(x_history) - 1], y_history[len(y_history) - 1])


def parse_move():
    '''
        Функция обработки параметров для перемещения и вызова функции перемещения
    '''
    try:
        dx = float(move_x.get())
        dy = float(move_y.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введена величина смещения")
        return

    x_cur = copy.deepcopy(x_history[len(x_history) - 1])
    y_cur = copy.deepcopy(y_history[len(y_history) - 1])
    
    move(x_cur, y_cur, dx, dy)


def parse_spin():
    '''
        Функция обработки параметров для поворота и вызова функции поворота
    '''
    try:
        x_c = float(center_x.get())  
        y_c = float(center_y.get()) 
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты центра поворота")

    try:
        angle = float(spin_angle.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введен угол поворота")

    x_cur = copy.deepcopy(x_history[len(x_history) - 1])
    y_cur = copy.deepcopy(y_history[len(y_history) - 1])

    spin(x_cur, y_cur, angle, x_c, y_c)


def set_figure_center(x_c, y_c):
    '''
        Функция для отрисовки в приложении текущего центра фигуры
    '''
    
    figure_c = Label(win, text = "Центр фигуры: (%3.2f;%3.2f)" %(x_c, y_c), width = 32, font="-family {Consolas} -size 17", bg = TEXT_COLOR)
    figure_c.place(x = CV_WIDE + 1, y = 850)


def parse_scale():
    '''
        Функция обработки параметров для масштабирования и вызова функции масштабирования
    '''
    try:
        x_c = float(center_x.get())  
        y_c = float(center_y.get()) 
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты центра поворота")

    try:
        kx = float(scale_x.get())  
        ky = float(scale_y.get()) 
    except:
        messagebox.showerror("Ошибка", "Неверно введены коэффициенты масштабирования")

    x_cur = copy.deepcopy(x_history[len(x_history) - 1])
    y_cur = copy.deepcopy(y_history[len(y_history) - 1])

    scale(x_cur, y_cur, x_c, y_c, kx, ky)


if __name__ == "__main__":
    '''
        Основной графический модуль
    '''

    win = Tk()
    win['bg'] = WIN_COLOR
    win.geometry("%dx%d" %(WIN_WIDTH, WIN_HEIGHT))
    win.title("Лабораторная работа #2 (Цветков И.А. ИУ7-43Б)")
    win.resizable(False, False)

    x_history = []
    y_history = []

    fig = plt.figure()
    
    canvas = FigureCanvasTkAgg(fig, master = win)
    plot = canvas.get_tk_widget()
    plot.place(x = 0, y = 0, width = CV_WIDE, height = CV_HEIGHT)
    build_empty_figure()

    x_all, y_all = init_all()

    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))

    canvas.draw()

    # Figure center
    figure_c = Label(win, text = "Центр фигуры: (%3.2f;%3.2f)" %(x_all[0][0], y_all[0][0]), width = 36, font="-family {Consolas} -size 17", bg = TEXT_COLOR)
    figure_c.place(x = CV_WIDE + 1, y = 850)

    # Center
    center_label = Label(win, text = "Центр(для масштабирования и поворота)", font="-family {Consolas} -size 16", bg = WIN_COLOR)
    center_label.place (x = CV_WIDE + 15, y = 20)

    center_x_label = Label(win, text = "X:", font="-family {Consolas} -size 14", bg = WIN_COLOR)
    center_x_label.place(x = CV_WIDE + 70, y = 50)
    center_x = Entry(win, font="-family {Consolas} -size 14", width = 9)
    center_x.insert(END, "0")
    center_x.place (x = CV_WIDE + 100, y = 50)

    center_y_label = Label(win, text = "Y:", font="-family {Consolas} -size 14", bg = WIN_COLOR)
    center_y_label.place(x = CV_WIDE + 270, y = 50)
    center_y = Entry(win, font="-family {Consolas} -size 14", width = 9)
    center_y.insert(END, "0")
    center_y.place (x = CV_WIDE + 300, y = 50)

    # Spin
    spin_label = Label(win, text = "Поворот", width = 36, font="-family {Consolas} -size 18", bg = TEXT_COLOR)
    spin_label.place(x = CV_WIDE + 1, y = 110)

    spin_angle_label = Label(win, text = "Угол°: ", font="-family {Consolas} -size 16", bg = WIN_COLOR)
    spin_angle_label.place(x = CV_WIDE + 160, y = 155)
    spin_angle = Entry(win, font="-family {Consolas} -size 16", width = 9)
    spin_angle.insert(END, "0")
    spin_angle.place (x = CV_WIDE + 240, y = 155)

    spin_btn = Button(win, text = "Повернуть", font="-family {Consolas} -size 14", command = lambda: parse_spin(), width = 15, height = 2, bg = TEXT_COLOR)
    spin_btn.place(x = CV_WIDE + 160, y = 200)

    # Scale
    scale_label = Label(win, text = "Масштабирование", width = 36, font="-family {Consolas} -size 18", bg = TEXT_COLOR)
    scale_label.place(x = CV_WIDE + 1, y = 300)

    scale_x_label = Label(win, text = "kx: ", font="-family {Consolas} -size 16", bg = WIN_COLOR)
    scale_x_label.place(x = CV_WIDE + 100, y = 360)
    scale_x = Entry(win, font="-family {Consolas} -size 14", width = 9)
    scale_x.insert(END, "1")
    scale_x.place (x = CV_WIDE + 140, y = 360)

    scale_y_label = Label(win, text = "ky: ", font="-family {Consolas} -size 16", bg = WIN_COLOR)
    scale_y_label.place(x = CV_WIDE + 270, y = 360)
    scale_y = Entry(win, font="-family {Consolas} -size 14", width = 9)
    scale_y.insert(END, "1")
    scale_y.place (x = CV_WIDE + 310, y = 360)

    scale_btn = Button(win, text = "Масштабировать", font="-family {Consolas} -size 14", command = lambda: parse_scale(), width = 15, height = 2, bg = TEXT_COLOR)
    scale_btn.place(x = CV_WIDE + 160, y = 420)

    # Move
    move_label = Label(win, text = "Перемещение", width = 36, font="-family {Consolas} -size 18", bg = TEXT_COLOR)
    move_label.place(x = CV_WIDE + 1, y = 520)

    move_x_label = Label(win, text = "dx: ", font="-family {Consolas} -size 16", bg = WIN_COLOR)
    move_x_label.place(x = CV_WIDE + 100, y = 580)
    move_x = Entry(win, font="-family {Consolas} -size 14", width = 9)
    move_x.insert(END, "0")
    move_x.place (x = CV_WIDE + 140, y = 580)

    move_y_label = Label(win, text = "dy: ", font="-family {Consolas} -size 16", bg = WIN_COLOR)
    move_y_label.place(x = CV_WIDE + 270, y = 580)
    move_y = Entry(win, font="-family {Consolas} -size 14", width = 9)
    move_y.insert(END, "0")
    move_y.place (x = CV_WIDE + 310, y = 580)

    move_btn = Button(win, text = "Передвинуть", font="-family {Consolas} -size 14", command = lambda: parse_move(), width = 15, height = 2, bg = TEXT_COLOR)
    move_btn.place(x = CV_WIDE + 160, y = 640)

    line = Label(win, text = "", width = 36, font="-family {Consolas} -size 18", bg = TEXT_COLOR)
    line.place(x = CV_WIDE + 1, y = 710)

    stab_back = Button(win, text = "Шаг назад", font="-family {Consolas} -size 14", command = lambda: step_backing(), width = 15, height = 2, bg = TEXT_COLOR)
    stab_back.place(x = CV_WIDE + 25, y = 760)

    clear = Button(win, text = "Сбросить", font="-family {Consolas} -size 14", command = lambda: reset(), width = 15, height = 2, bg = TEXT_COLOR)
    clear.place(x = CV_WIDE + 300, y = 760)

    win.mainloop()