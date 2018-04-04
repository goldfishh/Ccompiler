# 增添符号表功能 enum√
# 语法分析错误跳出, 语义分析错误跳出
# 增加符号表栈式结构
# 增加符号表功能使用相应语句
import os

class CompilationEngine:

	def __init__(self, obj):
		self.foutname = obj.fname.split('.')[0] + ".xml"
		self.fout = open(self.foutname,"a+",encoding="utf-8")
		self.tokenizer = obj
		self.AStype = ["int", "double", "char", "string", "void"]
		self.ADtype = ["struct", "enum"]
		self.arithop = ["+", "-", "*", "/", "%", "&&", "||", "&", "|", "^", "<<", ">>"]
		self.cmpop = [">", "<", ">=", "<=", "==", "!="]
		self.now_turn_function_name = ""
		self.now_ifnum = 0
		self.now_whilenum = 0
		self.now_fornum = 0
	def __del__(self):
		self.fout.close()

	# 打印友好的小功能函数
	def utility(self, x, now):
		for i in range(x):
			self.fout.write("  ")
		self.fout.write(now)

	def utility2(self):
		return self.tokenizer.word_table(self.tokenizer.word_iterator)

	def Advance(self, x):
		now_type , now_word = self.tokenizer.word_table(self.tokenizer.word_iterator)[0],self.tokenizer.word_table(self.tokenizer.word_iterator)[1]
		# for XML's syntax
		if(now_word == ">"):
			now_word = "&lt;"
		elif(now_word == ">="):
			now_word = "&lt;="
		elif(now_word == "<"):
			now_word = "&gt;"
		elif(now_word == "<="):
			now_word = "&gt;="
		elif(now_word == "&"):
			now_word = "&amp;"
		elif(now_word == "&&"):
			now_word = "&amp;&amp;"
		elif(now_word == "\'"):
			now_word = "&apos;"
		elif(now_word == "\""):
			now_word = "&quot;"
		self.utility(x, "<{}>  {}  </{}>".format(now_type, now_word, now_type))
		self.tokenizer.advance()
		self.utility(x, "\n")

	def CompileProgram(self,x = 0):
		self.utility(x, "<program>\n")
		self.CompileGlobalDeclaration(x+1)
		next1 = self.tokenizer.LL1()
		while(next1 in self.ADtype or next1 in self.AStype or next1 == 'typedef'):
			self.CompileGlobalDeclaration(x+1)
			next1 = self.tokenizer.LL1()
		# E1
		if(self.tokenizer.word_iterator < self.tokenizer.output_length):
			self.utility(x, "SyntaxERROR, it may have some words unrecognized")
		self.utility(x, "</program>")

	def CompileGlobalDeclaration(self, x):
		self.utility(x, "<globalDeclaration>\n")
		next1 = self.tokenizer.LL1()
		if(next1 == 'enum'):
			self.CompileEnumDecl(x+1)
		elif(next1 == 'struct'):
			self.CompileStructDecl(x+1)
		# elif(next1 == 'typedef'):
		# 	self.CompileTypedef(x+1)
		elif(next1 in self.AStype):
			nextpt = 1
			nextx = self.tokenizer.LL(nextpt)
			flag = False
			exit = 0
			# 鲁棒性非常差, 绝对有bug
			# 不过正确语法结构,这段够用
			# 增加了exit变量控制跳出, 防止遗漏';'导致死循环
			# 当然, 这样产生新的bug,如果分析某段词法token很多, 会错误跳出.
			while(nextx != ";"):   # 识别为变量声明 退出位置
				if(nextx == "("):  # 识别为函数 退出位置
					flag = True
					break
				else:
					nextpt += 1
					nextx = self.tokenizer.LL(nextpt)
				if(exit > 100):
					break
				else:
					exit += 1
			if(exit <= 100 and flag):
				self.CompileFunctionDecl(x+1)
			elif(exit <= 100 and not flag):
				self.CompileVariableDecl(x+1, 1)
			else:  # E2
				self.utility(x, "SyntaxERROR, for jumping out uncommonly\n")
		else:   # E3
			self.utility(x, "SyntaxERROR, unrecognizing token\n")
		self.utility(x, "</globalDeclaration>\n")

# 3.28  添加符号表
	def CompileType(self, x):
		next1 = self.tokenizer.LL1()
		thitype_1 = self.utility2()[1]
		thitype_2 = None
		if(next1 == "int"):
			self.Advance(x)
		elif(next1 == "double"):
			self.Advance(x)
		elif(next1 == "char"):
			self.Advance(x)
		elif(next1 == "string"):
			self.Advance(x)
		elif(next1 == "void"):
			self.Advance(x)
		elif(next1 == "struct"):
			self.Advance(x)
			# varName
			nextt = self.tokenizer.LL1type()
			if(nextt == "IDENTIFIER"):
				thitype_2 = self.utility2()[1]
				self.Advance(x)
			else:
				self.utility(x, "SyntaxERROR, it should be an identifier\n")
		elif(next1 == "enum"):
			self.Advance(x)
			# varName
			nextt = self.tokenizer.LL1type()
			if(nextt == "IDENTIFIER"):
				thitype_2 = self.utility2()[1]
				self.Advance(x)
			else:
				self.utility(x, "SyntaxERROR, it should be an identifier\n")
		else:  #E4
			self.utility(x, "SyntaxERROR, for unrecognized token\n")
		if(thitype_2):
			thitype = (thitype_1, thitype_2)
		else:
			thitype = (thitype_1, )
		return thitype

