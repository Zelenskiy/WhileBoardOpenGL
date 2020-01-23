import os
import subprocess
from datetime import datetime
import main
import threading

from graph_ogl import *


import pickle

import pyglet
from PIL import Image
from pyglet.gl import *

from pyglet.window import mouse, ImageMouseCursor

from sys import platform
import wx


from dialogWindow import *
import grab
if platform == "win32" or platform == "cygwin":
    pass
elif platform == "linux":
    pass

winPanel = None

#
# class MainFrame(wx.Frame):
#     def __init__(self):
#         wx.Frame.__init__(self, None, -1,
#                           style=wx.STAY_ON_TOP | wx.TAB_TRAVERSAL | wx.FRAME_NO_TASKBAR)
#         # self.SetTransparent(64)
#
#         self.panel = MainPanel(self)
#         self.Fit()
#         self.Centre()
#         self.SetSize(60, 30)
#         self.SetPosition((10, 40))
#         self.Show()
#
#
# class MainPanel(wx.Panel):
#     def __init__(self, frame):
#         wx.Panel.__init__(self, frame)
#
#         # Button 1
#         button_sizer = self._button_sizer(frame)
#
#         # Main sizer
#         main_sizer = wx.BoxSizer(wx.VERTICAL)
#         main_sizer.Add((0, 0))
#         main_sizer.Add(button_sizer)
#         self.SetSizer(main_sizer)
#         self.Fit()
#
#     def _button_sizer(self, frame):
#         cmd_screenshot = wx.Button(self, label='+')
#         button_sizer = wx.BoxSizer(wx.VERTICAL)
#         button_sizer.Add(cmd_screenshot)
#         cmd_screenshot.Bind(wx.EVT_BUTTON, self.OnScrClick)
#         return button_sizer
#
#     def OnScrClick(self, event):
#         self.set_visible(False)
#         self.insert_screenshot()


