'''
    Method of Middle Dot for cyrcle and ellipse
'''

from math import sqrt

from bresenham_method import add_dots_circle, add_dots_ellipse


def mid_dot_circle(dot_c, radius, color):

    x_c = dot_c[0]
    y_c = dot_c[1]

    x = 0
    y = radius

    delta = 1 - radius

    dots = []

    while (x <= y):
        add_dots_circle(dots, [x_c, y_c], [x, y], color)

        x += 1

        if (delta < 0):
            delta = delta + 2 * x + 1
        else:
            y -= 1
            delta = delta + 2 * (x - y) + 1

    return dots


def mid_dot_ellipse(dot_c, rad, color):

    x_c = dot_c[0]
    y_c = dot_c[1]

    x = 0
    y = rad[1]

    r_a_2 = rad[0] * rad[0]
    r_b_2 = rad[1] * rad[1]

    edge = round(rad[0] / sqrt(1 + r_b_2 / r_a_2))

    delta = r_b_2 - round(r_a_2 * (rad[1] - 1 / 4))

    dots = []

    while (x <= edge):
        add_dots_ellipse(dots, [x_c, y_c], [x, y], color)

        if (delta > 0):
            y -= 1
            delta = delta - r_a_2 * y * 2

        x += 1

        delta = delta + r_b_2 * (2 * x + 1)

    x = rad[0]
    y = 0

    r_a_2 = rad[0] * rad[0]
    r_b_2 = rad[1] * rad[1]

    edge = round(rad[1] / sqrt(1 + r_a_2 / r_b_2))

    delta = r_a_2 - round(r_b_2 * (x - 1 / 4))

    while (y <= edge):
        add_dots_ellipse(dots, [x_c, y_c], [x, y], color)

        if (delta > 0):
            x -= 1
            delta = delta - r_b_2 * x * 2

        y += 1

        delta = delta + r_a_2 * (2 * y + 1)

    return dots    



