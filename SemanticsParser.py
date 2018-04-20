import os
import time
import sys

from SymbolTable import SymbolTable
from Clexer_v4 import C_Lexer

class SemanticsParser:

	def __init__(self, obj):
		# self.foutname = obj.fname.split('.')[0] + ".xml"
		# self.fout = open(self.foutname,"a+",encoding="utf-8")
		self.tokenizer = obj
		self.symboltable = SymbolTable()
		self.AStype = ["int", "double", "char", "string", "void"]
		self.ADtype = ["struct", "enum"]
		self.arithop = ["+", "-", "*", "/", "%", "&&", "||", "&", "|", "^", "<<", ">>"]
		self.cmpop = [">", "<", ">=", "<=", "==", "!="]
		#语义分析
		self.stack = []
		self.pre_stack = []
		self.cur_exp = 0
		self.type_req = []
		self.func_type = ""
		self.error_list = []
		self.test = open("test.ert","w")
		self.func_params = []
		self.func_params_type = []
		self.external_library = {"printf","scanf","rand","srand","Sleep","kbhit","getch","system","time"}
		self.external_varia_num = 0
		self.external_varia_flag = 0

	def utility2(self):
		return self.tokenizer.word_table(self.tokenizer.word_iterator)

	def pushstack(self,next1):
		for i in range(0,self.cur_exp):
			self.stack[i].append(next1)
			self.pre_stack[i].append(next1)

	def pushtype_req(self,type1):
		self.type_req.append(type1)

	def gettype_req(self):
		length = len(self.type_req)
		try:
			return self.type_req[length - 1]
		except:
			#print("no type exists")
			pass

	def deltype_req(self):
		try:
			self.type_req.pop()
		except:
			#print("no type exists")
			pass

	def lookup_type(self,ID):
		for word in self.symboltable.variableStack:
			if(word['vname']==ID):
				return word['variable_type'][0]
		return "ERROR"

	def lookup_params(self,ID):
		for word in self.func_params_type:
			if(ID==word[0]):
				return word[1]
		return "ERROR"

	def checktype_req(self):
		self.test.write(str(self.stack)+"\n")
		self.test.write(str(self.type_req)+"\n")
		error_flag = 0
		func_flag = 0
		exp_type = self.gettype_req()
		if(exp_type=="INT_EXP"):
			for word in self.stack[self.cur_exp]:
				if(func_flag==1):
					if(word[1]==")"):
						func_flag = 0
						continue
					else:
						continue
				if(word[0]=="INT_CONST"):
					pass
				elif(word[0]=="INT_EXP" or word[0]=="NoRequest"):
					pass
				elif(word[0]=="IDENTIFIER"):
					if(word[1] in self.external_library):
						pass
					elif(self.lookup_type(word[1])=='int'):
						pass
					elif(self.lookup_params(word[1])=='int'):
						pass
					elif(word[1] in self.symboltable.functionTable.keys()):
						if(self.symboltable.functionTable[word[1]]["return_type"][0]=='int'):
							func_flag = 1
					else:
						error_expression = ""
						for word in self.pre_stack[self.cur_exp]:
							error_expression += word[1]
						self.error_list.append("Semantics ERROR:Expression \" "+error_expression+"\" does not match the expected type.")
						error_flag = 1
						break
				elif(word[0]=="SYMBOL"):
					if(word[1] in ["+", "-", "*", "/", "%"] or word[1] in ["[", "]", "(", ")"]):
						pass
					else:
						error_expression = ""
						for word in self.pre_stack[self.cur_exp]:
							error_expression += word[1]
						self.error_list.append("Semantics ERROR:Expression \" "+error_expression+"\" does not match the expected type.")
						error_flag = 1
						break
				else:
					error_expression = ""
					for word in self.pre_stack[self.cur_exp]:
						error_expression += word[1]
					self.error_list.append("Semantics ERROR:Expression \" "+error_expression+"\" does not match the expected type.")
					error_flag = 1
					break
					
		elif(exp_type=="FLOAT_EXP"):
			for word in self.stack[self.cur_exp]:
				if(func_flag==1):
					if(word[1]==")"):
						func_flag = 0
						continue
					else:
						continue
				if(word[0]=="FLOAT_CONST"):
					pass
				elif(word[0]=="FLOAT_EXP" or word[0]=="NoRequest"):
					pass
				elif(word[0]=="IDENTIFIER"):
					if(word[1] in self.external_library):
						pass
					elif(self.lookup_type(word[1])=='float'):
						pass
					elif(self.lookup_params(word[1])=='float'):
						pass
					elif(word[1] in self.symboltable.functionTable.keys()):
						if(self.symboltable.functionTable[word[1]]["return_type"][0]=='float'):
							func_flag = 1
					else:
						error_expression = ""
						for word in self.pre_stack[self.cur_exp]:
							error_expression += word[1]
						self.error_list.append("Semantics ERROR:Expression \" "+error_expression+"\" does not match the expected type.")
						error_flag = 1
						break
				elif(word[0]=="SYMBOL"):
					if(word[1] in ["+", "-", "*", "/", "%"] or word[1] in ["[","]","(",")"]):
						pass
					else:
						error_expression = ""
						for word in self.pre_stack[self.cur_exp]:
							error_expression += word[1]
						self.error_list.append("Semantics ERROR:Expression \" "+error_expression+"\" does not match the expected type.")
						error_flag = 1
						break
				else:
					error_expression = ""
					for word in self.pre_stack[self.cur_exp]:
						error_expression += word[1]
					self.error_list.append("Semantics ERROR:Expression \" "+error_expression+"\" does not match the expected type.")
					error_flag = 1
					break
					
		elif(exp_type=="CHAR_EXP"):
			for word in self.stack[self.cur_exp]:
				if(func_flag==1):
					if(word[1]==")"):
						func_flag = 0
						continue
					else:
						continue
				if(word[0]=="CHAR_CONST"):
					pass
				elif(word[0]=="CHAR_EXP" or word[0]=="NoRequest"):
					pass
				elif(word[0]=="IDENTIFIER"):
					if(word[1] in self.external_library):
						pass
					elif(self.lookup_type(word[1])=='char'):
						pass
					elif(self.lookup_params(word[1])=='char'):
						pass
					elif(word[1] in self.symboltable.functionTable.keys()):
						if(self.symboltable.functionTable[word[1]]["return_type"][0]=='char'):
							func_flag = 1
					else:
						error_expression = ""
						for word in self.pre_stack[self.cur_exp]:
							error_expression += word[1]
						self.error_list.append("Semantics ERROR:Expression \" "+error_expression+"\" does not match the expected type.")
						error_flag = 1
						break
				elif(word[0]=="SYMBOL"):
					if(word[1] in ["[","]","(",")"]):
						pass
					else:
						error_expression = ""
						for word in self.pre_stack[self.cur_exp]:
							error_expression += word[1]
						self.error_list.append("Semantics ERROR:Expression \" "+error_expression+"\" does not match the expected type.")
						error_flag = 1
						break
				else:
					error_expression = ""
					for word in self.pre_stack[self.cur_exp]:
						error_expression += word[1]
					self.error_list.append("Semantics ERROR:Expression \" "+error_expression+"\" does not match the expected type.")
					error_flag = 1
					break

		elif(exp_type=="STRING_EXP"):
			for word in self.stack[self.cur_exp]:
				if(func_flag==1):
					if(word[1]==")"):
						func_flag = 0
						continue
					else:
						continue
				if(word[0]=="STRING_CONST"):
					pass
				elif(word[0]=="STRING_EXP" or word[0]=="NoRequest"):
					pass
				elif(word[0]=="IDENTIFIER"):
					if(word[1] in self.external_library):
						pass
					elif(self.lookup_type(word[1])=='string'):
						pass
					elif(self.lookup_params(word[1])=='string'):
						pass
					elif(word[1] in self.symboltable.functionTable.keys()):
						if(self.symboltable.functionTable[word[1]]["return_type"][0]=='string'):
							func_flag = 1
					else:
						error_expression = ""
						for word in self.pre_stack[self.cur_exp]:
							error_expression += word[1]
						self.error_list.append("Semantics ERROR:Expression \" "+error_expression+"\" does not match the expected type.")
						error_flag = 1
						break
				elif(word[0]=="SYMBOL"):
					if(word[1] in ["[","]","(",")"]):
						pass
					else:
						error_expression = ""
						for word in self.pre_stack[self.cur_exp]:
							error_expression += word[1]
						self.error_list.append("Semantics ERROR:Expression \" "+error_expression+"\" does not match the expected type.")
						error_flag = 1
						break
				else:
					error_expression = ""
					for word in self.pre_stack[self.cur_exp]:
						error_expression += word[1]
					self.error_list.append("Semantics ERROR:Expression \" "+error_expression+"\" does not match the expected type.")
					error_flag = 1
					break

		elif(exp_type=="BOOL_EXP"):
			for word in self.stack[self.cur_exp]:
				if(func_flag==1):
					if(word[1]==")"):
						func_flag = 0
						continue
					else:
						continue
				if(word[0]=="SYMBOL"):
					if(word[1] in self.cmpop or word[1] in ["+", "-", "*", "/", "%", "&&", "||" , "!"] or word[1] in ["[","]","(",")"]):
						pass
					elif(word[1] in self.symboltable.functionTable.keys()):
						if(self.symboltable.functionTable[word[1]]["return_type"][0]=='bool'):
							func_flag = 1
					else:
						error_expression = ""
						for word in self.pre_stack[self.cur_exp]:
							error_expression += word[1]
						self.error_list.append("Semantics ERROR:Expression \" "+error_expression+"\" does not match the expected type.")
						error_flag = 1
						break
				else:
					pass

		elif(exp_type=="NoRequest"):
			pass

		self.deltype_req()
		if(error_flag == 0):
			return exp_type
		else:
			return "ERROR_EXP"


	def Advance(self, x):
		now_type , now_word = self.tokenizer.word_table(self.tokenizer.word_iterator)[0],self.tokenizer.word_table(self.tokenizer.word_iterator)[1]
		self.pushstack((now_type,now_word))
		# for XML's syntax
		# if(now_word == ">"):
		# 	now_word = "&lt;"
		# elif(now_word == ">="):
		# 	now_word = "&lt;="
		# elif(now_word == "<"):
		# 	now_word = "&gt;"
		# elif(now_word == "<="):
		# 	now_word = "&gt;="
		# elif(now_word == "&"):
		# 	now_word = "&amp;"
		# elif(now_word == "&&"):
		# 	now_word = "&amp;&amp;"
		# elif(now_word == "\'"):
		# 	now_word = "&apos;"
		# elif(now_word == "\""):
		# 	now_word = "&quot;"
		# self.utility(x, "<{}>  {}  </{}>".format(now_type, now_word, now_type))
		self.tokenizer.advance()
		# self.utility(x, "\n")

	def CompileProgram(self,x = 0):
		# self.utility(x, "<program>\n")
		self.CompileGlobalDeclaration(x+1)
		next1 = self.tokenizer.LL1()
		while(next1 in self.ADtype or next1 in self.AStype or next1 == 'typedef'):
			self.CompileGlobalDeclaration(x+1)
			next1 = self.tokenizer.LL1()
		# E1
		if(self.tokenizer.word_iterator < self.tokenizer.output_length):
			pass
			# self.utility(x, "SyntaxERROR, it may have some words unrecognized")
		# self.utility(x, "</program>")

	def CompileGlobalDeclaration(self, x):
		# self.utility(x, "<globalDeclaration>\n")
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
				pass
				# self.utility(x, "SyntaxERROR, for jumping out uncommonly\n")
		else:   # E3
			pass
			# self.utility(x, "SyntaxERROR, unrecognizing token\n")
		# self.utility(x, "</globalDeclaration>\n")

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
				pass
				# self.utility(x, "SyntaxERROR, it should be an identifier\n")
		elif(next1 == "enum"):
			self.Advance(x)
			# varName
			nextt = self.tokenizer.LL1type()
			if(nextt == "IDENTIFIER"):
				thitype_2 = self.utility2()[1]
				self.Advance(x)
			else:
				pass
				# self.utility(x, "SyntaxERROR, it should be an identifier\n")
		else:  #E4
			pass
			# self.utility(x, "SyntaxERROR, for unrecognized token\n")
		if(thitype_2):
			thitype = (thitype_1, thitype_2)
		else:
			thitype = (thitype_1, )
		return thitype

