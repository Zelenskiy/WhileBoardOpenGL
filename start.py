#!/usr/bin/python3.6
import glob
import os
import shutil
import time

import subprocess
import datetime
# import wx

# import threading


from graph_ogl import *

import pickle

import pyglet
from PIL import Image
from pyglet.gl import *

from pyglet.window import mouse, ImageMouseCursor

from sys import platform
# import wx

# from dialogWindow import *
import grab
import os.path
import configparser
import zipfile
from sys import argv
from math import ceil

if platform == "win32" or platform == "cygwin":
    pass
elif platform == "linux":
    pass


# winPanel = None


# class MainFrame(wx.Frame):
#     def __init__(self):
#         wx.Frame.__init__(self, None, -1,
#                           style=wx.STAY_ON_TOP | wx.TAB_TRAVERSAL | wx.FRAME_NO_TASKBAR | wx.BORDER_NONE)
#         self.SetTransparent(64)
#
#         self.panel = MainPanel(self)
#         self.Fit()
#         self.Centre()
#         self.SetSize(35, 55)
#         self.SetPosition((10, 40))
#         self.Show()


# class MainPanel(wx.Panel):
#
#     def __init__(self, frame):
#         wx.Panel.__init__(self, frame, )
#         self.x0 = 0
#         self.y0 = 0
#         self.isDown = False
#         self.isRotate = False
#
#         # Button 1
#         button_sizer = self._button_sizer(frame)
#
#         # Main sizer
#         main_sizer = wx.BoxSizer(wx.VERTICAL)
#         main_sizer.Add((0, 20))
#         main_sizer.Add(button_sizer)
#         self.SetSizer(main_sizer)
#         self.Fit()
#
#     def _button_sizer(self, frame):
#         cmd_screenshot = wx.BitmapButton(self, -1, wx.Image("img/ws_win.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
#         button_sizer = wx.BoxSizer(wx.VERTICAL)
#         button_sizer.Add(cmd_screenshot)
#         cmd_screenshot.Bind(wx.EVT_BUTTON, self.OnScrClick)
#         self.Bind(wx.EVT_LEFT_DOWN, self.pnlDown)
#         self.Bind(wx.EVT_MOTION, self.btnMove)
#         self.Bind(wx.EVT_LEFT_UP, self.btnUp)
#
#         return button_sizer
#
#     def btnDownPen(self, event):
#         # print("Down ", event)
#         self.isDown = True
#         self.x0 = event.x
#         self.y0 = event.y
#         window.tool = 1
#
#     def pnlDown(self, event):
#         # print("Down ", event)
#         self.isDown = True
#         self.x0 = event.x
#         self.y0 = event.y
#
#     def btnDownEr(self, event):
#         # print("Down ", event)
#         self.isDown = True
#         self.x0 = event.x
#         self.y0 = event.y
#         window.tool = 2
#
#     def btnMove(self, event):
#         if self.isDown:
#             # print(event.x, event.y)
#             widget = self.GetParent()
#             px, py = widget.GetPosition()
#             xx = px - self.x0 + event.x
#             yy = py - self.y0 + event.y
#             widget.SetPosition((xx, yy))
#
#     def btnUp(self, event):
#         # print("Up ",event)
#
#         self.isDown = False
#
#     def OnBtnClose(self, event):
#         self.close()
#
#     def SetPen(self, event):
#         window.tool = 1
#
#     def SetErr(self, event):
#         window.tool = 2
#
#     def OnScrClick(self, event):
#         window.insert_screenshot()
#
#     def SetColor(self, event, color=(0, 0, 1, 1)):
#         window.penColor = color


# def resize_image(input_image_path,
#                  output_image_path,
#                  size):
#     original_image = Image.open(input_image_path)
#     original_image.save(output_image_path + '.ori.png')
#     resized_image = original_image.resize(size)
#     resized_image.save(output_image_path)
#
#
# def resize_image2(input_image_path, output_image_path, size):
#     original_image = Image.open(input_image_path)
#     resized_image = original_image.resize(size)
#     resized_image.save(output_image_path)
#
#
# def insert_screenshot():
#     # window.set_visible(False)
#     #window.minimize()
#     time.sleep(2)
#
#     nnam = datetime.datetime.strftime(datetime.datetime.now(), 'tmp/' + "_%Y_%m_%d_%H_%M_%S") + '.png'
#     grab.screenshot_to_file(nnam)
#
#     width = 600
#     w = window.width
#     h = window.height
#     height = 9 * width // 16
#     x0, y0 = w - width - window.cx, h - height - window.cy
#     insert_image_from_file(nnam, x0, y0, width, height)
#
#
#
#     # window.set_visible(True)
#     #window.maximize()
#
#
# def insert_image_from_file(nnam, x0, y0, width, height):
#     k = {}
#     window.id += 1
#     k['id'] = window.id
#     k['name'] = 'image'
#     k['p'] = []
#     k['p'].append({'x': x0, 'y': y0})
#     k['p'].append({'x': x0 + width, 'y': y0 + height})
#     nnam_ = nnam + ".resize.png"
#     #print(1)
#
#     resize_image2(nnam, nnam_, (width, height))
#     #print(2)
#
#     image = pyglet.image.load(nnam_)
#     #print(3)
#
#     window.images[nnam_] = image
#     #print(4)
#
#     k['image'] = nnam_
#     k['thickness'] = window.penWidth
#     k['fordel'] = False
#     window.figures.append(k)
#     #print(5)
#     #print("images ", window.images)
#

