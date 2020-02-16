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


def draw_line_1(x0, y0, x1, y1, color=(0,0,1,1), thickness=1, smooth=False, dash=0):
    if smooth:
        draw_vu_line(x0, y0, x1, y1, color=color, thickness=thickness)
    else:
        if dash == 0:
            draw_line(x0, y0, x1, y1, color=color, thickness=thickness)
        else:
            dx = (x1 - x0)
            dy = (y1 - y0)
            if dx > 0:
                sx = 1
            else:
                sx = -1
            if dy > 0:
                sy = 1
            else:
                sy = -1
            if dx != 0:
                tangle = math.atan(dy / dx)
            else:
                tangle = -sy * math.pi / 2
            x_old, y_old = x0, y0
            if dash == 1:
                dash_len = thickness * 4
            else:
                dash_len = thickness * 1
            dash_len_x = dash_len * math.cos(tangle)
            dash_len_y = dash_len * math.sin(tangle)
            l = math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
            k = int(l / dash_len)
            for e in range(1, k + 2):
                x = x0 + sx * (e * dash_len_x - dash_len_x)
                y = y0 + sx * (e * dash_len_y - dash_len_y)
                if e % 2 != 1:
                    draw_line(x_old, y_old, x, y,  color=color, thickness=thickness)
                x_old, y_old = x, y
            # pass
            # x_old = x0 + sx * (k * dash_len_x - dash_len_x)
            # y_old = y0 + sx * (k * dash_len_y - dash_len_y)
            # draw_line(x_old, y_old, x1, y1, color, thickness)


def draw_vu_line(x0, y0, x1, y1, color=(1,1,1,1), thickness=1):
    r, g, b, a = color
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


def draw_arrow_head(X, Y, Angle, color=(1,1,1,1), thickness=1):
    Beta = 0.322
    # print("Angle ", Angle)
    LineLen = 4.74 * thickness
    CentLen = 3
    Angle = math.pi + Angle
    # print("thickness - ", thickness)

    A1 = Angle - Beta
    A2 = Angle + Beta
    x1, y1 = X, Y
    x2, y2 = X + int(LineLen * math.cos(A1)), Y - int(LineLen * math.sin(A1))
    x3, y3 = X + int(CentLen * math.cos(Angle)), Y - int(CentLen * math.sin(Angle))
    x4, y4 = X + int(LineLen * math.cos(A2)), Y - int(LineLen * math.sin(A2))
    # draw_fill_circle(x1, y1, int(thickness * 1.2), fon_color)

    # x0_ = math.cos(Angle) * LineLen
    # y0_ = math.sin(Angle) * LineLen
    # x1_ = x0_ + thickness / 2 * math.cos(Angle)
    # y1_ = y0_ + thickness / 2 * math.sin(Angle)
    # x2_ = x0_ - thickness / 2 * math.cos(Angle)
    # y2_ = y0_ - thickness / 2 * math.sin(Angle)
    # x3_ = x0_ - thickness / 2 * math.cos(Angle)
    # y3_ = y0_ - thickness / 2 * math.sin(Angle)
    # x4_ = x0_ + thickness / 2 * math.cos(Angle)
    # y4_ = y0_ + thickness / 2 * math.sin(Angle)
    # fill_4poly(x1_, y1_, x2_, y2_, x3_, y3_, x4_, y4_, (1, 1, 1, 1))

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

def longer_for_polyline(xx0, yy0, xx, yy, thickness, k):
    LineLen = -k * thickness
    l = dist_(xx0, yy0, xx, yy)
    angle = math.atan2(yy0 - yy, xx - xx0)
    x_, y_ = xx0 + (l - LineLen) * math.cos(angle), yy0 - (l - LineLen) * math.sin(angle)
    x0_, y0_ = xx - (l - LineLen) * math.cos(angle), yy + (l - LineLen) * math.sin(angle)
    return x0_, y0_, x_, y_


# def draw_line(x0, y0, x, y, color=(1, 0, 0, 1), thickness=1):
#     glColor4f(*color)
#     glLineWidth(thickness)
#     glBegin(GL_LINES)
#     glVertex2f(x0, y0)
#     glVertex2f(x, y)
#     glEnd()

def draw_line(x0, y0, x, y, color=(1, 0, 0, 1), thickness=1,smooth=False):
    glEnable(GL_BLEND)  # transparency
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # transparency
    glColor4f(*color)
    glLineWidth(thickness)
    glBegin(GL_LINES)
    glVertex2f(x0, y0)
    glVertex2f(x, y)
    glEnd()


def dist_(x0, y0, x, y):
    return math.sqrt((x0 - x) ** 2 + (y0 - y) ** 2)