# 3.28  添加符号表
	def CompileParameterList(self, x):
		# self.utility(x,"<parameterList>\n")
		paramslist = []
		self.func_params = []
		thisdict = dict()
		thistype = self.CompileType(x+1)  # type
		thisdict['type'] = thistype
		next1 = self.tokenizer.LL1()
		starnum = 0
		while(next1 == "*"):
			starnum = starnum + 1
			self.Advance(x+1)  # "*"
			next1 = self.tokenizer.LL1()
		thisdict['starnum'] = starnum
		next1 = self.tokenizer.LL1()
		self.func_params.append(next1)
		nextt = self.tokenizer.LL1type()
		if(nextt == "IDENTIFIER"):
			self.Advance(x+1)  # varName
		else:
			pass
			# self.utility(x, "SyntaxERROR, it should be an identifier\n")
		next1 = self.tokenizer.LL1()
		thisdict['isarray'] = False
		if(next1 == "["):
			thisdict['isarray'] = True
			weidu = []
			if(thisdict['starnum'] != 0):
				pass
				# self.utility(x, "SyntaxERROR, '*' and '['']' cannot use together\n")
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
							pass
							# self.utility(x, "SyntaxERROR, it should be a ']'\n")
					elif(next1 == "]"):
						self.Advance(x+1)  #']'
					else:
						pass
						# self.utility(x, "SyntaxERROR, unrecgonized token in parameterlist\n")
					if(thiweidu_2):
						thiweidu = (thiweidu_1, thiweidu_2)
					else:
						thiweidu = (thiweidu_1, )
					weidu.append(thiweidu)
					next1 = self.tokenizer.LL1()
			thisdict['weidu'] = weidu
		paramslist.append(thisdict)
		next1 = self.tokenizer.LL1()
		while(next1 == ","):
			self.Advance(x+1)  # ','

			thisdict = dict()
			thistype = self.CompileType(x + 1)  # type
			thisdict['type'] = thistype
			next1 = self.tokenizer.LL1()
			starnum = 0
			while (next1 == "*"):
				starnum = starnum + 1
				self.Advance(x + 1)  # "*"
				next1 = self.tokenizer.LL1()
			thisdict['starnum'] = starnum
			nextt = self.tokenizer.LL1type()
			if (nextt == "IDENTIFIER"):
				next1 = self.tokenizer.LL1()
				self.func_params.append(next1)
				self.Advance(x + 1)  # varName
			else:
				pass
				# self.utility(x, "SyntaxERROR, it should be an identifier\n")
			next1 = self.tokenizer.LL1()
			if (next1 == "["):
				thisdict['isarray'] = starnum
				weidu = []
				if (thisdict['starnum'] != 0):
					pass
					# self.utility(x, "SyntaxERROR, '*' and '['']' cannot use together\n")
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
							self.Advance(x + 1)  # ']'
						elif (next1 == "]"):
							self.Advance(x + 1)  # ']'
						else:
							pass
							# self.utility(x, "SyntaxERROR, unrecgonized token in parameterlist\n")
						if (thiweidu_2):
							thiweidu = (thiweidu_1, thiweidu_2)
						else:
							thiweidu = (thiweidu_1,)
						weidu.append(thiweidu)
						next1 = self.tokenizer.LL1()
				thisdict['weidu'] = weidu
			paramslist.append(thisdict)
			next1 = self.tokenizer.LL1()
		# self.utility(x,"</parameterList>\n")
		return paramslist

