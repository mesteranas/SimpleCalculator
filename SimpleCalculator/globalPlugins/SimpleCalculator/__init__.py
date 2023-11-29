import ui
import api
import globalPluginHandler
import wx
import gui
from keyboardHandler import KeyboardInputGesture
from scriptHandler import script
import addonHandler
addonHandler.initTranslation()

showDialog = None
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__ (self):
		super().__init__()
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.open= self.toolsMenu.Append(wx.ID_ANY, _("simple calculator"),_("open simple calculator dialog"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.run, self.open)

	@script(
description= _("open semple calculator dialog"),
category= _("SimpleCalculator"),
gesture="kb:nvda+alt+s")
	def script_start (self, gesture):
		self.run(1)
	def run(self,event):
		global showDialog
		if not showDialog:
			showDialog= mainDialog(gui.mainFrame)
			showDialog.Raise()
		else:
			showDialog.Raise()
	def terminate(self):
		try:
			self.toolsMenu.Remove(self.open)
		except :
			pass
class mainDialog(wx.Dialog):
	def __init__(self, parent):
		super(mainDialog, self).__init__(parent, title = _("Simple calculator"))
		wx.StaticText(self, -1, _("Arithmetic operation"))
		self.number1= wx.TextCtrl(self, -1)
		self.number1.Bind(wx.EVT_TEXT, self.onr)
		wx.StaticText(self, -1, _("result"))
		self.re= wx.TextCtrl(self, -1,style=wx.TE_MULTILINE+wx.HSCROLL+wx.TE_READONLY)
		self.Bind(wx.EVT_CHAR_HOOK, self.OnHook)
		copy=wx.Button(self,-1, _("copy"))
		self.Bind(wx.EVT_BUTTON, self.onLanguagec,copy)

		self.Show()
	def OnHook(self,event):
		k=event.GetKeyCode()
		if k==wx.WXK_ESCAPE:
			self.Destroy()
		event.Skip()
	def onLanguagec(self, event):
		if api.copyToClip(self.re.Value):
			ui.message(_("copied"))

	def onr(self, event):
		self.re.Value=""
		try:
			num1=eval(self.number1.Value)
			self.re.Value=str(num1)
		except:
			self.re.Value="error"