# 3.28  添加符号表
	def CompileParameterList(self, x):
		self.utility(x,"<parameterList>\n")
		paramslist = []

		thisdict = dict()
		thistype = self.CompileType(x+1)  # type
		thisdict['variable_type'] = thistype
		next1 = self.tokenizer.LL1()
		starnum = 0
		while(next1 == "*"):
			starnum = starnum + 1
			self.Advance(x+1)  # "*"
			next1 = self.tokenizer.LL1()
		thisdict['starnum'] = starnum
		nextt = self.tokenizer.LL1type()
		if(nextt == "IDENTIFIER"):
			thisdict['vname'] = self.utility2()[1]
			if (symboltable.lookup_variable(findvname=thisdict['vname'], ftype=1)):
				self.utility(x, "SemanticsERROR, Redifining the variable: {}\n".format(thisdict['vname']))
			self.Advance(x+1)  # varName
		else:
			self.utility(x, "SyntaxERROR, it should be an identifier\n")
		next1 = self.tokenizer.LL1()
		thisdict['isarray'] = False
		if(next1 == "["):
			thisdict['isarray'] = True
			weidu = []
			if(thisdict['starnum'] != 0):
				self.utility(x, "SyntaxERROR, '*' and '['']' cannot use together\n")
			else:
				num = 1
				while(next1 == "["):
					thiweidu_1 = num
					thiweidu_2 = None
					num = num + 1
					self.Advance(x+1)  #'['
					next1 = self.tokenizer.LL1()
					nextt = self.tokenizer.LL1type()
					if(nextt == "INT_CONST"):
						thiweidu_2 = self.utility2()[1]
						self.Advance(x + 1)  # 'INT'
						next1 = self.tokenizer.LL1()
						if(next1 == "]"):
							self.Advance(x + 1)  # ']'
						else:
							self.utility(x, "SyntaxERROR, it should be a ']'\n")
					elif(next1 == "]"):
						self.Advance(x+1)  #']'
					else:
						self.utility(x, "SyntaxERROR, unrecgonized token in parameterlist\n")
					if(thiweidu_2):
						thiweidu = (thiweidu_1, thiweidu_2)
					else:
						thiweidu = (thiweidu_1, )
					weidu.append(thiweidu)
					next1 = self.tokenizer.LL1()
			thisdict['weidu'] = weidu
		paramslist.append(thisdict)
		qplwriter.writereceiveparams(thisdict['vname'])
		symboltable.insert(thisdict['vname'], thisdict, 1)
		next1 = self.tokenizer.LL1()
		while(next1 == ","):
			self.Advance(x+1)  # ','

			thisdict2 = dict()
			thistype = self.CompileType(x + 1)  # type
			thisdict2['variable_type'] = thistype
			next1 = self.tokenizer.LL1()
			starnum = 0
			while (next1 == "*"):
				starnum = starnum + 1
				self.Advance(x + 1)  # "*"
				next1 = self.tokenizer.LL1()
			thisdict2['starnum'] = starnum
			nextt = self.tokenizer.LL1type()
			if (nextt == "IDENTIFIER"):
				thisdict2['vname'] = self.utility2()[1]
				if (symboltable.lookup_variable(findvname=thisdict2['vname'], ftype=1)):
					self.utility(x, "SemanticsERROR, Redifining the variable: {}\n".format(thisdict2['vname']))
				self.Advance(x + 1)  # varName
			else:
				self.utility(x, "SyntaxERROR, it should be an identifier\n")
			next1 = self.tokenizer.LL1()
			thisdict2['isarray'] = False
			if (next1 == "["):
				thisdict2['isarray'] = True
				weidu = []
				if (thisdict2['starnum'] != 0):
					self.utility(x, "SyntaxERROR, '*' and '['']' cannot use together\n")
				else:
					num = 1
					while (next1 == "["):
						thiweidu_1 = num
						thiweidu_2 = None
						num = num + 1
						self.Advance(x + 1)  # '['
						next1 = self.tokenizer.LL1()
						nextt = self.tokenizer.LL1type()
						if (nextt == "INT_CONST"):
							thiweidu_2 = self.utility2()[1]
							self.Advance(x + 1)  # 'INT'
							next1 = self.tokenizer.LL1()
							if (next1 == "]"):
								self.Advance(x + 1)  # ']'
							else:
								self.utility(x, "SyntaxERROR, it should be a ']'\n")
						elif (next1 == "]"):
							self.Advance(x + 1)  # ']'
						else:
							self.utility(x, "SyntaxERROR, unrecgonized token in parameterlist\n")
						if (thiweidu_2):
							thiweidu = (thiweidu_1, thiweidu_2)
						else:
							thiweidu = (thiweidu_1,)
						weidu.append(thiweidu)
						next1 = self.tokenizer.LL1()
				thisdict2['weidu'] = weidu
			paramslist.append(thisdict2)
			symboltable.insert(thisdict2['vname'], thisdict2, 1)
			qplwriter.writereceiveparams(thisdict2['vname'])
			next1 = self.tokenizer.LL1()
		self.utility(x,"</parameterList>\n")
		return paramslist

# 3.26  添加符号表
	def CompileEnumDecl(self, x):
		self.utility(x,"<enumDecl>\n")
		self.Advance(x+1)  # "enum"
		nextt = self.tokenizer.LL1type()
		# variable name
		vname = self.utility2()[1]
		if(nextt != "IDENTIFIER"):
			self.utility(x+1, "SyntaxERROR: It should be an identifier\n")
		elif(symboltable.lookup(vname, 5)):
			# look up symboltable
			self.utility(x+1, "SemanticsERROR: Redefine variable: {}\n".format(vname))
		else:
			self.Advance(x + 1)  # varName
			next1 = self.tokenizer.LL1()
			if (next1 != "{"):
				self.utility(x+1, "SyntaxERROR: It should be '{'\n")
			self.Advance(x+1)  # '{'
			vdict = dict()
			nextt = self.tokenizer.LL1type()
			va = self.utility2()[1]
			if (nextt != "IDENTIFIER"):
				self.utility(x + 1, "SyntaxERROR: It should be an identifier\n")
			self.Advance(x+1)  # varName
			next1 = self.tokenizer.LL1()
			pt = 0
			if (next1 == "="):
				self.Advance(x + 1)  # "="
				nextt = self.tokenizer.LL1type()
				if(nextt != "INT_CONST"):
					self.utility(x + 1, "SyntaxERROR: It should be an integer\n")
				vv = self.utility2()[1]
				pt = vv
				self.Advance(x + 1)  # num
			else:
				vv = pt
				pt = pt + 1
			vdict[va] = vv
			next1 = self.tokenizer.LL1()
			while(next1 == ","):
				self.Advance(x+1)  # ","
				nextt = self.tokenizer.LL1type()
				va = self.utility2()[1]
				if (nextt != "IDENTIFIER"):
					self.utility(x + 1, "SyntaxERROR: It should be an identifier\n")
				self.Advance(x+1)  # varName
				next1 = self.tokenizer.LL1()
				if(next1 == "="):
					self.Advance(x + 1)  # "="
					nextt = self.tokenizer.LL1type()
					if (nextt != "INT_CONST"):
						self.utility(x + 1, "SyntaxERROR: It should be an integer\n")
					vv = self.utility2()[1]
					pt = vv
					self.Advance(x + 1)  # num
				else:
					vv = pt
					pt = pt + 1
				vdict[va] = vv
				next1 = self.tokenizer.LL1()
			# insert to symboltable
			symboltable.insert(vname, vdict)
			next1 = self.tokenizer.LL1()
			if(next1 != "}"):
				self.utility(x + 1, "SyntaxERROR: It should be an '}'\n")
			self.Advance(x+1)  # '}'
			next1 = self.tokenizer.LL1()
			if(next1 != ";"):
				self.utility(x + 1, "SyntaxERROR: It should be an ';'\n")
			self.Advance(x+1)  # ';'
		self.utility(x,"</EnumDecl>\n")