# 3.26  添加符号表
	def CompileEnumDecl(self, x):
		# self.utility(x,"<enumDecl>\n")
		self.Advance(x+1)  # "enum"
		nextt = self.tokenizer.LL1type()
		# variable name
		vname = self.utility2()[1]
		if(nextt != "IDENTIFIER"):
			pass
			# self.utility(x+1, "SyntaxERROR: It should be an identifier\n")
		elif(self.symboltable.lookup(vname, 5)):
			# look up symboltable
			pass
			# self.utility(x+1, "SemanticsERROR: Redefine variable: {}\n".format(vname))
		else:
			self.Advance(x + 1)  # varName
			next1 = self.tokenizer.LL1()
			if (next1 != "{"):
				pass
				# self.utility(x+1, "SyntaxERROR: It should be '{'\n")
			self.Advance(x+1)  # '{'
			vdict = dict()
			nextt = self.tokenizer.LL1type()
			va = self.utility2()[1]
			if (nextt != "IDENTIFIER"):
				pass
				# self.utility(x + 1, "SyntaxERROR: It should be an identifier\n")
			self.Advance(x+1)  # varName
			next1 = self.tokenizer.LL1()
			pt = 0
			if (next1 == "="):
				self.Advance(x + 1)  # "="
				nextt = self.tokenizer.LL1type()
				if(nextt != "INT_CONST"):
					pass
					# self.utility(x + 1, "SyntaxERROR: It should be an integer\n")
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
					pass
					# self.utility(x + 1, "SyntaxERROR: It should be an identifier\n")
				self.Advance(x+1)  # varName
				next1 = self.tokenizer.LL1()
				if(next1 == "="):
					self.Advance(x + 1)  # "="
					nextt = self.tokenizer.LL1type()
					if (nextt != "INT_CONST"):
						pass
						# self.utility(x + 1, "SyntaxERROR: It should be an integer\n")
					vv = self.utility2()[1]
					pt = vv
					self.Advance(x + 1)  # num
				else:
					vv = pt
					pt = pt + 1
				vdict[va] = vv
				next1 = self.tokenizer.LL1()
			# insert to symboltable
			self.symboltable.insert(vname, vdict)
			next1 = self.tokenizer.LL1()
			if(next1 != "}"):
				pass
				# self.utility(x + 1, "SyntaxERROR: It should be an '}'\n")
			self.Advance(x+1)  # '}'
			next1 = self.tokenizer.LL1()
			if(next1 != ";"):
				pass
				# self.utility(x + 1, "SyntaxERROR: It should be an ';'\n")
			self.Advance(x+1)  # ';'
		# self.utility(x,"</EnumDecl>\n")