def draw_line_mod(x0, y0, x, y, color=(1, 0, 0, 1), fon_color=(1, 0, 0, 1), thickness=4, smooth=False, arrow=0,
                  dash=0):
    LineLen = 4.74 * thickness
    l = dist_(x0, y0, x, y)
    angle = math.atan2(y0 - y, x - x0)
    angle2 = math.atan2(y - y0, x0 - x)
    x_, y_ = x0 + (l - LineLen) * math.cos(angle), y0 - (l - LineLen) * math.sin(angle)
    x0_, y0_ = x - (l - LineLen) * math.cos(angle), y + (l - LineLen) * math.sin(angle)
    if arrow == 3:
        draw_line_1(x0, y0, x_, y_, color=color, thickness=thickness, dash=dash)
        draw_arrow_head(x, y, angle, color=color, thickness=thickness)
    elif arrow == 2:
        draw_line_1(x0_, y0_, x, y, color=color, thickness=thickness, dash=dash)
        draw_arrow_head(x0, y0, angle2, color=color, thickness=thickness)
    elif arrow == 1:
        draw_line_1(x0_, y0_, x_, y_, color=color, thickness=thickness, dash=dash)
        draw_arrow_head(x, y, angle, color=color, thickness=thickness)
        draw_arrow_head(x0, y0, angle2, color=color, thickness=thickness)
    else:
        draw_line_1(x0, y0, x, y, color=color, thickness=thickness, dash=dash)


