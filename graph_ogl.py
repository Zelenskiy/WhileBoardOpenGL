import math

# import pyautogui
# from tkinter import colorchooser

# import numpy as np
import pyglet
from pyglet.gl import *


def close_cross(x0, y0, x, y, color=(1, 0, 0, 1), thickness=1):
    draw_line(x0 + 4, y0 + 4, x - 4, y - 4, color, thickness)
    draw_line(x0 + 4, y - 4, x - 4, y0 + 4, color, thickness)


def resize_arr(x0, y0, x, y, color=(1, 0, 0, 1), thickness=1):
    draw_line(x0, y0, x, y, color, thickness)
    draw_line(x0, y0, x0, y0 - 10, color, thickness)
    draw_line(x0, y0, x0 + 10, y0, color, thickness)
    draw_line(x - 10, y, x, y, color, thickness)
    draw_line(x, y + 10, x, y, color, thickness)


"""
function HightBright(ColorPen:TColor; ColorFon:TColor; c:real):TColor;
var r, g, b: Byte;
    rf, gf, bf: Byte;
    rt, gt, bt:real;
begin
    ColorToRgb(ColorPen, r, g, b);
    ColorToRgb(ColorFon, rf, gf, bf);
    if r<rf  then rt := 1-c else rt := c;
    if g<gf  then gt := 1-c else gt := c;
    if b<bf  then bt := 1-c else bt := c;
    r := round(abs(rf-r) * (rt) + min(r,rf));
    g := round(abs(gf-g) * (gt) + min(g,gf));
    b := round(abs(bf-b) * (bt) + min(b,bf));
    HightBright := RGB(r,g,b);
end;

procedure plot(canvas:TCanvas; x, y: integer; c:real);
var penColor, fonColor:TColor;
begin
     penColor := canvas.Pen.Color;
     fonColor := Form1.fonColor;
     //Якшо під низом не колір пензля, то замінюємо його на новий
     if Canvas.Pixels[x,y] <> pen_C then
        Canvas.Pixels[x,y] := HightBright(pen_C, fon_C, c);
end;
  
"""


def hight_bright(color, fon_color, c):
    r, g, b, a = color
    rf, gf, bf, a = fon_color
    if r < rf:
        rt = 1 - c
    else:
        rt = c
    if g < gf:
        gt = 1 - c
    else:
        gt = c
    if b < bf:
        bt = 1 - c
    else:
        bt = c
    # r = round(abs(rf - r) * (rt) + min(r, rf))
    # g = round(abs(gf - g) * (gt) + min(g, gf))
    # b = round(abs(bf - b) * (bt) + min(b, bf))
    r, g, b = (r + rf) / 2, (g + gf) / 2, (b + bf) / 2
    return (r, g, b)


def plot(x, y, c, color, fon_color):
    c = hight_bright(color, fon_color, c)
    r, g, b = c
    glColor3f(r, g, b)
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()
    glFlush()


def ipart(x):
    return math.floor(x);


def round_(x):
    return ipart(x + 0.5)


def fpart(x):
    return x - math.floor(x)


def rfpart(x):
    return 1.0 - fpart(x)

def draw_line_1( x0,  y0, x1,  y1, color,thickness=1, smooth=False):
    if smooth:
        draw_vu_line(x0, y0, x1, y1, color, thickness)
    else:
        draw_line(x0, y0, x1, y1, color, thickness)



def draw_vu_line(x0, y0, x1, y1, color, thickness=1):
    r,g,b,a = color
    pyglet.gl.glColor4f(r, g, b, a)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH);
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    glLineWidth(thickness)
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                         ('v2i', (int(x0), int(y0), int(x1), int(y1))))


