import wx

class SubclassDialog(wx.Dialog):
    def __init__(self):              #инициируем диалог
        wx.Dialog.__init__(self, None, -1, 'Dialog Subclass',size=(120, 150),
                           style=wx.CAPTION|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL)

        okButton = wx.Button(self, wx.ID_OK, "OK", pos=(2, 2), size=(100, 32))
        okButton.SetDefault()
        cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel",pos=(2, 40), size=(100, 32))