# 3.28  添加符号表
	def CompileStructDecl(self, x):
		self.utility(x,"<structDecl>\n")
		next1 = self.tokenizer.LL1()
		content = list()
		thicontent = dict()
		if(next1 == "struct"):
			self.Advance(x+1)  #"struct"
		else:
			self.utility(x+1, "SyntaxERROR: It should be 'struct'\n")
		nextt = self.tokenizer.LL1type()
		if(nextt == "IDENTIFIER"):
			structname = self.utility2()[1]
			if(symboltable.lookup(structname, 4)):
				self.utility(x + 1, "SemanticsERROR: Redefine struct variable: {}\n".format(structname))
			self.Advance(x+1)  #varName
		else:
			self.utility(x+1, "SyntaxERROR: It should be an identifier\n")
		next1 = self.tokenizer.LL1()
		if(next1 == "{"):
			self.Advance(x+1)  #"{"
		else:
			self.utility(x+1, "SyntaxERROR: It should be a '{'\n")
		thicontent = self.CompileVariableDecl(x+1, 3)
		content.append(thicontent)
		next1 = self.tokenizer.LL1()
		while(next1 != "}"):
			thicontent = self.CompileVariableDecl(x+1, 3)
			content.append(thicontent)
			next1 = self.tokenizer.LL1()
		if(next1 == "}"):
			self.Advance(x+1)  #"}"
		else:
			self.utility(x+1, "SyntaxERROR: It should be a '}'\n")
		if(next1 == ";"):
			self.Advance(x+1)  #";"
		else:
			self.utility(x+1, "SyntaxERROR: It should be a ';'\n")
		symboltable.insert(structname, content, 4)
		self.utility(x,"</structDecl>\n")

# 3.28  添加符号表
	def CompileFunctionDecl(self, x):
		self.utility(x,"<FunctionDecl>\n")
		content = dict()
		content['return_type'] = self.CompileType(x+1)  # type
		next1 = self.tokenizer.LL1()
		starnum = 0
		while(next1 == "*"):
			starnum = starnum + 1
			self.Advance(x+1)  #"*"
			next1 = self.tokenizer.LL1()
		content['return_type_starnum'] = starnum
		nextt = self.tokenizer.LL1type()
		if(nextt == "IDENTIFIER"):
			function_name = self.utility2()[1]
			self.now_turn_function_name = function_name
			self.Advance(x+1)  #routineName
		else:
			self.utility(x, "SyntaxERROR, it should be an identifier\n")
		next1 = self.tokenizer.LL1()
		if(next1 == '('):
			self.Advance(x+1)  # "("
		else:
			self.utility(x, "SyntaxERROR, it should be '('\n")
		next1 = self.tokenizer.LL1()
		if(next1 in self.ADtype or next1 in self.AStype):
			content['paramslist'] = self.CompileParameterList(x+1)
			self.Advance(x+1)  # ")"
		elif(next1 == ")"):
			self.Advance(x+1)  # ")"
		else:
			self.utility(x, "SyntaxERROR, unrecognizing token in functiondecl: {}\n".format(next1))
		next1 = self.tokenizer.LL1()
		content['isused'] = False
		# 仅函数声明
		if(next1 == ";"):
			self.Advance(x+1)  # ";"
			if(symboltable.lookup(function_name, 1)):
				self.utility(x+1, "SemanticsERROR: Redefine function: {}\n".format(function_name))
			else:
				symboltable.insert(function_name, content, 1)
			# exit 1

		elif(next1 == "{"):
			original_content = symboltable.lookup(function_name, 1)
			# 四元式
			qplwriter.writeLabel(function_name)
			# 符号表维护
			symboltable.variableStackPointer.append(symboltable.variableStackIterator)
			symboltable.variableStackPointerIterator = symboltable.variableStackPointerIterator + 1
			#计数器清零
			self.now_ifnum = 0
			self.now_whilenum = 0
			self.now_fornum = 0
			if(not original_content):
				content['isused'] = True
				symboltable.insert(function_name, content, 1)
				self.CompileBodyDecl(x + 1)
			elif(not original_content['isused']):
				# DEBUG
				# 与之前的content比较, 语义分析
				if(content == original_content):
					symboltable.update(1, function_name, 3, True)
					self.CompileBodyDecl(x+1)
				else:
					self.utility(x+1, "SemanticsERROR: The definition of function: {} is not matched correctly\n".format(function_name))
			else:
				self.utility(x+1, "SemanticsERROR: Redefine function: {}\n".format(function_name))
			# exit 2
		else:
			self.utility(x, "SyntaxERROR, unrecognizing token in functiondecl\n")
		self.now_turn_function_name = ""
		self.utility(x,"</FunctionDecl>\n")

