'''
    Parametric method for circle and ellipse
'''


from math import sqrt, pi, cos, sin

from bresenham_method import add_dots_circle, add_dots_ellipse


def parametric_circle(dot_c, radius, color):
    x_c = dot_c[0]
    y_c = dot_c[1]

    step = 1 / radius

    alpha = 0
    dots = []

    while (alpha < pi / 4 + step):
        x = round(radius * cos(alpha))
        y = round(radius * sin(alpha))

        add_dots_circle(dots, [x_c, y_c], [x, y], color)

        alpha += step

    return dots


def parametric_ellips(dot_c, rad, color):
    x_c = dot_c[0]
    y_c = dot_c[1]

    if (rad[0] > rad[1]):
        step = 1 / rad[0]
    else:
        step = 1 / rad[1]

    alpha = 0
    dots = []

    while (alpha < pi / 2 + step):
        x = round(rad[0] * cos(alpha))
        y = round(rad[1] * sin(alpha))

        add_dots_ellipse(dots, [x_c, y_c], [x, y], color)

        alpha += step

    return dots