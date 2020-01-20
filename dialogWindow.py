import wx

class SubclassDialog(wx.Dialog):
    def __init__(self):              #РёРЅРёС†РёРёСЂСѓРµРј РґРёР°Р»РѕРі
        wx.Dialog.__init__(self, None, -1, 'Dialog Subclass',size=(120, 150),
                           style=wx.CAPTION|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL)
        okButton = wx.Button(self, wx.ID_OK, "OK", pos=(2, 2), size=(100, 32))
        # okButton.SetDefault()
        cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel",pos=(2, 40), size=(100, 32))

# class MainFrame(wx.Frame):
#     def __init__(self):
#         wx.Frame.__init__(self, None, -1,
#                           style=wx.STAY_ON_TOP|wx.TAB_TRAVERSAL)
#         self.SetTransparent(64)
#         self.panel = MainPanel(self)
#         self.Fit()
#         self.Centre()
#         self.Show()


# class MainPanel(wx.Panel):
#     def __init__(self, frame):
#         wx.Panel.__init__(self, frame)
#
#         # Button
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
#         # cmd_cancel = wx.Button(self,label='x')
#         button_sizer = wx.BoxSizer(wx.VERTICAL)
#         button_sizer.Add(cmd_screenshot)
#         # button_sizer.Add(cmd_cancel, flag=wx.ALIGN_RIGHT)
#         cmd_screenshot.Bind(wx.EVT_BUTTON,self.OnScrClick)
#         # cmd_screenshot.Bind(wx.EVT_BUTTON,self.OnScrClick)
#
#         return button_sizer
#
#     def OnScrClick(self,event):
#         print(111111111111)