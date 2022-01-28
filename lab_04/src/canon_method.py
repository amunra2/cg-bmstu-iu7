from math import sqrt

from draw import draw_pixel, draw_dots_circle, draw_dots_ellipse




def canon_circle(canvas_win, dot_c, radius, color, draw):
    
    x_c = dot_c[0]
    y_c = dot_c[1]

    edge = round(radius / sqrt(2))

    double_radius = radius * radius

    x = 0

    while (x <= edge):
        y = round(sqrt(double_radius - x * x))

        if draw:
            draw_dots_circle(canvas_win, [x_c, y_c], [x, y], color)

        x += 1


def canon_ellips(canvas_win, dot_c, rad, color, draw):
    x_c = dot_c[0]
    y_c = dot_c[1]

    r_a = rad[0]
    r_b = rad[1]

    double_ra = r_a * r_a
    double_rb = r_b * r_b

    edge = round(double_ra / sqrt(double_ra + double_rb))

    x = 0

    while (x <= edge):
        y = round(sqrt(1 - x * x / double_ra) * r_b)

        if draw:
            draw_dots_ellipse(canvas_win, [x_c, y_c], [x, y], color)

        x += 1

    edge = round(double_rb / sqrt(double_ra + double_rb))

    y = 0

    while (y <= edge):
        x = round(sqrt(1 - y * y / double_rb) * r_a)

        if draw:   
            draw_dots_ellipse(canvas_win, [x_c, y_c], [x, y], color)

        y += 1
    