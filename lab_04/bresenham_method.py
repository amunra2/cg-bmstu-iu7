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

    dots = []

    eps = 0

    while (x < y + 1):

        add_dots_bres_circle(dots, [x_c, y_c], [x, y], color)

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

    r_a_2 = rad[0] * rad[0]
    r_b_2 = rad[1] * rad[1]

    #delta_i = r_a + r_b - r_a * (2 * y)
    delta_i = r_b_2 - r_a_2 * (2 * y + 1)

    dots = []

    eps = 0

    while (y >= 0):

        add_dots_bres_ellipse(dots, [x_c, y_c], [x, y], color)

        if (delta_i < 0):
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


# def reflect_dots_diag(dots, xc, yc):
#     count_dots = len(dots)

#     for i in range(count_dots):
#         dots.append([dots[i][1] - yc + xc, dots[i][0] - xc + yc, dots[i][2]])

# def reflect_dots_Oy(dots, xc):
#     count_dots = len(dots)

#     for i in range(count_dots):
#         dots.append([-(dots[i][0] - xc) + xc, dots[i][1], dots[i][2]])

# def reflect_dots_Ox(dots, yc):
#     count_dots = len(dots)

#     for i in range(count_dots):
#         dots.append([dots[i][0], -(dots[i][1] - yc) + yc, dots[i][2]])
    

# def bresenham_ellipse(dot_c, rad, color):
#     x = 0
#     y = rad[1]
#     dots = [[x + dot_c[0], y + dot_c[1], color]]

#     xc = dot_c[0]
#     yc = dot_c[1]

#     sqr_ra = rad[0] * rad[0]
#     sqr_rb = rad[1] * rad[1]
#     delta = sqr_rb - sqr_ra * (2 * rad[1] + 1)

#     while y >= 0:
#         if delta <= 0:
#             d = 2 * delta + sqr_ra * (y + y + 2)
#             x += 1
#             delta += sqr_rb * (2 * x + 1)

#             if d >= 0:
#                 y -= 1
#                 delta += sqr_ra * (- y - y + 1)
#         else:
#             d = 2 * delta + sqr_rb * (- x - x + 2)
#             y -= 1
#             delta += sqr_ra * (- y - y + 1)

#             if d < 0:
#                 x += 1
#                 delta += sqr_rb * (2 * x + 1)

#         dots.append([x + xc, y + yc, color])

#     reflect_dots_Oy(dots, xc)
#     reflect_dots_Ox(dots, yc)

#     return dots