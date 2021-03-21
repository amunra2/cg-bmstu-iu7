from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas
from tkinter import messagebox
from math import sqrt, acos, degrees

from itertools import combinations

WIN_WIDTH = 1400
WIN_HEIGHT = 800

CV_WIDE = 800
CV_HEIGHT = 800

POINT_RAD = 3.5

TRIANGLE_1_COLOR = "green"
TRIANGLE_2_COLOR = "#400070"
BISEKS_1_COLOR = "#1e4169"
BISEKS_2_COLOR = "blue"
POINT_NAME_COLOR = "black"
POINT_COLOR = "red"
RESULT_LINE_COLOR = "#9311d9"
AXIS_COLOR = "darkgray"

PLACE_TO_DRAW = 0.8
INDENT_WIDTH = 0.1

TASK = "На плоскости даны два множества точек. Найти пару треугольников (первый треугольник в качестве вершин имеет три точки первого множества, второй треугольник - три точки второго множества) таких, что прямая, соединяющая точки пересечения биссектрис, образует минимальный угол с осью ординат"



def init_input_win():
    '''
        Функция для создания окна для ввода или изменения координат точки
    '''

    dot_win = Tk()
    dot_win.title("Точка")
    dot_win['bg'] = "orange"
    dot_win.geometry("270x200")
    dot_win.resizable(False, False)

    dot_x_label = Label(dot_win, text = "X: ", bg = "orange", font="-family {Consolas} -size 14")
    dot_x_label.place(x = 3, y = 30)
    dot_x = Entry(dot_win, font="-family {Consolas} -size 14")
    dot_x.focus()
    dot_x.place(x = 27, y = 30)

    dot_y_label = Label(dot_win, text = "Y: ", bg = "orange", font="-family {Consolas} -size 14")
    dot_y_label.place(x = 3, y = 70)
    dot_y = Entry(dot_win, font="-family {Consolas} -size 14")
    dot_y.place(x = 27, y = 70)

    return dot_win, dot_x, dot_y


def del_dot(dots_block, dots_list):
    '''
        Функция для удаления точки их выбранного множества
    '''
    try:
        place = dots_block.curselection()[0]
        dots_list.pop(place)

        dots_block.delete(0, END)

        for i in range(len(dots_list)):
            dot_str = "%d) (%-3.1f,%-3.1f)" %(i + 1, float(dots_list[i][0]), float(dots_list[i][1]))
            dots_list[i][2] = i + 1
            dots_block.insert(END, dot_str)
    except:
        messagebox.showerror("Ошибка", "Не выбрана точка для удаления")


def del_all_dots(dots_block, dots_list):
    '''
        Функция для удаления всех точек текущего множества
    '''
    if (len(dots_list) != 0):
        dots_block.delete(0, END)
        dots_list.clear()
    else:
        messagebox.showerror("Ошибка", "Нечего удалять")


def change_dot(dots_block, dots_list):
    '''
        Функция для изменения координат точки выбранного множества
    '''
    try:   
        place = dots_block.curselection()[0]
    except:
        messagebox.showerror("Ошибка", "Не выбрана точка для изменения")
        return

    dot_win, dot_x, dot_y = init_input_win()

    add_but = Button(dot_win, text = "Изменить", font="-family {Consolas} -size 14", command = lambda: read_dot(dots_block, dots_list, place, dot_x.get(), dot_y.get()))
    add_but.place(x = 70, y = 120)

    dot_win.mainloop()


def read_dot(dots_block, dots_list, place, dot_x, dot_y):
    '''
        Функция для чтения координат точки, их обработки и добавления в множество
    '''
    try:
        coords_dot = []

        coords_dot.append(float(dot_x))
        coords_dot.append(float(dot_y))
        
        if (place != END): # если нужно изменить точку
            dots_block.delete(place)
            dots_list.pop(place)
            coords_dot.append(place + 1)
            dots_list.insert(place, coords_dot)
        else: # если нужно добавить новую точку
            place = len(dots_list)
            coords_dot.append(place + 1)
            dots_list.append(coords_dot)

        dot_str = "%d) (%-3.1f,%-3.1f)" %(place + 1, float(dot_x), float(dot_y))
        dots_block.insert(place, dot_str)

        #print(dots_list)
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты точки")