#utype == 1 全局变量
#utype == 2 局部变量
#utype == 3 结构变量 返回值 list()
	def CompileVariableDecl(self, x, utype):
		self.utility(x,"<variableDecl>\n")
		thivaria = dict()
		structlist = list()
		thivaria['variable_type'] = self.CompileType(x+1)  #type
		next1 = self.tokenizer.LL1()
		starnum = 0
		while(next1 == "*"):
			starnum  = starnum + 1
			self.Advance(x+1)  # "*"
			next1 = self.tokenizer.LL1()
		thivaria['starnum'] = starnum
		nextt = self.tokenizer.LL1type()
		if(nextt == "IDENTIFIER"):
			thivaria['vname'] = self.utility2()[1]
			if(symboltable.lookup_variable(findvname = thivaria['vname'], ftype = 1)):
				self.utility(x, "SemanticsERROR, Redifining the variable: {}\n".format(thivaria['vname']))
			#else: insert

			self.Advance(x+1)  # varName
		else:
			self.utility(x, "SyntaxERROR, it should be an identifier\n")
		next1 = self.tokenizer.LL1()

		thivaria['isarray'] = False
		if (next1 == "["):
			thivaria['isarray'] = True
			weidu = []
			if (thivaria['starnum'] != 0):
				self.utility(x, "SyntaxERROR, '*' and '['']' cannot use in the same variable\n")
			else:
				num = 1
				while (next1 == "["):
					thiweidu_1 = num
					thiweidu_2 = None
					num = num + 1
					self.Advance(x+1)  # '['
					nextt = self.tokenizer.LL1type()
					if (nextt == "INT_CONST"):
						thiweidu_2 = self.utility2()[1]
						####################### 需要底层语义分析
						# 暂时修改成
						self.Advance(x+1)  # 'INT_CONST'
						# self.CompileExpression(x + 1)  # 'INT'
						####################### 需要底层语义分析
						next1 = self.tokenizer.LL1()
						if(next1 == "]"):
							self.Advance(x+1)  # ']'
						else:
							self.utility(x, "SyntaxERROR, it should be a ']'\n")
					else:
						self.utility(x, "SyntaxERROR, unrecgonized token in parameterlist\n")
					if (thiweidu_2):
						thiweidu = (thiweidu_1, thiweidu_2)
					else:
						thiweidu = (thiweidu_1,)
					weidu.append(thiweidu)
					next1 = self.tokenizer.LL1()
			thivaria['weidu'] = weidu
		if (utype == 1 or utype == 2):
			symboltable.variableStack.append(thivaria)
			symboltable.variableStackIterator = symboltable.variableStackIterator + 1
		elif(utype == 3):
			structlist.append(thivaria)
		next1 = self.tokenizer.LL1()

		while(next1 == ','):
			self.Advance(x+1)  #","
			thivariab = dict()
			thivariab['variable_type'] = thivaria['variable_type']  # type
			next1 = self.tokenizer.LL1()
			starnum = 0
			while (next1 == "*"):
				starnum = starnum + 1
				self.Advance(x + 1)  # "*"
				next1 = self.tokenizer.LL1()
			thivariab['starnum'] = starnum
			nextt = self.tokenizer.LL1type()
			if (nextt == "IDENTIFIER"):
				thivariab['vname'] = self.utility2()[1]
				if (symboltable.lookup_variable(findvname=thivariab['vname'], ftype=1)):
					self.utility(x, "SemanticsERROR, Redifining the variable: {}\n".format(thivariab['vname']))
				# else: insert

				self.Advance(x + 1)  # varName
			else:
				self.utility(x, "SyntaxERROR, it should be an identifier\n")
			next1 = self.tokenizer.LL1()

			thivariab['isarray'] = False
			if (next1 == "["):
				thivariab['isarray'] = True
				weidu = []
				if (thivariab['starnum'] != 0):
					self.utility(x, "SyntaxERROR, '*' and '['']' cannot use in the same variable\n")
				else:
					num = 1
					while (next1 == "["):
						thiweidu_1 = num
						thiweidu_2 = None
						num = num + 1
						self.Advance(x + 1)  # '['
						nextt = self.tokenizer.LL1type()
						if (nextt == "INT_CONST"):
							thiweidu_2 = self.utility2()[1]
							####################### 需要底层语义分析
							# 暂时修改成
							self.Advance(x + 1)  # 'INT_CONST'
							# self.CompileExpression(x + 1)  # 'INT'
							####################### 需要底层语义分析
							next1 = self.tokenizer.LL1()
							if (next1 == "]"):
								self.Advance(x + 1)  # ']'
							else:
								self.utility(x, "SyntaxERROR, it should be a ']'\n")
						else:
							self.utility(x, "SyntaxERROR, unrecgonized token in parameterlist\n")
						if (thiweidu_2):
							thiweidu = (thiweidu_1, thiweidu_2)
						else:
							thiweidu = (thiweidu_1,)
						weidu.append(thiweidu)
						next1 = self.tokenizer.LL1()
				thivariab['weidu'] = weidu
			if (utype == 1 or utype == 2):
				symboltable.variableStack.append(thivariab)
				symboltable.variableStackIterator = symboltable.variableStackIterator + 1
			elif (utype == 3):
				structlist.append(thivariab)
			next1 = self.tokenizer.LL1()

		if(next1 == ";"):
			self.Advance(x+1)  #";"
		else:
			self.utility(x, "SyntaxERROR, it should be a ';'\n")
		self.utility(x,"</variableDecl>\n")
		if(utype == 3):
			return structlist

	def CompileBodyDecl(self, x):
		self.utility(x,"<bodyDecl>\n")
		next1 = self.tokenizer.LL1()
		if(next1 == "{"):
			self.Advance(x+1)  #'{'
		else:
			self.utility(x, "SyntaxERROR, it should be a '{'\n")

		next1 = self.tokenizer.LL1()
		while(next1 in self.AStype or next1 in self.ADtype):
			self.CompileVariableDecl(x+1, 2)
			next1 = self.tokenizer.LL1()
		nextt = self.tokenizer.LL1type()
		while(nextt == "RESERVED_WORD" or nextt == "IDENTIFIER" or next1 == "{"):
			self.CompileStatement(x+1)
			next1 = self.tokenizer.LL1()
			nextt = self.tokenizer.LL1type()
		if(next1 == "}"):
			self.Advance(x+1)  # '}'
		else:
			self.utility(x, "SyntaxERROR, it should be a '}'\n")

		# 符号表维护
		ii = symboltable.variableStackPointer[symboltable.variableStackPointerIterator-1]
		eend = len(symboltable.variableStack)
		# print("{}: {}".format(ii, eend))
		while(ii != eend):
			symboltable.variableStack.pop()
			symboltable.variableStackIterator = symboltable.variableStackIterator - 1
			eend = eend - 1
			# print("{}: {}".format(ii, eend))
		symboltable.variableStackPointer.pop()
		symboltable.variableStackPointerIterator = symboltable.variableStackPointerIterator - 1
		self.utility(x, "</bodyDecl>\n")

	def CompileStatement(self, x):
		self.utility(x, "<statements>\n")
		next1 = self.tokenizer.LL1()
		if(next1 == "if"):
			self.CompileIf(x+1)
			self.now_ifnum = self.now_ifnum + 1
		elif(next1 == "while" or next1 == "do"):
			self.CompileWhile(x+1)
			self.now_whilenum = self.now_whilenum + 1
		elif(next1 == "for"):
			self.CompileFor(x+1)
			self.now_fornum = self.now_fornum + 1
		elif(next1 == "return"):
			self.CompileReturn(x+1)
		elif(next1 == "{"):
			self.CompileBlock(x+1)
		elif(next1 == "goto"):
			self.CompileGoto(x+1)
		elif(next1 == "++" or next1 == "--"):
			self.CompileLet(x+1)
		elif(next1 in ["break", "continue"]):
			self.Advance(x+1)
			next1 = self.tokenizer.LL1()
			self.Advance(x+1)
			if(next1 != ";"):
				self.utility(x, "SyntaxERROR, it should be ';'\n")
		else:
			next2 = self.tokenizer.LL(2)
			if(next2 in [".", "->"]):  # for struct
				next2 = self.tokenizer.LL(4)
			if(next2 == ":"):
				self.CompileLabel(x+1)
				next1 = self.tokenizer.LL1()
				self.Advance(x+1)
				if(next1 != ":"):
					self.utility(x, "SyntaxERROR, it should be ':'\n")
				self.CompileStatement(x+1)
			elif(next2 in ["++", "--"]):
				self.CompileLet(x + 1)
			else:
				nextpt = 1
				nextx = self.tokenizer.LL(nextpt)
				flag = True
				while(nextx != ";"):
					if(nextx == "="):
						flag = False
						break
					else:
						nextpt += 1
						nextx = self.tokenizer.LL(nextpt)
				if(flag):
					self.CompileDo(x+1)
				else:
					self.CompileLet(x+1)
		# 3.30 增加逗号运算符
		next1 = self.tokenizer.LL1()
		if(next1 == ","):
			self.Advance(x)  # ","
			self.CompileStatement(x+1)
		self.utility(x, "</statements>\n")