class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 30)

        # ============ Options ================
        self.load_options()
        self.tik = 0
        self.numVertex = 4
        self.pageMax = 1
        self.incr = 0
        self.screen_width = 0
        self.screen_height = 0

        # self.colorOrrange = (1.0, 0.5, 0.0, 1.0)
        # self.isGrid = True
        # self.isSmooth = False
        # self.penWidth = 7
        # self.errSize = 20
        # self.fullscr = False
        # self.penColor = self.colorOrrange
        # self.ramkaColor = (1, 0.5, 0, 1)
        # self.ramkaThickness = 2
        # self.fonColor = (0.91, 0.98, 0.79, 1.0)
        # self.gridColor = (0.82, 0.82, 0.82, 0.5)

        # ============ End options ================

        glClearColor(*self.fonColor)
        self.figures = []
        self.selectRamka = False
        self.isMinimized = False
        self.isPartingPolylinu = True
        self.isMove = False
        self.multiSelect = False
        self.isResize = False
        self.isExit = False
        self.isFill = False
        self.dragPanel = False
        self.selFigs = []

        self.isBtnClick = False
        self.colorPanelVisible = False
        self.widthPanelVisible = False
        self.figuresPanelVisible = False
        self.dashPanelVisible = False
        self.label = None
        self.pnlx = 75
        self.pnly = 75
        self.imMultisel = [pyglet.resource.image('img/multisel_no.png'), pyglet.resource.image('img/multisel.png')]
        self.buttons = [
            {'id': 20, 'text': 'Hand', 'image': pyglet.resource.image('img/hand.png'), 'tool': 20,
             'sel': False, 'align': 'left', 'command': ''},
            {'id': 8, 'text': 'Pen', 'image': pyglet.resource.image('img/ar.png'), 'tool': 8,
             'sel': False, 'align': 'left', 'command': ''},
            {'id': 1, 'text': 'Pen', 'image': pyglet.resource.image('img/pen.png'), 'tool': 1,
             'sel': True, 'align': 'left', 'command': ''},
            {'id': 2, 'text': 'Erazer', 'image': pyglet.resource.image('img/err.png'), 'tool': 2,
             'sel': False, 'align': 'left', 'command': ''},
            {'id': 9, 'text': 'FonErazer', 'image': pyglet.resource.image('img/errFon.png'), 'tool': 9,
             'sel': False, 'align': 'left', 'command': ''},
            {'id': 3, 'text': 'line', 'image': None, 'tool': 3,
             'sel': False, 'align': 'left', 'command': ''},
            {'id': 6, 'text': 'rectangle', 'image': None, 'tool': 4, 'sel': False, 'align': 'left', 'command': ''},
            {'id': 5, 'text': 'setFill', 'image': pyglet.resource.image('img/FillNotFill.png'), 'tool': 0, 'sel': False,
             'align': 'left', 'command': 'set_fill'},
            {'id': 55, 'text': 'setMultiselect', 'image': self.imMultisel[0], 'tool': 0,
             'sel': False, 'align': 'left', 'command': 'set_multisel'},
            {'id': 26, 'text': 'shot', 'image': pyglet.resource.image('img/shot.png'), 'tool': 26,
             'sel': False, 'align': 'left', 'command': 'set_shot'},
            {'id': 101, 'text': 'color', 'image': pyglet.resource.image('img/palitra.png'), 'tool': 0,
             'sel': False, 'align': 'left', 'command': 'set_colorpanel_visible'},
            {'id': 102, 'text': 'width', 'image': pyglet.resource.image('img/width.png'), 'tool': 0,
             'sel': False, 'align': 'left', 'command': 'set_widthpanel_visible'},

            # {'id': 103, 'text': 'width', 'image': pyglet.resource.image('img/add.png'),
            #  'tool': 0, 'sel': False, 'align': 'left', 'command':''},
            {'id': 106, 'text': 'arrow', 'image': pyglet.resource.image('img/arr.png'), 'tool': 0,
             'sel': False, 'align': 'left', 'command': 'set_arrowpanel_visible'},
            {'id': 107, 'text': 'dash', 'image': pyglet.resource.image('img/dot.png'), 'tool': 0,
             'sel': False, 'align': 'left', 'command': 'set_dashpanel_visible'},
            # {'id': 113, 'text': 'open', 'image': pyglet.resource.image('img/open.png'), 'tool': 0,
            #  'sel': False, 'align': 'left', 'command':''},

            {'id': 104, 'x': 75, 'y': 5, 'text': '<', 'image': pyglet.resource.image('img/left.png'), 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'set_page_left'},
            {'id': 105, 'x': 5, 'y': 5, 'text': '>', 'image': pyglet.resource.image('img/right.png'), 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'set_page_right'},

            {'id': 108, 'x': 75, 'y': 105, 'text': '<', 'image': None, 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'move_108'},
            {'id': 109, 'x': 5, 'y': 105, 'text': '>', 'image': None, 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'move_109'},
            {'id': 112, 'x': 40, 'y': 105, 'text': '...', 'image': None, 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'drag_panel'},
            {'id': 110, 'x': 40, 'y': 75, 'text': 'V', 'image': None, 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'move_110'},
            {'id': 111, 'x': 40, 'y': 135, 'text': 'U', 'image': None, 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'move_111'},

            {'id': 56, 'x': -500, 'y': -500, 'text': 'del selected', 'image': pyglet.resource.image('img/close.png'),
             'tool': 0,
             'sel': False, 'align': '', 'command': 'del_selected'},

            # {'id': 108, 'x': 75, 'y': 105, 'text': '<', 'image': pyglet.resource.image('img/leftb.png'), 'tool': 0,
            #  'sel': False, 'align': 'right', 'command':''},
            # {'id': 109, 'x': 5, 'y': 105, 'text': '>', 'image': pyglet.resource.image('img/rightb.png'), 'tool': 0,
            #  'sel': False, 'align': 'right', 'command':''},
            # {'id': 110, 'x': 40, 'y': 75, 'text': 'V', 'image': pyglet.resource.image('img/down.png'), 'tool': 0,
            #  'sel': False, 'align': 'right', 'command':''},
            # {'id': 111, 'x': 40, 'y': 135, 'text': 'U', 'image': pyglet.resource.image('img/up.png'), 'tool': 0,
            #  'sel': False, 'align': 'right', 'command':''},

        ]
        self.btnPnl = []
        for b in self.buttons:
            if 108 <= b['id'] <= 112:
                self.btnPnl.append(b)
        x = 5
        for b in self.buttons:
            if b['align'] == 'left':
                b['x'] = x
                b['y'] = 5
                x += 35

        self.colorPanelButtons = [
            {'id': 1, 'color': (1, 0, 0, 1)},
            {'id': 2, 'color': (1, 1, 0, 1)},
            {'id': 3, 'color': (0, 0.5, 0, 1)},
            {'id': 4, 'color': (0, 1, 1, 1)},
            {'id': 5, 'color': (0, 0, 1, 1)},
            {'id': 6, 'color': (0, 0, 0, 1)},
            {'id': 7, 'color': (1.0, 0.5, 0.0, 1.0)},
        ]
        self.figuresPanelButtons = [
            {'id': 3, 'tool': 6},
            {'id': 4, 'tool': 4},
            {'id': 5, 'tool': 6},
            {'id': 6, 'tool': 6},
            {'id': 40, 'tool': 6},
        ]
        self.arrowPanelButtons = [
            {'id': 1, 'image': pyglet.resource.image('img/lineArr2.png'), 'color': (1, 1, 1, 1)},
            {'id': 2, 'image': pyglet.resource.image('img/lineArr1.png'), 'color': (1, 1, 1, 1)},
            {'id': 3, 'image': pyglet.resource.image('img/lineArr.png'), 'color': (1, 1, 1, 1)},
            {'id': 0, 'image': pyglet.resource.image('img/lineWithArr.png'), 'color': (1, 1, 1, 1)},
        ]
        self.dashPanelButtons = [
            {'id': 1, 'image': pyglet.resource.image('img/shtrLine.png'), 'color': (1, 1, 1, 1)},
            {'id': 2, 'image': pyglet.resource.image('img/punktir.png'), 'color': (1, 1, 1, 1)},
            {'id': 0, 'image': pyglet.resource.image('img/lineWithArr.png'), 'color': (1, 1, 1, 1)},
        ]
        self.widthPanelButtons = [
            {'id': 1, 'width': 3},
            {'id': 2, 'width': 5},
            {'id': 3, 'width': 9},
            {'id': 4, 'width': 13},
            {'id': 5, 'width': 17},
            {'id': 6, 'width': 23},
            {'id': 7, 'width': 29},
            {'id': 8, 'width': 37},

        ]
        x_palitra, x_figures, x_arrow, x_dash, x_width = 0, 0, 0, 0, 0
        for b in self.buttons:
            if b['id'] == 101:
                x_palitra = b['x']
            if b['id'] == 6:
                x_figures = b['x']
            if b['id'] == 106:
                x_arrow = b['x']
            if b['id'] == 107:
                x_dash = b['x']
            if b['id'] == 102:
                x_width = b['x']

        y0 = 10
        for cp_btn in self.colorPanelButtons:
            cp_btn['x1'] = x_palitra
            cp_btn['x2'] = x_palitra + 55
            y0 += 35
            cp_btn['y1'] = y0
            cp_btn['y2'] = y0 + 35
        y0 = 10
        for f_btn in self.figuresPanelButtons:
            f_btn['x1'] = x_figures
            f_btn['x2'] = x_figures + 25
            y0 += 35
            f_btn['y1'] = y0
            f_btn['y2'] = y0 + 35
        y0 = 10
        for a_btn in self.arrowPanelButtons:
            a_btn['x1'] = x_arrow
            a_btn['x2'] = x_arrow + 55
            y0 += 35
            a_btn['y1'] = y0
            a_btn['y2'] = y0 + 35
        y0 = 10
        for d_btn in self.dashPanelButtons:
            d_btn['x1'] = x_dash
            d_btn['x2'] = x_dash + 55
            y0 += 35
            d_btn['y1'] = y0
            d_btn['y2'] = y0 + 35
        y0 = 10
        for w_btn in self.widthPanelButtons:
            w_btn['x1'] = x_width
            w_btn['x2'] = x_width + 55
            y0 += 35
            w_btn['y1'] = y0
            w_btn['y2'] = y0 + 25

        self.poly = []
        self.x0, self.y0 = 0, 0
        self.cx, self.cy = 0, 0

        self.tool = 1
        self.arr = 0
        self.f = True
        self.drawRight = True
        # self.drawRight = True

        self.step = 50
        self.screen_width = 800
        self.screen_height = 500
        self.scS = False
        self.arrowPanelVisible = False
        self.images = {}
        self.lenesPen = []

        # self.selDel = {}
        # self.selRes = {}
        self.id = 0
        self.dash = 0
        self.page = 1
        self.lastCommand = 1
        # self.wxStart()
        # Тут запустимо програму-панель
        homePath = os.path.dirname(__file__)
        # print(homePath)
        if platform == "win32" or platform == "cygwin":
            subprocess.Popen("lazexe\scrgrub.exe")
        elif platform == "linux":
            # subprocess.Popen(homePath+"/lazexe/scrgrub")
            # subprocess.Popen("lazexe/scrgrub")
            pass
        if len(argv) > 1:
            print(argv[1])
            z = zipfile.ZipFile(argv[1], 'r')
            z.extractall()
            self.load()
        else:
            self.autoload()

            # self.appDialog = wx.App()
        # self.dialog = SubclassDialog()
        # self.dialog.SetTransparent(64)
        # self.dialog.Show(True)

        # frame = wx.Frame(None, wx.ID_ANY, "Hello World")  # A Frame is a top-level self.

        # btnOk = wx.Button(self)
        # btnOk.SetSize(self, size=(100, 32))

        # self.alignToBottomRight(frame)

        # frame.Show(True)
        # pyglet.clock.schedule_interval(self.update, 1 / 10)

    # def show_screenshot_panel(self):
    #     # self.set_visible(False)
    #     result = self.dialog.ShowModal()  # показываем модальный диалог
    #     if result == wx.ID_OK:
    #         #print("OK")
    #         # self.set_visible(True)
    #         self.set_visible(False)
    #         self.insert_screenshot()
    #         # dialog.Destroy()
    #
    #     else:
    #         #print("Cancel")
    #         self.set_visible(True)

    def update(self):
        self.clear()

    def draw_color_panel(self):
        for btn in self.colorPanelButtons:
            draw_fill_rectangle(btn['x1'], btn['y1'], btn['x2'], btn['y2'], btn['color'])

    def draw_figures_panel(self):
        for btn in self.figuresPanelButtons:
            # Малюємо фігури на відповідних місцях панелі
            self.numVertex = btn['id']
            draw_poly(btn['x1'], btn['y1'], btn['x2'], btn['y2'], fill=self.isFill, id=btn['id'], numPoints=btn['id'],
                      color=self.penColor, fon_color=self.fonColor)

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

    def dash_arrow_panel(self):
        for btn in self.dashPanelButtons:
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
        data['pageMax'] = self.pageMax

        with open("tmp/figures.wb", "wb") as fp:
            pickle.dump(data, fp)

    def save_options(self):
        file_name = "wb.ini"

        data = {}
        data['colorOrrange'] = self.colorOrrange
        # data['numVertex'] = self.numVertex
        data['isGrid'] = self.isGrid
        data['isSmooth'] = self.isSmooth
        data['penWidth'] = self.penWidth
        data['errSize'] = self.errSize
        data['fullscr'] = self.fullscr
        data['penColor'] = self.penColor
        data['ramkaColor'] = self.ramkaColor
        data['ramkaThickness'] = self.ramkaThickness
        data['fonColor'] = self.fonColor
        data['gridColor'] = self.gridColor
        data['autosave'] = self.autosave

        config = configparser.ConfigParser()
        config['MAIN'] = data
        with open(file_name, 'w') as configfile:
            config.write(configfile)

    def load_options(self):
        if os.path.exists("tmp"):
            pass
        else:
            os.mkdir('tmp', mode=0o777)
        if os.path.exists("lessons"):
            pass
        else:
            os.mkdir('lessons', mode=0o777)

        file_name = "wb.ini"
        if os.path.exists(file_name):
            config = configparser.ConfigParser()
            config.read(file_name)
            data = config['MAIN']
            s = data['colororrange'].strip()[1:-1].split(',')
            self.colorOrrange = (float(s[0]), float(s[1]), float(s[2]), float(s[3]))
            s = data['pencolor'].strip()[1:-1].split(',')
            self.penColor = (float(s[0]), float(s[1]), float(s[2]), float(s[3]))
            s = data['ramkacolor'].strip()[1:-1].split(',')
            self.ramkaColor = (float(s[0]), float(s[1]), float(s[2]), float(s[3]))
            s = data['foncolor'].strip()[1:-1].split(',')
            self.fonColor = (float(s[0]), float(s[1]), float(s[2]), float(s[3]))
            s = data['gridcolor'].strip()[1:-1].split(',')
            self.gridColor = (float(s[0]), float(s[1]), float(s[2]), float(s[3]))
            # self.numVertex = int(data['numvertex'])
            self.isGrid = data['isgrid'] == 'True'
            self.isSmooth = data['issmooth'] == 'True'
            self.penWidth = int(data['penwidth'])
            self.errSize = int(data['errSize'])
            self.fullscr = data['fullscr'] == 'True'
            self.autosave = data['autosave'] == 'True'
            self.ramkaThickness = int(data['ramkathickness'])

        else:
            self.colorOrrange = (1.0, 0.5, 0.0, 1.0)
            # self.numVertex = 4
            self.isGrid = True
            self.isSmooth = False
            self.autosave = False
            self.penWidth = 7
            self.errSize = 20
            self.fullscr = False
            self.penColor = self.colorOrrange
            self.ramkaColor = (1, 0.5, 0, 1)
            self.ramkaThickness = 2
            self.fonColor = (0.91, 0.98, 0.79, 1.0)
            self.gridColor = (0.82, 0.82, 0.82, 0.2)
            self.save_options()

    def load(self, file=''):

        self.figures = []
        self.images = {}
        if file == '': file = 'tmp/figures.wb'

        with open(file, "rb") as fp:  # Unpickling
            data = pickle.load(fp)
        self.figures = data['figures']
        self.penColor = data['penColor']

        self.penWidth = data['penWidth']
        self.fonColor = data['fonColor']
        self.pageMax = data['pageMax']
        self.id = data['id']
        self.cx = data['cx']
        self.cy = data['cy']
        self.isGrid = data['isGrid']
        # Загрузка images
        for fig in self.figures:
            if fig['name'] == 'image':
                nnam_ = fig['image_name']
                image = pyglet.image.load(nnam_)
                image.anchor_x = image.width // 2
                image.anchor_y = image.height // 2

                self.images[nnam_] = {'sprite': pyglet.sprite.Sprite(image), 'image': image}

    def del_selected(self):
        for sel in self.selFigs:
            fig = sel['figobj']
            fig['fordel'] = True
        self.selFigs = []
        self.update_fig()
        for b in self.buttons:
            if b['id'] == 56:
                b['x'] = -500
                b['y'] = -500
                break

    def set_shot(self):
        self.set_visible(False)
        time.sleep(2)
        self.insert_screenshot()
        self.set_visible(True)

    def set_fill(self):
        # print("Зафарбовуємо чи ні виділену фігуру")
        self.isFill = not self.isFill
        # Зафарбовуємо чи ні виділену фігуру
        if self.tool == 8 and self.selFigs != []:
            for selFig in self.selFigs:
                selFig['figobj']['fill'] = self.isFill

    def set_colorpanel_visible(self):
        self.colorPanelVisible = not self.colorPanelVisible

    def set_multisel(self):
        self.multiSelect = not self.multiSelect
        for b in self.buttons:
            if b['id'] == 55:
                if self.multiSelect:
                    b['image'] = self.imMultisel[1]
                else:
                    b['image'] = self.imMultisel[0]
                break

    def set_widthpanel_visible(self):
        self.widthPanelVisible = not self.widthPanelVisible

    def set_arrowpanel_visible(self):
        self.arrowPanelVisible = not self.arrowPanelVisible

    def set_dashpanel_visible(self):
        self.dashPanelVisible = not self.dashPanelVisible

    def set_page_right(self):
        self.clear()
        self.page += 1
        if self.page > self.pageMax: self.pageMax = self.page
        self.cx = self.page * 100000 - 100000
        self.cy = 0

    def set_page_left(self):
        self.clear()
        self.page -= 1
        if self.page < 1:
            self.page = 1
        self.cx = self.page * 100000 - 100000
        self.cy = 0

    def drag_panel(self):
        self.dragPanel = True

    def move_108(self):
        self.clear()
        self.cx += 100

    def move_109(self):
        self.clear()
        self.cx -= 100

    def move_110(self):
        self.clear()
        self.cy += 100

    def move_111(self):
        self.clear()
        self.cy -= 100

    # def alignToBottomRight(self, win):
    #     dw, dh = wx.DisplaySize()
    #     w, h = win.GetSize()
    #     x = dw - w
    #     y = dh - h
    #     win.SetPosition((x, y))

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

    def screen_to_canvas(self, x, y):
        x -= self.cx
        y -= self.cy
        return x, y

    def canvas_to_screen(self, x, y):
        x += self.cx
        y += self.cy
        return x, y

    def resize_image(self, input_image_path,
                     output_image_path,
                     size):
        original_image = Image.open(input_image_path)
        original_image.save(output_image_path + '.ori.png')
        resized_image = original_image.resize(size)
        resized_image.save(output_image_path)

    def resize_image2(self, input_image_path, output_image_path, size):
        # print("resize_image2 1")
        original_image = Image.open(input_image_path)
        # print("resize_image2 2 size=", size)
        # print("original_image=", original_image)
        resized_image = original_image.resize(size)
        # print("resize_image2 3")
        resized_image.save(output_image_path)
        # print("resize_image2 4")

    # no order
    def insert_from_clipboard(self):
        nnam = datetime.datetime.strftime(datetime.datetime.now(), 'tmp/' + "_%Y_%m_%d_%H_%M_%S") + '.png'
        grab.ins_from_clip(nnam)
        print(nnam)

        width = 600
        w = self.width
        h = self.height
        height = 9 * width // 16
        x0, y0 = w - width - self.cx, h - height - self.cy
        self.insert_image_from_file(nnam, x0, y0, width, height)

    def insert_screenshot(self):
        self.lastCommand = 11
        self.set_visible(False)
        nnam = datetime.datetime.strftime(datetime.datetime.now(), 'tmp/' + "_%Y_%m_%d_%H_%M_%S") + '.png'
        grab.screenshot_to_file(nnam)
        width = 600
        self.set_visible(True)
        # self.maximize()

        w = self.width
        h = self.height
        height = 9 * width // 16
        x0, y0 = w - width - self.cx, h - height - self.cy
        self.insert_image_from_file(nnam, x0, y0, width, height)
        draw_line(-10000, -10000, -10001, -10001, self.fonColor, thickness=1)
        self.clear()

    def insert_image_from_file(self, nnam, x0, y0, width, height):
        k = {}
        self.id += 1
        k['id'] = self.id
        k['name'] = 'image'

        nnam_ = nnam + ".resize.png"
        self.resize_image2(nnam, nnam_, (width, height))
        image = pyglet.image.load(nnam_)

        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        k['p'] = []
        k['p'].append({'x': x0, 'y': y0})
        k['p'].append({'x': x0 + image.width, 'y': y0 + image.height})

        xcenter, ycenter = (x0 + x0 + image.width) / 2, (y0 + y0 + image.height) / 2
        k['center'] = {'x': xcenter, 'y': ycenter}

        # image = pyglet.resource.image(
        #     # image name
        #     nnam_,
        #
        #     # rotates the image 90 degrees clockwise
        #     #rotate=90,
        # )
        self.images[nnam_] = {'sprite': pyglet.sprite.Sprite(image), 'image': image}
        k['image_name'] = nnam_

        k['angle'] = 0
        k['thickness'] = self.penWidth
        k['fordel'] = False
        k['extrem'] = x0, y0, x0 + image.width, y0 + image.height
        self.figures.append(k)
        self.clear()

    def update_fig(self):
        new_list = []
        for f in self.figures:
            if not f['fordel']:
                new_list.append(f)
        self.figures = new_list.copy()
        self.selFigs = []

    def on_key_press(self, symbol, modifiers):
        if symbol == 65307:  # ESC
            self.closeApp()
        elif symbol == 65360:  # Home
            self.page = 1
            self.cx, self.cy = 0, 0
        elif symbol == 100:  # D    Save whiteboard
            self.save()
        elif symbol == 117:  # U    Open whiteboard
            self.load()
            self.clear()
        elif symbol == 65535:  # Delete
            if self.selFigs != []:
                for selFig in self.selFigs:
                    for fig in self.figures:
                        if fig['id'] == selFig['fig']:
                            selFig = {}
                            fig['fordel'] = True

            self.update_fig()

        elif symbol == 99:  # Change color
            self.set_color()
        elif symbol == 105:  # Insert image
            names = self.insert_screenshot().split('|')
        elif symbol == 65451:  # Change thickness +
            self.penWidth += 2
        elif symbol == 65453:  # Change thickness
            self.penWidth -= 2
            if self.penWidth < 1:
                self.penWidth = 1
        elif symbol == 65362:  # move canvas up
            self.cy -= 50
            self.lastCommand = 11
        elif symbol == 65364:  # Change canvas down
            self.cy += 50
            self.lastCommand = 11
        elif symbol == 65361:  # Change canvas left
            self.cx += 50
            self.lastCommand = 11
        elif symbol == 65363:  # Change canvas right
            self.cx -= 50
            self.lastCommand = 11
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
            # print('A key was pressed')
            # print(symbol)
            pass
        self.clear()

    def on_mouse_press(self, x, y, button, modifier):

        # Перевіряємо чи треба виходити
        if self.isExit:
            if self.width // 2 - 200 < x < self.width // 2 + 200 and self.height // 2 - 100 < y < self.height // 2 + 100:
                self.closeApp()
                # if winPanel != None:
                #     winPanel.close()
                # dialog.Destroy()
            else:
                self.isExit = False
        self.clear()
        self.incr = 0
        self.lenesPen = []
        if button == mouse.LEFT:
            self.f = True
            # Якщо панель ... видима
            if self.colorPanelVisible:
                for btn in self.colorPanelButtons:
                    if btn['x1'] < x < btn['x2'] and btn['y1'] < y < btn['y2']:
                        self.f = False
                        self.penColor = btn['color']
                        self.colorPanelVisible = False
                        # Змінюємо колір вибраної фігури якщо така є
                        if self.selFigs != []:
                            for selFig in self.selFigs:
                                fig = selFig['figobj']
                                fig['color'] = self.penColor

                        self.on_draw()
                        break
            if self.figuresPanelVisible:
                for btn in self.figuresPanelButtons:
                    if btn['x1'] < x < btn['x2'] and btn['y1'] < y < btn['y2']:
                        self.f = False
                        self.tool = btn['tool']
                        self.numVertex = btn['id']
                        # if self.tool == 5:
                        #     self.polygone = 40
                        # elif self.tool == 4:
                        #     self.polygone = 4
                        self.figuresPanelVisible = False

                        break
            if self.widthPanelVisible:
                for btn in self.widthPanelButtons:
                    if btn['x1'] < x < btn['x2'] and btn['y1'] < y < btn['y2']:
                        self.f = False
                        self.penWidth = btn['width']
                        self.widthPanelVisible = False
                        # Змінюємо товщину ліній вибраної фігури якщо така є
                        if self.selFig != []:
                            for selFig in self.selFigs:
                                fig = selFig['figobj']
                                fig['thickness'] = self.penWidth
                        break
            if self.arrowPanelVisible:
                for btn in self.arrowPanelButtons:
                    if btn['x1'] < x < btn['x2'] and btn['y1'] < y < btn['y2']:
                        self.f = False
                        self.arr = btn['id']
                        self.arrowPanelVisible = False
            if self.dashPanelVisible:
                for btn in self.dashPanelButtons:
                    if btn['x1'] < x < btn['x2'] and btn['y1'] < y < btn['y2']:
                        self.f = False
                        self.dash = btn['id']
                        self.dashPanelVisible = False
            for btn in self.buttons:
                btn['sel'] = False
                if btn['align'] == 'right':
                    xx, yy = self.width - btn['x'] - 35, btn['y']
                else:
                    xx, yy = btn['x'], btn['y']
                if (xx < x < xx + 32) and (yy < y < yy + 32):
                    btn['sel'] = True
                    # if btn['id'] == 4 or btn['id'] == 5:  # Fill figure
                    #     if self.tool == btn['tool']:
                    #         self.isFill = not self.isFill
                    #     self.tool = btn['tool']
                    tool = 4
                    if btn['command'] != '':
                        eval('self.' + btn['command'] + '()')
                    if btn['id'] == 6:
                        if self.numVertex == 4:
                            tool = 4
                        elif self.numVertex == 40:
                            tool = 5
                        if tool == self.tool:
                            self.figuresPanelVisible = not self.figuresPanelVisible
                        else:
                            self.tool = tool

                        # if self.tool == btn['tool']:
                        #     self.figuresPanelVisible = not self.figuresPanelVisible
                        #     self.draw_figures_panel()
                        # if self.polygone == 4:
                        #     self.tool = 4
                        # elif self.polygone == 40:
                        #     self.tool = 5



                    else:
                        if btn['tool'] != 0:
                            self.tool = btn['tool']
                    self.f = False
                    break

            if self.f:
                if self.tool != 8: self.selFigs = []
                if self.tool == 8:
                    if not self.multiSelect:
                        self.selFigs = []
                    # if modifier!=[]
                    pSel = []
                    for selFig in self.selFigs:
                        fig = selFig['figobj']
                        pSel += fig['p']
                    cx1, cy1, cx2, cy2 = border_polyline(pSel)
                    cx1, cy1 = self.canvas_to_screen(cx1, cy1)
                    cx2, cy2 = self.canvas_to_screen(cx2, cy2)

                    flag3 = ((cx2 < x < cx2 + 40) and (cy1 - 40 < y < cy1))
                    flag2 = ((cx1 < x < cx2) and (cy1 < y < cy2)) or flag3
                    flag = False
                    flag4 = False
                    for fig in reversed(self.figures):
                        x1, y1, x2, y2 = border_polyline(fig['p'])
                        x1, y1 = self.canvas_to_screen(x1, y1)
                        x2, y2 = self.canvas_to_screen(x2, y2)
                        # x-5,y0+5,x+25,y0-25
                        if ((x1 < x < x2) and (y1 < y < y2)):
                            flag4 = False
                        if ((x > x1) and (x < x2) and (y > y1) and (y < y2)) or (
                                (x2 + 2 < x < x2 + 18) and (y1 - 18 < y < y1)):
                            flag = True
                            selDel = {'x1': x1, 'y1': y1,
                                      'x2': x1 + 20, 'y2': y1 + 20}
                            # selRes = {'x1': x2 - 18 + 20, 'y1': y1 + 2 - 20,
                            #           'x2': x2 - 2 + 20, 'y2': y1 + 20 - 20}
                            # canvas.config(cursor="fleur")
                            xx1 = selDel['x1']
                            yy1 = selDel['y1']
                            xx2 = selDel['x2']
                            yy2 = selDel['y2']
                            if selDel != {}:
                                if (x > xx1) and (x < xx2) and (y > yy1) and (y < yy2) and len(self.selFigs) == 1:
                                    # Вилучаємо
                                    fig['fordel'] = True
                                    self.update_fig()
                            # Якщо ця фігура виділена, то повторно її не виділяємо
                            f1 = False
                            for sF in self.selFigs:
                                if sF['figobj']['id'] == fig['id']:
                                    f1 = True
                                    break
                            if not f1:
                                self.selFigs.append({})
                                self.selFigs[-1]['fig'] = fig['id']
                                self.selFigs[-1]['figobj'] = fig
                                self.selFigs[-1]['selDel'] = selDel
                                # self.selFigs[-1]['selRes'] = selRes
                                break

                    # Якщо клацнули поза фігурами, виділення знімаємо зі всіх
                    if not flag and not flag2:
                        self.selFigs = []
                    # Починаємо виділення рамкою
                    if not flag and not (self.isRotate or self.isMove or self.isResize) and not flag4 and len(
                            self.selFigs) < 1:
                        self.selectRamka = True
                        self.multiSelect = False
                        self.set_multisel()
                        self.x0 = x
                        self.y0 = y


                elif self.tool == 1 or self.tool == 9:
                    self.drawRight = True
                    self.x0, self.y0 = self.screen_to_canvas(x, y)
                    self.poly.clear()
                    self.poly.append({'x': self.x0, 'y': self.y0})
                    self.drawRight = len(self.figures) < 3 or self.lastCommand == 11
                # elif self.tool == 1:
                #     # self.clear()
                #     self.x0, self.y0 = self.screen_to_canvas(x, y)
                #     self.poly.clear()
                #     self.poly.append({'x': self.x0, 'y': self.y0})
                #     # self.drawRight = len(self.figures) < 3 or self.lastCommand == 11
                elif self.tool == 3:  # line
                    self.x0, self.y0 = self.screen_to_canvas(x, y)
                    self.poly.clear()
                    self.poly.append({'x': self.x0, 'y': self.y0})
                elif self.tool == 4:  # rectangle
                    self.x0, self.y0 = self.screen_to_canvas(x, y)
                    self.poly.clear()
                    self.poly.append({'x': self.x0, 'y': self.y0})
                elif self.tool == 5 or self.tool == 6:  # ellipse
                    self.x0, self.y0 = self.screen_to_canvas(x, y)
                    self.poly.clear()
                    self.poly.append({'x': self.x0, 'y': self.y0})
                # elif self.tool == 26:  # scheenshot mode
                #     pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.incr += 1
        # if self.drawRight: self.clear()
        if self.dragPanel:
            for b in self.btnPnl:
                b['x'] -= dx
                b['y'] += dy

        elif self.f:
            if self.tool == 1 or self.tool == 9:
                # draw_circle(x,y,2,color=(1,0,0,1),thickness=1)
                xx, yy = self.screen_to_canvas(x, y)
                self.poly.append({'x': xx, 'y': yy})
                x0 = self.poly[0]['x']
                y0 = self.poly[0]['y']
                if not self.isPartingPolylinu:
                    for p in self.poly:
                        x_ = p['x']
                        y_ = p['y']
                        xx0, yy0 = self.canvas_to_screen(x0, y0)
                        xx_, yy_ = self.canvas_to_screen(x_, y_)
                        if self.tool == 1:
                            pW = self.penWidth
                            color = self.penColor
                        else:
                            pW = self.errSize
                            color = self.fonColor
                        # xx0, yy0, xx_, yy_ = longer_for_polyline(xx0, yy0, xx_, yy_, pW, 0.2)
                        # self.lenesPen.append({'x1':xx0, 'y1':yy0, 'x2':xx_, 'y2':yy_, 'color':color, 'thickness':pW, 'smooth':self.isSmooth})
                        draw_line_1(xx0, yy0, xx_, yy_, color=color, thickness=pW, smooth=self.isSmooth)
                        x0, y0 = x_, y_
                else:

                    k = {}
                    self.id += 1
                    k['id'] = self.id
                    k['name'] = 'polyline'
                    x_0, y_0 = self.x0, self.y0

                    k['p'] = [{'x': x_0, 'y': y_0}, {'x': xx, 'y': yy}, ]

                    x0, y0, xx, yy = min(x_0, xx), min(y_0, yy), max(x_0, xx), max(y_0, yy)
                    k['extrem'] = x0, y0, xx, yy
                    xcenter, ycenter = (x0 + xx) / 2, (y0 + yy) / 2
                    if self.tool == 1:
                        pW = self.penWidth
                        color = self.penColor
                    else:
                        pW = self.errSize
                        color = self.fonColor
                    k['center'] = {'x': xcenter, 'y': ycenter}
                    k['color'] = color
                    k['thickness'] = pW
                    k['fordel'] = False

                    self.figures.append(k)

                self.x0, self.y0 = self.screen_to_canvas(x, y)
            # elif self.tool == 9:  # Витирання кольором фону
            #     # self.drawRight = True
            #     xx, yy = self.screen_to_canvas(x, y)
            #     self.poly.append({'x': xx, 'y': yy})
            #     x0 = self.poly[0]['x']
            #     y0 = self.poly[0]['y']
            #     for p in self.poly:
            #         x_ = p['x']
            #         y_ = p['y']
            #         xx0, yy0 = self.canvas_to_screen(x0, y0)
            #         xx_, yy_ = self.canvas_to_screen(x_, y_)
            #         xx0, yy0, xx_, yy_ = longer_for_polyline(xx0, yy0, xx_, yy_, self.penWidth, 0.2)
            #         draw_line_1(xx0, yy0, xx_, yy_, color=self.fonColor, thickness=self.errSize, smooth=False)
            #         x0, y0 = x_, y_
            #     self.x0, self.y0 = self.screen_to_canvas(x, y)
            elif self.tool == 2:
                if self.incr % 4 == 0: self.clear()
                draw_fill_rectangle(x + self.errSize // 2, y + self.errSize // 2, x - self.errSize // 2,
                                    y - self.errSize // 2, color=(1, 1, 0, 1))
                # draw_line(x + self.errSize // 2, y + self.errSize // 2,
                #           x - self.errSize // 2, y - self.errSize // 2, color=(1, 1, 0, 1), thickness=self.errSize)
                for f in self.figures:
                    x_min, y_min, x_max, y_max = border_polyline(f['p'])
                    x_min, y_min = self.canvas_to_screen(x_min, y_min)
                    x_max, y_max = self.canvas_to_screen(x_max, y_max)
                    if dist((x_max + x_min) // 2, (y_max + y_min) // 2, x, y, self.errSize):
                        # #print('del')
                        f['fordel'] = True
                        break
                self.update_fig()
                # self.clear()
            elif self.tool == 3:
                self.clear()
                draw_line_mod(self.x0 + self.cx, self.y0 + self.cy, x, y, color=self.penColor, fon_color=self.fonColor,
                              thickness=self.penWidth, arrow=self.arr, dash=self.dash)
                # draw_line(self.x0 + self.cx, self.y0 + self.cy, x, y, color=self.penColor,
                #           thickness=self.penWidth)
            # elif self.tool == 5:  # ellipse
            #     if self.isFill:
            #         # draw_fill_ellipse(self.x0 + self.cx, self.y0 + self.cy, x, y, color=self.penColor, thickness=self.penWidth)
            #         draw_ellipse(self.x0 + self.cx, self.y0 + self.cy, x, y, color=self.penColor,
            #                      thickness=self.penWidth)
            #     else:
            #         draw_ellipse(self.x0 + self.cx, self.y0 + self.cy, x, y, color=self.penColor,
            #                      thickness=self.penWidth)
            elif self.tool == 6:  # polygone
                self.clear()
                draw_poly_wo_bg(self.x0 + self.cx, self.y0 + self.cy, x, y, color=self.penColor,
                                fill=self.isFill, thickness=self.penWidth, numPoints=self.numVertex, id=self.numVertex,
                                dash=self.dash)
            elif self.tool == 4:
                self.clear()
                if self.isFill:
                    fill_4poly(self.x0 + self.cx, self.y0 + self.cy,
                               self.x0 + self.cx, y,
                               x, y,
                               x, self.y0 + self.cy,  # TODO
                               color=self.penColor)

                else:
                    x1, y1 = self.canvas_to_screen(self.x0, self.y0)
                    x2, y2 = self.canvas_to_screen(self.x0, y - self.cy)
                    x3, y3 = self.canvas_to_screen(x - self.cx, y - self.cy)
                    x4, y4 = self.canvas_to_screen(x - self.cx, self.y0)
                    draw_rectangle(x1, y1, x2, y2, x3, y3, x4, y4, color=self.penColor, thickness=self.penWidth,
                                   dash=self.dash)
            elif self.tool == 20:
                self.cx += dx
                self.cy += dy
                self.clear()
            elif self.tool == 8:
                self.clear()
                if self.selectRamka:
                    # x0, y0 = self.canvas_to_screen(self.x0, self.y0)
                    # print("222222222")
                    draw_polygon([{'x': self.x0, 'y': self.y0},
                                  {'x': x, 'y': self.y0},
                                  {'x': x, 'y': y},
                                  {'x': self.x0, 'y': y}],
                                 color=self.ramkaColor, thickness=1, dash=0)
                else:
                    pSel = []
                    for selFig in self.selFigs:
                        fig = selFig['figobj']
                        pSel.append({'coord': fig['p'], 'name': fig['name'], 'figobj': fig})
                    cx1, cy1, cx2, cy2 = border_polyline_1(pSel)
                    cx1, cy1 = self.canvas_to_screen(cx1, cy1)
                    cx2, cy2 = self.canvas_to_screen(cx2, cy2)
                    x_center, y_center, = (cx1 + cx2) / 2, (cy1 + cy2) / 2
                    # Умова для перетягування
                    if (((cx1 < x < cx2 and cy1 < y < cy2) and not ((cy2 - 20 < y < cy2) and (
                            x_center - 10 < x < x_center + 10)) or self.isMove) and not self.isResize) and (
                            not self.isRotate):
                        # print("Тягнемо")
                        # print("self.isRotate", self.isRotate)
                        self.isResize = False
                        self.isMove = True
                        self.isRotate = False
                        for fi in pSel:
                            for p in fi['coord']:
                                p['x'] += dx
                                p['y'] += dy
                    # Умова для зміни розмірів #x-5,y0+5,x+25,y0-25
                    elif (((cx2 - 5 < x < cx2 + 25) and (cy1 - 25 < y < cy1 + 5)) or self.isResize) and (
                            not self.isRotate):
                        self.isResize = True
                        self.isMove = False
                        self.isRotate = False

                        xx, yy = self.screen_to_canvas(x, y)
                        cx1, cy1 = self.screen_to_canvas(cx1, cy1)
                        cx2, cy2 = self.screen_to_canvas(cx2, cy2)
                        for fi in pSel:
                            for p in fi['coord']:
                                kx = (p['x'] - cx1) / (xx - cx1)
                                ky = (p['y'] - cy2) / (yy - cy2)
                                p['x'] += kx * dx
                                p['y'] += ky * dy


                    # умова для обертання
                    elif ((cy2 - 20 < y < cy2) and (x_center - 10 < x < x_center + 10)) or self.isRotate:
                        self.isResize = False
                        self.isMove = False
                        self.isRotate = True
                        x0, y0 = self.screen_to_canvas(x_center, y_center)
                        angle = math.atan(-dx / 100)
                        for fi in pSel:
                            for p in fi['coord']:
                                xx, yy = p['x'], p['y']
                                if fi['name'] != 'image':
                                    p['x'] = (xx - x0) * math.cos(angle) - (yy - y0) * math.sin(angle) + x0
                                    p['y'] = (xx - x0) * math.sin(angle) + (yy - y0) * math.cos(angle) + y0
                                else:
                                    fi['figobj']['angle'] -= angle * 180 / math.pi
                                    # x0, y0 = x0 + (xx - x0), y0 + (yy - y0)
                                    # p['x'] = (xx - x0) * math.cos(angle) - (yy - y0) * math.sin(angle) + x0
                                    # p['y'] = (xx - x0) * math.sin(angle) + (yy - y0) * math.cos(angle) + y0

                    cx1, cy1, cx2, cy2 = border_polyline_1(pSel)
                    cx1, cy1 = self.canvas_to_screen(cx1, cy1)
                    cx2, cy2 = self.canvas_to_screen(cx2, cy2)
                    if len(self.selFigs) > 1:
                        for b in self.buttons:
                            if b['id'] == 56:
                                b['x'] = cx1 - 20
                                b['y'] = cy2 - 20
                                break

    # def parting(self, xs, parts):
    #     part_len = ceil(len(xs) / parts)
    #     return [xs[part_len * k:part_len * (k + 2)] for k in range(parts)]

    def on_mouse_release(self, x, y, button, modifiers):
        self.dragPanel = False
        self.drawRight = True
        self.lenesPen = []
        if self.selectRamka:
            self.selectRamka = False
            xx, yy = self.screen_to_canvas(x, y)
            x0, y0 = self.screen_to_canvas(self.x0, self.y0)
            if x0 > xx: x0, xx = xx, x0
            if y0 > yy: y0, yy = yy, y0

            for fig in self.figures:
                x_min, y_min, x_max, y_max = border_polyline(fig['p'])
                if (x0 < x_min and xx > x_max) and (y0 < y_min and yy > y_max):
                    self.selFigs.append({'fig': fig['id'], 'figobj': fig})

        else:
            xx, yy = self.width - 75 - self.pnlx, 75 + self.pnly
            if not ((xx < x < xx + 100) and (yy < y < yy + 100)):
                if self.f:
                    # self.clear()

                    if self.tool == 1 or self.tool == 9:
                        # if self.isPartingPolylinu:
                        #     parts = len(self.poly)  // 10
                        #     if parts == 0: parts = 1
                        # else:
                        #     parts = 1
                        # poly_s = self.parting(self.poly, parts)
                        #
                        # for poly in poly_s:
                        #     k = {}
                        #     self.id += 1
                        #     k['id'] = self.id
                        #     k['name'] = 'polyline'
                        #     k['p'] = poly
                        #     x0, y0, xx, yy = border_polyline(k['p'])
                        #     k['extrem'] = x0, y0, xx, yy
                        #     xcenter, ycenter = (x0 + xx) / 2, (y0 + yy) / 2
                        #     if self.tool == 1:
                        #         pW = self.penWidth
                        #         color = self.penColor
                        #     else:
                        #         pW = self.errSize
                        #         color = self.fonColor
                        #     k['center'] = {'x': xcenter, 'y': ycenter}
                        #     k['color'] = color
                        #     k['thickness'] = pW
                        #     k['fordel'] = False
                        #
                        #     self.figures.append(k)

                        if self.isPartingPolylinu:
                            pass
                            # x_0, y_0 = self.poly[0]['x'],self.poly[0]['y']
                            # for line in self.poly:
                            #     k = {}
                            #     self.id += 1
                            #     k['id'] = self.id
                            #     k['name'] = 'polyline'
                            #     k['p'] = [{'x': x_0, 'y': y_0}, {'x': line['x'], 'y': line['y']}, ]
                            #     x_0, y_0 = line['x'], line['y']
                            #     # k['p'] = self.poly.copy()
                            #     x0, y0, xx, yy = min(x_0, line['x']), min(y_0, line['y']), max(x_0, line['x']), max(y_0, line['y'])
                            #     k['extrem'] = x0, y0, xx, yy
                            #     xcenter, ycenter = (x0 + xx) / 2, (y0 + yy) / 2
                            #     if self.tool == 1:
                            #         pW = self.penWidth
                            #         color = self.penColor
                            #     else:
                            #         pW = self.errSize
                            #         color = self.fonColor
                            #     k['center'] = {'x': xcenter, 'y': ycenter}
                            #     k['color'] = color
                            #     k['thickness'] = pW
                            #     k['fordel'] = False
                            #
                            #     self.figures.append(k)

                        else:
                            k = {}
                            self.id += 1
                            k['id'] = self.id
                            k['name'] = 'polyline'
                            k['p'] = self.poly.copy()
                            # k['p'] = self.poly.copy()
                            x0, y0, xx, yy = border_polyline(k['p'])
                            k['extrem'] = x0, y0, xx, yy
                            xcenter, ycenter = (x0 + xx) / 2, (y0 + yy) / 2
                            if self.tool == 1:
                                pW = self.penWidth
                                color = self.penColor
                            else:
                                pW = self.errSize
                                color = self.fonColor
                            k['center'] = {'x': xcenter, 'y': ycenter}
                            k['color'] = color
                            k['thickness'] = pW
                            k['fordel'] = False

                            self.figures.append(k)
                    # if self.tool == 9:
                    #     k = {}
                    #     self.id += 1
                    #     k['id'] = self.id
                    #     k['name'] = 'polyline'
                    #     k['p'] = self.poly.copy()
                    #     x0, y0, xx, yy = border_polyline(k['p'])
                    #     xcenter, ycenter = (x0 + xx) / 2, (y0 + yy) / 2
                    #     k['center'] = {'x': xcenter, 'y': ycenter}
                    #     k['color'] = self.fonColor
                    #     k['thickness'] = self.errSize
                    #     k['fordel'] = False
                    #     self.figures.append(k)
                    elif self.tool == 3:
                        k = {}
                        x0, y0 = self.screen_to_canvas(self.x0, self.y0)
                        xx, yy = self.screen_to_canvas(x, y)
                        self.poly.append({'x': xx, 'y': yy})
                        self.id += 1
                        k['id'] = self.id
                        k['name'] = 'line'
                        k['p'] = self.poly.copy()
                        xcenter, ycenter = (x0 + xx) / 2, (y0 + yy) / 2
                        k['center'] = {'x': xcenter, 'y': ycenter}
                        k['color'] = self.penColor
                        k['thickness'] = self.penWidth
                        k['arrow'] = self.arr
                        k['dash'] = self.dash
                        k['fordel'] = False
                        k['extrem'] = min(x0, xx), min(y0, yy), max(x0, xx), max(y0, yy)
                        self.figures.append(k)
                    elif self.tool == 4:
                        k = {}

                        # x0, y0 = self.screen_to_canvas(self.x0, self.y0)
                        x0, y0 = self.poly[0]['x'], self.poly[0]['y']
                        xx, yy = self.screen_to_canvas(x, y)
                        self.poly.append({'x': xx, 'y': y0})
                        self.poly.append({'x': xx, 'y': yy})
                        self.poly.append({'x': x0, 'y': yy})
                        self.id += 1
                        k['id'] = self.id
                        if self.isFill:
                            k['name'] = 'quadrangle_fill'
                        else:
                            k['name'] = 'quadrangle'
                        k['p'] = self.poly.copy()
                        k['color'] = self.penColor
                        xcenter, ycenter = (x0 + xx) / 2, (y0 + yy) / 2
                        k['center'] = {'x': xcenter, 'y': ycenter}
                        k['thickness'] = self.penWidth
                        k['dash'] = self.dash
                        k['fill'] = self.isFill
                        k['fordel'] = False
                        k['extrem'] = min(x0, xx), min(y0, yy), max(x0, xx), max(y0, yy)
                        self.figures.append(k)
                    elif self.tool == 6:
                        k = {}
                        x0, y0 = self.x0, self.y0
                        xx, yy = self.screen_to_canvas(x, y)
                        x0, y0 = self.poly[0]['x'], self.poly[0]['y']
                        points = border_to_points(x0, y0, xx, yy, numPoints=self.numVertex)

                        self.id += 1
                        k['id'] = self.id
                        if self.isFill:
                            k['name'] = 'polygone_fill'
                        else:
                            k['name'] = 'polygone'
                        k['p'] = points
                        x0, y0, xx, yy = border_polyline(k['p'])
                        k['extrem'] = x0, y0, xx, yy
                        xcenter, ycenter = (x0 + xx) / 2, (y0 + yy) / 2
                        k['center'] = {'x': xcenter, 'y': ycenter}
                        # k['numVertex'] = self.numVertex
                        k['fill'] = self.isFill
                        k['dash'] = self.dash
                        k['color'] = self.penColor
                        k['thickness'] = self.penWidth
                        k['fordel'] = False
                        self.figures.append(k)
                    elif self.tool == 8:
                        if self.isResize:
                            # Зміна розміру малюнка
                            for selFig in self.selFigs:
                                f = selFig['figobj']
                                if f['name'] == 'image':
                                    if selFig['fig'] == f['id']:
                                        if selFig['fig'] != []:
                                            x0 = f['p'][0]['x']
                                            y0 = f['p'][0]['y']
                                            width = int(f['p'][1]['x'] - x0)
                                            height = int(f['p'][1]['y'] - y0)
                                            ori_image_name = f['image_name'][:-11]
                                            f['p'][1]['x'] = f['p'][0]['x'] + width
                                            f['p'][1]['y'] = f['p'][0]['y'] + height
                                            f['fordel'] = True
                                            self.update_fig()
                                            self.insert_image_from_file(ori_image_name, x0, y0, width, height)
                                            break
                        pSel = []
                        for selFig in self.selFigs:
                            fig = selFig['figobj']
                            cx1, cy1, cx2, cy2 = border_polyline(fig['p'])
                            fig['extrem'] = cx1, cy1, cx2, cy2
                            pSel += fig['p']
                        cx1, cy1, cx2, cy2 = border_polyline(pSel)

                        cx1, cy1 = self.canvas_to_screen(cx1, cy1)
                        cx2, cy2 = self.canvas_to_screen(cx2, cy2)
                        if len(self.selFigs) > 1:
                            for b in self.buttons:
                                if b['id'] == 56:
                                    b['x'] = cx1 - 20
                                    b['y'] = cy2 - 20
                                    break
        self.clear()
        self.isMove = False
        self.isResize = False
        self.isRotate = False
        self.lastCommand = 0
        # print(self.figures)
        if len(self.selFigs) < 2:
            for b in self.buttons:
                if b['id'] == 56:
                    b['x'] = -500
                    b['y'] = -500
                    break

    def on_draw(self):
        # Перевіряємо наявність зовнішніх даних та підвантажуємо їх за потребою

        self.drawRight = True
        # if self.drawRight:

        w = self.screen_width
        h = self.screen_height
        count = 0
        if self.isGrid:
            for y in range(0, h, self.step):
                draw_line_1(0, y, w, y, color=self.gridColor, thickness=1, smooth=self.isSmooth, dash=0)
            for x in range(0, w, self.step):
                draw_line_1(x, 0, x, h, color=self.gridColor, thickness=1, smooth=self.isSmooth, dash=0)

        # print("len figures ", len(self.figures))

        for f in self.figures:
            r = f['thickness'] // 2
            self.x_min, self.y_min, self.x_max, self.y_max = f['extrem']
            x_min, y_min, x_max, y_max = f['extrem']
            # x_min, y_min, x_max, y_max = border_polyline(f['p'])
            x_min, y_min = self.canvas_to_screen(x_min, y_min)
            x_max, y_max = self.canvas_to_screen(x_max, y_max)
            # if x_min < w and x_max > 0 and y_min < h and y_max > 0:
            if x_min < self.width and x_max > 0 and y_min < self.height and y_max > 0:
                count += 1
                if f['name'] == 'polyline':
                    x0 = f['p'][0]['x']
                    y0 = f['p'][0]['y']
                    for p in f['p']:
                        x = p['x']
                        y = p['y']
                        xx0, yy0 = self.canvas_to_screen(x0, y0)
                        xx, yy = self.canvas_to_screen(x, y)

                        # draw_fill_circle(x0,y0,r,color=f['color'],thickness=1)
                        # draw_fill_circle(xx,yy,r,color=f['color'],thickness=1)
                        draw_line_1(xx0, yy0, xx, yy, color=f['color'], thickness=f['thickness'],
                                    smooth=self.isSmooth)
                        # draw_line_1(xx0, yy0, xx, yy, color=f['color'], thickness=f['thickness'],
                        #             smooth=self.isSmooth)
                        x0, y0 = x, y
                elif f['name'] == 'line':
                    x0, y0 = self.canvas_to_screen(f['p'][0]['x'], f['p'][0]['y'])
                    x_, y_ = self.canvas_to_screen(f['p'][1]['x'], f['p'][1]['y'])
                    draw_line_mod(x0, y0, x_, y_, color=f['color'], fon_color=self.fonColor,
                                  thickness=f['thickness'], arrow=f['arrow'], dash=f['dash'])
                elif f['name'] == 'quadrangle_fill' or f['name'] == 'quadrangle':
                    x1, y1 = self.canvas_to_screen(f['p'][0]['x'], f['p'][0]['y'])
                    x2, y2 = self.canvas_to_screen(f['p'][1]['x'], f['p'][1]['y'])
                    x3, y3 = self.canvas_to_screen(f['p'][2]['x'], f['p'][2]['y'])
                    x4, y4 = self.canvas_to_screen(f['p'][3]['x'], f['p'][3]['y'])
                    if f['fill']:
                        fill_4poly(x1, y1, x2, y2, x3, y3, x4, y4, f['color'])
                    else:
                        points = [{'x': x1, 'y': y1}, {'x': x2, 'y': y2}, {'x': x3, 'y': y3}, {'x': x4, 'y': y4}]
                        draw_polygon(points, color=f['color'], thickness=f['thickness'], dash=f['dash'])
                elif f['name'] == 'polygone' or f['name'] == 'polygone_fill':
                    np = []
                    for p in f['p']:
                        x, y = self.canvas_to_screen(p['x'], p['y'])
                        np.append({'x': x, 'y': y})
                    if f['fill']:
                        draw_fill_polygon(np, color=f['color'], thickness=f['thickness'])
                    else:
                        draw_polygon(np, color=f['color'], thickness=f['thickness'], dash=f['dash'])
                elif f['name'] == 'image':
                    x0 = f['p'][0]['x']
                    y0 = f['p'][0]['y']
                    xcenter, ycenter = f['center']['x'], f['center']['y']

                    # Це щоб не було засвітки
                    draw_line(-10000, -10000, -10001, -10001, (1, 1, 1, 1), thickness=1)

                    # Центр обертання.
                    image = self.images[f['image_name']]['image']
                    w = image.width // 2
                    h = image.height // 2

                    # Кут повороту
                    self.images[f['image_name']]['sprite'].rotation = f['angle']

                    # координати лівого нижнього кута з ккординат центра
                    self.images[f['image_name']]['sprite'].position = (x0 + w + self.cx, y0 + h + self.cy)

                    self.images[f['image_name']]['sprite'].draw()

        # Draw grid
        # Це щоб не було засвітки на кнопках
        draw_line(-10000, -10000, -10001, -10001, self.fonColor, thickness=1)
        # Draw buttons
        for btn in self.buttons:
            if btn['align'] == 'right':
                x, y = self.width - btn['x'] - 35, btn['y']
            else:
                x, y = btn['x'], btn['y']
            if btn['image'] != None:
                btn['image'].blit(x, y)
            if btn['sel']:
                draw_line(x + 2, y - 2, x + 28, y - 2, color=self.fonColor, thickness=2)
            if btn['id'] == 3:
                draw_line(x + 2, y + 2, x + 28, y + 28, color=self.penColor, thickness=4)

            if btn['id'] == 6:
                draw_poly(x + 2, y, x + 28, y + 28, id=self.numVertex, numPoints=self.numVertex,
                          color=self.penColor, fon_color=self.fonColor, fill=self.isFill)
                draw_line(-10000, -10000, -10001, -10001, self.fonColor, thickness=1)

            if btn['id'] == 112:
                draw_fill_reg_polygon(x + 2, y + 28, x + 28, y, angleStart=0, numPoints=4,
                                      color=(0, 0.5, 0.5, 0.5))
            if btn['id'] == 108:
                draw_fill_reg_polygon(x + 2, y + 28, x + 28, y, angleStart=180, numPoints=3,
                                      color=(0, 0.5, 0.5, 0.5))
            if btn['id'] == 109:
                draw_fill_reg_polygon(x + 2, y + 28, x + 28, y, angleStart=0, numPoints=3, color=(0, 0.5, 0.5, 0.5))
            if btn['id'] == 110:
                draw_fill_reg_polygon(x + 2, y + 28, x + 28, y, angleStart=270, numPoints=3,
                                      color=(0, 0.5, 0.5, 0.5))
            if btn['id'] == 111:
                draw_fill_reg_polygon(x + 2, y + 28, x + 28, y, angleStart=90, numPoints=3,
                                      color=(0, 0.5, 0.5, 0.5))

            if self.tool == btn['tool']:
                draw_fill_circle(x + 5, y + 34, 3, color=self.penColor)
                draw_line(-10000, -10000, -10001, -10001, self.fonColor, thickness=1)

        draw_line(-10000, -10000, -10001, -10001, self.fonColor, thickness=1)
        if self.figuresPanelVisible:
            self.draw_figures_panel()
        if self.colorPanelVisible:
            self.draw_color_panel()
        if self.widthPanelVisible:
            self.draw_width_panel()
        if self.arrowPanelVisible:
            self.draw_arrow_panel()
        if self.dashPanelVisible:
            self.dash_arrow_panel()
        # рамка виділення
        if len(self.selFigs) > 0:
            pSel = []
            r, g, b, a = self.ramkaColor
            ramkaColorChild = ((1 + r) / 2, (1 + g) / 2, (1 + b) / 2, a)
            for selFig in self.selFigs:
                fig = selFig['figobj']
                pSel += fig['p']
                cx1, cy1, cx2, cy2 = border_polyline(fig['p'])
                cx1, cy1 = self.canvas_to_screen(cx1, cy1)
                cx2, cy2 = self.canvas_to_screen(cx2, cy2)
                x_center, y_center, = (cx1 + cx2) / 2, (cy1 + cy2) / 2
                # draw_ramka_top(cx1 - 2, cy1 - 2, cx2 + 2, cy2 + 2,
                #                center=(self.canvas_to_screen(x_center, y_center)),
                #                color=ramkaColorChild, thickness=self.ramkaThickness, rotate=False, resize=False,
                #                close=False)
            x1, y1, x2, y2 = border_polyline(pSel)
            x_center, y_center, = (x1 + x2) / 2, (y1 + y2) / 2
            x1, y1 = self.canvas_to_screen(x1, y1)
            x2, y2 = self.canvas_to_screen(x2, y2)
            # ff = fig['name'] != 'image'
            draw_ramka_top(x1 - 2, y1 - 2, x2 + 2, y2 + 2,
                           center=(self.canvas_to_screen(x_center, y_center)),
                           color=self.ramkaColor, thickness=self.ramkaThickness, rotate=True, resize=True,
                           close=len(self.selFigs) == 1)

            draw_line(-10000, -10000, -10001, -10001, color=self.fonColor, thickness=1)

        labelPage = pyglet.text.Label(str(self.page),
                                      font_name='Arial',
                                      font_size=24,
                                      x=self.width - 60, y=22,
                                      anchor_x='center', anchor_y='center')
        labelPage.set_style("color", (3, 105, 25, 255))
        labelPage.draw()
        if self.isExit:
            self.label.draw()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.clear()
        self.cy -= scroll_y * 10
        self.lastCommand = 11

    def on_close(self):
        self.label = pyglet.text.Label('x',
                                       font_name='Wingdings',
                                       font_size=96,
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center')
        self.label.set_style("color", (255, 0, 0, 255))
        self.isExit = True
        self.label.draw()

    def on_hide(self):
        # print ('HIDE')
        self.isMinimized = True

    def on_activate(self):
        # print('SHOW')
        self.isMinimized = False

    def zipLesson(self):
        nnam = datetime.datetime.strftime(datetime.datetime.now(), 'lessons/' + "%Y_%m_%d_%H_%M_%S") + '.zip'
        z = zipfile.ZipFile(nnam, 'w')  # Создание нового архива
        for root, dirs, files in os.walk('tmp'):  # Список всех файлов и папок в директории folder
            for file in files:
                z.write(os.path.join(root, file))  # Создание относительных путей и запись файлов в архив
        z.close()

    def closeApp(self):
        self.save_options()
        self.save()
        self.zipLesson()
        # time.sleep(2)
        filelist = glob.glob(os.path.join('tmp', "*.*"))
        for f in filelist:
            os.remove(f)
        file_name = "lazexe/tmp_f.bmp"
        if os.path.exists(file_name):
            os.remove(file_name)
        file_name = "lazexe/tmp.bmp"
        if os.path.exists(file_name):
            os.remove(file_name)

        raise SystemExit

    def autoload(self):
        # figures.wb
        file_name = "tmp/figures.wb"
        if os.path.exists(file_name):
            self.load(file_name)

    # def on_show(self):
    #     # self.maximize()
    #     pass

    # def on_activate(self):
    # file_name = "lazexe/tmp.bmp"
    # if os.path.exists(file_name):
    #     self.pageMax += 1
    #     self.page = self.pageMax
    #     self.cx = self.page * 100000 - 100000
    #     self.cy = 0
    #     # self.set_page_right()
    #     width = 600
    #     # self.set_visible(True)
    #
    #     w = self.width
    #     h = self.height
    #     height = 9 * width // 16
    #     x0, y0 = w - width - self.cx, h - height - self.cy
    #     nnam = datetime.datetime.strftime(datetime.datetime.now(), 'tmp/' + "_%Y_%m_%d_%H_%M_%S") + '.png'
    #     shutil.copy(file_name, nnam)
    #     self.insert_image_from_file(nnam, x0, y0, width, height)
    #     os.remove(file_name)
    #
    # file_name = "lazexe/tmp_f.bmp"
    # if os.path.exists(file_name):
    #     self.pageMax += 1
    #     self.page = self.pageMax
    #     self.cx = self.page * 100000 - 100000
    #     self.cy = 0
    #     width = self.screen_width
    #     height = self.screen_height
    #     nnam = datetime.datetime.strftime(datetime.datetime.now(), 'tmp/' + "_%Y_%m_%d_%H_%M_%S") + '.png'
    #     shutil.copy(file_name, nnam)
    #     self.insert_image_from_file(nnam, 2 - self.cx, 2 - self.cy, width - 20, height - 20)
    #     os.remove(file_name)

    # else:
    #     file_name = "tmp.bmp"
    #     if os.path.exists(file_name):
    #         self.set_page_right()
    #         width = 600
    #         # self.set_visible(True)
    #         self.maximize()
    #         w = self.width
    #         h = self.height
    #         height = 9 * width // 16
    #         x0, y0 = w - width - self.cx, h - height - self.cy
    #         nnam = datetime.datetime.strftime(datetime.datetime.now(), 'tmp/' + "_%Y_%m_%d_%H_%M_%S") + '.png'
    #         shutil.copy(file_name, nnam)
    #         self.insert_image_from_file(nnam, x0, y0, width, height)
    #         os.remove(file_name)

    # draw figures in visible part of window
    # self.clear()
    # if True:
    # print("draw")
    # self.maximize()
    def update(self, dt):
        self.tik += 1
        if self.autosave and self.tik % 5 == 0:
            self.save()
            # print("saved ", dt)
            self.tik = 0

        if self.isMinimized:
            file_name = "lazexe/tmp.bmp"
            if os.path.exists(file_name):
                self.pageMax += 1
                self.page = self.pageMax
                self.cx = self.page * 100000 - 100000
                self.cy = 0
                width = 600
                w = self.width
                h = self.height
                height = 9 * width // 16
                x0, y0 = w - width - self.cx, h - height - self.cy
                nnam = datetime.datetime.strftime(datetime.datetime.now(), 'tmp/' + "_%Y_%m_%d_%H_%M_%S") + '.png'
                shutil.copy(file_name, nnam)
                self.insert_image_from_file(nnam, x0, y0, width, height)
                os.remove(file_name)
                self.set_fullscreen(True)
                self.set_fullscreen(False)
                self.clear()
            file_name = "lazexe/tmp_f.bmp"
            if os.path.exists(file_name):
                self.pageMax += 1
                self.page = self.pageMax
                self.cx = self.page * 100000 - 100000
                self.cy = 0
                width = self.screen_width
                height = self.screen_height
                nnam = datetime.datetime.strftime(datetime.datetime.now(), 'tmp/' + "_%Y_%m_%d_%H_%M_%S") + '.png'
                shutil.copy(file_name, nnam)
                self.insert_image_from_file(nnam, 2 - self.cx, 2 - self.cy, width - 20, height - 20)
                os.remove(file_name)
                self.set_fullscreen(True)
                self.set_fullscreen(False)
                self.clear()


def oglStart():
    display = pyglet.canvas.get_display()
    w = display.get_screens()[0].width
    h = display.get_screens()[0].height

    window = MyWindow(w, h - 62, caption="WhiteBoard", resizable=True, visible=False)
    window.screen_width = w
    window.screen_height = h
    # context = window.context
    # config = context.config
    # config.double_buffer

    window.set_location(2, 24)

    # window.maximize()
    window.clear()
    window.on_draw()
    window.set_visible()
    pyglet.clock.schedule_interval(window.update, 5)
    pyglet.app.run()


if __name__ == "__main__":
    oglStart()