def add_dot(dots_block, dots_list):
    '''
        Функция для добавления точки в множество
    '''
    dot_win, dot_x, dot_y = init_input_win()

    add_but = Button(dot_win, text = "Добавить", font="-family {Consolas} -size 14", command = lambda: read_dot(dots_block, dots_list,END, dot_x.get(), dot_y.get()))
    add_but.place(x = 70, y = 120)

    dot_win.mainloop()



def line(x1, y1, x2, y2):
    '''
        Функция для вычисления длины отрезка по координатам его концов
    '''
    return (sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)))


def line_koefs(x1, y1, x2, y2):
    '''
        Функция для вычисления коэффециентов в уравнении прямой (по координатам)
    '''
    a = y1 - y2
    b = x2 - x1
    c = x1*y2 - x2*y1

    return a, b, c


def biseks_equation(a1, b1, c1, a2, b2, c2):
    # (a1*x + b1*y + c1) / (sqrt(a1*a1 + b1*b1)) = -(a2*x + b2*y + c2) / (sqrt(a2*a2 + b2*b2))
    '''
        Функция для нахождения коэффициентов уравнения биссектрисы
    '''

    sqrt_1 = sqrt(a1*a1 + b1*b1)
    sqrt_2 = sqrt(a2*a2 + b2*b2)

    a_res = a1 * sqrt_2 + a2 * sqrt_1
    b_res = b1 * sqrt_2 + b2 * sqrt_1
    c_res = c1 * sqrt_2 + c2 * sqrt_1

    return a_res, b_res, c_res


def find_bisseks_intersection(x1, y1, x2, y2, x3, y3):
    '''
        Функция для нахождения точки пересечения биссектрис треугольника
    '''

    a1, b1, c1 = line_koefs(x1, y1, x2, y2)
    a2, b2, c2 = line_koefs(x2, y2, x3, y3)
    a3, b3, c3 = line_koefs(x1, y1, x3, y3)

    a_bisek_1, b_bisek_1, c_bisek_1 = biseks_equation(a2, b2, c2, a3, b3, c3)
    a_bisek_2, b_bisek_2, c_bisek_2 = biseks_equation(a1, b1, c1, a3, b3, c3)

    x0, y0 = solve_lines_intersection(a_bisek_1, b_bisek_1, c_bisek_1, a_bisek_2, b_bisek_2, c_bisek_2)

    print("x0 = %f, y0 = %f" %(x0, y0))

    return x0, y0


def solve_lines_intersection(a1, b1, c1, a2, b2, c2):
    '''
        Функция для решения системы из двух уравнений методом Крамера (для нахождения точки пересечения двух прямых по коэффициентам уравнений этих прямых)
    '''

    opr = a1*b2 - a2*b1
    opr1 = (-c1)*b2 - b1*(-c2)
    opr2 = a1*(-c2) - (-c1)*a2

    x = opr1 / opr
    y = opr2 / opr

    return x, y


def check_lines_intersection(x11, y11, x12, y12, x21, y21, x22, y22):
    '''
        Функция для нахождения точки пересечения двух прямых
    '''
    a1, b1, c1 = line_koefs(x11, y11, x12, y12)
    a2, b2, c2 = line_koefs(x21, y21, x22, y22)

    return solve_lines_intersection(a1, b1, c1, a2, b2, c2)


def check_triangle(x1, y1, x2, y2, x3, y3):
    '''
        Функция для проверки существования треугольника (если одна сторона больше суммы двух ее сторон)
    '''
    a = line(x1, y1, x2, y2)
    b = line(x2, y2, x3, y3)
    c = line(x1, y1, x3, y3)

    if ((a + b > c) and (a + c > b) and (b + c > a)):
        return 1
    else:
        return 0


def translate_point(x, y, x_min, y_min, k):
    '''
        Функция для перевода точки в нужные координаты (для масштабирования)
    '''
    x = INDENT_WIDTH * CV_WIDE + (x - x_min) * k
    y = INDENT_WIDTH * CV_HEIGHT + (y - y_min) * k

    return x, y