# def draw_vu_line(x1, y1, x2, y2, color, fon_color):
#     dx = x2 - x1
#     dy = y2 - y1
#     if dx == 0: dx = 1
#     gradient = dy / dx
#     steep = abs(dy) > abs(dx)
#
#     if steep:
#         x1, y1 = y1, x1
#         x2, y2 = y2, x2
#
#     if x2 < x1:
#         x1, x2 = x2, x1
#         y1, y2 = y2, y1
#
#     dx = x2 - x1
#     dy = y2 - y1
#     if dx == 0: dx = 1
#     gradient = dy / dx
#
#     # handle first endpoint
#     xend = round(x1)
#     yend = y1 + gradient * (xend - x1)
#     xgap = rfpart(x1 + 0.5)
#     xpxl1 = xend  # this will be used in the main loop
#     ypxl1 = ipart(yend)
#
#     if (steep):  # устанавливаем 2 пикселя с разной прозрачностью
#         plot(ypxl1, xpxl1, rfpart(yend) * xgap, color, fon_color)
#         plot(ypxl1 + 1, xpxl1, fpart(yend) * xgap, color, fon_color)
#     else:
#         plot(xpxl1, ypxl1, rfpart(yend) * xgap, color, fon_color)
#         plot(xpxl1, ypxl1 + 1, fpart(yend) * xgap, color, fon_color)
#
#     # сохраняем для основного цикла
#     intery = yend + gradient
#
#     # обработка конца отрезка(аналогично началу)
#     xend = round(x2)
#     yend = y2 + gradient * (xend - x2)
#     xgap = fpart(x2 + 0.5)
#
#     xpxl2 = xend;
#     ypxl2 = ipart(yend);
#
#     if (steep):
#         plot(ypxl2, xpxl2, rfpart(yend) * xgap, color, fon_color)
#         plot(ypxl2 + 1, xpxl2, fpart(yend) * xgap, color, fon_color)
#     else:
#         plot(xpxl2, ypxl2, rfpart(yend) * xgap, color, fon_color)
#         plot(xpxl2, ypxl2 + 1, fpart(yend) * xgap, color, fon_color)
#
#     # основной цикл
#     for x in range(xpxl1 + 1, xpxl2):
#         if (steep):  # устанавливаем 2 пикселя с разной прозрачностью в зависимости от удаленности от отрезка
#             plot(ipart(intery), x, rfpart(intery), color, fon_color)
#             plot(ipart(intery) + 1, x, fpart(intery), color, fon_color)
#         else:
#             plot(x, ipart(intery), rfpart(intery), color, fon_color)
#             plot(x, ipart(intery) + 1, fpart(intery), color, fon_color)
#
#         intery = intery + gradient


def draw_arrow_head(X, Y, Angle, LW, arrow, color, fon_color, thickness):
    Beta = 0.322
    LineLen = 4.74 * thickness
    CentLen = 3
    Angle = math.pi + Angle
    # print("thickness - ", thickness)

    A1 = Angle - Beta
    A2 = Angle + Beta
    x1, y1 = X, Y
    x2, y2 = X + int(LineLen * LW * math.cos(A1)), Y - int(LineLen * LW * math.sin(A1))
    x3, y3 = X + int(CentLen * LW * math.cos(Angle)), Y - int(CentLen * LW * math.sin(Angle))
    x4, y4 = X + int(LineLen * LW * math.cos(A2)), Y - int(LineLen * LW * math.sin(A2))
    draw_fill_circle(x1, y1, int(thickness * 1.2), fon_color)
    fill_4poly(x1, y1, x2, y2, x3, y3, x4, y4, color)

# def draw_Line(x1, y1, x2, y2, color, fon_color, thickness=1):
#     pen_W = thickness
#     pen_C = color
#     fon_C = fon_color
#     r = pen_W // 2
#     dx = abs(x1 - x2)
#     dy = abs(y1 - y2);
#     len = math.sqrt(dx ** 2 + dy ** 2)
#     if len == 0: len = 1
#     sin_a = dx / len
#     cos_a = dy / len
#     rc = r * cos_a
#     if (y1 - y2) * (x1 - x2) < 0:
#         rs = r * sin_a
#     else:
#         rs = - r * sin_a
#     x11 = round(x1 - rc)
#     x12 = round(x1 + rc)
#     y11 = round(y1 - rs)
#     y12 = round(y1 + rs)
#     x21 = round(x2 - rc)
#     x22 = round(x2 + rc)
#     y21 = round(y2 - rs)
#     y22 = round(y2 + rs)
#     draw_vu_line(x11, y11, x21, y21, color, fon_color)
#     draw_vu_line(x12, y12, x22, y22, color, fon_color)
#     # draw_line(x1, y1, x2, y2, color, thickness)

