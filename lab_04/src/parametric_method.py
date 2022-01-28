'''
    Parametric method for circle and ellipse
'''


from math import sqrt, pi, cos, sin

from draw import draw_dots_circle, draw_dots_ellipse


def parametric_circle(canvas_win, dot_c, radius, color, draw):
    x_c = dot_c[0]
    y_c = dot_c[1]

    step = 1 / radius

    alpha = 0

    while (alpha < pi / 4 + step):
        x = round(radius * cos(alpha))
        y = round(radius * sin(alpha))

        if draw:
            draw_dots_circle(canvas_win, [x_c, y_c], [x, y], color)

        alpha += step



def parametric_ellips(canvas_win, dot_c, rad, color, draw):
    x_c = dot_c[0]
    y_c = dot_c[1]

    if (rad[0] > rad[1]):
        step = 1 / rad[0]
    else:
        step = 1 / rad[1]

    alpha = 0

    while (alpha < pi / 2 + step):
        x = round(rad[0] * cos(alpha))
        y = round(rad[1] * sin(alpha))

        if draw:
            draw_dots_ellipse(canvas_win, [x_c, y_c], [x, y], color)

        alpha += step