def name_point(x1, y1, num, x1_place, y1_place, x2_place, y2_place, x3_place, y3_place, color):
    '''
        Функция для вычисления нужного расположения точки и ее постановка на холст
    '''

    x_min = min(x1_place, x2_place, x3_place)
    x_max = max(x1_place, x2_place, x3_place)
    y_min = min(y1_place, y2_place, y3_place)
    y_max = max(y1_place, y2_place, y3_place)

    move_x = 0
    move_y = 0

    if (x1_place == x_min):
        move_x -= 15
    if (x1_place == x_max):
        move_x += 15
    if (y1_place == y_min):
        move_y -= 15
    if (y1_place == y_max):
        move_y += 15 

    if (move_x == 0) and (move_y == 0):
        if (x1_place > x2_place):
            move_x -= 20
        else:
            move_x += 20
        
        if (y1_place > y2_place):
            move_y -= 20
        else:
            move_y += 20

    
    canvas_win.create_text(x1_place + move_x, -(y1_place + move_y) + CV_HEIGHT, text = "(%d) [%.1f;%.1f]" %(num, x1, y1), font="-family {Consolas} -size 11", fill = color)



def build_triangle(x1, y1, num1, x2, y2, num2, x3, y3, num3, x_min, y_min, k, triangle_color, point_name_color):
    '''
        Функция для отрисовки треугольника и его вершин
    '''

    x1_trans, y1_trans = translate_point(x1, y1, x_min, y_min, k)
    x2_trans, y2_trans = translate_point(x2, y2, x_min, y_min, k)
    x3_trans, y3_trans = translate_point(x3, y3, x_min, y_min, k)

    canvas_win.create_line(x1_trans, -y1_trans + CV_HEIGHT, x2_trans, -y2_trans + CV_HEIGHT, width = 4, fill = triangle_color)
    canvas_win.create_line(x2_trans, -y2_trans + CV_HEIGHT, x3_trans, -y3_trans + CV_HEIGHT, width = 4, fill = triangle_color)
    canvas_win.create_line(x1_trans, -y1_trans + CV_HEIGHT, x3_trans, -y3_trans + CV_HEIGHT, width = 4, fill = triangle_color)

    canvas_win.create_oval(x1_trans - POINT_RAD, -(y1_trans - POINT_RAD) + CV_HEIGHT, x1_trans + POINT_RAD, -(y1_trans + POINT_RAD) + CV_HEIGHT, width = 1, outline = POINT_COLOR, fill = POINT_COLOR)
    canvas_win.create_oval(x2_trans - POINT_RAD, -(y2_trans - POINT_RAD) + CV_HEIGHT, x2_trans + POINT_RAD, -(y2_trans + POINT_RAD) + CV_HEIGHT, width = 1, outline = POINT_COLOR, fill = POINT_COLOR)
    canvas_win.create_oval(x3_trans - POINT_RAD, -(y3_trans - POINT_RAD) + CV_HEIGHT, x3_trans + POINT_RAD, -(y3_trans + POINT_RAD) + CV_HEIGHT, width = 1, outline = POINT_COLOR, fill = POINT_COLOR)

    name_point(x1, y1, num1, x1_trans, y1_trans, x2_trans, y2_trans, x3_trans, y3_trans, point_name_color)
    name_point(x2, y2, num2, x2_trans, y2_trans, x1_trans, y1_trans, x3_trans, y3_trans, point_name_color)
    name_point(x3, y3, num3, x3_trans, y3_trans, x2_trans, y2_trans, x1_trans, y1_trans, point_name_color)



def build_biseks(x1, y1, x2, y2, x3, y3, x_min, y_min, k, line_color):
    '''
        Функция для отрисовки биссектрис треугольника и точки их пересечения
    '''
    x0, y0 = find_bisseks_intersection(x1, y1, x2, y2, x3, y3)

    x2_b, y2_b = check_lines_intersection(x1, y1, x3, y3, x2, y2, x0, y0)
    x1_b, y1_b = check_lines_intersection(x2, y2, x3, y3, x1, y1, x0, y0)
    x3_b, y3_b = check_lines_intersection(x1, y1, x2, y2, x3, y3, x0, y0)

    x1, y1 = translate_point(x1, y1, x_min, y_min, k)
    x2, y2 = translate_point(x2, y2, x_min, y_min, k)
    x3, y3 = translate_point(x3, y3, x_min, y_min, k)

    x1_b, y1_b = translate_point(x1_b, y1_b, x_min, y_min, k)
    x2_b, y2_b = translate_point(x2_b, y2_b, x_min, y_min, k)
    x3_b, y3_b = translate_point(x3_b, y3_b, x_min, y_min, k)

    x0, y0 = translate_point(x0, y0, x_min, y_min, k)

    canvas_win.create_line(x1, -y1 + CV_HEIGHT, x1_b, -y1_b + CV_HEIGHT, width = 4, fill = line_color)
    canvas_win.create_line(x2, -y2 + CV_HEIGHT, x2_b, -y2_b + CV_HEIGHT, width = 4, fill = line_color)
    canvas_win.create_line(x3, -y3 + CV_HEIGHT, x3_b, -y3_b + CV_HEIGHT, width = 4, fill = line_color)

    canvas_win.create_oval(x0 - POINT_RAD, -(y0 - POINT_RAD) + CV_HEIGHT, x0 + POINT_RAD, -(y0 + POINT_RAD) + CV_HEIGHT, width = 1, outline = "red", fill = "red")


