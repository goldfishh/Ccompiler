ERRORTYPE1  = ""
ERRORTYPE2  = ""
ERRORTYPE3  = ""
ERRORTYPE4  = ""
ERRORTYPE5  = ""
ERRORTYPE6  = ""
ERRORTYPE7  = ""
ERRORTYPE8  = ""
ERRORTYPE9  = ""
ERRORTYPE10 = ""


class SymbolTable:

	def __init__(self):
		self.functionTable = dict()
		self.variableTable = dict()
		self.structTable = dict()
		self.enumTable = dict()
		self.variableStack = list()
		self.variableStackPointer = [0]

		self.variableStackIterator = 0
		self.variableStackPointerIterator = 1
# ftype == 1 只查看当前一层变量定义 用于判断当前是否可定义变量
# ftype == 2 迭代查看全层变量 用于取值
	def lookup_variable(self, findvname, ftype):
		i = len(self.variableStackPointer) - 1
		while(i >= 0):
			thisi = self.variableStackPointer[i]
			while(thisi < len(self.variableStack)):
				thivaria = self.variableStack[thisi]
				if(thivaria['vname'] == findvname):
					return thivaria
				else:
					thisi = thisi + 1
			if(ftype == 2):
				i = i - 1
			else:
				break
		return False

	def update(self, tabletype, name, index, value):
		if(tabletype == 1):
			self.functionTable[name][index] = value

	def insert(self, name, content, type):
		if(type == 1):
			if (name in self.functionTable):
				return ERRORTYPE1
			else:
				self.functionTable[name] = content
		elif(type == 2):
			if (name in self.variableTable):
				return ERRORTYPE2
			else:
				self.variableTable[name] = content
		elif(type == 4):
			if (name in self.structTable):
				return ERRORTYPE4
			else:
				self.structTable[name] = content
		elif(type == 5):
			if (name in self.enumTable):
				return ERRORTYPE5
			else:
				self.enumTable[name] = content

	def lookup(self, name, type):
		if(type == 1):
			if (name not in self.functionTable):
				return False
			else:
				return self.functionTable[name]
		elif(type == 2):
			if (name not in self.variableTable):
				return False
			else:
				return self.variableTable[name]
		elif(type == 4):
			if (name not in self.structTable):
				return False
			else:
				return self.structTable[name]
		elif(type == 5):
			if (name not in self.enumTable):
				return False
			else:
				return self.enumTable[name]