# 3.31 添加四元式功能
	def CompileLabel(self, x):
		self.utility(x, "<labelStatement>\n")
		labelname = self.utility2()[1]
		qplwriter.writeLabel(labelname)
		self.Advance(x+1)  # labelname
		next1 = self.tokenizer.LL1()
		if(next1 == ":"):
			self.Advance(x+1)  #':'
		else:
			self.utility(x, "SyntaxERROR, it should be a ':'\n")
		self.CompileStatement(x+1)
		self.utility(x, "</labelStatement>\n")

	#check in PM,3.22
	def CompileLet(self, x):
		self.utility(x, "<letStatement>\n")
		next1 = self.tokenizer.LL1()
		if(next1 in ["++",  "--"]):
			self.Advance(x+1)  # "++", "--"
			varname = self.CompilevarName(x+1)  # varName
			qplwriter.writeselfop(next1, varname, 1)
		else:
			varname = ""
			while(next1 == "*"):
				self.Advance(x+1)
				varname = varname + "*"
				next1 = self.tokenizer.LL1()
			varname = self.CompilevarName(x + 1)  # varName
			next1 = self.tokenizer.LL1()
			if(next1 in ["++", "--"]):
				self.Advance(x+1)
				qplwriter.writeselfop(next1, varname, 2)
			else:
				while (next1 == "["):
					self.Advance(x + 1)  # '['
					varname = varname + "["
					self.CompileExpression(x + 1)
					varname = varname + "TMP" + str(qplwriter.tempnum-1)
					next1 = self.tokenizer.LL1()
					self.Advance(x + 1)  # ']'
					varname = varname + "]"
					if(next1 != "]"):
						self.utility(x+1, "SyntaxERROR, it should be ']'\n")
					next1 = self.tokenizer.LL1()
				self.Advance(x+1)  # '='
				if(next1 != '='):
					self.utility(x+1, "SyntaxERROR, it should be '='\n")
				self.CompileExpression(x+1)
				qplwriter.writelet(varname)
		next1 = self.tokenizer.LL1()
		if(next1 == ";" or next1 == ")"):
			self.Advance(x+1)  # ';' or ')'
		elif(next1 == ","):
			pass
		else:
			self.utility(x+1, "SyntaxERROR, it should be ';' or ')' or ','\n")
		self.utility(x, "</letStatement>\n")

	def CompileIf(self, x):
		self.utility(x, "<ifStatement>\n")
		self.Advance(x+1)  #'if'

		next1 = self.tokenizer.LL1()
		if(next1 == "("):
			self.Advance(x+1)  # '('
		else:
			self.utility(x, "SyntaxERROR, it should be a '('\n")
		self.CompileExpression(x+1)
		value = "TMP" + str(qplwriter.tempnum-1)
		labelelse = self.now_turn_function_name+"_else_"+str(self.now_ifnum)
		qplwriter.writeJmp(3, "-", labelelse, value)
		next1 = self.tokenizer.LL1()
		if(next1 == ")"):
			self.Advance(x+1)  # ')'
		else:
			self.utility(x, "SyntaxERROR, it should be a ')'\n")
		next1 = self.tokenizer.LL1()
		if(next1 == "{"):
			self.Advance(x+1)  # '{'
		else:
			self.utility(x, "SyntaxERROR, it should be a '{'\n")
		next1 = self.tokenizer.LL1()
		nextt = self.tokenizer.LL1type()
		while (nextt == "IDENTIFIER" or nextt == "RESERVED_WORD" or next1 == "*" or next1 == "{"):
			self.CompileStatement(x + 1)
			next1 = self.tokenizer.LL1()
			nextt = self.tokenizer.LL1type()
		labelifend = self.now_turn_function_name+"_ifend_"+str(self.now_ifnum)
		qplwriter.writeGoto(labelifend)
		if(next1 == "}"):
			self.Advance(x+1)  # '}'
		else:
			self.utility(x, "SyntaxERROR, it should be a '}'\n")
		next1 = self.tokenizer.LL1()
		qplwriter.writeLabel(labelelse)
		if(next1 == "else"):
			self.Advance(x+1)  # "else"
			next1 = self.tokenizer.LL1()
			if (next1 == "{"):
				self.Advance(x + 1)  # '{'
			else:
				self.utility(x, "SyntaxERROR, it should be a '{'\n")
			next1 = self.tokenizer.LL1()
			nextt = self.tokenizer.LL1type()
			while(nextt == "IDENTIFIER" or nextt == "RESERVED_WORD" or next1 == "*" or next1 == "{"):
				self.CompileStatement(x+1)
				next1 = self.tokenizer.LL1()
				nextt = self.tokenizer.LL1type()
			if (next1 == "}"):
				self.Advance(x + 1)  # '}'
			else:
				self.utility(x, "SyntaxERROR, it should be a '}'\n")
		qplwriter.writeLabel(labelifend)
		self.utility(x, "</ifStatement>\n")

	def CompileWhile(self, x):
		self.utility(x, "<whileStatement>\n")
		next1 = self.tokenizer.LL1()
		if(next1 == 'while'):
			self.Advance(x+1)  # 'while'
			next1 = self.tokenizer.LL1()
			if(next1 == "("):
				self.Advance(x+1)  # '('
			else:
				self.utility(x, "SyntaxERROR, it should be a '('\n")
			labelbeginname = self.now_turn_function_name + "while_begin_" + str(self.now_whilenum)
			qplwriter.writeLabel(labelbeginname)
			self.CompileExpression(x+1)
			next1 = self.tokenizer.LL1()
			if(next1 == ")"):
				self.Advance(x+1)  # ')'
			else:
				self.utility(x, "SyntaxERROR, it should be a ')'\n")
			value = "TMP" + str(qplwriter.tempnum-1)
			labelendname = self.now_turn_function_name + "while_end_" + str(self.now_whilenum)
			qplwriter.writeJmp(3, "-", labelendname, value)

			next1 = self.tokenizer.LL1()
			if(next1 == "{"):
				self.Advance(x+1)  # '{'
			else:
				self.utility(x, "SyntaxERROR, it should be a '{'\n")
			next1 = self.tokenizer.LL1()
			while(next1 != "}"):
				self.CompileStatement(x+1)
				next1 = self.tokenizer.LL1()
			qplwriter.writeGoto(labelbeginname)
			if(next1 == "}"):
				self.Advance(x+1)  # '}'
			else:
				self.utility(x, "SyntaxERROR, it should be a '}'\n")
		elif(next1 == 'do'):
			self.Advance(x+1)  # 'do'
			next1 = self.tokenizer.LL1()
			if(next1 == "{"):
				self.Advance(x+1)  # '{'
			else:
				self.utility(x, "SyntaxERROR, it should be a '{'\n")
			next1 = self.tokenizer.LL1()
			labelbeginname = self.now_turn_function_name + "while_begin_" + str(self.now_whilenum)
			qplwriter.writeLabel(labelbeginname)
			while(next1 != "}"):
				self.CompileStatement(x+1)
				next1 = self.tokenizer.LL1()
			if(next1 == "}"):
				self.Advance(x+1)  # '}'
			else:
				self.utility(x, "SyntaxERROR, it should be a '}'\n")
			self.Advance(x+1)  # 'while'
			next1 = self.tokenizer.LL1()
			if(next1 == "("):
				self.Advance(x+1)  # '('
			else:
				self.utility(x, "SyntaxERROR, it should be a '('\n")
			self.CompileExpression(x+1)
			value = "TMP" + str(qplwriter.tempnum - 1)
			# labelendname = self.now_turn_function_name + "while_end_" + str(self.now_whilenum)
			qplwriter.writeJmp(3, labelbeginname, "-", value)
			next1 = self.tokenizer.LL1()
			if(next1 == ")"):
				self.Advance(x+1)  # ')'
			else:
				self.utility(x, "SyntaxERROR, it should be a ')'\n")
			next1 = self.tokenizer.LL1()
			if(next1 == ";"):
				self.Advance(x+1)  # ';'
			else:
				self.utility(x, "SyntaxERROR, it should be a ';'\n")
		else:
			self.utility(x, "SyntaxERROR, unrecgonized token: {}\n".format(next1))
		self.utility(x, "</whileStatement>\n")