def find_angle_between_two_lines(x11, y11, x12, y12, x21, y21, x22, y22):
    '''
        Функция для нахождения угла между двумя прямыми
    '''
    a1, b1, c1 = line_koefs(x11, y11, x12, y12)
    a2, b2, c2 = line_koefs(x21, y21, x22, y22)

    print(c1, c2)

    angle = (a1*a2 + b1*b2) / (sqrt(a1*a1 + b1*b1) * sqrt(a2*a2 + b2*b2))

    return degrees(acos(angle))


def find_scale(rem_data):
    '''
        Функция для нахождения коэффициента масштабирования (используя все точки полотна)
    '''
    if (rem_data[6][0] != rem_data[7][0]): # добавить точку пересечения с осью игрик (если она есть, а ее не будет при равенстве иксов)
        x_axis, y_axis = check_lines_intersection(rem_data[6][0], rem_data[6][1], rem_data[7][0], rem_data[7][1], 0, 0, 0, 1)
        coords = []
        coords.append(x_axis)
        coords.append(y_axis)
        rem_data.append(coords)
    
    x_min = rem_data[0][0]
    y_min = rem_data[0][1]
    x_max = rem_data[0][0]
    y_max = rem_data[0][1]

    for point in rem_data:
        if (point[0] < x_min):
            x_min = point[0]
        if (point[1] < y_min):
            y_min = point[1]
        if (point[0] > x_max):
            x_max = point[0]
        if (point[1] > y_max):
            y_max = point[1]

    if y_min > 0:
        y_min = -1
    if x_min > 0:
        x_min = -1
    if x_max < 0:
        x_max = 1
    if y_max < 0:
        y_max = 1

    k_x = (PLACE_TO_DRAW * CV_WIDE) / (x_max - x_min)
    k_y = (PLACE_TO_DRAW * CV_HEIGHT) / (y_max - y_min)

    return min(k_x, k_y), x_min, y_min


def draw_axises(x_min, y_min, k, color):
    '''
        Функция для отрисовки осей координат
    '''
    x_axis_x1, x_axis_y1 = translate_point(CV_WIDE, 0, x_min, y_min, k)
    x_axis_x2, x_axis_y2 = translate_point(-CV_WIDE, 0, x_min, y_min, k)

    y_axis_x1, y_axis_y1 = translate_point(0 , CV_HEIGHT, x_min, y_min, k)
    y_axis_x2, y_axis_y2 = translate_point(0, -CV_HEIGHT, x_min, y_min, k)

    print(x_axis_x1, x_axis_x2, y_axis_y1, y_axis_y2)

    # Coord lines
    canvas_win.create_line(-CV_WIDE, -x_axis_y1 + CV_HEIGHT, CV_WIDE, -x_axis_y2 + CV_HEIGHT, width = 4, fill = color)
    canvas_win.create_line(y_axis_x1, -CV_HEIGHT, y_axis_x2, CV_HEIGHT, width = 4, fill = color)