def draw_line(x0, y0, x, y, color=(1, 0, 0, 1), thickness=1):
    glColor4f(*color)
    glLineWidth(thickness)
    glBegin(GL_LINES)
    glVertex2f(x0, y0)
    glVertex2f(x, y)
    glEnd()


def draw_line_mod(x0, y0, x, y, color=(1, 0, 0, 1), fon_color=(1, 0, 0, 1), thickness=4, arrow=0, dash=(1, 0)):
    # print ("thickness - ", thickness)
    # glColor4f(*color)
    # glLineWidth(thickness)
    # glBegin(GL_LINES)
    # glVertex2f(x0, y0)
    # glVertex2f(x, y)
    # glEnd()
    draw_line_1(x0, y0, x, y, color, thickness=thickness)
    # Рисуємо стрілки
    LW = 1
    if arrow == 3:
        angle = math.atan2(y0 - y, x - x0)
        draw_arrow_head(x, y, angle, LW, arrow, color, fon_color, thickness)
    elif arrow == 2:
        angle = math.atan2(y - y0, x0 - x)
        draw_arrow_head(x0, y0, angle, LW, arrow, color, fon_color, thickness)
    elif arrow == 1:
        angle = math.atan2(y0 - y, x - x0)
        draw_arrow_head(x, y, angle, LW, arrow, color, fon_color, thickness)
        angle = math.atan2(y - y0, x0 - x)
        draw_arrow_head(x0, y0, angle, LW, arrow, color, fon_color, thickness)


# def rectangle_vulg(x0, y0, x, y, color=(1, 0, 0, 1), thickness=1):
#     # x0,y0 = x0-10,y0-10
#     glColor4f(*color)
#     glLineWidth(thickness)
#     glBegin(GL_LINES)
#     glVertex2f(x0, y0)
#     glVertex2f(x, y0)
#     glEnd()
#     glBegin(GL_LINES)
#     glVertex2f(x, y0)
#     glVertex2f(x, y)
#     glEnd()
#     glBegin(GL_LINES)
#     glVertex2f(x, y)
#     glVertex2f(x0, y)
#     glEnd()
#     glBegin(GL_LINES)
#     glVertex2f(x0, y)
#     glVertex2f(x0, y0)
#     glEnd()
def draw_ramka_top(x0, y0, x, y, color=(1, 0, 0, 1), thickness=1):
    glColor4f(*color)
    glLineWidth(thickness)
    glBegin(GL_LINES)
    glVertex2f(x0, y - 10)
    glVertex2f(x0, y)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(x0, y)
    glVertex2f(x0 + 10, y)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(x - 10, y)
    glVertex2f(x, y)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x, y - 10)
    glEnd()


def draw_circle(x0, y0, r, color=(0, 0, 0, 1), thickness=1):
    numPoints = 200
    verts = []
    for i in range(numPoints):
        angle = math.radians(float(i) / numPoints * 360.0)
        x = r * math.cos(angle) + x0
        y = r * math.sin(angle) + y0
        verts += [x, y]
    glLineWidth(thickness)
    circle = pyglet.graphics.vertex_list(numPoints, ('v2f', verts))
    glColor4f(*color)
    circle.draw(GL_LINE_LOOP)


def draw_regular_polygon(x0, y0, r, numPoints=3, angleStart=90, color=(0, 0, 0, 1), thickness=1):
    verts = []
    for i in range(numPoints):
        angle = math.radians(float(i) / numPoints * 360.0 + angleStart)
        x = r * math.cos(angle) + x0
        y = r * math.sin(angle) + y0
        verts += [x, y]
    glLineWidth(thickness)
    circle = pyglet.graphics.vertex_list(numPoints, ('v2f', verts))
    glColor4f(*color)
    circle.draw(GL_LINE_LOOP)