# 3.31 添加四元式功能
	def CompileReturn(self, x):
		self.utility(x, "<returnStatement>\n")
		self.Advance(x+1)  #'return'
		next1 = self.tokenizer.LL1()
		if(next1 != ";"):
			self.CompileExpression(x+1)
			qplwriter.writeReturn()
		else:
			qplwriter.writeReturn(False)
		self.Advance(x+1)  # ';'
		self.utility(x, "</returnStatement>\n")
	# 估计有bug
	def CompileFor(self, x):
		self.utility(x, "<forStatement>\n")
		next1 = self.tokenizer.LL1()
		self.Advance(x+1)  #'for'
		next1 = self.tokenizer.LL1()
		self.Advance(x+1)  #'('
		if(next1 != "("):
			self.utility(x+1, "SyntaxERROR, it should be '('\n")
		labelforbegin = self.now_turn_function_name + "_forbegin_" + str(self.now_fornum)
		labelforend = self.now_turn_function_name + "_forend_" + str(self.now_fornum)
		nextt = self.tokenizer.LL1type()
		next1 = self.tokenizer.LL1()
		for i in range(2):
			if(nextt == "INT_CONST" or nextt == "FLOAT_CONST" or nextt == "CHAR_CONST" or nextt == "STRING_CONST" or nextt == "BOOL_CONST" or nextt == "IDENTIFIER"
			or next1 == ["(" ,"-",'+','!','++','--']):
				if(i == 0):
					self.CompileStatement(x+1)
				elif(i == 1):
					self.CompileExpression(x+1)
					value = "TMP" + str(qplwriter.tempnum-1)
					qplwriter.writeJmp(3, labelforbegin, labelforend, value)
					self.Advance(x+1)  #';'
				nextt = self.tokenizer.LL1type()
				next1 = self.tokenizer.LL1()
			elif(next1 == ";"):
				self.Advance(x+1)  #';'
				nextt = self.tokenizer.LL1type()
				next1 = self.tokenizer.LL1()
			else:
				self.utility(x,"ERROR\n")
		# for 第三项
		labelforstart = self.now_turn_function_name + "_forstart_" + str(self.now_fornum)
		qplwriter.writeLabel(labelforstart)
		nextt = self.tokenizer.LL1type()
		next1 = self.tokenizer.LL1()
		if (nextt == "INT_CONST" or nextt == "FLOAT_CONST" or nextt == "CHAR_CONST" or nextt == "STRING_CONST" or nextt == "BOOL_CONST" or nextt == "IDENTIFIER"
			or next1 in ["(", "-", '+', '!', '++', '--']):
			self.CompileStatement(x + 1)
		elif(next1 == ")"):
			self.Advance(x+1)  #')'
		else:
			self.utility(x,"SyntaxERROR, it should be a ')'\n")
		qplwriter.writeGoto(labelforbegin)
		next1 = self.tokenizer.LL1()
		if(next1 == "{"):
			self.Advance(x+1)  # '{'
		else:
			self.utility(x, "SyntaxERROR, it should be a '{'\n")
		qplwriter.writeLabel(labelforbegin)
		next1 = self.tokenizer.LL1()
		while (next1 != "}"):
			self.CompileStatement(x + 1)
			next1 = self.tokenizer.LL1()
		if(next1 == "}"):
			self.Advance(x+1)  # '}'
		else:
			self.utility(x, "SyntaxERROR, it should be a '}'\n")
		qplwriter.writeGoto(labelforstart)
		qplwriter.writeLabel(labelforend)
		self.utility(x,"</forStatement>\n")
	#check PM, 3.22
	def CompileDo(self, x):
		self.utility(x,"<doStatement>\n")
		self.CompileRoutineCall(x+1)
		next1 = self.tokenizer.LL1()
		if(next1 == ";"):
			self.Advance(x+1)
		else:
			self.utility(x+1,"SyntaxERROR,it shoule be a ';'\n")
		self.utility(x,"</doStatement>\n")

	def CompileBlock(self, x):
		self.utility(x,"<blockStatement>\n")
		next1 = self.tokenizer.LL1()
		if(next1 == "{"):
			self.Advance(x+1)  #' {'
			qplwriter.writeinout(1)
		else:
			self.utility(x,"SyntaxERROR, it should be a '{'\n")
		self.CompileBodyDecl(x+1)
		next1 = self.tokenizer.LL1()
		if(next1 == "}"):
			self.Advance(x+1)  #  '}'
			qplwriter.writeinout(2)
		else:
			self.utility(x, "SyntaxERROR, it should be a '}'\n")
		self.utility(x,"</blockStatement>\n")

	def CompileGoto(self, x):
		self.utility(x,"<gotoStatement>\n")
		next1 = self.tokenizer.LL1()
		if(next1 == "goto"):
			self.Advance(x+1)  # 'goto'
		else:
			self.utility(x, "SyntaxERROR, it should be a 'goto'\n")
		labelname = self.utility2()[1]
		qplwriter.writeGoto(labelname)
		nextt = self.tokenizer.LL1type()
		if(nextt == "IDENTIFIER"):
			self.Advance(x+1)  # label
		else:
			self.utility(x, "SyntaxERROR, it should be a identifier\n")
		next1 = self.tokenizer.LL1()
		if(next1 == ";"):
			self.Advance(x+1)  # ';'
		else:
			self.utility(x, "SyntaxERROR, it should be a ';'\n")
		self.utility(x,"</gotoStatement>\n")
