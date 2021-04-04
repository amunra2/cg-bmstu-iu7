'''
    Bresenham method for circle and ellipse
'''

from math import sqrt


def add_dots_bres_circle(dots, dot_c, dot_dif, color):
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

    edge = round(radius / sqrt(2))

    dots = []

    eps = 0

    while (y > edge):

        add_dots_bres_circle(dots, [x_c, y_c], [x, y], color)

        if (delta_i < 0):
            eps = 2 * delta_i + 2 * y - 1

            if (eps <= 0):
                param = 1
            else:
                param = 2
        elif (delta_i > 0):
            eps = 2 * delta_i - 2 * x - 1

            if (eps <= 0):
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


def add_dots_bres_ellipse(dots, dot_c, dot_dif, color):
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

    r_a = rad[0] * rad[0]
    r_b = rad[1] * rad[1]

    delta_i = r_a + r_b - r_a * (2 * y)

    dots = []

    eps = 0

    while (y >= 0):

        add_dots_bres_ellipse(dots, [x_c, y_c], [x, y], color)

        if (delta_i < 0):
            eps = 2 * delta_i + (2 * y - 1) * r_a

            if (eps <= 0):
                param = 1
            else:
                param = 2
        elif (delta_i > 0):
            eps = 2 * delta_i + (- 2 * x - 1) * r_b

            if (eps <= 0):
                param = 2
            else:
                param = 3
        else:
            param = 2

        if (param == 1):
            x = x + 1
            delta_i = delta_i + (2 * x) * r_b + r_b
        elif (param == 2):
            x = x + 1
            y = y - 1
            delta_i = delta_i + (2 * x) * r_b - (2 * y + 2) * r_a + (r_a + r_b)
        else:
            y = y - 1
            delta_i = delta_i - (2 * y + 2) * r_a + r_a


    return dots