# 3.28  添加符号表
	def CompileStructDecl(self, x):
		# self.utility(x,"<structDecl>\n")
		next1 = self.tokenizer.LL1()
		content = list()
		thicontent = dict()
		if(next1 == "struct"):
			self.Advance(x+1)  #"struct"
		else:
			pass
			# self.utility(x+1, "SyntaxERROR: It should be 'struct'\n")
		nextt = self.tokenizer.LL1type()
		if(nextt == "IDENTIFIER"):
			structname = self.utility2()[1]
			if(self.symboltable.lookup(structname, 4)):
				pass
				# self.utility(x + 1, "SemanticsERROR: Redefine struct variable: {}\n".format(structname))
			self.Advance(x+1)  #varName
		else:
			pass
			# self.utility(x+1, "SyntaxERROR: It should be an identifier\n")
		next1 = self.tokenizer.LL1()
		if(next1 == "{"):
			self.Advance(x+1)  #"{"
		else:
			pass
			# self.utility(x+1, "SyntaxERROR: It should be a '{'\n")
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
			pass
			# self.utility(x+1, "SyntaxERROR: It should be a '}'\n")
		if(next1 == ";"):
			self.Advance(x+1)  #";"
		else:
			pass
			# self.utility(x+1, "SyntaxERROR: It should be a ';'\n")
		self.symboltable.insert(structname, content, 4)
		# self.utility(x,"</structDecl>\n")

# 3.28  添加符号表
	def CompileFunctionDecl(self, x):
		# self.utility(x,"<FunctionDecl>\n")
		content = dict()
		content['return_type'] = self.CompileType(x+1)  # type
		#print(content['return_type'])
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
			self.Advance(x+1)  #routineName
		else:
			pass
			# self.utility(x, "SyntaxERROR, it should be an identifier\n")
		next1 = self.tokenizer.LL1()
		if(next1 == '('):
			self.Advance(x+1)  # "("
		else:
			pass
			# self.utility(x, "SyntaxERROR, it should be '('\n")
		next1 = self.tokenizer.LL1()
		if(next1 in self.ADtype or next1 in self.AStype):
			content['paramslist'] = self.CompileParameterList(x+1)
			self.Advance(x+1)  # ")"
		elif(next1 == ")"):
			self.Advance(x+1)  # ")"
		else:
			pass
			# self.utility(x, "SyntaxERROR, unrecognizing token in functiondecl\n")
		next1 = self.tokenizer.LL1()
		content['isused'] = False
		# 仅函数声明
		if(next1 == ";"):
			self.Advance(x+1)  # ";"
			if(self.symboltable.lookup(function_name, 1)):
				pass
				# self.utility(x+1, "SemanticsERROR: Redefine function: {}\n".format(function_name))
			else:
				self.symboltable.insert(function_name, content, 1)
			# exit 1

		elif(next1 == "{"):
			self.func_params_type = []
			self.func_type = content['return_type'][0]
			#self.func_params = content['']
			original_content = self.symboltable.lookup(function_name, 1)
			if(function_name in self.symboltable.functionTable.keys()):
				if('paramslist' in self.symboltable.functionTable[function_name]):
					#print(symboltable.functionTable[function_name]['paramslist'])
					i = 0
					for param in self.symboltable.functionTable[function_name]['paramslist']:
						self.func_params_type.append((self.func_params[i],param['type'][0]))
						i += 1
					# print(self.func_params_type)
			if(not original_content):
				content['isused'] = True
				self.symboltable.insert(function_name, content, 1)
				self.CompileBodyDecl(x + 1)
			elif(not original_content['isused']):
				# DEBUG
				# 与之前的content比较, 语义分析
				if(content == original_content):
					self.symboltable.update(1, function_name, 3, True)
					self.CompileBodyDecl(x+1)
				else:
					pass
					# self.utility(x+1, "SemanticsERROR: The definition of function: {} is not matched correctly\n".format(function_name))
			else:
				pass
				# self.utility(x+1, "SemanticsERROR: Redefine function: {}\n".format(function_name))
			# exit 2
		else:
			pass
			# self.utility(x, "SyntaxERROR, unrecognizing token in functiondecl\n")
		# self.utility(x,"</FunctionDecl>\n")