def draw_result_line(rem_data, x_min, y_min, k, color):
    '''
        Функция для отрисовки линии, соединяющей точки пересечения биссектрис двух треугольников, а также пересекающей ось OY
    '''

    if (rem_data[6][0] == rem_data[7][0]) and (rem_data[6][1] == rem_data[7][1]): # наложение точек пересечения биссектрис
        return

    x1_c, y1_c = translate_point(rem_data[6][0], rem_data[6][1], x_min, y_min, k)
    x2_c, y2_c = translate_point(rem_data[7][0], rem_data[7][1], x_min, y_min, k)
    
    if (rem_data[6][0] == rem_data[7][0]): # треугольники друг над другом
        canvas_win.create_line(x1_c, -CV_HEIGHT, x2_c, CV_HEIGHT, width = 4, fill = color)
    else:
        x_axis, y_axis = check_lines_intersection(rem_data[6][0], rem_data[6][1], rem_data[7][0], rem_data[7][1], 0, 0, 0, 1)
        x_axis, y_axis = translate_point(x_axis, y_axis, x_min, y_min, k)

        canvas_win.create_line(x1_c, -y1_c + CV_HEIGHT, x2_c, -y2_c + CV_HEIGHT, width = 4, fill = color) # centers

        canvas_win.create_line(x1_c, -y1_c + CV_HEIGHT, x_axis, -y_axis + CV_HEIGHT, width = 4, fill = color) # axis and one of centers

    canvas_win.create_oval(x1_c - POINT_RAD, -(y1_c - POINT_RAD) + CV_HEIGHT, x1_c + POINT_RAD, -(y1_c + POINT_RAD) + CV_HEIGHT, width = 1, outline = "red", fill = "red")
    canvas_win.create_oval(x2_c - POINT_RAD, -(y2_c - POINT_RAD) + CV_HEIGHT, x2_c + POINT_RAD, -(y2_c + POINT_RAD) + CV_HEIGHT, width = 1, outline = "red", fill = "red")


def draw_result(rem_data):
    '''
        Функция для вызова отрисовщиков всех необходимых объектов
    '''
    k, x_min, y_min = find_scale(rem_data)

    # Coord lines
    draw_axises(x_min, y_min, k, AXIS_COLOR)

    # Biseks
    build_biseks(rem_data[0][0], rem_data[0][1],rem_data[1][0], rem_data[1][1], rem_data[2][0], rem_data[2][1], x_min, y_min, k, BISEKS_1_COLOR)

    build_biseks(rem_data[3][0], rem_data[3][1],rem_data[4][0], rem_data[4][1], rem_data[5][0], rem_data[5][1], x_min, y_min, k, BISEKS_2_COLOR)

    # Triangles
    build_triangle(rem_data[0][0], rem_data[0][1], rem_data[0][2], rem_data[1][0], rem_data[1][1], rem_data[1][2], rem_data[2][0], rem_data[2][1], rem_data[2][2], x_min, y_min, k, TRIANGLE_1_COLOR, POINT_NAME_COLOR)

    build_triangle(rem_data[3][0], rem_data[3][1], rem_data[3][2], rem_data[4][0], rem_data[4][1], rem_data[4][2], rem_data[5][0], rem_data[5][1], rem_data[5][2], x_min, y_min, k, TRIANGLE_2_COLOR, POINT_NAME_COLOR)

    # Connection of centers
    draw_result_line(rem_data, x_min, y_min, k, RESULT_LINE_COLOR)


def print_result(angle, x1_c, y1_c, x2_c, y2_c):
    '''
        Функция для вывода результатов вычисления (минимального угла), а также обозначения всех линий на холсте
    '''

    if (angle == 180):
        messagebox.showinfo("Угол", "Нельзя вычислить угол, так как ось OY и прямая, соединяющая центры пересечения биссектрис двух треугольников, параллельны)")
        return

    res_win = Tk()
    res_win.title("Результаты")
    res_win.geometry("850x400")
    res_win.resizable(False, False)

    res_label = Label(res_win, text = "Результаты", font="-family {Consolas} -size 14", fg = "black")
    res_label.place(x = 400, y = 15)

    triangle1_label = Label(res_win, text = "Треугольник из первого множества", font="-family {Consolas} -size 14", fg = TRIANGLE_1_COLOR)
    triangle1_label.place(x = 100, y = 50)

    biseks1_label = Label(res_win, text = "Биссектрисы первого треугольника", font="-family {Consolas} -size 14", fg = BISEKS_1_COLOR)
    biseks1_label.place(x = 100, y = 75)

    intersec1_label = Label(res_win, text = "Точка пересечения биссектрис - [%3.1f;%3.1f]" %(x1_c, y1_c) , font="-family {Consolas} -size 14", fg = "black")
    intersec1_label.place(x = 100, y = 100)

    triangle2_label = Label(res_win, text = "Треугольник из второго множества", font="-family {Consolas} -size 14", fg = TRIANGLE_2_COLOR)
    triangle2_label.place(x = 100, y = 140)

    biseks2_label = Label(res_win, text = "Биссектрисы второго треугольника", font="-family {Consolas} -size 14", fg = BISEKS_2_COLOR)
    biseks2_label.place(x = 100, y = 165)

    intersec2_label = Label(res_win, text = "Точка пересечения биссектрис - [%3.1f;%3.1f]" %(x2_c, y2_c) , font="-family {Consolas} -size 14", fg = "black")
    intersec2_label.place(x = 100, y = 190)

    result_line_label = Label(res_win, text = "Линия, соединяющая точки пересечения\n     биссектрис двух треугольников", font="-family {Consolas} -size 14", fg = RESULT_LINE_COLOR)
    result_line_label.place(x = 100, y = 230)

    axis_label = Label(res_win, text = "Оси координат (декартовые)", font="-family {Consolas} -size 14", fg = AXIS_COLOR)
    axis_label.place(x = 100, y = 290)


    angle_label = Label(res_win, text = "ОТВЕТ: угол между линией, соединяющей точки пересечения биссектрис двух\n треугольников, и осью OY равен   %3.2f   градусов" %(angle), font="-family {Consolas} -size 14", fg = "black")
    angle_label.place(x = 50, y = 350)

    res_win.mainloop()



