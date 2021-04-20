




def draw_pixel(canvas_win, dot):
    canvas_win.create_line(dot[0], dot[1], dot[0] + 1, dot[1], fill = dot[2].hex)
    # for dot in dots:
    #    canvas_win.create_line(dot[0], dot[1], dot[0] + 1, dot[1], fill = dot[2].hex)


def draw_dots_circle(canvas_win, dot_c, dot_dif, color):
    x_c = dot_c[0]
    y_c = dot_c[1]

    x = dot_dif[0]
    y = dot_dif[1]

    draw_pixel(canvas_win, [x_c + x, y_c + y, color])
    draw_pixel(canvas_win, [x_c - x, y_c + y, color])
    draw_pixel(canvas_win, [x_c + x, y_c - y, color])
    draw_pixel(canvas_win, [x_c - x, y_c - y, color])

    draw_pixel(canvas_win, [x_c + y, y_c + x, color])
    draw_pixel(canvas_win, [x_c - y, y_c + x, color])
    draw_pixel(canvas_win, [x_c + y, y_c - x, color])
    draw_pixel(canvas_win, [x_c - y, y_c - x, color])


def draw_dots_ellipse(canvas_win, dot_c, dot_dif, color):
    x_c = dot_c[0]
    y_c = dot_c[1]

    x = dot_dif[0]
    y = dot_dif[1]

    draw_pixel(canvas_win, [x_c + x, y_c + y, color])
    draw_pixel(canvas_win, [x_c - x, y_c + y, color])
    draw_pixel(canvas_win, [x_c + x, y_c - y, color])
    draw_pixel(canvas_win, [x_c - x, y_c - y, color])