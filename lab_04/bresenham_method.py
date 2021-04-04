'''
    Bresenham method for circle and ellipse
'''

from math import sqrt


def add_dots_circle(dots, dot_c, dot_dif, color):
    x_c = dot_c[0]
    y_c = dot_c[1]

    x = dot_dif[0]
    y = dot_dif[1]

    dots.append([x_c + x, y_c + y, color])
    dots.append([x_c - x, y_c + y, color])
    dots.append([x_c + x, y_c - y, color])
    dots.append([x_c - x, y_c - y, color])

    dots.append([x_c + y, y_c + x, color])
    dots.append([x_c - y, y_c + x, color])
    dots.append([x_c + y, y_c - x, color])
    dots.append([x_c - y, y_c - x, color])


def bresenham_circle(dot_c, radius, color):

    x_c = round(dot_c[0])
    y_c = round(dot_c[1])

    x = 0
    y = radius

    delta_i = 2 * (1 - radius)

    dots = []

    eps = 0

    while (x < y):

        add_dots_circle(dots, [x_c, y_c], [x, y], color)

        if (delta_i < 0):
            eps = 2 * delta_i + 2 * y - 1

            if (eps < 0):
                param = 1
            else:
                param = 2
        elif (delta_i > 0):
            eps = 2 * delta_i - 2 * x - 1

            if (eps < 0):
                param = 2
            else:
                param = 3
        else:
            param = 2

        if (param == 1):
            x = x + 1
            delta_i = delta_i + 2 * x + 1
        elif (param == 2):
            x = x + 1
            y = y - 1
            delta_i = delta_i + 2 * x - 2 * y + 2
        else:
            y = y - 1
            delta_i = delta_i - 2 * y + 1

    return dots


def add_dots_ellipse(dots, dot_c, dot_dif, color):
    x_c = dot_c[0]
    y_c = dot_c[1]

    x = dot_dif[0]
    y = dot_dif[1]

    dots.append([x_c + x, y_c + y, color])
    dots.append([x_c - x, y_c + y, color])
    dots.append([x_c + x, y_c - y, color])
    dots.append([x_c - x, y_c - y, color])


def bresenham_ellipse(dot_c, rad, color):

    x_c = round(dot_c[0])
    y_c = round(dot_c[1])

    x = 0
    y = rad[1]

    r_a_2 = rad[0] * rad[0]
    r_b_2 = rad[1] * rad[1]

    #delta_i = r_a_2 + r_b_2 - r_a_2 * (2 * y)
    delta_i = r_b_2 - r_a_2 * (2 * y + 1)

    dots = []

    eps = 0

    while (y >= 0):

        add_dots_ellipse(dots, [x_c, y_c], [x, y], color)

        if (delta_i <= 0):
            eps = 2 * delta_i + (2 * y + 2) * r_a_2

            if (eps < 0):
                param = 1
            else:
                param = 2
        elif (delta_i > 0):
            eps = 2 * delta_i + (- 2 * x + 2) * r_b_2

            if (eps < 0):
                param = 2
            else:
                param = 3
        else:
            param = 2

        if (param == 1):
            x = x + 1
            delta_i = delta_i + (2 * x) * r_b_2 + r_b_2
        elif (param == 2):
            x = x + 1
            y = y - 1
            delta_i = delta_i + (2 * x) * r_b_2 - (2 * y) * r_a_2 + (r_a_2 + r_b_2)
        else:
            y = y - 1
            delta_i = delta_i - (2 * y) * r_a_2 + r_a_2


    return dots
