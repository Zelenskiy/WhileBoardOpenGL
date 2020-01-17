import os
import subprocess
from datetime import datetime
from math import sqrt

# import pyautogui
import pyglet
from PIL import Image
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


class MyWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # E9FBCA    233/255,251/255,202/255
        self.set_minimum_size(400, 30)
        self.fonColor = (233 / 255, 251 / 255, 202 / 255, 1.0)
        self.gridColor = (208 / 255, 208 / 255, 208 / 255, 0.1)
        glClearColor(233 / 255, 251 / 255, 202 / 255, 1.0)
        self.figures = []
        self.isGrid = True
        self.buttons = [
            {'id': 8, 'x': 5, 'y': 5, 'text': 'Pen', 'image': pyglet.resource.image('img/ar.png'), 'tool': 8,
             'sel': False},
            {'id': 1, 'x': 40, 'y': 5, 'text': 'Pen', 'image': pyglet.resource.image('img/pen.png'), 'tool': 1,
             'sel': True},
            {'id': 2, 'x': 75, 'y': 5, 'text': 'Erazer', 'image': pyglet.resource.image('img/err.png'), 'tool': 2,
             'sel': False},
            {'id': 3, 'x': 110, 'y': 5, 'text': 'line', 'image': pyglet.resource.image('img/line.png'), 'tool': 3,
             'sel': False},
            {'id': 4, 'x': 145, 'y': 5, 'text': 'line', 'image': pyglet.resource.image('img/_ClearFill.png'),
             'tool': 4, 'sel': False},
            {'id': 26, 'x': 180, 'y': 5, 'text': 'shot', 'image': pyglet.resource.image('img/shot.png'), 'tool': 26,
             'sel': False},
            {'id': 101, 'x': 215, 'y': 5, 'text': 'color', 'image': pyglet.resource.image('img/palitra.png'), 'tool': 1,
             'sel': False},
            {'id': 102, 'x': 250, 'y': 5, 'text': 'width', 'image': pyglet.resource.image('img/width.png'), 'tool': 1,
             'sel': False},
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
        self.images = {}
        self.selFig = {}
        self.id = 0


    def resize_image(self, input_image_path,
                     output_image_path,
                     size):
        original_image = Image.open(input_image_path)
        original_image.save(output_image_path+'.ori.png')
        width, height = original_image.size
        # print('The original image size is {wide} wide x {height} '
        #       'high'.format(wide=width, height=height))

        resized_image = original_image.resize(size)
        width, height = resized_image.size
        # print('The resized image size is {wide} wide x {height} '
        #       'high'.format(wide=width, height=height))
        resized_image.show()
        resized_image.save(output_image_path)

    def insert_image_from_file(self):
        # For linux
        # TODO no odgrg with cyrylic symbols
        s = ""
        try:
            output = subprocess.check_output('zenity --file-selection --multiple --filename tmp',
                                             shell=True)
            for o in output:
                s += chr(o)
        except:
            pass

        if s != "":
            s = s.strip()
            names = s.split('|')
        else:
            names = []
        w = window.width
        h = window.height
        i=0
        for name in names:
            k = {}

            width = 600
            height = 9*width//16
            k['name'] = 'image'
            k['p'] = []
            k['p'].append({'x':w - width - self.cx - i, 'y':h - height - self.cy - i})
            k['p'].append({'x': width - i, 'y': height - i})  # TODO поправити висоту малюнка
            i += 25
            # image = pyglet.image.load(name.strip())
            nnam = name.strip()
            nnam_ = datetime.strftime(datetime.now(), "_%Y_%m_%d_%H_%M_%S") + '.png'

            self.resize_image(nnam, 'tmp/'+nnam_, (width,height))

            image = pyglet.image.load('tmp/'+nnam_)

            self.images['tmp/'+nnam_] = image

            k['image'] = 'tmp/'+nnam_
            k['thickness'] = self.penWidth
            k['fordel'] = False
            self.figures.append(k)
            # line(10000,10000,10001,10001,color=(1,1,1,1))

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
        elif symbol == 65535:  # Delete
            if self.selFig != {}:
                for fig in self.figures:
                    if fig['id'] == self.selFig['fig']:
                        self.selFig = {}
                        fig['fordel'] = True
                        break
            new_list = []
            for f in self.figures:
                if not f['fordel']:
                    new_list.append(f)
            self.figures = new_list.copy()

        elif symbol == 99:  # Change color
            self.set_color()
        elif symbol == 105:  # Insert image
            names = self.insert_image_from_file().split('|')
            for n in names:
                print(n)
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
        elif symbol == 103:  # set grid
            self.isGrid = not self.isGrid
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
                btn['sel'] = False
                if (btn['x'] < x < btn['x'] + 32) and (btn['y'] < y < btn['y'] + 32):
                    btn['sel'] = True
                    if btn['id'] == 4:  # Fill figure
                        self.tool = btn['tool']
                    elif btn['id'] == 101:  # Changr color pen
                        self.set_color()
                    elif btn['id'] == 102:  # Changr width pen
                        self.set_width(self.penWidth)
                    else:
                        self.tool = btn['tool']
                    self.f = False
                    break
            if self.f:
                if self.tool == 8:
                    print("Увімкнення виділення")
                    # [{'name': 'polyline', 'p': [{'x': 429, 'y': 444}, {'x': 437, 'y': 448}, {'x': 438, 'y': 449}, {'x': 444, 'y': 449}, {'x': 449, 'y': 450}, {'x': 454, 'y': 450}, {'x': 462, 'y': 451}, {'x': 486, 'y': 451}, {'x': 498, 'y': 450}, {'x': 506, 'y': 446}, {'x': 512, 'y': 440}, {'x': 517, 'y': 432}, {'x': 519, 'y': 420}, {'x': 526, 'y': 401}, {'x': 527, 'y': 395}, {'x': 529, 'y': 391}, {'x': 530, 'y': 386}, {'x': 532, 'y': 382}, {'x': 534, 'y': 377}, {'x': 538, 'y': 372}, {'x': 546, 'y': 359}, {'x': 552, 'y': 352}, {'x': 560, 'y': 343}, {'x': 567, 'y': 338}, {'x': 573, 'y': 336}, {'x': 579, 'y': 332}, {'x': 580, 'y': 332}, {'x': 588, 'y': 332}, {'x': 588, 'y': 332}, {'x': 593, 'y': 331}], 'color': (1, 0, 0, 1), 'thickness': 4, 'fordel': False}]
                    for fig in reversed(self.figures):
                        x1, y1, x2, y2 = border_polyline(fig['p'])
                        if (x > x1) and (x < x2) and (y > y1) and (y < y2):
                            # canvas.config(cursor="fleur")
                            self.selFig['fig'] = fig['id']
                            # if self.selFig != {}:
                            #     canvas.coords(self.selFig['0'], x1 - 1, y1 - 1, x2 + 1, y2 + 1)
                            #     canvas.coords(self.selFig['D'], x2 - 10, abs(y1 + y2) // 2 - 10, x2 + 10,
                            #                   abs(y1 + y2) // 2 + 10)
                            #     self.selFig['Obj'] = fig
                            fl = True
                            break
                        else:
                            # canvas.config(cursor="tcross")
                            pass

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
                        # print('del')
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


            if self.tool == 1:
                k = {}
                self.id += 1
                k['id'] = self.id
                k['name'] = 'polyline'
                k['p'] = self.poly.copy()
                k['color'] = self.penColor
                k['thickness'] = self.penWidth
                k['fordel'] = False
                self.figures.append(k)
            elif self.tool == 3:
                k = {}
                self.poly.append({'x': x - self.cx, 'y': y - self.cy})
                self.id += 1
                k['id'] = self.id
                k['name'] = 'line'
                k['p'] = self.poly.copy()
                k['color'] = self.penColor
                k['thickness'] = self.penWidth
                k['fordel'] = False
                self.figures.append(k)
            elif self.tool == 4:
                k = {}
                self.poly.append({'x': x - self.cx, 'y': y - self.cy})
                self.id += 1
                k['id'] = self.id
                k['name'] = 'rectangle'
                k['p'] = self.poly.copy()
                k['color'] = self.penColor
                k['thickness'] = self.penWidth
                k['fordel'] = False
                self.figures.append(k)

        print(self.figures)
        window.clear()

    def on_draw(self):
        # draw figures in visible part of window
        w = window.width
        h = window.height
        count = 0
        for f in self.figures:
            x_min, y_min, x_max, y_max = border_polyline(f['p'])
            if x_min + self.cx < w and x_max + self.cx > 0 and y_min + self.cy < h and y_max + self.cy > 0:
                count += 1
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
                elif f['name'] == 'image':
                    x0 = f['p'][0]['x']
                    y0 = f['p'][0]['y']
                    x = f['p'][1]['x']
                    y = f['p'][1]['y']
                    image = self.images[f['image']]
                    # Це щоб не було засвітки
                    line(10000, 10000, 10001, 10001, color=(1, 1, 1, 1), thickness=1)
                    image.blit(x0 + self.cx, y0 + self.cy)

                    # image.blit(x + self.cx, y + self.cy )


        # Draw grid
        if self.isGrid:
            for y in range(0, 4000, self.step):
                line(0, y, 4000, y, color=self.gridColor, thickness=1)
            for x in range(0, 4000, self.step):
                line(x, 0, x, 4000, color=self.gridColor, thickness=1)

        # Це щоб не було засвітки на кнопках
        rectangle(10000, 10000, 10001, 10001, color=(1, 1, 1, 1), thickness=1)
        # Draw buttons
        for btn in self.buttons:
            btn['image'].blit(btn['x'], btn['y'])
            if btn['sel']:
                line(btn['x'] + 2, btn['y'] - 2, btn['x'] + 28, btn['y'] - 2, color=self.gridColor, thickness=2)
        # # Це щоб не було засвітки на кнопках
        # rectangle(10000, 10000, 10001, 10001, color=(1, 1, 1, 1), thickness=1)

    def on_show(self):
        # print("wwwwwwwwwwwww")
        pass

    # No order

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # print("scrool ", scroll_y)
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
        pass
        # if self.scS:
        #     name = 'tmp/' + datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S") + '.png'
        #     # os.system('gnome-screenshot -d 2 -f ' + name)
        #     # output = subprocess.check_output('/usr/bin/gnome-screenshot -d 2 -f ' + name, shell=True)
        #     myCmd = './scrsht.sh '+ name
        #     os.system(myCmd)
        #
        #     self.scS = False
        #     print("All")
        #     window.maximize()

    def btnScrInsertInCanvasClick(self):
        window.minimize()
        # Тут треба паузу зротити
        self.scS = True
        if self.scS:
            name = 'tmp/' + datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S") + '.png'
            # os.system('gnome-screenshot -d 2 -f ' + name)
            # output = subprocess.check_output('/usr/bin/gnome-screenshot -d 2 -f ' + name, shell=True)
            myCmd = './scrsht.sh ' + name
            os.system(myCmd)

            self.scS = False
            # print("All")
            window.maximize()

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
