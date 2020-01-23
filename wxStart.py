import wx
import main

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          style=wx.STAY_ON_TOP | wx.TAB_TRAVERSAL | wx.FRAME_NO_TASKBAR)
        # self.SetTransparent(64)

        self.panel = MainPanel(self)
        self.Fit()
        self.Centre()
        self.SetSize(60, 30)
        self.SetPosition((10, 40))



class MainPanel(wx.Panel):
    def __init__(self, frame):
        wx.Panel.__init__(self, frame)

        # Button 1
        button_sizer = self._button_sizer(frame)

        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add((0, 0))
        main_sizer.Add(button_sizer)
        self.SetSizer(main_sizer)
        self.Fit()

    def _button_sizer(self, frame):
        cmd_screenshot = wx.Button(self, label='+')
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer.Add(cmd_screenshot)
        cmd_screenshot.Bind(wx.EVT_BUTTON, self.OnScrClick)
        return button_sizer

    def OnScrClick(self, event):
        print (main.l)

def wxStart():
    print(main.l)
    x = True
    app = wx.App()
    frame = MainFrame()
    frame.SetWindowStyle(style=wx.STAY_ON_TOP | wx.TAB_TRAVERSAL)
    frame.SetSize(size=(90, 50))
    frame.Show()
    # frame.SetPosition()
    # frame.SetTransparent(64)
    app.MainLoop()
