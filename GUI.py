import wx
import os
import defaultFile
from Clexer_v4 import C_Lexer
from Cparser import CompilationEngine
class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title, size = (450,620))
		self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
		self.CreateStatusBar()
		self.nowfile = ""

		# 设置菜单
		filemenu = wx.Menu()

		# 文件栏
		hwItem = filemenu.Append(wx.ID_FILE1, u"HelloWorld!", u"编译预定义源程序")
		msItem = filemenu.Append(wx.ID_FILE2, u"归并排序", u"编译预定义源程序")
		tetrisItem = filemenu.Append(wx.ID_FILE3, u"俄罗斯方块", u"编译预定义源程序")
		filemenu.AppendSeparator()
		openItem = filemenu.Append(wx.ID_OPEN, u"打开文件", u"请选择打开符合编译器语法规则C语言程序")
		exitItem = filemenu.Append(wx.ID_EXIT, u"退出", u"退出程序")

		# 操作栏
		operationmenu = wx.Menu()
		lexerItem = operationmenu.Append(wx.ID_ANY, u"词法分析", u"词法分析")
		parserItem = operationmenu.Append(wx.ID_ANY, u"语法分析", u"语法分析")
		operationmenu.AppendSeparator()
		sysItem = operationmenu.Append(wx.ID_ANY, u"四元式生成", u"四元式生成")
		operationmenu.AppendSeparator()
		interpreterItem = operationmenu.Append(wx.ID_ANY, u"解释四元式", u"解释四元式")
		operationmenu.AppendSeparator()
		pythonItem = operationmenu.Append(wx.ID_ANY, u"执行目标代码", u"python执行目标代码")

		# 关于栏
		aboutmenu = wx.Menu()
		cfinfoItem = aboutmenu.Append(wx.ID_ANY, u"词法说明", u"编译器词法说明")
		yfinfoItem = aboutmenu.Append(wx.ID_ANY, u"语法说明", u"编译器语法说明")
		sysinfoItem = aboutmenu.Append(wx.ID_ANY, u"四元式说明", u"编译器四元式说明")
		aboutmenu.AppendSeparator()
		aboutItem = aboutmenu.Append(wx.ID_ABOUT, u"关于这个程序", u"想要了解下吗?")

		# 母菜单
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, u"文件")
		menuBar.Append(operationmenu, u"操作")
		menuBar.Append(aboutmenu, u"关于")

		# 绑定事件处理
		self.Bind(wx.EVT_MENU, self.OnDefaultFilehw, hwItem)
		self.Bind(wx.EVT_MENU, self.OnDefaultFilems, msItem)
		self.Bind(wx.EVT_MENU, self.OnDefaultFiletetris, tetrisItem)
		self.Bind(wx.EVT_MENU, self.OnOpen, openItem)
		self.Bind(wx.EVT_MENU, self.OnExit, exitItem)

		self.Bind(wx.EVT_MENU, self.OnLexer, lexerItem)
		self.Bind(wx.EVT_MENU, self.OnParser, parserItem)
		self.Bind(wx.EVT_MENU, self.OnSys, sysItem)
		self.Bind(wx.EVT_MENU, self.OnInterpreter, interpreterItem)
		self.Bind(wx.EVT_MENU, self.OnPython, pythonItem)

		self.Bind(wx.EVT_MENU, self.OnCfinfo, cfinfoItem)
		self.Bind(wx.EVT_MENU, self.OnYfinfo, yfinfoItem)
		self.Bind(wx.EVT_MENU, self.OnSysinfo, sysinfoItem)
		self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

		self.SetMenuBar(menuBar)
		self.Show(True)

	# 文件栏bind函数
	def OnDefaultFilehw(self, event):
		fout = open("helloworld.c", "w", encoding = "utf-8")
		fout.write(defaultFile.helloworldfile)
		self.nowfile = "helloworld.c"
		self.control.SetValue(defaultFile.helloworldfile)

	def OnDefaultFilems(self, event):
		fout = open("mergesort.c", "w", encoding = "utf-8")
		self.nowfile = "mergesort.c"
		fout.write(defaultFile.mergesortfile)
		self.control.SetValue(defaultFile.mergesortfile)

	def OnDefaultFiletetris(self, event):
		fout = open("tetris.c", "w", encoding = "utf-8")
		self.nowfile = "tetris.c"
		fout.write(defaultFile.tetrisfile)
		self.control.SetValue(defaultFile.tetrisfile)

	def OnOpen(self, event):
		self.dirname = ''
		dlg = wx.FileDialog(self, u"请选择C语言文件", self.dirname, "", "*.c", wx.FD_OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			self.nowfile = os.path.join(self.dirname, self.filename)
			f = open(self.nowfile, 'r', encoding = "utf-8")
			self.control.SetValue(f.read())
			f.close()
		dlg.Destroy()

	def OnExit(self, event):
		self.Close(True)

	#操作栏bind函数
	def OnLexer(self, event):
		if(self.nowfile != ""):
			lexer = C_Lexer(self.nowfile)
			lexer.preScanner()
			lexer.preAnalyzer()
			lexer.analyzer()
			flexer = open(lexer.file_output, "r", encoding="utf-8")
			self.control.SetValue(flexer.read())
		else:
			pass

	def OnParser(self, event):
		if(self.nowfile != ""):
			lexer = C_Lexer(self.nowfile)
			lexer.preScanner()
			lexer.preAnalyzer()
			lexer.analyzer()
			parser = CompilationEngine(lexer)
			parser.CompileProgram()
			parser.__del__()
			fparser = open(parser.foutname, "r", encoding="utf-8")
			self.control.SetValue(fparser.read())
		else:
			pass

	def OnSys(self, event):
		if(self.nowfile != ""):
			lexer = C_Lexer(self.nowfile)
			lexer.preScanner()
			lexer.preAnalyzer()
			lexer.analyzer()
			parser = CompilationEngine(lexer)
			parser.CompileProgram()
			parser.__del__()
			fsys = open(parser.qplwriter.foutname, "r", encoding="utf-8")
			self.control.SetValue(fsys.read())
			print(fsys.read())

		else:
			pass

	def OnInterpreter(self, event):
		pass

	def OnPython(self, event):
		pass


	# 关于栏bind函数
	def OnCfinfo(self, event):
		dlg = wx.MessageDialog(self, defaultFile.cftext, "C-语言词法说明", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnYfinfo(self, event):
		dlg = wx.MessageDialog(self, defaultFile.yftext, "C-语言语法说明", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnSysinfo(self, event):
		dlg = wx.MessageDialog(self, defaultFile.systext, "C-语言四元式说明", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnAbout(self, event):
		dlg = wx.MessageDialog(self, defaultFile.aboutus, "关于", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()
app = wx.App(False) #创建1个APP，禁用stdout/stderr重定向
frame = MainWindow(None,  "C-语言编译器")  #这是一个顶层的window
app.MainLoop()