def draw_ramka_top(x0, y0, x, y, color=(1, 0, 0, 1), thickness=1, center=(0,0), rotate=True, resize=True, close=True):
    glColor4f(*color)
    glLineWidth(thickness)
    xc0,yc0 = center
    draw_circle(xc0, yc0, 10, color=color, thickness=1)
    draw_line(xc0-20, yc0, xc0+20, yc0,  color=color, thickness=1)
    draw_line(xc0, yc0-20, xc0, yc0+20, color=color, thickness=1)
    if rotate:
        draw_line_mod((x0 + x) // 2 - 15, y - 12, (x0 + x) // 2, y - 6, color=color, thickness=2, arrow=2)
        draw_line_mod((x0 + x) // 2 + 15, y - 12,(x0 + x) // 2 , y - 6,  color=color, thickness=2, arrow=2)
    #кнопка видалення фігури
    if close:
        draw_line(x0 + 4, y0 + 4, x0 + 20, y0 + 20,  color, thickness=4)
        draw_line(x0 + 4, y0 +20, x0 + 20, y0 + 4, color, thickness=4)
    #кнопка зміни розмірів фігури
    if resize:
        draw_line_mod(x-5,y0+5,x+25,y0-25,color=color, thickness=4,arrow=1)

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


def draw_ellipse(x1, y1, x2, y2, numPoints=1000, color=(0, 0, 0, 1), thickness=1):
    x0, y0 = (x1 + x2) / 2, (y1 + y2) / 2
    rx, ry = abs(x1 - x2) / 2, abs(y1 - y2) / 2
    verts = []
    for i in range(numPoints):
        angle = math.radians(float(i) / numPoints * 360.0)
        x = rx * math.cos(angle) + x0
        y = ry * math.sin(angle) + y0
        verts += [x, y]
    glLineWidth(thickness)
    circle = pyglet.graphics.vertex_list(numPoints, ('v2f', verts))
    glColor4f(*color)
    circle.draw(GL_LINE_LOOP)


def draw_fill_ellipse(x1, y1, x2, y2, numPoints=1000, color=(0, 0, 0, 1), thickness=1):
    x0, y0 = (x1 + x2) / 2, (y1 + y2) / 2
    rx, ry = abs(x1 - x2) / 2, abs(y1 - y2) / 2
    verts = []
    numPoints = int(numPoints)
    for i in range(numPoints):
        angle = math.radians(float(i) / numPoints * 360.0)
        x = rx * math.cos(angle) + x0
        y = ry * math.sin(angle) + y0
        verts += [x, y]
        draw_line(x0, y0, x, y, color=color, thickness=1)
    glLineWidth(thickness)
    circle = pyglet.graphics.vertex_list(numPoints, ('v2f', verts))
    glColor4f(*color)
    circle.draw(GL_LINE_LOOP)


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
    # glEnable(GL_BLEND)
    circle.draw(GL_LINE_LOOP)



def draw_fill_reg_polygon(x1, y1, x2, y2, numPoints=3, angleStart=90, color=(0, 0, 0, 1), thickness=1):
    x0, y0 = (x1 + x2) / 2, (y1 + y2) / 2
    rx, ry = abs(x1 - x2) / 2, abs(y1 - y2) / 2
    verts = []
    xstart, ystart = x0, y0
    for i in range(numPoints):
        angle = math.radians(float(i) / numPoints * 360.0 + angleStart)
        x = rx * math.cos(angle) + x0
        y = ry * math.sin(angle) + y0
        verts += [x, y]
        fill_3poly(x0, y0, x, y, xstart, ystart, color)
        xstart, ystart = x, y
    fill_3poly(x0, y0, x, y, verts[0], verts[1], color)
    glLineWidth(thickness)
    circle = pyglet.graphics.vertex_list(numPoints, ('v2f', verts))
    glColor4f(*color)

    circle.draw(GL_LINE_LOOP)

def draw_fill_polygon(points, color=(0, 0, 0, 1), thickness=1):
    verts = []
    numPoints = len(points)
    x_min, y_min, x_max, y_max=border_polyline(points)
    x0,y0 = (x_min+x_max)/2, (y_min+y_max)/2
    x1, y1 = points[0]['x'], points[0]['y']
    x2, y2 = points[-1]['x'], points[-1]['y']
    fill_3poly(x1, y1, x2, y2, x0, y0, color)
    for p in points:
        x,y = p['x'],p['y']
        fill_3poly(x1, y1, x, y, x0, y0, color)
        x1, y1 = x, y
        verts+=[x, y]
    glLineWidth(thickness)
    circle = pyglet.graphics.vertex_list(numPoints, ('v2f', verts))
    glColor4f(*color)
    circle.draw(GL_LINE_LOOP)

def draw_polygon(points, color=(0, 0, 0, 1), thickness=1, dash=0):
    glLineWidth(thickness)
    verts = []
    xstart, ystart = points[0]['x'], points[0]['y']
    for p in points:
        verts.append(p['x'])
        verts.append(p['y'])
    numPoints = len(verts) // 2
    circle = pyglet.graphics.vertex_list(numPoints, ('v2f', verts))
    glColor4f(*color)
    if dash == 0:
        circle.draw(GL_LINE_LOOP)
    else:
        # circle.draw(GL_LINE_LOOP)
        x0, y0 = verts[0], verts[1]
        for i in range(0, len(verts) // 2 + 1):
            x, y = verts[i * 2 - 2], verts[i * 2 - 1]
            draw_line_mod(x0, y0, x, y, color=color, fon_color=(1, 0, 0, 1), thickness=thickness,
                          smooth=False, arrow=0, dash=dash)
            x0, y0 = x, y

def border_to_points(x1, y1, x2, y2, numPoints=3,angleStart=90):
    x0, y0 = (x1 + x2) / 2, (y1 + y2) / 2
    rx, ry = abs(x1 - x2) / 2, abs(y1 - y2) / 2
    verts = []
    for i in range(numPoints):
        angle = math.radians(float(i) / numPoints * 360.0 + angleStart)
        x = rx * math.cos(angle) + x0
        y = ry * math.sin(angle) + y0
        verts.append({'x':x, 'y':y})
    return verts

def draw_regular_polygon(x1, y1, x2, y2, numPoints=3, angleStart=90, color=(0, 0, 0, 1), thickness=1, dash=0):
    x0, y0 = (x1 + x2) / 2, (y1 + y2) / 2
    rx, ry = abs(x1 - x2) / 2, abs(y1 - y2) / 2
    verts = []
    for i in range(numPoints):
        angle = math.radians(float(i) / numPoints * 360.0 + angleStart)
        x = rx * math.cos(angle) + x0
        y = ry * math.sin(angle) + y0
        verts += [x, y]
    glLineWidth(thickness)
    circle = pyglet.graphics.vertex_list(numPoints, ('v2f', verts))
    glColor4f(*color)
    if dash == 0:
        circle.draw(GL_LINE_LOOP)
    else:
        # circle.draw(GL_LINE_LOOP)
        x0, y0 = verts[0], verts[1]
        for i in range(0, len(verts) // 2 + 1):
            x, y = verts[i * 2 - 2], verts[i * 2 - 1]
            draw_line_mod(x0, y0, x, y, color=color, fon_color=(1, 0, 0, 1), thickness=thickness,
                          smooth=False, arrow=0, dash=dash)
            x0, y0 = x, y


def draw_regular0_polygon(x0, y0, r, numPoints=3, angleStart=90, color=(0, 0, 0, 1), thickness=1):
    # x1, x2 = x0 - r, x0 + r
    # y1, y2 = y0 - r, y0 + r
    # rx, ry = abs(x1 - x2) / 2, abs(y1 - y2) / 2
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


# def draw_rectangle(x1, y1, x2, y2, x3, y3, x4, y4, color=(1, 0, 0, 1), thickness=1):
#     glColor4f(*color)
#     glLineWidth(thickness)
#     glBegin(GL_LINES)
#     glVertex2f(x1, y1)
#     glVertex2f(x2, y2)
#     glEnd()
#     glBegin(GL_LINES)
#     glVertex2f(x2, y2)
#     glVertex2f(x3, y3)
#     glEnd()
#     glBegin(GL_LINES)
#     glVertex2f(x3, y3)
#     glVertex2f(x4, y4)
#     glEnd()
#     glBegin(GL_LINES)
#     glVertex2f(x4, y4)
#     glVertex2f(x1, y1)
#     glEnd()
def draw_rectangle(x1, y1, x2, y2, x3, y3, x4, y4, color=(1, 0, 0, 1), thickness=1, dash=0):
    # k = 0
    # for i in range(k):
    #     x1, x2, x3, x4 = x2, x3, x4, x1
    #     y1, y2, y3, y4 = y2, y3, y4, y1
    # x1 += thickness // 2
    # x2 -= thickness // 2
    # x3 -= thickness // 2
    # x4 += thickness // 2
    # y1 -= thickness // 2
    # y2 -= thickness // 2
    # y3 += thickness // 2
    # y4 += thickness // 2
    draw_line_1(x1, y1, x2, y2, color, thickness=thickness, smooth=False, dash=dash)
    draw_line_1(x3, y3, x2, y2, color, thickness=thickness, smooth=False, dash=dash)
    draw_line_1(x3, y3, x4, y4, color, thickness=thickness, smooth=False, dash=dash)
    draw_line_1(x1, y1, x4, y4, color, thickness=thickness, smooth=False, dash=dash)

    # glColor4f(*color)
    # glLineWidth(thickness)
    # glBegin(GL_LINES)
    # glVertex2f(x1, y1)
    # glVertex2f(x2, y2)
    # glEnd()
    # glBegin(GL_LINES)
    # glVertex2f(x2, y2)
    # glVertex2f(x3, y3)
    # glEnd()
    # glBegin(GL_LINES)
    # glVertex2f(x3, y3)
    # glVertex2f(x4, y4)
    # glEnd()
    # glBegin(GL_LINES)
    # glVertex2f(x4, y4)
    # glVertex2f(x1, y1)
    # glEnd()


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
    glEnable(GL_BLEND)  # transparency
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # transparency
    pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES, ('v2f', [x1, y1, x2, y2, x3, y3]),
                         ('c4f', [r, g, b, a, r, g, b, a, r, g, b, a]))


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


def draw_poly(x1, y1, x2, y2, id=4, numPoints=4, color=(0, 0, 0, 1), fon_color=(1, 1, 1, 1), fill=False):
    x0, y0 = (x1 + x2) // 2, (y1 + y2) // 2
    r = (x0 - x1)
    draw_fill_rectangle(x0 - r, y0 - r, x0 + r, y0 + r, color=fon_color)
    if id == 4:
        angle = 45
    else:
        angle = 90
    if fill:
        draw_fill_regular_polygon(x0, y0, r, numPoints=numPoints, angleStart=angle, color=color, thickness=2)

    else:
        # draw_polygon(x1, y1, x2, y2, numPoints=numPoints, angleStart=angle, color=color, thickness=2)
        draw_regular0_polygon(x0, y0, r, numPoints=numPoints, angleStart=angle, color=color, thickness=2)


def draw_poly_wo_bg(x1, y1, x2, y2, id=4, numPoints=4, color=(0, 0, 0, 1), fon_color=(1, 1, 1, 1), fill=False,
                    thickness=4, dash=0):
    x0, y0 = (x1 + x2) // 2, (y1 + y2) // 2
    r = (x0 - x1)
    if id == 4:
        angle = 45
    elif id == 3:
        angle = -30
    else:
        angle = 90

    if fill:
        # draw_regular_polygon(x0, y0, r, numPoints=numPoints, angleStart=angle, color=color, thickness=thickness)
        draw_fill_reg_polygon(x1, y1, x2, y2, numPoints=numPoints, angleStart=angle, color=color, thickness=thickness)

    else:
        # draw_regular_polygon(x0, y0, r, numPoints=numPoints, angleStart=angle, color=color, thickness=thickness)
        draw_regular_polygon(x1, y1, x2, y2, numPoints=numPoints, angleStart=angle, color=color, thickness=thickness,
                             dash=dash)