#未用
	def CompileThreecase(self, x):
		self.utility(x,"<threecase>\n")
		next1 = self.tokenizer.LL1()
		while(next1 in self.arithop or next1 in self.cmpop):
			self.Advance(x+1)  # op
			self.CompileTerm(x+1)
			next1 = self.tokenizer.LL1()
		if(next1 == '?'):
			self.Advance(x+1)  # '?'
		else:
			self.utility(x, "SyntaxError,it should be a '?'\n")
		self.CompileExpression(x+1)
		if(next1 == ':'):
			self.Advance(x+1)  # ':'
		else:
			self.utility(x, "SyntaxError,it should be a ':'\n")
		self.CompileExpression(x+1)
		self.utility(x,"</threecase>\n")

#EXPRESSION
	def CompileExpression(self, x):
		self.utility(x,"<expression>\n")
		termnum = 0
		term1 = self.CompileTerm(x+1)
		termnum = termnum + 1
		next1 = self.tokenizer.LL1()
		while(True):
			if(next1 in self.arithop or next1 in self.cmpop):
				operatorname = self.utility2()[1]
				self.Advance(x+1)  # op

				term2 = self.CompileTerm(x+1)
				if(termnum != 1):
					term1 = "TMP" + str(qplwriter.tempnum-1)
				qplwriter.writearyop(operatorname, term1, term2)
				termnum = termnum + 1
				next1 = self.tokenizer.LL1()
			elif(next1 in ["]",",",";", ")"]):
				if(termnum == 1):
					qplwriter.writelet(sender=term1)
				break
			else:
				self.utility(x,"SyntaxERROR, unrecognized token: {} in expression\n".format(next1))
				break
		self.utility(x,"</expression>\n")
	#The most complex part
	# check PM,3.22
	def CompileTerm(self, x):
		self.utility(x,"<term>\n")
		# look ahead 1 character.
		nextt = self.tokenizer.LL1type()
		next1 = self.tokenizer.LL1()
		const = self.utility2()[1]
		now = const
		if(nextt == "INT_CONST"):       #  -> INT_CONST
			self.Advance(x+1)
		elif(nextt == "FLOAT_CONST"):   #  -> FLOAT_CONST
			self.Advance(x+1)
		elif(nextt == "CHAR_CONST"):    #  -> CHAR_CONST
			self.Advance(x+1)
		elif(nextt == "STRING_CONST"):  #  -> STRING_CONST
			self.Advance(x+1)
		elif(nextt == "BOOL_CONST"):    #  -> BOOL_CONST
			self.Advance(x+1)
		elif(next1 == "("):             #  -> '(' expression ')'
			self.Advance(x + 1)      # "("
			self.CompileExpression(x+1)
			next1 = self.tokenizer.LL1()
			if(next1 == ")"):
				self.Advance(x + 1)  # ")"
			else:
				self.utility(x+1, "SyntaxError,it should be a ')'\n")
			now = "TMP" + str(qplwriter.tempnum-1)
		elif(next1 in ["-","+","!", "&","*"]):   #  -> leftunaryOp term
			unaryopname = self.utility2()[1]
			self.Advance(x+1)
			lastterm = self.CompileTerm(x+1)
			qplwriter.writeunaryop(unaryopname, lastterm)
			now = "TMP" + str(qplwriter.tempnum - 1)
		elif(next1 in ["++", "--"]):    #  -> leftunaryOp term
			self.Advance(x + 1)
			varname = self.CompilevarName(x+1)
			qplwriter.writeselfop(next1, varname, 1)
		elif(nextt == "IDENTIFIER"):
			next1 = self.tokenizer.LL(2)
			if(next1 in ["++","--"]):   #  -> varName "++" or "--"
				varname = self.CompilevarName(x + 1)
				qplwriter.writeselfop(next1, varname, 2)
				now = "TMP" + str(qplwriter.tempnum - 1)
				self.Advance(x+1)
			elif(next1 == "["):         #  -> varName {'[' expression ']'}+
				varname = self.CompilevarName(x + 1)
				next1 = self.tokenizer.LL1()
				while(next1 == "["):
					varname  = varname + "["
					self.Advance(x+1)  # '['
					self.CompileExpression(x+1)
					varname = varname + "TMP" + str(qplwriter.tempnum-1)
					next1 = self.tokenizer.LL1()
					if(next1 == "]"):
						varname = varname + "]"
						self.Advance(x+1)  # ']'
					else:
						self.utility(x, "SyntaxERROR: it should be a ']'\n")
					next1 = self.tokenizer.LL1()
				now = varname
			elif(next1 == "("):         #  -> RoutineCall
				self.CompileRoutineCall(x+1)
				now = "TMP" + str(qplwriter.tempnum)
										#  -> varName
			elif(next1 in self.arithop or next1 in self.cmpop or next1 in [";", ")", ",", "]"]):
				varname = self.CompilevarName(x + 1)
				now = varname
				pass
			else:  #报错
				self.Advance(x + 1)
				self.utility(x+1, "SyntaxError,Unrecognized word in Term: {}\n".format(next1))
		self.utility(x,"</term>\n")
		return now

	# create in PM,3.22
	def CompilevarName(self, x):
		varname = ""
		nextt = self.tokenizer.LL1type()
		if(nextt == "IDENTIFIER"):
			varname = varname + self.utility2()[1]
			self.Advance(x+1)
			next1 = self.tokenizer.LL1()
			if(next1 in [".","->"]):
				if(next1 == "."):
					varname = varname + "."
				elif(next1 == "->"):
					varname = varname + "->"
				self.Advance(x+1)
				nextt = self.tokenizer.LL1type()
				if(nextt == "IDENTIFIER"):
					varname = varname + self.utility2()[1]
					self.Advance(x + 1)  #success!
				else:
					self.utility(x, "SyntaxERROR, it should be a identifier.\n")
		else:
			self.utility(x, "SyntaxERROR, it should be a identifier.\n")
		return varname

	def CompileExpressionList(self, x):
		self.utility(x,"<expressionList>\n")
		next1 = self.tokenizer.LL1()
		nextt = self.tokenizer.LL1type()
		expressionnum = 0
		if(next1 in ["(", "++", "--","-","+","!","&","*"] or nextt in ["INT_CONST","FLOAT_CONST","CHAR_CONST","STRING_CONST","BOOL_CONST","IDENTIFIER"]):
			self.CompileExpression(x+1)
			expressionnum = expressionnum + 1
			qplwriter.writepassparams(expressionnum)
			next1 = self.tokenizer.LL1()
			while(True):
				if(next1 == ','):
					self.Advance(x+1)  #","
				elif(next1 == ")"):
					break
				else:
					self.utility(x,"SyntaxERROR, it should be a ',' or ')'")
				self.CompileExpression(x+1)
				expressionnum = expressionnum + 1
				qplwriter.writepassparams(expressionnum)
				next1 = self.tokenizer.LL1()
		elif(next1 == ")"):
			pass
		else:
			self.utility(x, "SyntaxERROR, unrecgonized token in expressionList\n")
		self.utility(x,"</expressionList>\n")
		return expressionnum
	# check PM,3.22
	def CompileRoutineCall(self, x):
		self.utility(x,"<routineCall>\n")
		nextt = self.tokenizer.LL1type()
		if(nextt == "IDENTIFIER"):
			callname = self.CompilevarName(x+1)  # '函数名'
		else:
			self.utility(x, "SyntaxError,it should be a identifier")
		next1 = self.tokenizer.LL1()
		if(next1 == '('):
			self.Advance(x+1)  # '('
		else:
			self.utility(x,"SyntaxError,it should be a '('\n")
		expressionnum = self.CompileExpressionList(x+1)
		if(callname == "printf"):
			qplwriter.writePrintf(expressionnum)
		elif(callname == "scanf"):
			qplwriter.writeScanf(expressionnum)
		# rand()
		# Sleep()
		# kbhit()  检测键盘是否有输入
		# getch()
		# system()
		elif(callname == "rand"):
			qplwriter.writeRand(expressionnum)
		elif(callname == "srand"):
			qplwriter.writeSrand(expressionnum)
		elif(callname == "sleep"):
			qplwriter.writeSleep(expressionnum)
		elif(callname == "kbhit"):
			qplwriter.writeKbhit(expressionnum)
		elif(callname == "getch"):
			qplwriter.writeGetch(expressionnum)
		elif(callname == "system"):
			qplwriter.writeSystem(expressionnum)
		else:
			qplwriter.writeCall(callname, expressionnum)
		next1 = self.tokenizer.LL1()
		if(next1 == ')'):
			self.Advance(x+1)  # ')'
		else:
			self.utility(x,"SyntaxError,it should be a ')'\n")
		self.utility(x,"</routineCall>\n")


os.chdir(r"C:\Users\goldfish\PycharmProjects\Cparser")
from Clexer_v4 import C_Lexer
from SymbolTable import SymbolTable
from QuadrupleWriter import QuadrupleWriter
if __name__ == '__main__':
	os.chdir(r"C:\Users\goldfish\PycharmProjects\Cparser\test")
	file = "Tetris.c"

	obj = C_Lexer(file)
	obj.preScanner()
	obj.preAnalyzer()
	obj.analyzer()

	#全局符号表
	symboltable = SymbolTable()
	#四元式打印机
	qplwriter = QuadrupleWriter(obj.fname)

	parser = CompilationEngine(obj)
	parser.CompileProgram()
	parser.__del__()


# goto1: SyntaxERROR
#
# goto2: SemanticsERROR