class MyWindow(pyglet.window.Window):

    # def show_screenshot_panel(self):
    #     # self.set_visible(False)
    #     result = self.dialog.ShowModal()  # показываем модальный диалог
    #     if result == wx.ID_OK:
    #         print("OK")
    #         # self.set_visible(True)
    #         self.set_visible(False)
    #         self.insert_screenshot()
    #         # dialog.Destroy()
    #
    #     else:
    #         print("Cancel")
    #         self.set_visible(True)


    def draw_color_panel(self):
        for btn in self.colorPanelButtons:
            draw_fill_rectangle(btn['x1'], btn['y1'], btn['x2'], btn['y2'], btn['color'])

    def draw_width_panel(self):
        for btn in self.widthPanelButtons:
            h = btn['y2'] - btn['y1']
            y = btn['y1'] + h // 2
            draw_fill_rectangle(btn['x1'], btn['y1'], btn['x2'], btn['y2'], self.fonColor)
            draw_fill_rectangle(btn['x1'], y - btn['width'] // 2, btn['x2'], y + btn['width'] // 2, self.penColor)

    def draw_arrow_panel(self):
        for btn in self.arrowPanelButtons:
            h = btn['y2'] - btn['y1']
            y = btn['y1'] + h // 2
            draw_fill_rectangle(btn['x1'], btn['y1'], btn['x2'], btn['y2'], self.fonColor)
            btn['image'].blit(btn['x1'], btn['y1'])
            # draw_fill_rectangle(btn['x1'], y - btn['width'] // 2, btn['x2'], y + btn['width'] // 2, self.penColor)

    def save(self):
        data = {}
        data['figures'] = self.figures
        data['penColor'] = self.penColor
        data['penWidth'] = self.penWidth
        data['fonColor'] = self.fonColor
        data['cx'] = self.cx
        data['cy'] = self.cy
        data['id'] = self.id
        data['isGrid'] = self.isGrid

        with open("test.wb", "wb") as fp:
            pickle.dump(data, fp)

    def load(self):

        self.figures = []
        self.images = {}

        with open("test.wb", "rb") as fp:  # Unpickling
            data = pickle.load(fp)
        self.figures = data['figures']
        self.penColor = data['penColor']

        self.penWidth = data['penWidth']
        self.fonColor = data['fonColor']
        self.id = data['id']
        self.cx = data['cx']
        self.cy = data['cy']
        self.isGrid = data['isGrid']
        # Загрузка images
        for fig in self.figures:
            if fig['name'] == 'image':
                nnam_ = fig['image']
                image = pyglet.image.load(nnam_)
                self.images[nnam_] = image

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # E9FBCA    233/255,251/255,202/255
        self.set_minimum_size(400, 30)

        # ============ Options ================
        self.isGrid = True
        self.isSmooth = False
        self.penWidth = 7
        self.errSize = 20
        self.fullscr = False
        self.penColor = (0, 0, 1, 1)
        self.ramkaColor = (1, 0.5, 0, 1)
        self.ramkaThickness = 2
        self.fonColor = (0.91, 0.98, 0.79, 1.0)
        self.gridColor = (0.82, 0.82, 0.82, 0.5)

        # ============ End options ================

        glClearColor(*self.fonColor)
        self.figures = []
        self.isMove = False
        self.isResize = False
        self.isExit = False
        self.isFill = False

        self.isBtnClick = False
        self.colorPanelVisible = False
        self.widthPanelVisible = False
        self.label = None
        self.buttons = [
            {'id': 8, 'text': 'Pen', 'image': pyglet.resource.image('img/ar.png'), 'tool': 8,
             'sel': False, 'align': 'left'},
            {'id': 1, 'text': 'Pen', 'image': pyglet.resource.image('img/pen.png'), 'tool': 1,
             'sel': True, 'align': 'left'},
            {'id': 2, 'text': 'Erazer', 'image': pyglet.resource.image('img/err.png'), 'tool': 2,
             'sel': False, 'align': 'left'},
            {'id': 3, 'text': 'line', 'image': pyglet.resource.image('img/line.png'), 'tool': 3,
             'sel': False, 'align': 'left'},
            {'id': 4, 'text': 'rectangle', 'image': pyglet.resource.image('img/_ClearFill.png'),
             'tool': 4, 'sel': False, 'align': 'left'},
            {'id': 5, 'text': 'ellipse', 'image': pyglet.resource.image('img/ellFill.png'),
             'tool': 5, 'sel': False, 'align': 'left'},
            {'id': 26, 'text': 'shot', 'image': pyglet.resource.image('img/shot.png'), 'tool': 26,
             'sel': False, 'align': 'left'},
            {'id': 101, 'text': 'color', 'image': pyglet.resource.image('img/palitra.png'), 'tool': 0,
             'sel': False, 'align': 'left'},
            {'id': 102, 'text': 'width', 'image': pyglet.resource.image('img/width.png'), 'tool': 0,
             'sel': False, 'align': 'left'},
            {'id': 103, 'text': 'width', 'image': pyglet.resource.image('img/add.png'),
             'tool': 0, 'sel': False, 'align': 'left'},
            {'id': 106, 'text': 'arrow', 'image': pyglet.resource.image('img/arr.png'), 'tool': 0,
             'sel': False, 'align': 'left'},
            {'id': 104, 'x': 75, 'y': 5, 'text': '<', 'image': pyglet.resource.image('img/left.png'), 'tool': 0,
             'sel': False, 'align': 'right'},
            {'id': 105, 'x': 5, 'y': 5, 'text': '>', 'image': pyglet.resource.image('img/right.png'), 'tool': 0,
             'sel': False, 'align': 'right'},

        ]
        x = 5
        for b in self.buttons:
            if b['align'] == 'left':
                b['x'] = x
                b['y'] = 5
                x += 35

        self.colorPanelButtons = [
            {'id': 1, 'x1': 215, 'y1': 10 + 35, 'x2': 25 + 247, 'y2': 10 + 70, 'color': (1, 0, 0, 1)},
            {'id': 2, 'x1': 215, 'y1': 10 + 70, 'x2': 25 + 247, 'y2': 10 + 105, 'color': (1, 1, 0, 1)},
            {'id': 3, 'x1': 215, 'y1': 10 + 105, 'x2': 25 + 247, 'y2': 10 + 140, 'color': (0, 1, 0, 1)},
            {'id': 4, 'x1': 215, 'y1': 10 + 140, 'x2': 25 + 247, 'y2': 10 + 175, 'color': (0, 1, 1, 1)},
            {'id': 5, 'x1': 215, 'y1': 10 + 175, 'x2': 25 + 247, 'y2': 10 + 210, 'color': (0, 0, 1, 1)},
            {'id': 6, 'x1': 215, 'y1': 10 + 210, 'x2': 25 + 247, 'y2': 10 + 245, 'color': (0, 0, 0, 1)},
        ]
        self.arrowPanelButtons = [
            {'id': 1, 'x1': 320, 'y1': 10 + 35, 'x2': 48 + 320, 'y2': 10 + 70,
             'image': pyglet.resource.image('img/lineArr2.png'), 'color': (1, 1, 1, 1)},
            {'id': 2, 'x1': 320, 'y1': 10 + 70, 'x2': 48 + 320, 'y2': 10 + 105,
             'image': pyglet.resource.image('img/lineArr1.png'), 'color': (1, 1, 1, 1)},
            {'id': 3, 'x1': 320, 'y1': 10 + 105, 'x2': 48 + 320, 'y2': 10 + 140,
             'image': pyglet.resource.image('img/lineArr.png'), 'color': (1, 1, 1, 1)},
            {'id': 0, 'x1': 320, 'y1': 10 + 140, 'x2': 48 + 320, 'y2': 10 + 175,
             'image': pyglet.resource.image('img/lineWithArr.png'), 'color': (1, 1, 1, 1)},
        ]
        self.widthPanelButtons = [
            {'id': 1, 'x1': 250, 'y1': 10 + 35, 'x2': 50 + 282, 'y2': 10 + 70, 'width': 3},
            {'id': 2, 'x1': 250, 'y1': 10 + 70, 'x2': 50 + 282, 'y2': 10 + 105, 'width': 5},
            {'id': 3, 'x1': 250, 'y1': 10 + 105, 'x2': 50 + 282, 'y2': 10 + 140, 'width': 9},
            {'id': 4, 'x1': 250, 'y1': 10 + 140, 'x2': 50 + 282, 'y2': 10 + 175, 'width': 13},
            {'id': 5, 'x1': 250, 'y1': 10 + 175, 'x2': 50 + 282, 'y2': 10 + 210, 'width': 17},
            {'id': 6, 'x1': 250, 'y1': 10 + 210, 'x2': 50 + 282, 'y2': 10 + 245, 'width': 23},
            {'id': 7, 'x1': 250, 'y1': 10 + 245, 'x2': 50 + 282, 'y2': 10 + 280, 'width': 29},
            {'id': 8, 'x1': 250, 'y1': 10 + 280, 'x2': 50 + 282, 'y2': 10 + 315, 'width': 37},
            # {'id': 9, 'x1': 250, 'y1': 10 + 315, 'x2': 50 + 282, 'y2': 10 + 350, 'width': 45},
            # {'id': 5, 'x1': 250, 'y1': 10 + 175, 'x2': 282, 'y2': 10 + 210, 'width': 32},

        ]
        self.poly = []
        self.x0, self.y0 = 0, 0
        self.cx, self.cy = 0, 0

        self.tool = 1
        self.arr = 0
        self.f = True
        self.drawRight = True

        self.step = 50
        self.screen_width = 800
        self.screen_height = 500
        self.scS = False
        self.arrowPanelVisible = False
        self.images = {}
        self.selFig = {}
        self.selDel = {}
        self.selRes = {}
        self.id = 0
        self.page = 1



        # self.appDialog = wx.App()
        # self.dialog = SubclassDialog()
        # self.dialog.SetTransparent(64)
        # self.dialog.Show(True)

        # frame = wx.Frame(None, wx.ID_ANY, "Hello World")  # A Frame is a top-level self.

        # btnOk = wx.Button(self)
        # btnOk.SetSize(self, size=(100, 32))


        # self.alignToBottomRight(frame)

        # frame.Show(True)

    def alignToBottomRight(self, win):
        dw, dh = wx.DisplaySize()
        w, h = win.GetSize()
        x = dw - w
        y = dh - h
        win.SetPosition((x, y))

    def resize_image(self, input_image_path,
                     output_image_path,
                     size):
        original_image = Image.open(input_image_path)
        original_image.save(output_image_path + '.ori.png')
        width, height = original_image.size
        resized_image = original_image.resize(size)
        width, height = resized_image.size
        resized_image.save(output_image_path)

    def set_color(self):
        # For linux
        if platform == "win32" or platform == "cygwin":
            self.colorPanelVisible = True


        elif platform == "linux":
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

    def resize_image2(self, input_image_path, output_image_path, size):
        original_image = Image.open(input_image_path)
        resized_image = original_image.resize(size)
        resized_image.save(output_image_path)

    def screen_to_canvas(self, x, y):
        x -= self.cx
        y -= self.cy
        return x, y

    def canvas_to_screen(self, x, y):
        x += self.cx
        y += self.cy
        return x, y



    def insert_screenshot(self):
        self.set_visible(False)
        nnam = datetime.strftime(datetime.now(), 'tmp/' + "_%Y_%m_%d_%H_%M_%S") + '.png'
        grab.screenshot_to_file(nnam)
        width = 600
        w = self.width
        h = self.height
        height = 9 * width // 16
        x0, y0 = w - width - self.cx, h - height - self.cy
        self.insert_image_from_file(nnam, x0, y0, width, height)
        self.set_visible(True)
        self.maximize()

    def insert_image_from_file(self, nnam, x0, y0, width, height):
        k = {}
        self.id += 1
        k['id'] = self.id
        k['name'] = 'image'
        k['p'] = []
        k['p'].append({'x': x0, 'y': y0})
        k['p'].append({'x': x0 + width, 'y': y0 + height})
        nnam_ = nnam + ".resize.png"
        self.resize_image2(nnam, nnam_, (width, height))
        image = pyglet.image.load(nnam_)
        self.images[nnam_] = image
        k['image'] = nnam_
        k['thickness'] = self.penWidth
        k['fordel'] = False
        self.figures.append(k)

    def update_fig(self):
        new_list = []
        for f in self.figures:
            if not f['fordel']:
                new_list.append(f)
        self.figures = new_list.copy()

    def on_key_press(self, symbol, modifiers):
        if symbol == 65307:  # ESC
            # TODO поміняти потім
            self.close()
            if winPanel != None:
                winPanel.close()
            # self.on_close()
        elif symbol == 65360:  # Home
            self.page = 1
            self.cx, self.cy = 0, 0
        elif symbol == 100:  # D    Save whiteboard
            print("save")
            self.save()
        elif symbol == 117:  # U    Open whiteboard
            print("load")
            self.load()
            self.clear()
        elif symbol == 65535:  # Delete
            if self.selFig != {}:
                for fig in self.figures:
                    if fig['id'] == self.selFig['fig']:
                        self.selFig = {}
                        fig['fordel'] = True
                        break
            self.update_fig()

        elif symbol == 99:  # Change color
            self.set_color()
        elif symbol == 105:  # Insert image
            names = self.insert_screenshot().split('|')
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
            self.set_fullscreen(self.fullscr)
            self.clear()
        elif symbol == 115:  # set S
            self.insert_screenshot()
            # if platform == "win32" or platform == "cygwin":
            #     self.insert_screenshot()
            # elif platform == "linux":
            #     # self.btnScrInsertInCanvasClick()
            #     self.insert_screenshot()


        elif symbol == 112:  # set pen
            self.tool = 1
        elif symbol == 101:  # set erazer
            self.tool = 2
        elif symbol == 119:  # set width
            self.set_width(self.penWidth)
        elif symbol == 103:  # set grid
            self.isGrid = not self.isGrid
        elif symbol == 109:  # set
            self.set_fullscreen(False)
            self.minimize()
            self.fullscr = True
            self.set_fullscreen(self.fullscr)


        else:
            print('A key was pressed')
            print(symbol)
        self.clear()

    def on_mouse_press(self, x, y, button, modifier):

        self.f = True
        # Перевіряємо чи треба виходити
        if self.isExit:
            if self.width // 2 - 200 < x < self.width // 2 + 200 and self.height // 2 - 100 < y < self.height // 2 + 100:
                self.close()
                # if winPanel != None:
                #     winPanel.close()
                # dialog.Destroy()
            else:
                self.isExit = False

        if button == mouse.LEFT:
            # Якщо панель кольору видима
            if self.colorPanelVisible:
                for btn in self.colorPanelButtons:
                    if btn['x1'] < x < btn['x2'] and btn['y1'] < y < btn['y2']:
                        self.f = False
                        self.penColor = btn['color']
                        self.colorPanelVisible = False
                        # Змінюємо колір вибраної фігури якщо така є
                        if self.selFig != {}:
                            for fig in self.figures:
                                if fig['id'] == self.selFig['fig']:
                                    fig['color'] = self.penColor

                        break
            if self.widthPanelVisible:
                for btn in self.widthPanelButtons:
                    if btn['x1'] < x < btn['x2'] and btn['y1'] < y < btn['y2']:
                        self.f = False
                        self.penWidth = btn['width']
                        self.widthPanelVisible = False
                        # Змінюємо товщину ліній вибраної фігури якщо така є
                        if self.selFig != {}:
                            for fig in self.figures:
                                if fig['id'] == self.selFig['fig']:
                                    fig['thickness'] = self.penWidth
                        break
            if self.arrowPanelVisible:
                for btn in self.arrowPanelButtons:
                    if btn['x1'] < x < btn['x2'] and btn['y1'] < y < btn['y2']:
                        self.f = False
                        self.arr = btn['id']
                        self.arrowPanelVisible = False
                        # print(self.arr)
            for btn in self.buttons:
                btn['sel'] = False
                if btn['align'] == 'right':
                    xx, yy = self.width - btn['x'] - 35, btn['y']
                else:
                    xx, yy = btn['x'], btn['y']
                if (xx < x < xx + 32) and (yy < y < yy + 32):
                    btn['sel'] = True
                    if btn['id'] == 4 or btn['id'] == 5:  # Fill figure
                        if self.tool == btn['tool']:
                            self.isFill = not self.isFill
                        self.tool = btn['tool']
                    elif btn['id'] == 26:  # Діалогове вікно
                        # hide main window
                        self.set_visible(False)
                        # show panel window
                        self.show_screenshot_panel()

                    elif btn['id'] == 101:  # Changr color pen
                        self.colorPanelVisible = not self.colorPanelVisible
                    elif btn['id'] == 102:  # Changr width pen
                        self.widthPanelVisible = not self.widthPanelVisible
                    elif btn['id'] == 106:  # Chang arrow
                        self.arrowPanelVisible = not self.arrowPanelVisible
                    elif btn['id'] == 105:  # Сторінка вправо
                        self.clear()
                        self.page += 1
                        self.cx = self.page * 100000 - 100000
                    elif btn['id'] == 104:  # Сторінка вліво
                        self.clear()
                        self.page -= 1
                        if self.page < 1:
                            self.page = 1
                        self.cx = self.page * 100000 - 100000
                    else:
                        if btn['tool'] != 0:
                            self.tool = btn['tool']
                    self.f = False
                    break

            if self.f:
                if self.tool != 8: self.selFig = {}
                if self.tool == 8:
                    # self.selFig = {}
                    # [{'name': 'polyline', 'p': [{'x': 429, 'y': 444}, {'x': 437, 'y': 448}, {'x': 438, 'y': 449}, {'x': 444, 'y': 449}, {'x': 449, 'y': 450}, {'x': 454, 'y': 450}, {'x': 462, 'y': 451}, {'x': 486, 'y': 451}, {'x': 498, 'y': 450}, {'x': 506, 'y': 446}, {'x': 512, 'y': 440}, {'x': 517, 'y': 432}, {'x': 519, 'y': 420}, {'x': 526, 'y': 401}, {'x': 527, 'y': 395}, {'x': 529, 'y': 391}, {'x': 530, 'y': 386}, {'x': 532, 'y': 382}, {'x': 534, 'y': 377}, {'x': 538, 'y': 372}, {'x': 546, 'y': 359}, {'x': 552, 'y': 352}, {'x': 560, 'y': 343}, {'x': 567, 'y': 338}, {'x': 573, 'y': 336}, {'x': 579, 'y': 332}, {'x': 580, 'y': 332}, {'x': 588, 'y': 332}, {'x': 588, 'y': 332}, {'x': 593, 'y': 331}], 'color': (1, 0, 0, 1), 'thickness': 4, 'fordel': False}]
                    for fig in reversed(self.figures):
                        x1, y1, x2, y2 = border_polyline(fig['p'])
                        x1, y1 = self.canvas_to_screen(x1, y1)
                        x2, y2 = self.canvas_to_screen(x2, y2)
                        # x1, y1, x2, y2 = x1 + self.cx, y1 + self.cy, x2 + self.cx, y2 + self.cy
                        # x -=self.cx; y -=self.cy
                        if ((x > x1) and (x < x2) and (y > y1) and (y < y2)) or (
                                x2 - 18 + 20 < x < x2 - 2 + 20 and y1 + 2 - 20 < y < y1 + 20 - 20):
                            self.selDel = {'x1': x1, 'y1': y1,
                                           'x2': x1 + 20, 'y2': y1 + 20}
                            self.selRes = {'x1': x2 - 18 + 20, 'y1': y1 + 2 - 20,
                                           'x2': x2 - 2 + 20, 'y2': y1 + 20 - 20}
                            # canvas.config(cursor="fleur")
                            xx1 = self.selDel['x1']
                            yy1 = self.selDel['y1']
                            xx2 = self.selDel['x2']
                            yy2 = self.selDel['y2']
                            if self.selDel != {}:
                                if (x > xx1) and (x < xx2) and (y > yy1) and (y < yy2):
                                    # Вилучаємо
                                    print("Вилучаємо")
                                    fig['fordel'] = True
                                    self.update_fig()
                            self.selFig['fig'] = fig['id']

                            fl = True

                            break
                        else:
                            self.selFig = {}
                            self.selDel = {}
                            # canvas.config(cursor="tcross")
                            pass

                elif self.tool == 1:
                    # self.clear()

                    self.x0, self.y0 = self.screen_to_canvas(x, y)
                    self.poly.clear()
                    self.poly.append({'x': self.x0, 'y': self.y0})
                    self.drawRight = False
                elif self.tool == 3:  # line
                    self.x0, self.y0 = self.screen_to_canvas(x, y)
                    self.poly.clear()
                    self.poly.append({'x': self.x0, 'y': self.y0})

                elif self.tool == 4:  # rectangle
                    self.x0, self.y0 = self.screen_to_canvas(x, y)
                    self.poly.clear()
                    self.poly.append({'x': self.x0, 'y': self.y0})
                elif self.tool == 5:  # ellipse
                    self.x0, self.y0 = self.screen_to_canvas(x, y)

                elif self.tool == 26:  # scheenshot mode
                    pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.drawRight: self.clear()

        if self.f:
            if self.tool == 1:
                xx, yy = self.screen_to_canvas(x, y)
                self.poly.append({'x': xx, 'y': yy})
                x0 = self.poly[0]['x']
                y0 = self.poly[0]['y']
                for p in self.poly:
                    x_ = p['x']
                    y_ = p['y']
                    xx0, yy0 = self.canvas_to_screen(x0, y0)
                    xx_, yy_ = self.canvas_to_screen(x_, y_)
                    # draw_fill_circle(xx0, yy0, int(self.penWidth * 0.4), self.penColor)
                    # draw_fill_circle(xx, yy, int(self.penWidth * 0.4), self.penColor)
                    # draw_line(xx0, yy0, xx_, yy_, color=self.penColor, thickness=self.penWidth)
                    xx0, yy0, xx_, yy_ = longer_for_polyline(xx0, yy0, xx_, yy_, self.penWidth, 0.2)
                    draw_line_1(xx0, yy0, xx_, yy_, color=self.penColor, thickness=self.penWidth, smooth=self.isSmooth)
                    x0, y0 = x_, y_
                self.x0, self.y0 = self.screen_to_canvas(x, y)
            elif self.tool == 2:
                draw_line(x + self.errSize // 2, y + self.errSize // 2,
                          x - self.errSize // 2, y - self.errSize // 2, color=(1, 1, 0, 1), thickness=self.errSize)
                for f in self.figures:
                    x_min, y_min, x_max, y_max = border_polyline(f['p'])
                    x_min, y_min = self.canvas_to_screen(x_min, y_min)
                    x_max, y_max = self.canvas_to_screen(x_max, y_max)
                    if dist((x_max + x_min) // 2, (y_max + y_min) // 2, x, y, self.errSize):
                        # print('del')
                        f['fordel'] = True
                        break
                self.update_fig()
                # self.clear()
            elif self.tool == 3:
                draw_line_mod(self.x0 + self.cx, self.y0 + self.cy, x, y, color=self.penColor, fon_color=self.fonColor,
                              thickness=self.penWidth, arrow=self.arr)
                # draw_line(self.x0 + self.cx, self.y0 + self.cy, x, y, color=self.penColor,
                #           thickness=self.penWidth)
            elif self.tool == 5:  # ellipse
                if self.isFill:
                    # draw_fill_ellipse(self.x0 + self.cx, self.y0 + self.cy, x, y, color=self.penColor, thickness=self.penWidth)
                    draw_ellipse(self.x0 + self.cx, self.y0 + self.cy, x, y, color=self.penColor,
                                 thickness=self.penWidth)
                else:
                    draw_ellipse(self.x0 + self.cx, self.y0 + self.cy, x, y, color=self.penColor,
                                 thickness=self.penWidth)

            elif self.tool == 4:
                self.clear()
                if self.isFill:
                    fill_4poly(self.x0 + self.cx, self.y0 + self.cy,
                               self.x0 + self.cx, y,
                               x, y,
                               x, self.y0 + self.cy,  # TODO
                               color=self.penColor)

                else:
                    # draw_rectangle(self.x0 + self.cx, self.y0 + self.cy,
                    #                self.x0 + self.cx, y,
                    #                x, y,
                    #                x, self.y0 + self.cy,
                    #                color=self.penColor, thickness=self.penWidth)
                    x1, y1 = self.canvas_to_screen(self.x0, self.y0)
                    x2, y2 = self.canvas_to_screen(self.x0, y - self.cy)
                    x3, y3 = self.canvas_to_screen(x - self.cx, y - self.cy)
                    x4, y4 = self.canvas_to_screen(x - self.cx, self.y0)
                    draw_rectangle(x1, y1, x2, y2, x3, y3, x4, y4, color=self.penColor, thickness=self.penWidth)


            elif self.tool == 8:
                if self.selFig != {}:
                    for fig in self.figures:
                        if fig['id'] == self.selFig['fig']:
                            x1, y1, x2, y2 = border_polyline(fig['p'])
                            x1, y1 = self.canvas_to_screen(x1, y1)
                            x2, y2 = self.canvas_to_screen(x2, y2)
                            if ((x1 < x < x2 and y1 < y < y2) or self.isMove) and not self.isResize:
                                self.isMove = True
                                self.isResize = False
                                for p in fig['p']:
                                    p['x'] += dx
                                    p['y'] += dy
                                self.selDel['x1'] += dx
                                self.selDel['y1'] += dy
                                self.selDel['x2'] += dx
                                self.selDel['y2'] += dy
                                self.selRes['x1'] += dx
                                self.selRes['y1'] += dy
                                self.selRes['x2'] += dx
                                self.selRes['y2'] += dy
                                break
                            xr1, yr1, xr2, yr2 = self.selRes['x1'], self.selRes['y1'], self.selRes['x2'], \
                                                 self.selRes['y2']
                            if (xr1 - 10 < x < xr2 + 10 and yr1 - 10 < y < yr2 + 10) or self.isResize:
                                self.isMove = False
                                self.isResize = True
                                # Координати верхньої лівої точки x1, y2
                                xx, yy = self.screen_to_canvas(x, y)
                                xx1, yy1 = self.screen_to_canvas(x1, y1)
                                xx2, yy2 = self.screen_to_canvas(x2, y2)
                                for p in fig['p']:
                                    kx = (p['x'] - xx1) / (xx - xx1)
                                    ky = (p['y'] - yy2) / (yy - yy2)
                                    p['x'] += kx * dx
                                    p['y'] += ky * dy
                                self.selDel['x1'] = x1
                                self.selDel['y1'] = y1
                                self.selDel['x2'] = x1 + 20
                                self.selDel['y2'] = y1 + 20

                                self.selRes['x1'] = x2
                                self.selRes['y1'] = y1 - 20
                                self.selRes['x2'] = x2 + 20
                                self.selRes['y2'] = y1
                                if fig['name'] == 'image':
                                    # [{'id': 1, 'name': 'image', 'p': [{'x': 417, 'y': 224}, {'x': 1017, 'y': 561}], 'image': 'tmp/_2020_01_17_21_30_24.png.resize.png', 'thickness': 4, 'fordel': False}]
                                    size = (int(x2 - x1), int(y2 - y1))
                                    # print(size)
                                    self.images[fig['image']] = self.images[fig['image']].resize(size)
                                    # resized_image = self.original_image.resize(size)

                                break

    def on_mouse_release(self, x, y, button, modifiers):

        self.drawRight = True
        if self.f:
            # self.clear()

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
                xx, yy = self.screen_to_canvas(x, y)
                self.poly.append({'x': xx, 'y': yy})
                self.id += 1
                k['id'] = self.id
                k['name'] = 'line'
                k['p'] = self.poly.copy()
                k['color'] = self.penColor
                k['thickness'] = self.penWidth
                k['arrow'] = self.arr
                k['fordel'] = False
                self.figures.append(k)
            elif self.tool == 4:
                k = {}

                x0, y0 = self.x0, self.y0
                xx, yy = self.screen_to_canvas(x, y)
                self.poly.append({'x': xx, 'y': y0})
                self.poly.append({'x': xx, 'y': yy})
                self.poly.append({'x': x0, 'y': yy})
                # self.poly.append({'x': x0 - self.cx, 'y': y - self.cy})
                # self.poly.append({'x': x - self.cx, 'y': y - self.cy})
                # self.poly.append({'x': x - self.cx, 'y': y0 - self.cy})
                self.id += 1
                k['id'] = self.id
                if self.isFill:
                    k['name'] = 'rectangle_fill'
                else:
                    k['name'] = 'rectangle'
                k['p'] = self.poly.copy()
                k['color'] = self.penColor
                k['thickness'] = self.penWidth
                k['fordel'] = False
                self.figures.append(k)
            elif self.tool == 5:
                k = {}
                self.poly = []

                x0, y0 = self.x0, self.y0
                xx, yy = self.screen_to_canvas(x, y)
                self.poly.append({'x': x0, 'y': y0})
                self.poly.append({'x': xx, 'y': yy})
                self.id += 1
                k['id'] = self.id
                if self.isFill:
                    k['name'] = 'ellipse_fill'
                else:
                    k['name'] = 'ellipse'
                k['p'] = self.poly.copy()
                k['color'] = self.penColor
                k['thickness'] = self.penWidth
                k['arrow'] = self.arr
                k['fordel'] = False
                self.figures.append(k)
            elif self.tool == 8:
                if self.isResize:
                    # Зміна розміру малюнка
                    for f in self.figures:
                        if f['name'] == 'image':
                            if self.selFig['fig'] == f['id']:
                                if self.selFig['fig'] != []:
                                    # x1,y1,x2,y2 = border_polyline(self.selFig['fig'])
                                    x0 = f['p'][0]['x']
                                    y0 = f['p'][0]['y']
                                    width = int(f['p'][1]['x'] - x0)
                                    height = int(f['p'][1]['y'] - y0)
                                    ori_image_name = f['image'][:-11]
                                    f['p'][1]['x'] = f['p'][0]['x'] + width
                                    f['p'][1]['y'] = f['p'][0]['y'] + height
                                    f['fordel'] = True
                                    self.update_fig()
                                    self.insert_image_from_file(ori_image_name, x0, y0, width, height)
                                    break

        self.clear()
        self.isMove = False
        self.isResize = False

    def on_draw(self):
        # draw figures in visible part of window
        if self.drawRight:
            # if True:

            w = self.width
            h = self.height
            # Draw grid
            if self.isGrid:
                for y in range(0, h, self.step):
                    draw_line_1(0, y, w, y, color=self.gridColor, thickness=1, smooth=self.isSmooth)
                for x in range(0, w, self.step):
                    draw_line_1(x, 0, x, h, color=self.gridColor, thickness=1, smooth=self.isSmooth)
            count = 0
            for f in self.figures:
                x_min, y_min, x_max, y_max = border_polyline(f['p'])
                x_min, y_min = self.canvas_to_screen(x_min, y_min)
                x_max, y_max = self.canvas_to_screen(x_max, y_max)
                if x_min < w and x_max > 0 and y_min < h and y_max > 0:
                    count += 1
                    if f['name'] == 'polyline':
                        x0 = f['p'][0]['x']
                        y0 = f['p'][0]['y']
                        for p in f['p']:
                            x = p['x']
                            y = p['y']
                            # line(x0 , y0 , x , y , color=f['color'], thickness=f['thickness'])
                            xx0, yy0 = self.canvas_to_screen(x0, y0)
                            xx, yy = self.canvas_to_screen(x, y)
                            xx0, yy0, xx, yy = longer_for_polyline(xx0, yy0, xx, yy, f['thickness'], 0.2)
                            draw_line_1(xx0, yy0, xx, yy, color=f['color'], thickness=f['thickness'],
                                        smooth=self.isSmooth)
                            x0, y0 = x, y
                    elif f['name'] == 'line':
                        x0, y0 = self.canvas_to_screen(f['p'][0]['x'], f['p'][0]['y'])
                        x_, y_ = self.canvas_to_screen(f['p'][1]['x'], f['p'][1]['y'])
                        draw_line_mod(x0, y0, x_, y_, color=f['color'], fon_color=self.fonColor,
                                      thickness=f['thickness'], arrow=f['arrow'])
                    elif f['name'] == 'ellipse':
                        x0, y0 = self.canvas_to_screen(f['p'][0]['x'], f['p'][0]['y'])
                        x_, y_ = self.canvas_to_screen(f['p'][1]['x'], f['p'][1]['y'])
                        draw_ellipse(x0, y0, x_, y_, color=f['color'], thickness=f['thickness'])
                    elif f['name'] == 'ellipse_fill':
                        x0, y0 = self.canvas_to_screen(f['p'][0]['x'], f['p'][0]['y'])
                        x_, y_ = self.canvas_to_screen(f['p'][1]['x'], f['p'][1]['y'])
                        num = max(abs(x0 - x_), abs(y0 - y_)) * 4
                        draw_fill_ellipse(x0, y0, x_, y_, numPoints=num, color=f['color'], thickness=f['thickness'])
                    elif f['name'] == 'rectangle_fill':
                        x1, y1 = self.canvas_to_screen(f['p'][0]['x'], f['p'][0]['y'])
                        x2, y2 = self.canvas_to_screen(f['p'][1]['x'], f['p'][1]['y'])
                        x3, y3 = self.canvas_to_screen(f['p'][2]['x'], f['p'][2]['y'])
                        x4, y4 = self.canvas_to_screen(f['p'][3]['x'], f['p'][3]['y'])
                        fill_4poly(x1, y1, x2, y2, x3, y3, x4, y4, f['color'])
                    elif f['name'] == 'rectangle':
                        x1, y1 = self.canvas_to_screen(f['p'][0]['x'], f['p'][0]['y'])
                        x2, y2 = self.canvas_to_screen(f['p'][1]['x'], f['p'][1]['y'])
                        x3, y3 = self.canvas_to_screen(f['p'][2]['x'], f['p'][2]['y'])
                        x4, y4 = self.canvas_to_screen(f['p'][3]['x'], f['p'][3]['y'])
                        draw_rectangle(x1, y1, x2, y2, x3, y3, x4, y4, color=f['color'], thickness=f['thickness'])
                    elif f['name'] == 'image':
                        x0 = f['p'][0]['x']
                        y0 = f['p'][0]['y']
                        x = f['p'][1]['x']
                        y = f['p'][1]['y']
                        image = self.images[f['image']]
                        # Це щоб не було засвітки
                        draw_line(-10000, -10000, -10001, -10001, (1, 1, 1, 1), thickness=1)
                        image.blit(x0 + self.cx, y0 + self.cy)

                        # image.blit(x + self.cx, y + self.cy )

            # Це щоб не було засвітки на кнопках
            draw_line(-10000, -10000, -10001, -10001, self.fonColor, thickness=1)
            # Draw buttons
            for btn in self.buttons:
                if btn['align'] == 'right':
                    x, y = self.width - btn['x'] - 35, btn['y']
                else:
                    x, y = btn['x'], btn['y']
                btn['image'].blit(x, y)
                if btn['sel']:
                    draw_line(x + 2, y - 2, x + 28, y - 2, color=self.fonColor, thickness=2)
                if btn['id'] == 4:
                    if self.isFill:
                        fill_4poly(x + 2, y + 2,
                                   x + 2, y + 28,
                                   x + 28, y + 28,
                                   x + 28, y + 2, self.penColor)
                if btn['id'] == 5:
                    if self.isFill:
                        draw_fill_ellipse(x + 2, y + 2, x + 28, y + 28, numPoints=100, color=self.penColor)
                        draw_line(-10000, -10000, -10001, -10001, self.fonColor, thickness=1)
                if self.tool == btn['tool']:
                    draw_fill_circle(x + 5, y + 34, 3, color=self.penColor)
                    draw_line(-10000, -10000, -10001, -10001, self.fonColor, thickness=1)
            # # Це щоб не було засвітки на кнопках
            # rectangle(10000, 10000, 10001, 10001, color=(1, 1, 1, 1), thickness=1)
            if self.colorPanelVisible:
                self.draw_color_panel()
            if self.widthPanelVisible:
                self.draw_width_panel()
            if self.arrowPanelVisible:
                self.draw_arrow_panel()
            # рамка виділення
            if self.selFig != {}:
                for fig in self.figures:
                    if fig['id'] == self.selFig['fig']:
                        x1, y1, x2, y2 = border_polyline(fig['p'])
                        x1, y1 = self.canvas_to_screen(x1, y1)
                        x2, y2 = self.canvas_to_screen(x2, y2)
                        draw_ramka_top(x1 - 2, y1 - 2, x2 + 2, y2 + 2,
                                       color=self.ramkaColor, thickness=self.ramkaThickness)
                        # витавляємо малюнок корзини
                        draw_line(-10000, -10000, -10001, -10001, color=self.fonColor, thickness=1)
                        # self.trash_image.blit(self.selDel['x1'] + self.cx,
                        #                       self.selDel['y1'] + self.cy)
                        # self.resize_image.blit(self.selRes['x1'] + self.cx,
                        #                        self.selRes['y1'] + self.cy)
                        close_cross(self.selDel['x1'] + 0, self.selDel['y1'] + 0,
                                    self.selDel['x2'] + 0, self.selDel['y2'] + 0,
                                    color=self.ramkaColor, thickness=self.ramkaThickness
                                    )

                        resize_arr(self.selRes['x1'] + 0, self.selRes['y2'] + 0,
                                   self.selRes['x2'] + 0, self.selRes['y1'] + 0,
                                   color=self.ramkaColor, thickness=self.ramkaThickness)

            labelPage = pyglet.text.Label(str(self.page),
                                          font_name='Arial',
                                          font_size=24,
                                          # x=400, y=200,
                                          x=self.width - 60, y=22,
                                          anchor_x='center', anchor_y='center')
            labelPage.set_style("color", (3, 105, 25, 255))
            labelPage.draw()
            if self.isExit:
                self.label.draw()

        # draw_fill_ellipse(40, 400, 800, 50,  color=(0, 0, 0, 1), thickness=10)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.clear()
        self.cy -= scroll_y * 10

    def on_close(self):
        self.label = pyglet.text.Label('x',
                                       font_name='Wingdings',
                                       font_size=96,
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center')
        self.label.set_style("color", (255, 0, 0, 255))
        self.isExit = True
        self.label.draw()


def oglStart():
    main.l=1
    window = MyWindow(1000, 726, caption="WhiteBoard", resizable=True)
    window.set_location(200, 2)
    # self.maximize()
    window.clear()
    window.on_draw()
    pyglet.app.run()

if __name__ == "__main__":
    oglStart()