def solution(dots1_list, dots2_list):
    '''
        Функция для нахождения минимального угла между осью OY и прямой, соединяющей точки пересечения биссектрис двух треугольников, путем полного перебора. Также вызывет функцию, выводящую результат на экран
    '''
    canvas_win.delete("all")

    if (len(dots1_list) < 3):
        messagebox.showerror("Ошибка", "Недостаточно точек для построения треугольника по координатам из первого множества")
        return
    elif (len(dots2_list) < 3):
        messagebox.showerror("Ошибка", "Недостаточно точек для построения треугольника по координатам из второго множества")
        return

    dots1_combs = list(combinations(dots1_list, 3))
    dots2_combs = list(combinations(dots2_list, 3))

    min_angle = 180

    flag = 0
    solved = 0

    for item1 in dots1_combs:
        for item2 in dots2_combs:
            x11 = item1[0][0]; y11 = item1[0][1]
            x12 = item1[1][0]; y12 = item1[1][1]
            x13 = item1[2][0]; y13 = item1[2][1]
            x21 = item2[0][0]; y21 = item2[0][1]
            x22 = item2[1][0]; y22 = item2[1][1]
            x23 = item2[2][0]; y23 = item2[2][1] 

            if (check_triangle(x11, y11, x12, y12, x13, y13) == 0):
                flag = 1
            elif (check_triangle(x21, y21, x22, y22, x23, y23) == 0):
                flag = 2
            else:
                solved = 1
                x10, y10 = find_bisseks_intersection(x11, y11, x12, y12, x13, y13)
                x20, y20 = find_bisseks_intersection(x21, y21, x22, y22, x23, y23)

                #print("\n\n\n", x10, y10, x20, y20, "\n\n\n")

                if (x10 == x20) and (y10 == y20):
                    solved = 2 # наложение точек пересечения биссектрис

                    if (min_angle == 180): # при наличии нужного решения не следует менять набор точек для построения
                        rem_data = [[x11, y11, item1[0][2]], [x12, y12, item1[1][2]], [x13, y13, item1[2][2]], [x21, y21, item2[0][2]], [x22, y22, item2[1][2]], [x23, y23, item2[2][2]], [x10, y10], [x20, y20], [0, 0]]
                else:
                    angle = find_angle_between_two_lines(x10, y10, x20, y20, 0, 0, 0, 1)

                    if (angle > 90):
                        angle = 180 - angle

                    print("\n\nangle = ", angle, ", min_angle = ", min_angle, "\n\n")

                    if (angle < min_angle):
                        min_angle = angle

                        if (min_angle == 0):
                            min_angle = 180

                        rem_data = [[x11, y11, item1[0][2]], [x12, y12, item1[1][2]], [x13, y13, item1[2][2]], [x21, y21, item2[0][2]], [x22, y22, item2[1][2]], [x23, y23, item2[2][2]], [x10, y10], [x20, y20], [0, 0]]

    if (flag == 1) and (solved == 0):
        messagebox.showerror("Ошибка", "Невозможно построить треугольник по заданным кооридинатам из первого множества")
        return
    elif (flag == 2) and (solved == 0):
        messagebox.showerror("Ошибка", "Невозможно построить треугольник по заданным кооридинатам из второго множества")
        return

    if (solved == 2) and (min_angle == 180):
        draw_result(rem_data)
        messagebox.showinfo("Ошибка", "Точки пересечения биссектрис треугольников наложились друг на друга, следовательно невозможно построить прямую, соединяющую их центры")
        return

    draw_result(rem_data)

    print_result(min_angle, rem_data[6][0], rem_data[6][1], rem_data[7][0], rem_data[7][1])



