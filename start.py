import os
import subprocess
from datetime import datetime
from math import sqrt

# import pyautogui
import pyglet
from pyglet.gl import *
from pyglet.window import mouse


def line(x0, y0, x, y, color=(1, 0, 0, 1), thickness=1):
    glColor4f(*color)
    glLineWidth(thickness)
    glBegin(GL_LINES)
    glVertex2f(x0, y0)
    glVertex2f(x, y)
    glEnd()


def rectangle(x0, y0, x, y, color=(1, 0, 0, 1), thickness=1):
    glColor4f(*color)
    glLineWidth(thickness)
    glBegin(GL_LINES)
    glVertex2f(x0, y0)
    glVertex2f(x, y0)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(x, y0)
    glVertex2f(x, y)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x0, y)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(x0, y)
    glVertex2f(x0, y0)
    glEnd()


class Quad:
    def __init__(self, x, y, w, h):
        self.indices = [0, 1, 2, 2, 3, 0]
        self.vertex = [-0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.5, 0.5, 0.0, -0.5, 0.5, 0.0]
        self.color = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, ]

    def render(self):
        self.vertices = pyglet.graphics.draw_indexed(4, GL_TRIANGLES, self.indices, ('v3f', self.vertex),
                                                     ('c3f', self.color))


def dist(x0, y0, x, y, r):
    d = sqrt((x - x0) ** 2 + (y - y0) ** 2)
    return d < r


def mediana(x1, x2):
    return abs(x1 + x2) // 2


def border_polyline(points):
    print(points)
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


class MyWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # E9FBCA    233/255,251/255,202/255
        self.set_minimum_size(400, 30)
        self.fonColor = (233 / 255, 251 / 255, 202 / 255, 1.0)
        self.gridColor = (208 / 255, 208 / 255, 208 / 255, 1.0)
        glClearColor(233 / 255, 251 / 255, 202 / 255, 1.0)
        self.figures = []
        self.buttons = [
            {'id': 1, 'x': 5, 'y': 5, 'text': 'Pen', 'image': pyglet.resource.image('img/pen.png'), 'tool': 1},
            {'id': 2, 'x': 40, 'y': 5, 'text': 'Erazer', 'image': pyglet.resource.image('img/err.png'), 'tool': 2},
            {'id': 3, 'x': 75, 'y': 5, 'text': 'line', 'image': pyglet.resource.image('img/line.png'), 'tool': 3},
            {'id': 4, 'x': 110, 'y': 5, 'text': 'line', 'image': pyglet.resource.image('img/_ClearFill.png'),
             'tool': 4},
            {'id': 26, 'x': 145, 'y': 5, 'text': 'line', 'image': pyglet.resource.image('img/shot.png'), 'tool': 26},
        ]
        self.poly = []
        self.x0, self.y0 = 0, 0
        self.cx, self.cy = 0, 0
        self.penWidth = 4
        self.errSize = 20
        self.tool = 1
        self.f = True
        self.fullscr = True
        self.penColor = (1, 0, 0, 1)
        self.step = 50
        self.screen_width = 800
        self.screen_height = 500
        self.scS = False

    def set_color(self):
        # For linux
        try:
            output = subprocess.check_output('zenity --color-selection  --color red --show-palette  --text="Stuff"',
                                             shell=True)
            s = ""
            for o in output:
                s += chr(o)
            s = s[4:-2]
            cs = s.split(',')
            self.penColor = (int(cs[0]) / 256, int(cs[1]) / 256, int(cs[2]) / 256, 1)
        except:
            pass

    def set_width(self, w):
        try:
            output = subprocess.check_output(
                'zenity --scale --title="Товщина лінії" --text="Виберіть товщину лінії"  --min-value=4 --max-value=40 --value=' + str(
                    w) + ' --step=1',
                shell=True)
            s = ""
            for o in output:
                s += chr(o)
            s = s[0:-1]
            self.penWidth = int(s)
        except:
            pass

    def on_key_press(self, symbol, modifiers):
        if symbol == 65307:  # ESC
            # TODO поміняти потім
            window.close()
            # self.on_close()
        elif symbol == 65360:  # Home
            self.cx, self.cy = 0, 0
        elif symbol == 99:  # Change color
            self.set_color()
        elif symbol == 65451:  # Change thickness +
            self.penWidth += 2
        elif symbol == 65453:  # Change thickness
            self.penWidth -= 2
            if self.penWidth < 1:
                self.penWidth = 1
        elif symbol == 65362:  # move canvas up
            self.cy += 50
        elif symbol == 65364:  # Change canvas down
            self.cy -= 50
        elif symbol == 65361:  # Change canvas left
            self.cx -= 50
        elif symbol == 65363:  # Change canvas right
            self.cx += 50
        elif symbol == 102:  # full screen
            self.fullscr = not self.fullscr
            window.set_fullscreen(self.fullscr)
            window.clear()
        elif symbol == 115:  # set S
            self.btnScrInsertInCanvasClick()
        elif symbol == 112:  # set pen
            self.tool = 1
        elif symbol == 101:  # set erazer
            self.tool = 2
        elif symbol == 119:  # set width
            self.set_width(self.penWidth)
        elif symbol == 109:  # set
            window.set_fullscreen(False)
            window.minimize()
            self.fullscr = True
            window.set_fullscreen(self.fullscr)


        else:
            print('A key was pressed')
            print(symbol)
        window.clear()

    def on_mouse_press(self, x, y, button, modifier):
        self.f = True
        if button == mouse.LEFT:
            for btn in self.buttons:
                if (btn['x'] < x < btn['x'] + 32) and (btn['y'] < y < btn['y'] + 32):
                    if btn['id'] == 4:  # Fill figure
                        self.tool = btn['tool']

                    else:
                        self.tool = btn['tool']
                    self.f = False
                    break
            if self.f:
                if self.tool == 1:
                    # window.clear()
                    self.x0, self.y0 = x - self.cx, y - self.cy
                    self.poly.clear()
                    self.poly.append({'x': self.x0, 'y': self.y0})
                elif self.tool == 3 or self.tool == 4:
                    self.x0, self.y0 = x - self.cx, y - self.cy
                    self.poly.clear()
                    self.poly.append({'x': self.x0, 'y': self.y0})
                elif self.tool == 26:  # scheenshot mode
                    pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        window.clear()
        if self.f:
            if self.tool == 1:
                self.poly.append({'x': x - self.cx, 'y': y - self.cy})
                x0 = self.poly[0]['x']
                y0 = self.poly[0]['y']
                for p in self.poly:
                    x_ = p['x']
                    y_ = p['y']
                    line(x0 + self.cx, y0 + self.cy, x_ + self.cx, y_ + self.cy, color=self.penColor,
                         thickness=self.penWidth)
                    x0, y0 = x_, y_
                self.x0, self.y0 = x, y
            elif self.tool == 2:
                line(x + self.errSize // 2, y + self.errSize // 2,
                     x - self.errSize // 2, y - self.errSize // 2, color=(1, 1, 0, 1), thickness=self.errSize)
                for f in self.figures:
                    x_min, y_min, x_max, y_max = border_polyline(f['p'])
                    if dist((x_max + x_min) // 2, (y_max + y_min) // 2, x - self.cx, y - self.cy, self.errSize):
                        print('del')
                        f['fordel'] = True
                        break
                new_list = []
                for f in self.figures:
                    if not f['fordel']:
                        new_list.append(f)
                self.figures = new_list.copy()
                # window.clear()
            elif self.tool == 3:

                line(self.x0 + self.cx, self.y0 + self.cy, x, y, color=self.penColor,
                     thickness=self.penWidth)
            elif self.tool == 4:

                rectangle(self.x0 + self.cx, self.y0 + self.cy, x, y, color=self.penColor,
                          thickness=self.penWidth)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.f:
            # window.clear()
            print("on_mouse_release")

            if self.tool == 1:
                k = {}
                k['name'] = 'polyline'
                k['p'] = self.poly.copy()
                k['color'] = self.penColor
                k['thickness'] = self.penWidth
                k['fordel'] = False
                self.figures.append(k)
            elif self.tool == 3:
                k = {}
                self.poly.append({'x': x - self.cx, 'y': y - self.cy})
                k['name'] = 'line'
                k['p'] = self.poly.copy()
                k['color'] = self.penColor
                k['thickness'] = self.penWidth
                k['fordel'] = False
                self.figures.append(k)
            elif self.tool == 4:
                k = {}
                self.poly.append({'x': x - self.cx, 'y': y - self.cy})
                k['name'] = 'rectangle'
                k['p'] = self.poly.copy()
                k['color'] = self.penColor
                k['thickness'] = self.penWidth
                k['fordel'] = False
                self.figures.append(k)

        window.clear()

    def on_draw(self):

        for f in self.figures:
            if f['name'] == 'polyline':
                x0 = f['p'][0]['x']
                y0 = f['p'][0]['y']
                for p in f['p']:
                    x = p['x']
                    y = p['y']
                    # line(x0 , y0 , x , y , color=f['color'], thickness=f['thickness'])
                    line(x0 + self.cx, y0 + self.cy, x + self.cx, y + self.cy, color=f['color'],
                         thickness=f['thickness'])
                    x0, y0 = x, y
            elif f['name'] == 'line':
                x0 = f['p'][0]['x']
                y0 = f['p'][0]['y']
                for p in f['p']:
                    x = p['x']
                    y = p['y']
                    # line(x0 , y0 , x , y , color=f['color'], thickness=f['thickness'])
                    line(x0 + self.cx, y0 + self.cy, x + self.cx, y + self.cy, color=f['color'],
                         thickness=f['thickness'])
                    x0, y0 = x, y
            elif f['name'] == 'line':
                x0 = f['p'][0]['x']
                y0 = f['p'][0]['y']
                x_ = f['p'][1]['x']
                y_ = f['p'][1]['y']
                line(x0 + self.cx, y0 + self.cy, x_ + self.cx, y_ + self.cy, color=f['color'],
                     thickness=f['thickness'])
            elif f['name'] == 'rectangle':
                x0 = f['p'][0]['x']
                y0 = f['p'][0]['y']
                x_ = f['p'][1]['x']
                y_ = f['p'][1]['y']

                rectangle(x0 + self.cx, y0 + self.cy, x_ + self.cx, y_ + self.cy, color=f['color'],
                          thickness=f['thickness'])

        # Draw grid

        # Draw grid
        for y in range(0, 4000, self.step):
            line(0, y, 4000, y, color=self.gridColor, thickness=1)
        for x in range(0, 4000, self.step):
            line(x, 0, x, 4000, color=self.gridColor, thickness=1)

        # Це щоб не було засвітки на кнопках
        rectangle(10000, 10000, 10001, 10001, color=(1, 1, 1, 1), thickness=1)
        # Draw buttons
        for btn in self.buttons:
            btn['image'].blit(btn['x'], btn['y'])

    def on_show(self):
        print("wwwwwwwwwwwww")

    # No order

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        print("scrool ", scroll_y)
        self.cy -= scroll_y * 10
        # rectangle(10000, 10000, 10001, 10001, color=(1, 1, 1, 1), thickness=1)
        window.clear()

    def on_close(self):
        proc = subprocess.Popen("zenity --question --text='Вийти з програми?'", shell=True)
        proc.communicate()
        if proc.returncode:
            print("Cancel was pressed")
        else:
            print("Ok was pressed")
            window.clear()
            window.close()

    def on_hide(self):
        print("qqqqqqqqqqq")
        name = 'tmp/' + datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S") + '.png'
        # os.system('gnome-screenshot -d 2 -f ' + name)
        # output = subprocess.check_output('/usr/bin/gnome-screenshot -d 2 -f ' + name, shell=True)
        myCmd = './scrsht.sh '+ name
        os.system(myCmd)

        window.maximize()

        self.scS = False


    def btnScrInsertInCanvasClick(self):
        window.minimize()
        # Тут треба паузу зротити
        self.scS = True

        pass
        # print('btnClick')
        # floatWindow.wm_attributes("-alpha", "0.0")
        # width = 600
        # self.window_width = root.winfo_width()
        # self.window_height = root.winfo_height()
        # x0 = -self.xc + self.window_width - width - 40
        # y0 = -self.yc + 20

        #
        # k = self.screen_width / (self.screen_height + 75)
        # height = int(width / k)
        # image = image.resize((width, height), Image.ANTIALIAS)
        # root.wm_state('normal')
        # self.images.append(ImageTk.PhotoImage(image))
        # k = []
        # c = {}
        # c['name'] = name
        # c['x'] = x0
        # c['y'] = y0
        # c['width'] = width
        # c['height'] = height
        # k.append(canvas.create_image(x0, y0, image=self.images[-1], state=NORMAL, anchor=NW))
        # k.append("image")
        # k.append(c)
        # self.figures.append(k)
        #
        # floatWindow.destroy()



    # def btnScrClick(self):
    #     print('btnScrClick')
    #     floatWindow = MyFloatWindow(40, 35, caption="", resizable=False, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
    #     floatWindow.set_location(20, 20)
    #     glClearColor(1.0, 1.0, 1.0, 0.5)
    #     floatWindow.clear()


    #     floatWindow.overrideredirect(1)
    #     floatWindow.wm_attributes("-topmost", True)
    #     floatWindow.wm_attributes("-alpha", "0.5")
    #     btnScrInsertInCanvas.pack(fill=BOTH, expand=True)
    #     self.btnPenClick()


if __name__ == "__main__":
    window = MyWindow(4020, 2000, caption="WhiteBoard", resizable=True)
    # window.maximize()
    window.clear()

    window.on_draw()
    # color_dialog.on_draw()
    pyglet.app.run()