#utype == 1 全局变量
#utype == 2 局部变量
#utype == 3 结构变量 返回值 list()
	def CompileVariableDecl(self, x, utype):
		# self.utility(x,"<variableDecl>\n")
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
			if(self.symboltable.lookup_variable(findvname = thivaria['vname'], ftype = 1)):
				pass
				# self.utility(x, "SemanticsERROR, Redifining the variable: {}\n".format(thivaria['vname']))
			#else: insert

			self.Advance(x+1)  # varName
		else:
			pass
			# self.utility(x, "SyntaxERROR, it should be an identifier\n")
		next1 = self.tokenizer.LL1()

		thivaria['isarray'] = False
		if (next1 == "["):
			thivaria['isarray'] = True
			weidu = []
			if (thivaria['starnum'] != 0):
				pass
				# self.utility(x, "SyntaxERROR, '*' and '['']' cannot use in the same variable\n")
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
							pass
							# self.utility(x, "SyntaxERROR, it should be a ']'\n")
					else:
						pass
						# self.utility(x, "SyntaxERROR, unrecgonized token in parameterlist\n")
					if (thiweidu_2):
						thiweidu = (thiweidu_1, thiweidu_2)
					else:
						thiweidu = (thiweidu_1,)
					weidu.append(thiweidu)
					next1 = self.tokenizer.LL1()
			thivaria['weidu'] = weidu
		if (utype == 1 or utype == 2):
			self.symboltable.variableStack.append(thivaria)
			self.symboltable.variableStackIterator = self.symboltable.variableStackIterator + 1
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
				if (self.symboltable.lookup_variable(findvname=thivariab['vname'], ftype=1)):
					pass
					# self.utility(x, "SemanticsERROR, Redifining the variable: {}\n".format(thivariab['vname']))
				# else: insert

				self.Advance(x + 1)  # varName
			else:
				pass
				# self.utility(x, "SyntaxERROR, it should be an identifier\n")
			next1 = self.tokenizer.LL1()

			thivariab['isarray'] = False
			if (next1 == "["):
				thivariab['isarray'] = True
				weidu = []
				if (thivariab['starnum'] != 0):
					pass
					# self.utility(x, "SyntaxERROR, '*' and '['']' cannot use in the same variable\n")
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
								pass
								# self.utility(x, "SyntaxERROR, it should be a ']'\n")
						else:
							pass
							# self.utility(x, "SyntaxERROR, unrecgonized token in parameterlist\n")
						if (thiweidu_2):
							thiweidu = (thiweidu_1, thiweidu_2)
						else:
							thiweidu = (thiweidu_1,)
						weidu.append(thiweidu)
						next1 = self.tokenizer.LL1()
				thivariab['weidu'] = weidu
			if (utype == 1 or utype == 2):
				self.symboltable.variableStack.append(thivariab)
				self.symboltable.variableStackIterator = self.symboltable.variableStackIterator + 1
			elif (utype == 3):
				structlist.append(thivariab)
			next1 = self.tokenizer.LL1()

		if(next1 == ";"):
			self.Advance(x+1)  #";"
		else:
			pass
			# self.utility(x, "SyntaxERROR, it should be a ';'\n")
		# self.utility(x,"</variableDecl>\n")
		if(utype == 3):
			return structlist

	def CompileBodyDecl(self, x):
		# self.utility(x,"<bodyDecl>\n")
		next1 = self.tokenizer.LL1()
		if(next1 == "{"):
			self.Advance(x+1)  #'{'
		else:
			pass
			# self.utility(x, "SyntaxERROR, it should be a '{'\n")

		# 符号表维护
		self.symboltable.variableStackPointer.append(self.symboltable.variableStackIterator)
		self.symboltable.variableStackPointerIterator = self.symboltable.variableStackPointerIterator + 1

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
			pass
			# self.utility(x, "SyntaxERROR, it should be a '}'\n")

		# print(symboltable.variableStack)
		# for word in symboltable.variableStack:
		# 	print(word)

		# 符号表维护
		ii = self.symboltable.variableStackPointer[self.symboltable.variableStackPointerIterator-1]
		eend = len(self.symboltable.variableStack)
		# print("{}: {}".format(ii, eend))
		while(ii != eend):
			self.symboltable.variableStack.pop()
			self.symboltable.variableStackIterator = self.symboltable.variableStackIterator - 1
			eend = eend - 1
			# print("{}: {}".format(ii, eend))
		self.symboltable.variableStackPointer.pop()
		self.symboltable.variableStackPointerIterator = self.symboltable.variableStackPointerIterator - 1
		# self.utility(x, "</bodyDecl>\n")

	def CompileStatement(self, x):
		# self.utility(x, "<statements>\n")
		next1 = self.tokenizer.LL1()
		nextt = self.tokenizer.LL1type()
		if(next1 == "if"):
			self.CompileIf(x+1)
		elif(next1 == "while" or next1 == "do"):
			self.CompileWhile(x+1)
		elif(next1 == "for"):
			self.CompileFor(x+1)
		elif(next1 == "return"):
			self.CompileReturn(x+1)
		elif(next1 == "{"):
			self.CompileBlock(x+1)
		elif(next1 == "goto"):
			self.CompileGoto(x+1)
		elif(next1 == "++" or next1 == "--"):
			self.CompileLet(x + 1)
		elif(next1 in ["break", "continue"]):
			self.Advance(x+1)
			next1 = self.tokenizer.LL1()
			self.Advance(x+1)
			if(next1 != ";"):
				pass
				# self.utility(x, "SyntaxERROR, it should be ';'\n")
		else:
			next2 = self.tokenizer.LL(2)
			if(next2 in [".", "->"]):  # for struct
				next2 = self.tokenizer.LL(4)
			if(next2 == ":"):
				self.CompileLabel(x+1)
				next1 = self.tokenizer.LL1()
				self.Advance(x+1)
				if(next1 != ":"):
					pass
					# self.utility(x, "SyntaxERROR, it should be ':'\n")
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

		# self.utility(x, "</statements>\n")

	def CompileLabel(self, x):
		# self.utility(x, "<labelStatement>\n")
		self.Advance(x+1)  #':'
		self.CompileStatement(x+1)
		# self.utility(x, "</labelStatement>\n")

	#check in PM,3.22
	def CompileLet(self, x):
		# self.utility(x, "<letStatement>\n")
		next1 = self.tokenizer.LL1()
		if(self.tokenizer.word_table(self.tokenizer.word_iterator)[0]=='IDENTIFIER'):
			ID_type = self.lookup_type(self.tokenizer.word_table(self.tokenizer.word_iterator)[1])
			ID_name = self.tokenizer.word_table(self.tokenizer.word_iterator)[1]
		if(next1 in ["++",  "--"]):
			self.Advance(x+1)  # "++", "--"
			self.CompilevarName(x+1)  # varName
		else:
			while(next1 == "*"):
				self.Advance(x+1)
				next1 = self.tokenizer.LL1()
			self.CompilevarName(x + 1)  # varName
			next1 = self.tokenizer.LL1()
			if(next1 in ["++", "--"]):
				self.Advance(x+1)
			else:
				while (next1 == "["):
					self.Advance(x + 1)  # '['
					self.pushtype_req("INT_EXP")
					self.CompileExpression(x + 1)
					next1 = self.tokenizer.LL1()
					self.Advance(x + 1)  # ']'
					if(next1 != "]"):
						pass
						# self.utility(x+1, "SyntaxERROR, it should be ']'\n")
					next1 = self.tokenizer.LL1()
				self.Advance(x+1)  # '='
				if(next1 != '='):
					pass
					# self.utility(x+1, "SyntaxERROR, it should be '='\n")
				if(ID_type == "int"):
					self.pushtype_req("INT_EXP")
				elif(ID_type == "float"):
					self.pushtype_req("FLOAT_EXP")
				elif(ID_type == "char"):
					self.pushtype_req("CHAR_EXP")
				elif(ID_type == "string"):
					self.pushtype_req("STRING_EXP")
				elif(ID_type == "bool"):
					self.pushtype_req("BOOL_EXP")
				else:
					print("ID " + ID_name + " does not exist!")
					# time.sleep(1000)
					sys.exit(0)
				self.CompileExpression(x+1)
		next1 = self.tokenizer.LL1()
		if(next1 == ";" or next1 == ")"):
			self.Advance(x+1)  # ';' or ')'
		elif(next1 == ","):
			pass
		else:
			pass
			# self.utility(x+1, "SyntaxERROR, it should be ';' or ')' or ','\n")
		# self.utility(x, "</letStatement>\n")

	def CompileIf(self, x):
		# self.utility(x, "<ifStatement>\n")
		self.pushtype_req("BOOL_EXP")
		self.Advance(x+1)  #'if'
		self.Advance(x+1)  # '('
		self.CompileExpression(x+1)
		self.Advance(x+1)  # ')'
		self.Advance(x+1)  # '{'
		next1 = self.tokenizer.LL1()
		while (next1 != "}"):
			self.CompileStatement(x + 1)
			next1 = self.tokenizer.LL1()
		self.Advance(x+1)  # '}'
		next1 = self.tokenizer.LL1()
		if(next1 == "else"):
			self.Advance(x+1)  # "else"
			self.Advance(x+1)  # '{'
			next1 = self.tokenizer.LL1()
			while(next1 != "}"):
				self.CompileStatement(x+1)
				next1 = self.tokenizer.LL1()
			self.Advance(x+1)  # '}'
		# self.utility(x, "</ifStatement>\n")

	def CompileWhile(self, x):
		# self.utility(x, "<whileStatement>\n")
		next1 = self.tokenizer.LL1()
		if(next1 == 'while'):
			self.pushtype_req("BOOL_EXP")
			self.Advance(x+1)  # 'while'
			self.Advance(x+1)  # '('
			self.CompileExpression(x+1)
			self.Advance(x+1)  # ')'
			self.Advance(x+1)  # '{'
			next1 = self.tokenizer.LL1()
			while(next1 != "}"):
				self.CompileStatement(x+1)
				next1 = self.tokenizer.LL1()
			self.Advance(x+1)  # '}'
		elif(next1 == 'do'):
			self.Advance(x+1)  # 'do'
			self.Advance(x+1)  # '{'
			next1 = self.tokenizer.LL1()
			while(next1 != "}"):
				self.CompileStatement(x+1)
				next1 = self.tokenizer.LL1()
			self.Advance(x+1)  # '{'
			self.Advance(x+1)  # 'while'
			self.Advance(x+1)  # '('
			self.pushtype_req("BOOL_EXP")
			self.CompileExpression(x+1)
			self.Advance(x+1)  # ')'
			self.Advance(x+1)  # ';'
		# self.utility(x, "</whileStatement>\n")

	def CompileReturn(self, x):
		# self.utility(x, "<returnStatement>\n")
		self.Advance(x+1)  #'return'
		next1 = self.tokenizer.LL1()
		if(next1 != ";"):
			#检测return类型是否匹配函数类型
			if(self.func_type == "int"):
				self.pushtype_req("INT_EXP")
			elif(self.func_type == "float"):
				self.pushtype_req("FLOAT_EXP")
			elif(self.func_type == "char"):
				self.pushtype_req("CHAR_EXP")
			elif(self.func_type == "string"):
				self.pushtype_req("STRING_EXP")
			elif(self.func_type == "bool"):
				self.pushtype_req("BOOL_EXP")
			else:
				print("Return type does not exist!")
				# time.sleep(5)
				sys.exit(0)
			self.CompileExpression(x+1)
		self.Advance(x+1)  # ';'
		# self.utility(x, "</returnStatement>\n")
	# 估计有bug
	def CompileFor(self, x):
		# self.utility(x, "<forStatement>\n")
		next1 = self.tokenizer.LL1()
		self.Advance(x+1)  #'for'
		next1 = self.tokenizer.LL1()
		self.Advance(x+1)  #'('
		if(next1 != "("):
			pass
			# self.utility(x+1, "SyntaxERROR, it should be '('\n")

		nextt = self.tokenizer.LL1type()
		next1 = self.tokenizer.LL1()

		for i in range(2):
			if(nextt == "INT_CONST" or nextt == "FLOAT_CONST" or nextt == "CHAR_CONST" or nextt == "STRING_CONST" or nextt == "BOOL_CONST" or nextt == "IDENTIFIER"
			or next1 == ["(" ,"-",'+','!','++','--']):
				if(i == 0):
					self.CompileStatement(x+1)
				elif(i == 1):
					self.pushtype_req("BOOL_EXP")
					self.CompileExpression(x+1)
					self.Advance(x+1)  #';'
				nextt = self.tokenizer.LL1type()
				next1 = self.tokenizer.LL1()
			elif(next1 == ";"):
				self.Advance(x+1)  #';'
				nextt = self.tokenizer.LL1type()
				next1 = self.tokenizer.LL1()
			else:
				pass
				# self.utility(x,"ERROR\n")

		nextt = self.tokenizer.LL1type()
		next1 = self.tokenizer.LL1()
		if (nextt == "INT_CONST" or nextt == "FLOAT_CONST" or nextt == "CHAR_CONST" or nextt == "STRING_CONST" or nextt == "BOOL_CONST" or nextt == "IDENTIFIER"
			or next1 in ["(", "-", '+', '!', '++', '--']):
			self.CompileStatement(x + 1)
		elif(next1 == ")"):
			self.Advance(x+1)  #')'
		else:
			pass
			# self.utility(x,"ERROR\n")
		next1 = self.tokenizer.LL1()
		if(next1 == "{"):
			self.Advance(x+1)  # '{'
		else:
			pass
			# self.utility(x,"ERROR\n")
		next1 = self.tokenizer.LL1()
		while (next1 != "}"):
			self.CompileStatement(x + 1)
			next1 = self.tokenizer.LL1()
		if(next1 == "}"):
			self.Advance(x+1)  # '}'
		else:
			pass
			# self.utility(x,"ERROR\n")
		# self.utility(x,"</forStatement>\n")
	#check PM, 3.22
	def CompileDo(self, x):
		# self.utility(x,"<doStatement>\n")
		self.CompileRoutineCall(x+1)
		next1 = self.tokenizer.LL1()
		if(next1 == ";"):
			self.Advance(x+1)
		else:
			pass
			# self.utility(x+1,"SyntaxERROR,it shoule be a ';'\n")
		# self.utility(x,"</doStatement>\n")

	def CompileBlock(self, x):
		# self.utility(x,"<blockStatement>\n")
		next1 = self.tokenizer.LL1()
		if(next1 == "{"):
			self.Advance(x+1)  #' {'
		else:
			pass
			# self.utility(x,"ERROR\n")
		self.CompileBodyDecl(x+1)
		next1 = self.tokenizer.LL1()
		if(next1 == "}"):
			self.Advance(x+1)  #  '}'
		else:
			pass
			# self.utility(x,"ERROR\n")
		# self.utility(x,"</blockStatement>\n")
	

	def CompileGoto(self, x):
		# self.utility(x,"<gotoStatement>\n")
		self.Advance(x+1)  # 'goto'
		self.Advance(x+1)  # label
		self.Advance(x+1)  # ';'
		# self.utility(x,"</gotoStatement>\n")


