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

import os.path
import configparser
import zipfile
from sys import argv

from pyglet.window import key

if platform == "win32" or platform == "cygwin":
    pass
elif platform == "linux":
    pass




class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 30)

        # ============ Options ================

        self.load_options()

        # ============ End options ================

        self.isPaste = False
        self.figTMP = None
        self.tik = 0
        self.x_00 = 0
        self.y_00 = 0
        self.tik_anti_blind = 0
        self.numVertex = 4
        self.pageMax = 1
        self.incr = 0
        self.screen_width = 0
        self.screen_height = 0
        self.figures_for_draw = []

        glClearColor(*self.fonColor)

        self.figures = []
        self.drawOk = True;
        self.selectRamka = False
        self.isMinimized = False
        self.isMove = False
        self.multiSelect = False
        self.isResize = False
        self.isExit = False
        self.isFill = False
        self.dragPanel = False
        self.isFullscreen = True
        self.selFigs = []

        self.isBtnClick = False
        self.colorPanelVisible = False
        self.widthPanelVisible = False
        self.figuresPanelVisible = False
        self.dashPanelVisible = False
        self.history = []
        self.label = None
        self.pnlx = 75
        self.pnly = 75
        self.imMultisel = [pyglet.resource.image('img/multisel_no.png'), pyglet.resource.image('img/multisel.png')]
        self.imPaste = [pyglet.resource.image('img/paste_disable.png'), pyglet.resource.image('img/paste.png')]
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

            {'id': 101, 'text': 'color', 'image': pyglet.resource.image('img/palitra.png'), 'tool': 0,
             'sel': False, 'align': 'left', 'command': 'set_colorpanel_visible'},
            {'id': 102, 'text': 'width', 'image': pyglet.resource.image('img/width.png'), 'tool': 0,
             'sel': False, 'align': 'left', 'command': 'set_widthpanel_visible'},


            {'id': 106, 'text': 'arrow', 'image': pyglet.resource.image('img/arr.png'), 'tool': 0,
             'sel': False, 'align': 'left', 'command': 'set_arrowpanel_visible'},
            {'id': 107, 'text': 'dash', 'image': pyglet.resource.image('img/dot.png'), 'tool': 0,
             'sel': False, 'align': 'left', 'command': 'set_dashpanel_visible'},
            {'id': 0, 'text': '', 'image': None, 'tool': 0, 'sel': False, 'align': 'left', 'command': ''},
            {'id': 118, 'text': '', 'image': pyglet.resource.image('img/undo.png'), 'tool': 0,
             'sel': False, 'align': 'left', 'command': 'undo'},
            {'id': 0, 'text': '', 'image': None, 'tool': 0, 'sel': False, 'align': 'left', 'command': ''},
            {'id': 119, 'text': '', 'image': pyglet.resource.image('img/paste_disable.png'), 'tool': 0,
             'sel': False, 'align': 'left', 'command': 'insert_image_from_clipboard'},

            {'id': 0, 'text': '', 'image': None, 'tool': 0, 'sel': False, 'align': 'left', 'command': ''},
            {'id': 113, 'text': 'dash', 'image': pyglet.resource.image('img/minimize2.png'), 'tool': 0,
             'sel': False, 'align': 'left', 'command': 'set_minimize'},
            {'id': 0, 'text': '', 'image': None, 'tool': 0, 'sel': False, 'align': 'left', 'command': ''},
            {'id': 115, 'text': 'dash', 'image': pyglet.resource.image('img/closeApp.png'), 'tool': 0,
             'sel': False, 'align': 'left', 'command': 'closeApp'},


            {'id': 104, 'x': 75, 'y': 5, 'text': '<', 'image': pyglet.resource.image('img/left.png'), 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'set_page_left'},
            {'id': 105, 'x': 5, 'y': 5, 'text': '>', 'image': pyglet.resource.image('img/right.png'), 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'set_page_right'},

            {'id': 108, 'x': self.dragPanelx + 70, 'y': self.dragPanely + 100, 'text': '<', 'image': None, 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'move_108'},
            {'id': 109, 'x': self.dragPanelx, 'y': self.dragPanely + 100, 'text': '>', 'image': None, 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'move_109'},
            {'id': 112, 'x': self.dragPanelx + 35, 'y': self.dragPanely + 100, 'text': '...', 'image': None, 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'drag_panel'},
            {'id': 110, 'x': self.dragPanelx + 35, 'y': self.dragPanely + 70, 'text': 'V', 'image': None, 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'move_110'},
            {'id': 111, 'x': self.dragPanelx + 35, 'y': self.dragPanely + 130, 'text': 'U', 'image': None, 'tool': 0,
             'sel': False, 'align': 'right', 'command': 'move_111'},

            {'id': 56, 'x': -500, 'y': -500, 'text': 'del selected', 'image': pyglet.resource.image('img/trash32.png'),
             'tool': 0,
             'sel': False, 'align': '', 'command': 'del_selected'},
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
                if b['id'] == 0:
                    x += 14
                else:
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

        self.step = 50
        self.screen_width = 800
        self.screen_height = 500
        self.scS = False
        self.arrowPanelVisible = False
        self.images = {}
        self.lenesPen = []

        self.id = 0
        self.dash = 0
        self.page = 1
        self.lastCommand = 1
        # Тут запустимо програму-панель
        homePath = os.path.dirname(__file__)
        if platform == "win32" or platform == "cygwin":
            subprocess.Popen("lazexe\scrgrub.exe")
        elif platform == "linux":
            pass
        # Работаем
        file_name = 'is_work.txt'
        f = open(file_name, 'tw', encoding='utf-8')
        f.close()

        if len(argv) > 1:
            # print(argv[1])
            if os.path.exists(argv[1]):
                z = zipfile.ZipFile(argv[1], 'r')
                z.extractall()
                self.load()
        else:
            self.autoload()

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

    def dash_arrow_panel(self):
        for btn in self.dashPanelButtons:
            h = btn['y2'] - btn['y1']
            y = btn['y1'] + h // 2
            draw_fill_rectangle(btn['x1'], btn['y1'], btn['x2'], btn['y2'], self.fonColor)
            btn['image'].blit(btn['x1'], btn['y1'])

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
        data['dragPanelx'] = self.dragPanelx
        data['dragPanely'] = self.dragPanely
        data['isPartingPolylinu'] = self.isPartingPolylinu

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
            self.isGrid = data['isgrid'] == 'True'
            self.isSmooth = data['issmooth'] == 'True'
            self.penWidth = int(data['penwidth'])
            self.errSize = int(data['errSize'])
            self.fullscr = data['fullscr'] == 'True'
            self.autosave = data['autosave'] == 'True'
            self.isPartingPolylinu = data['isPartingPolylinu'] == 'True'
            self.ramkaThickness = int(data['ramkathickness'])
            self.dragPanelx = int(data['dragPanelx'])
            self.dragPanely = int(data['dragPanely'])

        else:
            self.colorOrrange = (1.0, 0.5, 0.0, 1.0)
            # self.numVertex = 4
            self.dragPanelx, self.dragPanely = 5, 5
            self.isGrid = True
            self.isSmooth = True
            self.autosave = True
            self.penWidth = 7
            self.errSize = 20
            self.fullscr = False
            self.isPartingPolylinu = True
            self.penColor = self.colorOrrange
            self.ramkaColor = (1, 0.5, 0, 1)
            self.ramkaThickness = 2
            self.fonColor = (0.91, 0.98, 0.79, 1.0)
            self.gridColor = (0.82, 0.82, 0.82, 1.0)
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
        self.update_figures()
        for b in self.buttons:
            if b['id'] == 56:
                b['x'] = -500
                b['y'] = -500
                break

    def insert_image_from_clipboard(self):

        if platform == "linux":
            file_name = 'image.bmp'
            if os.path.exists(file_name):
                nnam = datetime.datetime.strftime(datetime.datetime.now(), 'tmp/' + "_%Y_%m_%d_%H_%M_%S") + '.png'
                image = pyglet.image.load(file_name)
                image.save(nnam)
                if not self.multiSelect:
                    os.remove(file_name)
                x, y = self.screen_to_canvas(300, 300)
                w = 600
                h = int(image.height / image.width * w)
                self.insert_image_from_file(nnam, x, y, w, h)
                self.tool = 8
        elif platform == "win32" or platform == "cygwin":
            from PIL import ImageGrab
            nnam = datetime.datetime.strftime(datetime.datetime.now(), 'tmp/' + "_%Y_%m_%d_%H_%M_%S") + '.png'
            image = ImageGrab.grabclipboard()
            image.save(nnam)
            x, y = self.screen_to_canvas(300, 300)
            w = 600
            h = int(image.height / image.width * w)
            self.insert_image_from_file(nnam, x, y, w, h)
            self.tool = 8

    def undo(self):
        self.figures = []
        if self.history != []:
            self.figures = self.history[-1].copy()
            del self.history[-1]
            self.clear()

    def set_shot(self):
        self.set_visible(False)
        time.sleep(2)
        self.insert_screenshot()
        self.set_visible(True)

    def set_fill(self):
        self.isFill = not self.isFill
        # Зафарбовуємо чи ні виділену фігуру
        if self.tool == 8 and self.selFigs != []:
            for selFig in self.selFigs:
                selFig['figobj']['fill'] = self.isFill

    def set_minimize(self):
        self.minimize()

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

    # --START-- робота зі зміною положення полотна
    def set_page_right(self):
        self.drawOk = True
        self.clear()
        self.page += 1
        if self.page > self.pageMax: self.pageMax = self.page
        self.cx = self.page * 100000 - 100000
        self.cy = 0
        self.update_figures_wo_del()

    def set_page_left(self):
        self.drawOk = True
        self.clear()
        self.page -= 1
        if self.page < 1:
            self.page = 1
        self.cx = self.page * 100000 - 100000
        self.cy = 0
        self.update_figures_wo_del()

    def move_108(self):
        self.drawOk = True
        self.clear()
        self.cx += 100
        self.update_figures_wo_del()

    def move_109(self):
        self.drawOk = True
        self.clear()
        self.cx -= 100
        self.update_figures_wo_del()

    def move_110(self):
        self.drawOk = True
        self.clear()
        self.cy += 100
        self.update_figures_wo_del()

    def move_111(self):
        self.drawOk = True
        self.clear()
        self.cy -= 100
        self.update_figures_wo_del()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.drawOk = True
        # print(scroll_x, scroll_y)
        self.clear()
        self.cy -= scroll_y * 10
        self.lastCommand = 11
        self.update_figures_wo_del()

    # -- END -- робота зі зміною положення полотна

    def figure_on_screen(self, board_coords):
        self.x_min, self.y_min, self.x_max, self.y_max = board_coords
        x_min, y_min, x_max, y_max = board_coords
        x_min, y_min = self.canvas_to_screen(x_min, y_min)
        x_max, y_max = self.canvas_to_screen(x_max, y_max)
        return x_min < self.width and x_max > 0 and y_min < self.height and y_max > 0

    def update_figures_wo_del(self):

        self.tik_anti_blind = 0
        for f in self.figures:
            f['visible'] = self.figure_on_screen(f['extrem'])

    def update_figures(self):
        new_list = []
        for f in self.figures:
            if not f['fordel']:
                new_list.append(f)
        self.figures = new_list.copy()
        self.selFigs = []

    def drag_panel(self):
        self.dragPanel = True


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
        original_image = Image.open(input_image_path)
        resized_image = original_image.resize(size)
        resized_image.save(output_image_path)



    # def insert_screenshot(self):
    #     self.lastCommand = 11
    #     self.set_visible(False)
    #     nnam = datetime.datetime.strftime(datetime.datetime.now(), 'tmp/' + "_%Y_%m_%d_%H_%M_%S") + '.png'
    #     grab.screenshot_to_file(nnam)
    #     width = 600
    #     self.set_visible(True)
    #     # self.maximize()
    #
    #     w = self.width
    #     h = self.height
    #     height = 9 * width // 16
    #     x0, y0 = w - width - self.cx, h - height - self.cy
    #     self.insert_image_from_file(nnam, x0, y0, width, height)
    #     draw_line(-10000, -10000, -10001, -10001, self.fonColor, thickness=1)
    #     self.clear()

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

        self.images[nnam_] = {'sprite': pyglet.sprite.Sprite(image), 'image': image}
        k['image_name'] = nnam_

        k['angle'] = 0
        k['thickness'] = self.penWidth
        k['fordel'] = False
        k['extrem'] = x0, y0, x0 + image.width, y0 + image.height
        k['visible'] = self.figure_on_screen(k['extrem'])

        self.figures.append(k)
        self.clear()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:  # ESC
            self.closeApp()
        elif symbol == key.HOME:  # Home
            self.drawOk = True
            self.page = 1
            self.cx, self.cy = 0, 0
        elif symbol == key.UP:  # move canvas up
            self.drawOk = True
            self.cy -= 50
            self.lastCommand = 11
        elif symbol == key.DOWN:  # Change canvas down
            self.drawOk = True
            self.cy += 50
            self.lastCommand = 11
        elif symbol == key.LEFT:  # Change canvas left
            self.drawOk = True
            self.cx += 50
            self.lastCommand = 11
        elif symbol == key.RIGHT:  # Change canvas right
            self.drawOk = True
            self.cx -= 50
            self.lastCommand = 11
        elif symbol == key.F:  # full scrffeen
            self.fullscr = not self.fullscr
            self.set_fullscreen(self.fullscr)
            self.clear()
        elif symbol == key.G:  # set grid
            self.isGrid = not self.isGrid

        else:
            print('A key was pressed')
            print(symbol)
            pass
        self.clear()

    def on_mouse_press(self, x, y, button, modifier):

        self.drawOk = True

        # self.tik_anti_blind += 1

        # Перевіряємо чи треба виходити
        if self.isExit:
            if self.width // 2 - 200 < x < self.width // 2 + 200 and self.height // 2 - 100 < y < self.height // 2 + 100:
                self.closeApp()
                # if winPanel != None:
                #     winPanel.close()
                # dialog.Destroy()
            else:
                self.isExit = False
        # self.clear()
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
                if btn['id'] == 0:
                    ww = 16
                else:
                    ww = 32
                btn['sel'] = False
                if btn['align'] == 'right':
                    xx, yy = self.width - btn['x'] - 35, btn['y']
                else:
                    xx, yy = btn['x'], btn['y']
                if (xx < x < xx + ww) and (yy < y < yy + 32):
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
                self.x0, self.y0 = self.screen_to_canvas(x, y)
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
                                    self.update_figures()
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
                    self.drawOk = False
                    # self.drawRight = True
                    self.x_00, self.y_00 = x, y

                elif self.tool == 3:  # line
                    self.drawOk = True
                    self.x0, self.y0 = (x, y)
                    self.id += 1
                    k = {}
                    k['id'] = self.id
                    k['name'] = 'line'
                    k['color'] = self.penColor
                    k['thickness'] = self.penWidth
                    k['smooth'] = self.isSmooth
                    k['arrow'] = self.arr
                    k['dash'] = self.dash
                    k['fordel'] = False
                    k['visible'] = False
                    k['p'] =[]
                    self.figures.append(k)

                elif self.tool == 4:  # rectangle
                    self.drawOk = True
                    self.x0, self.y0 = self.screen_to_canvas(x, y)
                    self.id += 1
                    k = {}
                    k['id'] = self.id
                    k['name'] = 'polygone'
                    k['color'] = self.penColor
                    k['thickness'] = self.penWidth
                    k['smooth'] = self.isSmooth
                    k['arrow'] = 0
                    k['dash'] = self.dash
                    k['fordel'] = False
                    k['visible'] = False
                    k['fill'] = False
                    k['p'] =[]
                    self.figures.append(k)

                elif self.tool == 5 or self.tool == 6:  # ellipse
                    self.drawOk = True
                    self.x_00, self.y_00 = x, y
                    self.id += 1
                    k = {}
                    k['id'] = self.id
                    k['name'] = 'polygone'
                    k['color'] = self.penColor
                    k['thickness'] = self.penWidth
                    k['smooth'] = self.isSmooth
                    k['arrow'] = 0
                    k['dash'] = self.dash
                    k['fordel'] = False
                    k['visible'] = False
                    k['fill'] = False
                    k['p'] = []
                    k['extrem'] = 0, 0, 0, 0
                    self.figures.append(k)
        if self.f:
            self.history.append(self.figures.copy())

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # if self.tik_anti_blind < 5: self.clear()

        self.incr += 1
        if self.dragPanel:
            for b in self.btnPnl:
                b['x'] -= dx
                b['y'] += dy
            self.dragPanelx -= dx
            self.dragPanely += dy
            self.clear()

        elif self.f:
            if self.tool == 1 or self.tool == 9:
                # if self.tool == 9: self.drawOk = True
                x0,y0 = self.screen_to_canvas(self.x_00, self.y_00)
                xx, yy = self.screen_to_canvas(x, y)
                k = {}
                self.id += 1
                k['id'] = self.id
                k['name'] = 'line'
                x_0, y_0 = self.x0, self.y0
                k['p'] = [{'x': x_0, 'y': y_0}, {'x': xx, 'y': yy}, ]
                k['extrem'] = min(x_0, xx), min(y_0, yy), max(x_0, xx), max(y_0, yy)

                xcenter, ycenter = (x0 + xx) / 2, (y0 + yy) / 2
                if self.tool == 1:
                    pW = self.penWidth
                    colr = self.penColor
                else:
                    pW = self.errSize
                    colr = self.fonColor
                k['center'] = {'x': xcenter, 'y': ycenter}
                k['color'] = colr
                k['thickness'] = pW
                k['fordel'] = False
                k['smooth'] = self.isSmooth
                k['arrow'] = 0
                k['dash'] = self.dash
                k['visible'] = True
                draw_line(x_0 + self.cx, y_0 + self.cy, xx + self.cx, yy + self.cy, color=colr, thickness=pW)
                draw_circle_fill(xx + self.cx, yy + self.cy, pW/2.5, color=colr)
                self.figures.append(k)
                self.x_00, self.y_00 = x, y
                self.x0, self.y0 = self.screen_to_canvas(x, y)

            elif self.tool == 2:
                if self.incr % 4 == 0: self.clear()
                for f in self.figures:
                    x_min, y_min, x_max, y_max = border_polyline(f['p'])
                    x_min, y_min = self.canvas_to_screen(x_min, y_min)
                    x_max, y_max = self.canvas_to_screen(x_max, y_max)
                    if dist((x_max + x_min) // 2, (y_max + y_min) // 2, x, y, self.errSize):
                        f['fordel'] = True
                        break
                self.update_figures()

            elif self.tool == 3:
                self.clear()
                self.drawOk = True
                self.figTMP = None

                self.figTMP = draw_line_mod(self.x0, self.y0, x, y, color=self.penColor, fon_color=self.fonColor,
                              thickness=self.penWidth, arrow=self.arr, dash=self.dash, smooth=self.isSmooth)
                xx, yy = self.screen_to_canvas(x, y)
                xcenter, ycenter = (self.x0+xx) / 2, (self.y0+yy) / 2
                k = self.figures[-1]
                k['center'] = {'x': xcenter, 'y': ycenter}
                x0, y0 = self.screen_to_canvas(self.x0, self.y0)

                k['p'] = [{'x': x0, 'y': y0}, {'x': xx, 'y': yy}]
                k['extrem'] = min(x0, xx), min(y0, yy), max(x0, xx), max(y0, yy)
                k['visible'] = self.figure_on_screen(k['extrem'])

            elif self.tool == 6 or self.tool == 5:  # polygone

                self.drawOk = True
                self.clear()
                xx0, yy0 = (self.x_00, self.y_00)
                draw_poly_wo_bg(xx0, yy0, x, y, color=self.penColor,
                                fill=self.isFill, thickness=self.penWidth, numPoints=self.numVertex, id=self.numVertex,
                                dash=self.dash)

                xx, yy = self.screen_to_canvas(x, y)
                x0, y0 = self.screen_to_canvas(self.x_00, self.y_00)
                xcenter, ycenter = (self.x0 + xx) / 2, (self.y0 + yy) / 2
                k = self.figures[-1]
                k['center'] = {'x': xcenter, 'y': ycenter}
                k['p'] = border_to_points(x0, y0, xx, yy, numPoints=self.numVertex, angleStart=90)
                k['extrem'] = min(x0, xx), min(y0, yy), max(x0, xx), max(y0, yy)
                k['visible'] = self.figure_on_screen(k['extrem'])
                k['fill'] = self.isFill
                # self.drawOk = True


            elif self.tool == 4:
                self.clear()
                self.drawOk = True
                self.figTMP = None
                k = self.figures[-1]
                if self.isFill:
                    self.figTMP = fill_4poly(self.x0 + self.cx, self.y0 + self.cy,
                                             self.x0 + self.cx, y,
                                             x, y,
                                             x, self.y0 + self.cy,  # TODO
                                             color=self.penColor)
                    k['fill'] = True
                    k['name'] = 'polygone_fill'


                else:
                    x1, y1 = self.canvas_to_screen(self.x0, self.y0)
                    x2, y2 = self.canvas_to_screen(self.x0, y - self.cy)
                    x3, y3 = self.canvas_to_screen(x - self.cx, y - self.cy)
                    x4, y4 = self.canvas_to_screen(x - self.cx, self.y0)
                    self.figTMP = draw_rectangle(x1, y1, x2, y2, x3, y3, x4, y4, color=self.penColor, thickness=self.penWidth,
                                                 dash=self.dash)
                    k['fill'] = False
                xcenter, ycenter = (self.x0 + x - self.cx) / 2, (self.y0 + y - self.cy) / 2

                k['center'] = {'x': xcenter, 'y': ycenter}
                k['p'] = [{'x': self.x0, 'y': self.y0},
                          {'x': self.x0, 'y': y - self.cy},
                          {'x': x - self.cx, 'y': y - self.cy},
                          {'x': x - self.cx, 'y': self.y0}]
                k['extrem'] = min(self.x0, x - self.cx), min(y - self.cy, y - self.cy), \
                              max(self.x0, x - self.cx), max(y - self.cy, y - self.cy)
                k['visible'] = self.figure_on_screen(k['extrem'])



            elif self.tool == 20:
                self.cx += dx
                self.cy += dy
                self.clear()
            elif self.tool == 8:
                self.clear()
                if self.selectRamka:
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
                        angle = math.atan(-dx / 300)
                        for fi in pSel:
                            for p in fi['coord']:
                                xx, yy = p['x'], p['y']
                                if fi['name'] != 'image':
                                    p['x'] = (xx - x0) * math.cos(angle) - (yy - y0) * math.sin(angle) + x0
                                    p['y'] = (xx - x0) * math.sin(angle) + (yy - y0) * math.cos(angle) + y0
                                else:
                                    fi['figobj']['angle'] -= angle * 180 / math.pi
                    cx1, cy1, cx2, cy2 = border_polyline_1(pSel)
                    cx1, cy1 = self.canvas_to_screen(cx1, cy1)
                    cx2, cy2 = self.canvas_to_screen(cx2, cy2)
                    if len(self.selFigs) > 1:
                        for b in self.buttons:
                            if b['id'] == 56:
                                b['x'] = cx1 - 20
                                b['y'] = cy2 - 20
                                break


    def on_mouse_release(self, x, y, button, modifiers):
        self.dragPanel = False
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
                    if self.tool == 8:
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
                                            self.update_figures()
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
                    elif self.tool == 1 or self.tool == 9:
                        pass

        self.isMove = False
        self.isResize = False
        self.isRotate = False
        self.lastCommand = 0
        if len(self.selFigs) < 2:
            for b in self.buttons:
                if b['id'] == 56:
                    b['x'] = -500
                    b['y'] = -500
                    break
        self.figures_for_draw = []

    def draw_figures(self):
        # for f in self.figures_for_draw:
        for f in self.figures:
            if not f['visible']: continue
            if  f['name'] == 'line':
                x0, y0 = self.canvas_to_screen(f['p'][0]['x'], f['p'][0]['y'])
                x_, y_ = self.canvas_to_screen(f['p'][1]['x'], f['p'][1]['y'])
                # draw_line_1(x0, y0, x_, y_, color=f['color'], thickness=f['thickness'], dash=f['dash'])
                draw_line_mod(x0, y0, x_, y_, color=f['color'], fon_color=self.fonColor,
                              thickness=f['thickness'], arrow=f['arrow'], dash=f['dash'], smooth=f['smooth'])
                draw_circle_fill(x_, y_, f['thickness'] / 2.5, color=f['color'])
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

                # Це щоб не було засвітки
                draw_line(-10000, -10000, -10001, -10001, (1, 1, 1, 1), thickness=1)

                if f['angle'] == 0:
                    image = self.images[f['image_name']]['image']
                    w = image.width // 2
                    h = image.height // 2
                    image.blit(x0 + w + self.cx, y0 + h + self.cy)
                else:

                    # Центр обертання.
                    image = self.images[f['image_name']]['image']
                    w = image.width // 2
                    h = image.height // 2

                    # Кут повороту
                    self.images[f['image_name']]['sprite'].rotation = f['angle']

                    # координати лівого нижнього кута з ккординат центра
                    self.images[f['image_name']]['sprite'].position = (x0 + w + self.cx, y0 + h + self.cy)
                    self.images[f['image_name']]['sprite'].draw()

    def draw_buttons_and_panels(self):
        # Це щоб не було засвітки на кнопках
        draw_line(-10000, -10000, -10001, -10001, self.fonColor, thickness=1)
        # Draw buttons
        for btn in self.buttons:
            if btn['align'] == 'right':
                x, y = self.width - btn['x'] - 35, btn['y']
            else:
                x, y = btn['x'], btn['y']
            xx = x + 28
            if btn['id'] == 0: xx = x + 4
            draw_line(-10000, -10000, -10001, -10001, self.fonColor, thickness=1)
            if btn['image'] != None:
                draw_line(-10000, -10000, -10001, -10001, self.fonColor, thickness=1)
                btn['image'].blit(x, y)

            if btn['sel']:
                draw_line(x + 2, y - 2, xx, y - 2, color=self.fonColor, thickness=2)

            if btn['id'] == 3:
                draw_line(x + 2, y + 2, xx, y + 28, color=self.penColor, thickness=4)

            if btn['id'] == 6:
                draw_poly(x + 2, y, xx, y + 28, id=self.numVertex, numPoints=self.numVertex,
                          color=self.penColor, fon_color=self.fonColor, fill=self.isFill)
                draw_line(-10000, -10000, -10001, -10001, self.fonColor, thickness=1)

            if btn['id'] == 112:
                draw_fill_reg_polygon(x + 2, y + 28, xx, y, angleStart=0, numPoints=4,
                                      color=(0, 0.5, 0.5, 0.5))
            if btn['id'] == 108:
                draw_fill_reg_polygon(x + 2, y + 28, xx, y, angleStart=180, numPoints=3,
                                      color=(0, 0.5, 0.5, 0.5))
            if btn['id'] == 109:
                draw_fill_reg_polygon(x + 2, y + 28, xx, y, angleStart=0, numPoints=3, color=(0, 0.5, 0.5, 0.5))
            if btn['id'] == 110:
                draw_fill_reg_polygon(x + 2, y + 28, xx, y, angleStart=270, numPoints=3,
                                      color=(0, 0.5, 0.5, 0.5))
            if btn['id'] == 111:
                draw_fill_reg_polygon(x + 2, y + 28, xx, y, angleStart=90, numPoints=3,
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

    def draw_grid(self):
        w = self.screen_width
        h = self.screen_height
        if self.isGrid:
            for y in range(0, h, self.step):
                draw_line_grid(0, y, w, y, color=self.gridColor)
            for x in range(0, w, self.step):
                draw_line_grid(x, 0, x, h, color=self.gridColor)

    def draw_sel_ramka(self):
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

    def on_draw(self):

        # if (self.tik_anti_blind < 10) : self.drawOk = True
        if self.drawOk:
            # self.clear()

            self.draw_figures()
            self.draw_grid()
            self.draw_sel_ramka()
            self.draw_buttons_and_panels()

            # self.draw_grid()
            labelPage = pyglet.text.Label(str(self.page),
                                          font_name='Arial',
                                          font_size=24,
                                          x=self.width - 60, y=22,
                                          anchor_x='center', anchor_y='center')
            labelPage.set_style("color", (3, 105, 25, 255))
            labelPage.draw()

        # self.flip()

        # lab1 = pyglet.text.Label(str(len(self.history)),
        #                               font_name='Arial',
        #                               font_size=24,
        #                               x=500, y=500,
        #                               anchor_x='center', anchor_y='center')
        # lab1.set_style("color", (3, 105, 25, 255))
        # lab1.draw()

        if self.isExit:
            self.label.draw()

    # def on_resize(self, width, height):

    #     if self.tik_anti_blind >5:
    #         self.update_figures_wo_del()
    #         self.maximize()

    def on_close(self):
        self.label = pyglet.text.Label('x',
                                       font_name='Wingdings',
                                       font_size=96,
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center')
        self.label.set_style("color", (255, 0, 0, 255))
        self.isExit = True
        self.label.draw()

    def on_deactivate(self):
        self.isMinimized = True
        file_name = 'flag.txt'
        f = open(file_name, 'tw', encoding='utf-8')
        f.close()

    def on_hide(self):
        self.isMinimized = True
        file_name = 'flag.txt'
        f = open(file_name, 'tw', encoding='utf-8')
        f.close()

    def on_activate(self):
        self.isMinimized = False
        file_name = 'flag.txt'
        if os.path.exists(file_name):
            os.remove(file_name)

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
        file_name = "tmp_f.bmp"
        if os.path.exists(file_name):
            os.remove(file_name)
        file_name = "tmp.bmp"
        if os.path.exists(file_name):
            os.remove(file_name)
        file_name = 'is_work.txt'
        if os.path.exists(file_name):
            os.remove(file_name)
        file_name = 'image.bmp'
        if os.path.exists(file_name):
            os.remove(file_name)
        file_name = 'image.bmp.resize.png'
        if os.path.exists(file_name):
            os.remove(file_name)

        raise SystemExit

    def autoload(self):
        # figures.wb
        file_name = "tmp/figures.wb"
        if os.path.exists(file_name):
            self.load(file_name)

    def update(self, dt):
        # self.drawOk = True
        self.tik += 1
        # print(self.tik)
        # print(self.autosave)
        if self.autosave and self.tik % 5 == 0:
            self.save()
            self.tik = 0

        if platform == "win32" or platform == "cygwin":
            for b in self.buttons:
                if b['id'] == 119:
                    b['image'] = self.imPaste[1]
                    break
        elif platform == "linux":
            file_name = "image.bmp"
            for b in self.buttons:
                if b['id'] == 119:
                    if os.path.exists(file_name):
                        b['image'] = self.imPaste[1]
                    else:
                        b['image'] = self.imPaste[0]
                    break

        if self.isMinimized:
            # Перевіряємо наявність зовнішніх даних та підвантажуємо їх за потребою
            file_name = "tmp.bmp"
            if os.path.exists(file_name):
                image = pyglet.image.load(file_name)
                self.pageMax += 1
                self.page = self.pageMax
                self.cx = self.page * 100000 - 100000
                self.cy = 0
                width = 600
                w = self.width
                h = self.height
                height = image.height * width // image.width
                x0, y0 = w - width - self.cx, h - height - self.cy
                nnam = datetime.datetime.strftime(datetime.datetime.now(), 'tmp/' + "_%Y_%m_%d_%H_%M_%S") + '.png'
                shutil.copy(file_name, nnam)
                self.insert_image_from_file(nnam, x0, y0, width, height)
                os.remove(file_name)
                self.maximize()
                self.set_fullscreen(True)
                self.set_fullscreen(False)
                if self.fullscr:
                    self.set_fullscreen(True)
                self.clear()
            file_name = "tmp_f.bmp"
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
                self.maximize()
                self.set_fullscreen(True)
                self.set_fullscreen(False)
                if self.fullscr:
                    self.set_fullscreen(True)
                self.clear()


def oglStart():
    display = pyglet.canvas.get_display()
    w = display.get_screens()[0].width
    h = display.get_screens()[0].height
    config = pyglet.gl.Config(double_buffer=False)

    window = MyWindow(w, h - 62, caption="WhiteBoard", resizable=True, visible=False, config=config)
    window.screen_width = w
    window.screen_height = h
    window.set_fullscreen(window.fullscr)
    ico = pyglet.image.load('img/ws1.ico')
    window.set_icon(ico)
    #

    window.set_location(2, 24)

    # window.maximize()
    window.clear()
    window.on_draw()
    window.set_visible()
    pyglet.clock.schedule_interval(window.update, 5.0 / 1.0)
    pyglet.app.run()


if __name__ == "__main__":
    oglStart()