if __name__ == "__main__":
    '''
        Тело программы, организующее работу главного окна
    '''

    dots1_list = []
    dots2_list = []

    win = Tk()
    win['bg'] = 'orange'
    win.geometry("%dx%d" %(WIN_WIDTH, WIN_HEIGHT))
    win.title("Лабораторная работа #1 (Цветков И.А. ИУ7-43Б)")
    win.resizable(False, False)

    canvas_win = Canvas(win, width = CV_WIDE, height = CV_HEIGHT, bg = "#fff3e6")
    canvas_win.place(x = 300, y = 0)

    # Множество точек 1
    dots1_label = Label(text = "Множество точек 1", bg = 'orange', font="-family {Consolas} -size 18")
    dots1_label.place(x = 30, y = 10)

    dots1_block = Listbox(bg = "#fff3e6")
    dots1_block.configure(height = 15, width = 25)
    dots1_block.configure(font="-family {Consolas} -size 14")
    dots1_block.place(x = 10, y = 50)

    add1 = Button(text = "Добавить", width = 9, height = 2,  font="-family {Consolas} -size 14", command = lambda: add_dot(dots1_block, dots1_list))
    add1.place(x = 10, y = 430)

    del1 = Button(text = "Удалить", width = 9, height = 2, font="-family {Consolas} -size 14", command = lambda: del_dot(dots1_block, dots1_list))
    del1.place(x = 160, y = 430)

    chg1 = Button(text = "Изменить", width = 9, height = 2, font="-family {Consolas} -size 14", command = lambda: change_dot(dots1_block, dots1_list))
    chg1.place(x = 10, y = 500)

    del_all1 = Button(text = "Очистить\nвсё", width = 9, height = 2, font="-family {Consolas} -size 14", command = lambda: del_all_dots(dots1_block, dots1_list))
    del_all1.place(x = 160, y = 500)

    # Множество точек 2
    dots2_label = Label(text = "Множество точек 2", bg = 'orange', font="-family {Consolas} -size 18")
    dots2_label.place(x = 30 + CV_WIDE + 300, y = 10)

    dots2_block = Listbox(bg = "#fff3e6")
    dots2_block.configure(height = 15, width = 25)
    dots2_block.configure(font="-family {Consolas} -size 14")
    dots2_block.place(x = 10 + CV_WIDE + 300, y = 50)

    add2 = Button(text = "Добавить", width = 9, height = 2,  font="-family {Consolas} -size 14", command = lambda: add_dot(dots2_block, dots2_list))
    add2.place(x = 10 + CV_WIDE + 300, y = 430)

    del2 = Button(text = "Удалить", width = 9, height = 2, font="-family {Consolas} -size 14", command = lambda: del_dot(dots2_block, dots2_list))
    del2.place(x = 160 + CV_WIDE + 300, y = 430)

    chg2 = Button(text = "Изменить", width = 9, height = 2, font="-family {Consolas} -size 14", command = lambda: change_dot(dots2_block, dots2_list))
    chg2.place(x = 10 + CV_WIDE + 300, y = 500)

    del_all2 = Button(text = "Очистить\nвсё", width = 9, height = 2, font="-family {Consolas} -size 14", command = lambda: del_all_dots(dots2_block, dots2_list))
    del_all2.place(x = 160 + CV_WIDE + 300, y = 500)

    solve = Button(text = "Решить задачу", width = 23, height = 2, font="-family {Consolas} -size 14", command = lambda: solution(dots1_list, dots2_list))
    solve.place(x = 10 + CV_WIDE + 300, y = 700)

    task = Button(text = "Вывести условие задачи", width = 23, height = 2, font="-family {Consolas} -size 14", command = lambda: messagebox.showinfo("Задание", TASK))
    task.place(x = 10, y = 700)

    win.mainloop()