def draw_fill_regular_polygon(x0, y0, r, numPoints=3, angleStart=90, color=(0, 0, 0, 1), thickness=1):
    verts = []
    xstart, ystart = x0, y0
    for i in range(numPoints):
        angle = math.radians(float(i) / numPoints * 360.0 + angleStart)
        x = r * math.cos(angle) + x0
        y = r * math.sin(angle) + y0
        verts += [x, y]
        fill_3poly(x0, y0, x, y, xstart, ystart, color)
        xstart, ystart = x, y
    fill_3poly(x0, y0, x, y, verts[0], verts[1], color)
    glLineWidth(thickness)
    circle = pyglet.graphics.vertex_list(numPoints, ('v2f', verts))
    glColor4f(*color)
    circle.draw(GL_LINE_LOOP)


def draw_fill_circle(x0, y0, r, color=(0, 0, 0, 1), thickness=1):
    numPoints = r * 10
    verts = []
    for i in range(numPoints):
        angle = math.radians(float(i) / numPoints * 360.0)
        x = r * math.cos(angle) + x0
        y = r * math.sin(angle) + y0
        verts += [x, y]
        draw_line(x0, y0, x, y, color=color, thickness=1)
    glLineWidth(thickness)
    circle = pyglet.graphics.vertex_list(numPoints, ('v2f', verts))
    glColor4f(*color)
    circle.draw(GL_LINE_LOOP)


def draw_rectangle(x1, y1, x2, y2, x3, y3, x4, y4, color=(1, 0, 0, 1), thickness=1):
    glColor4f(*color)
    glLineWidth(thickness)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(x3, y3)
    glVertex2f(x4, y4)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(x4, y4)
    glVertex2f(x1, y1)
    glEnd()


def draw_fill_rectangle(x1, y1, x2, y2, color):
    r, g, b, a = color
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x1, y1, x2, y1, x2, y2, x1, y2]),
                         ('c3f', [r, g, b, r, g, b, r, g, b, r, g, b]))


def fill_4poly(x1, y1, x2, y2, x3, y3, x4, y4, color):
    r, g, b, a = color
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x1, y1, x2, y2, x3, y3, x4, y4]),
                         ('c3f', [r, g, b, r, g, b, r, g, b, r, g, b]))


def fill_3poly(x1, y1, x2, y2, x3, y3, color=(0, 0, 0, 1)):
    r, g, b, a = color
    pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES, ('v2f', [x1, y1, x2, y2, x3, y3]),
                         ('c3f', [r, g, b, r, g, b, r, g, b]))


class Quad:
    def __init__(self, x, y, w, h):
        self.indices = [0, 1, 2, 2, 3, 0]
        self.vertex = [-0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.5, 0.5, 0.0, -0.5, 0.5, 0.0]
        self.color = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, ]

    def render(self):
        self.vertices = pyglet.graphics.draw_indexed(4, GL_TRIANGLES, self.indices, ('v3f', self.vertex),
                                                     ('c3f', self.color))


def dist(x0, y0, x, y, r):
    d = math.sqrt((x - x0) ** 2 + (y - y0) ** 2)
    return d < r


def mediana(x1, x2):
    return abs(x1 + x2) // 2


def border_polyline(points):
    # print(points)
    if points == []:
        return 0, 0, 0, 0
    x_min = points[0]['x']
    y_min = points[0]['y']
    x_max = points[0]['x']
    y_max = points[0]['y']
    for p in points:
        if p['x'] > x_max:
            x_max = p['x']
        if p['y'] > y_max:
            y_max = p['y']
        if p['x'] < x_min:
            x_min = p['x']
        if p['y'] < y_min:
            y_min = p['y']

    return x_min, y_min, x_max, y_max

# class MyFloatWindow(pyglet.window.Window):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def on_key_press(self, symbol, modifiers):
#         print("aaaaaaaaa")
#

# class DlgWindow(pyglet.window.Window):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.set_location(50,100)
#
#
#
#     def on_mouse_press(self, x, y, button, modifiers):
#         window.insert_screenshot()
#         winPanel.close()
#
#
#     def on_close(self):
#         window.set_visible(True)