#EXPRESSION
	def CompileExpression(self, x):
		if(self.cur_exp==0):
			self.stack = []
			self.pre_stack = []
		self.cur_exp += 1
		self.stack = self.stack +[[]]
		self.pre_stack = self.pre_stack + [[]]

		# self.utility(x,"<expression>\n")
		self.CompileTerm(x+1)
		next1 = self.tokenizer.LL1()
		while(True):
			if(next1 in self.arithop or next1 in self.cmpop):
				self.Advance(x+1)  # op
				self.CompileTerm(x+1)
				next1 = self.tokenizer.LL1()
			elif(next1 in ["]",",",";", ")"]):
				break
			else:
				# self.utility(x,"ERROR")
				break
		# self.utility(x,"</expression>\n")
		self.cur_exp -= 1
		#print(self.stack[self.cur_exp])
		exp_type = self.checktype_req()
		if(self.cur_exp!=0):
			length = len(self.stack[self.cur_exp])
			for i in range(0,length):
				self.stack[self.cur_exp-1].pop()
			self.stack[self.cur_exp-1].append((exp_type,"EXP"))
		self.stack.pop()
		self.pre_stack.pop()
		#print(self.type_req)
	#The most complex part
	# check PM,3.22
	def CompileTerm(self, x):
		# self.utility(x,"<term>\n")
		# look ahead 1 character.
		nextt = self.tokenizer.LL1type()
		next1 = self.tokenizer.LL1()
		if(nextt == "INT_CONST"):       #  -> INT_CONST
			self.Advance(x + 1)
		elif(nextt == "FLOAT_CONST"):   #  -> FLOAT_CONST
			self.Advance(x + 1)
		elif(nextt == "CHAR_CONST"):    #  -> CHAR_CONST
			self.Advance(x + 1)
		elif(nextt == "STRING_CONST"):  #  -> STRING_CONST
			self.Advance(x + 1)
		elif(nextt == "BOOL_CONST"):    #  -> BOOL_CONST
			self.Advance(x + 1)
		elif(next1 == "("):             #  -> '(' expression ')'
			self.Advance(x + 1)  # "("
			self.pushtype_req(self.gettype_req())
			self.CompileExpression(x+1)
			next1 = self.tokenizer.LL1()
			if(next1 == ")"):
				self.Advance(x + 1)  # ")"
			else:
				pass
				# self.utility(x+1, "SyntaxError,it should be a ')'\n")
		elif(next1 in ["-","+","!", "&","*"]):   #  -> leftunaryOp term
			self.Advance(x + 1)
			self.CompileTerm(x + 1)
		elif(next1 in ["++", "--"]):    #  -> leftunaryOp term
			self.Advance(x + 1)
			self.CompilevarName(x+1)
		elif(nextt == "IDENTIFIER"):
			# self.CompilevarName(x + 1)
			next1 = self.tokenizer.LL(2)
			if(next1 in ["++","--"]):   #  -> varName "++" or "--"
				self.CompilevarName(x + 1)
				self.Advance(x+1)
			elif(next1 == "["):         #  -> varName {'[' expression ']'}+
				self.CompilevarName(x + 1)
				next1 = self.tokenizer.LL1()
				while(next1 == "["):
					self.Advance(x+1)  # '['
					self.pushtype_req("INT_EXP")
					self.CompileExpression(x+1)
					self.Advance(x+1)  # ']'
					next1 = self.tokenizer.LL1()
			elif(next1 == "("):         #  -> RoutineCall
				self.CompileRoutineCall(x+1)
										#  -> varName
			elif(next1 in self.arithop or next1 in self.cmpop or next1 in [";", ")", ",", "]"]):
				self.CompilevarName(x + 1)
				pass
			else:  #报错
				self.Advance(x + 1)
				# self.utility(x+1, "SyntaxError,Unregonize word in Term: {}\n".format(next1))
		# self.utility(x,"</term>\n")
	#create in PM,3.22
	def CompilevarName(self, x):
		next1 = self.tokenizer.LL1()
		nextt = self.tokenizer.LL1type()
		flag = True
		if(nextt == "IDENTIFIER"):
			self.Advance(x+1)
			next1 = self.tokenizer.LL1()
			if(next1 in [".","->"]):
				self.Advance(x + 1)
				nextt = self.tokenizer.LL1type()
				if(nextt == "IDENTIFIER"):
					self.Advance(x + 1)  #success!
				else:
					flag = False
		else:
			flag = False
		if(not flag):
			pass
			# self.utility(x+1, "SyntaxERROR, cann't identify the identifier: {}\n".format(next1))

	def CompileExpressionList(self, x):
		# self.utility(x,"<expressionList>\n")
		next1 = self.tokenizer.LL1()
		if(next1 != ")"):
			if(self.external_varia_flag==1):
				self.pushtype_req("NoRequest")
			self.CompileExpression(x+1)
			next1 = self.tokenizer.LL1()
			while(True):
				if(next1 == ','):
					self.Advance(x+1)  #","
				elif(next1 == ")"):
					break
				else:
					pass
					# self.utility(x,"ERROR")
				if(self.external_varia_flag==1):
					self.pushtype_req("NoRequest")
				self.CompileExpression(x+1)
				next1 = self.tokenizer.LL1()
		# self.utility(x,"</expressionList>\n")
	# check PM,3.22
	def CompileRoutineCall(self, x):
		self.external_varia_flag = 0
		# self.utility(x,"<routineCall>\n")
		self.CompilevarName(x+1)  # '函数名'
		return_type = []
		func_name = self.tokenizer.word_table(self.tokenizer.word_iterator-1)[1]
		if(func_name in self.external_library):
			self.external_varia_flag = 1
			return_type = []
		else:
			func_info = self.symboltable.functionTable.get(func_name)
			try:
				return_type_list = func_info['paramslist']
				params_num = len(return_type_list)
				return_type = []
				for word in return_type_list:
					return_type.append(word["type"][0])
			except:
				pass
		# print(func_name)
		# print(symboltable.functionTable)
		next1 = self.tokenizer.LL1()
		if(next1 == '('):
			self.Advance(x+1)  # '('
		else:
			pass
			# self.utility(x,"SyntaxError,it should be a '('\n")
		for param_type in return_type:
			if(param_type == "int"):
				self.pushtype_req("INT_EXP")
			elif(param_type == "float"):
				self.pushtype_req("FLOAT_EXP")
			elif(param_type == "char"):
				self.pushtype_req("CHAR_EXP")
			elif(param_type == "string"):
				self.pushtype_req("STRING_EXP")
			elif(param_type == "bool"):
				self.pushtype_req("BOOL_EXP")
		self.CompileExpressionList(x+1)
		next1 = self.tokenizer.LL1()
		if(next1 == ')'):
			self.Advance(x+1)  # ')'
		else:
			pass
			# self.utility(x,"SyntaxError,it should be a ')'\n")
		next1 = self.tokenizer.LL1()
		# self.utility(x,"</routineCall>\n")

	def CompileThreecase(self, x):
		# self.utility(x,"<threecase>\n")
		next1 = self.tokenizer.LL1()
		while(next1 in self.arithop or next1 in self.cmpop):
			self.Advance(x+1)  # op
			self.CompileTerm(x+1)
			next1 = self.tokenizer.LL1()
		if(next1 == '?'):
			self.Advance(x+1)  # '?'
		else:
			pass
			# self.utility(x, "SyntaxError,it should be a '?'\n")
		self.CompileExpression(x+1)
		if(next1 == ':'):
			self.Advance(x+1)  # ':'
		else:
			pass
			# self.utility(x, "SyntaxError,it should be a ':'\n")
		self.CompileExpression(x+1)
		# self.utility(x,"</threecase>\n")

	def main(self):
		self.CompileProgram()
		length = len(self.error_list)
		if(length > 0):
			for error in self.error_list:
				print(error)
		else:
			print("No Semantics ERROR")

if __name__ == '__main__':
	# os.chdir(r"C:\Users\Administrator\Desktop\C Compiler\Ccompiler-master\Ccompiler-master\test")
	file = sys.argv[1]

	obj = C_Lexer(file)
	obj.preScanner()
	obj.preAnalyzer()
	obj.analyzer()

	parser = SemanticsParser(obj)
	parser.main()
	parser.__del__()

	# time.sleep(1000)
# goto1: SyntaxERROR
#
# goto2: SemanticsERROR
