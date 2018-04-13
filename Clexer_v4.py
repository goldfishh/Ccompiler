import re
import os
import time

class C_Lexer:
	def __init__(self,file):
		# PreScanner variable quantity
		self.change_table = []
		self.contents_pre = ""
		self.contents_fur = ""
		# Read file
		self.fr = open(file,"r", encoding = "utf-8")
		self.contents = self.fr.read()
		self.fname = file
		# Output file
		self.output=[]
		self.file_output = re.sub(r'\.c',"T.txt",file)
		self.output_length = 0
		# Create identifer table([Token,Hash,Name,Tyle,Class,Value,BType,BClass,BValue, IdSize])
		self.identifer_table=[]
		# Remove annotation
		self.contents = re.sub(r'\/\/[^\n]*',"",self.contents)
		self.contents = re.sub(r'\/\*[\d\D]*?\*\/',"",self.contents)
		# Remove macro definition(nonsupport)
		self.contents = re.sub(r'\#include[^\n]*',"",self.contents)
		self.contents = re.sub(r'\#endif[^\n]*',"",self.contents)
		self.contents = re.sub(r'\#ifndef[^\n]*',"",self.contents)
		self.contents = re.sub(r'\#ifdef[^\n]*',"",self.contents)
		# Get content length
		self.length = len(self.contents)

		# Symbol table
		self.symbol_table = ["{","}","(",")","[","]",
							".","->",",",";",
							"+","-","*","/","\\","%","<<",">>","&",
							"|","~","^",
							"!","&&","||","++","--","?",":",
							"=","*=","/=","%=","+=","-=","<<=",">>=","&=","^=","|=",
							"==","!=",">","<",">=","<=",
							"\"","\'","#"]
		self.single_symbol = ["{","}","(",")","[","]",
							".","->",",",";",
							"+","-","*","/","\\","%","&",
							"|","~","^",
							"!","?",":",
							"=",
							">","<",
							"\"","\'","#"] 
		#Keywords table
		self.keywords_table = ["auto","register","union","volatile",
								"double","int","long","char","struct","float","short","unsigned","signed","void","enum",
								"if","else","for","continue","break","while","switch","case","default",
								"extern","static","const",
								"goto","do","return",
								"sizeof",
								"typedef",
								]
		#Alpha indicator
		self.fp=0

		#Variable quantity for grammar analyzer
		self.word_iterator = 0

	#Alpha
	def IsAlpha(self,c):
		if(((c<='z')and(c>='a'))or((c<='Z')and(c>='A'))):
			return 1
		else:
			return 0

	#Number
	def IsNum(self,c):
		if((c>='0')and(c<='9')):
			return 1
		else:
			return 0

	#Decimal
	def IsDecimal(self,c):
		if(c=='.'):
			return 1
		else:
			return 0

	#Keywords
	def IsKeywords(self,word):
		for Keyword in self.keywords_table:
			if(word==Keyword):
				return 1
		return 0

	#SingleSymbol
	def IsSingleSymbol(self,c):
		for Symbol in self.single_symbol:
			if(c==Symbol):
				return 1
		return 0

	#QuickSort
	def quickSort(self,low,high):
		if(low>=high):
			return
		first = low
		last = high
		key = self.change_table[first][2]
		key_val = self.change_table[first]

		while(first < last):
			while(first < last and self.change_table[last][2] >= key):
				last -= 1
			self.change_table[first] = self.change_table[last]
			while(first < last and self.change_table[last][2] <= key):
				first += 1
			self.change_table[last] = self.change_table[first]
		self.change_table[first] = key_val
		self.quickSort(low,first-1)
		self.quickSort(first+1,high)

	#PreScanner
	# 主要建 self.change_table
	# 并做简单的冲突处理
	def preScanner(self):
		flag = 1
		searchplace = self.contents
		prelength = 0
		##define
		while(flag==1):
			try:
				length_searchplace = len(searchplace)
				cut = re.search(r'#define (.*) (.*)',searchplace).span(0)
				searchOBJ = re.search(r'#define (.*) (.*)',searchplace,re.M|re.I)
				id1 = searchOBJ.group(1)
				id2 = searchOBJ.group(2)

				if(id1!=id2):
					self.change_table = self.change_table + [[id1,id2,cut[1]+prelength,self.length]]
				else:
					print("ERROR:PreDef error")
				searchplace = searchplace[cut[1]:length_searchplace]
				prelength = prelength + cut[1]
			except:
				flag = 0

		flag = 1
		searchplace = self.contents
		prelength = 0
		#typedef
		while(flag==1):
			try:
				length_searchplace = len(searchplace)
				cut = re.search(r'typedef (.*) (.*);',searchplace).span(0)
				searchOBJ = re.search(r'typedef (.*) (.*);',searchplace,re.M|re.I)
				id1 = searchOBJ.group(1)
				id2 = searchOBJ.group(2)	

				if(id1!=id2):
					self.change_table = self.change_table + [[id2,id1,cut[1]+prelength,self.length]]
				else:
					print("ERROR:PreDef error")
				searchplace = searchplace[cut[1]:length_searchplace]
				prelength = prelength + cut[1]
			except:
				flag = 0

		flag = 1
		searchplace = self.contents
		prelength = 0
		#enum
		while(flag==1):
			try:
				length_searchplace = len(searchplace)
				cut = re.search(r'enum(.*){(.*)};',searchplace).span(0)
				searchOBJ = re.search(r'enum(.*){(.*)};',searchplace,re.M|re.I)
				name = searchOBJ.group(1)
				terms = searchOBJ.group(2)

				terms = terms +",}"
				flag_terms = 1
				id1 = ""
				id2 = ""
				id2_val = "1"
				i= 0
				while(terms[i]!="}"):
					if(terms[i]!="," and terms[i]!="="):
						if(flag_terms==1):
							id1 += terms[i]
						else:
							id2 += terms[i]
					elif(terms[i]=="="):
						flag_terms = 2
					elif(terms[i]==","):
						flag_terms = 1
						if(id2!=""):
							id2_val = str(int(id2) + 1)
							self.change_table = self.change_table + [[id1,id2,cut[1]+prelength,self.length]]
						else:
							self.change_table = self.change_table + [[id1,id2_val,cut[1]+prelength,self.length]]
							id2_val = str(int(id2_val) + 1)
						id1 = ""
						id2 = ""
					i += 1
				searchplace = searchplace[cut[1]:length_searchplace]
				prelength = prelength + cut[1]
			except:
				flag = 0
		#fast sort to sort the change_table
		change_table_length = len(self.change_table)
		self.quickSort(0,change_table_length-1)

		for i in range(0,change_table_length-1):
			for j in range(change_table_length-1,i,-1):
				if(self.change_table[i][0]==self.change_table[j][0]):
					self.change_table[i][3] = self.change_table[j][2]
				if(self.change_table[i][0]==self.change_table[j][1]):
					self.change_table[j][1] = self.change_table[i][1]

	#Changer
	def changer(self):
		#Preparation
		ch = self.contents[self.fp]
		length_change_table = len(self.change_table)

		#Identifier or Reserved words
		if(self.IsAlpha(ch)==1):
			st_pos = self.fp
			word = ""
			word = word + ch
			self.fp += 1
			ch = self.contents[self.fp]

			while(self.IsNum(ch)==1 or self.IsAlpha(ch)==1 or ch=="_"):
				word = word + ch
				self.fp += 1
				ch = self.contents[self.fp]

			ed_pos = self.fp

			if(self.IsKeywords(word)==2):
				pass
			else:
				if(self.IsKeywords(word)==1):
					pass
				else:
					for term in self.change_table:
						if(word==term[0] and (st_pos>term[2] and ed_pos<term[3])):
							difference = len(term[1]) - len(term[0])
							self.contents = self.contents[0:st_pos] + term[1] +self.contents[ed_pos:self.length]
							self.length = len(self.contents)
							self.fp += difference
							for i in range(0,length_change_table):
								if(st_pos<self.change_table[i][2]):
									self.change_table[i][2] += difference
								if(st_pos<self.change_table[i][3]):
									self.change_table[i][3] += difference
						else:
							pass
		
		else:	
			#Constant
			if(self.IsNum(ch)==1):
				number = ""
				number = number + ch
				decimal_count = 0
				self.fp += 1
				ch = self.contents[self.fp]

				while(self.IsNum(ch)==1 or self.IsDecimal(ch)==1):
					number = number + ch
					if(self.IsDecimal(ch)==1):
						decimal_count += 1
					self.fp += 1
					ch = self.contents[self.fp]
				
				if(self.IsDecimal(self.contents[self.fp-1])==1):
					decimal_count += 1

				if(decimal_count==0):
					pass
				else:
					if(decimal_count==1):
						pass
					else:
						pass

			else:
				#Symbol and Char/String-constant
				if(self.IsSingleSymbol(ch)==1):
					if(ch=='\''):
						error_flag = 0
						char_constant = ""
						char_constant = char_constant + '\''
						self.fp += 1
						ch = self.contents[self.fp]
						while(ch!='\''):
							if(ch=='\\'):
								if(self.contents[self.fp+1]=='\n'):
									self.fp += 2
									ch = self.contents[self.fp]
									continue
								else:
									char_constant = char_constant + ch
									self.fp +=1
									ch = self.contents[self.fp]
									continue
							if(ch=='\n'):
								if(self.contents[self.fp-1]=='\\'):
									self.fp +=1
									ch = self.contents[self.fp]
									continue
								else:
									error_flag = 1
							char_constant = char_constant + ch
							self.fp += 1
							ch = self.contents[self.fp]
						char_constant = char_constant + '\''
						self.fp += 1
						if(error_flag==0):
							pass
						else:
							pass
					else:
						if(ch=='\"'):
							error_flag = 0
							string_constant = ""
							string_constant = string_constant + '\"'
							self.fp += 1
							ch = self.contents[self.fp]
							while(ch!='\"'):
								if(ch=='\\'):
									if(self.contents[self.fp+1]=='\n'):
										self.fp += 2
										ch = self.contents[self.fp]
										continue
									else:
										string_constant = string_constant + ch
										self.fp +=1
										ch = self.contents[self.fp]
										continue
								if(ch=='\n'):
									if(self.contents[self.fp-1]=='\\'):
										self.fp +=1
										ch = self.contents[self.fp]
										continue
									else:
										error_flag = 1
								string_constant = string_constant + ch
								self.fp += 1
								ch = self.contents[self.fp]
							string_constant = string_constant + '\"'
							self.fp += 1
							if(error_flag==0):
								pass
							else:
								pass
						else:
							mark = ""
							mark = mark + ch
							
							if(ch=='[' or ch==']' or ch=='(' or ch==')' or ch=='{' or ch=='}' or ch==')' or ch=='.' or ch==',' or ch==';' or ch=='~' or ch=='?' or ch==':' or ch=='\\' or ch=='#'):
								#self.output = self.output + [["SYMBOL",mark]]
								self.fp += 1
							
							elif(ch=='-'):
								self.fp += 1
								ch = self.contents[self.fp]
								if(ch=='>' or ch=='=' or ch=='-'):
									mark = mark + ch
									#self.output = self.output + [["SYMBOL",mark]]
									self.fp +=1
								else:
									#self.output = self.output + [["SYMBOL",mark]]
									pass
							
							elif(ch=='+'):
								self.fp += 1
								ch = self.contents[self.fp]
								if(ch=='+' or ch=='='):
									mark = mark + ch
									#self.output = self.output + [["SYMBOL",mark]]
									self.fp +=1
								else:
									#self.output = self.output + [["SYMBOL",mark]]
									pass

							elif(ch=='*' or ch=='/' or ch=='%' or ch=='^' or ch=='!' or ch=='='):
								self.fp += 1
								ch = self.contents[self.fp]
								if(ch=='='):
									mark = mark + ch
									#self.output = self.output + [["SYMBOL",mark]]
									self.fp +=1
								else:
									#self.output = self.output + [["SYMBOL",mark]]
									pass

							elif(ch=='&'):
								self.fp += 1
								ch = self.contents[self.fp]
								if(ch=='&' or ch=='='):
									mark = mark + ch
									#self.output = self.output + [["SYMBOL",mark]]
									self.fp +=1
								else:
									#self.output = self.output + [["SYMBOL",mark]]
									pass

							elif(ch=='|'):
								self.fp += 1
								ch = self.contents[self.fp]
								if(ch=='|' or ch=='='):
									mark = mark + ch
									#self.output = self.output + [["SYMBOL",mark]]
									self.fp +=1
								else:
									#self.output = self.output + [["SYMBOL",mark]]
									pass

							elif(ch=='<'):
								self.fp += 1
								ch = self.contents[self.fp]
								if(ch=='<'):
									mark = mark + ch
									self.fp += 1
									ch = self.contents[self.fp]
									if(ch=='='):
										mark = mark + ch
										#self.output = self.output + [["SYMBOL",mark]]
										self.fp +=1
									else:
										#self.output = self.output + [["SYMBOL",mark]]
										pass
								elif(ch=='='):
									mark = mark + ch
									#self.output = self.output + [["SYMBOL",mark]]
									self.fp +=1
								else:
									#self.output = self.output + [["SYMBOL",mark]]
									pass

							elif(ch=='>'):
								self.fp += 1
								ch = self.contents[self.fp]
								if(ch=='>'):
									mark = mark + ch
									self.fp += 1
									ch = self.contents[self.fp]
									if(ch=='='):
										mark = mark + ch
										#self.output = self.output + [["SYMBOL",mark]]
										self.fp +=1
									else:
										#self.output = self.output + [["SYMBOL",mark]]
										pass
								elif(ch=='='):
									mark = mark + ch
									#self.output = self.output + [["SYMBOL",mark]]
									self.fp +=1
								else:
									#self.output = self.output + [["SYMBOL",mark]]
									pass

							else:
								print("Code error!\nPlease check the symbol part.")

				else:
					print("Cannot analyze code "+ch+" .")

	def preAnalyzer(self):
		self.fp = 0
		self.length = len(self.contents)
		while(self.fp<self.length):
			ch = self.contents[self.fp]
			if(ch==' ' or ch == '\t' or ch == '\n'):
				self.fp +=1
			else:
				self.changer()

		self.contents = re.sub(r'#define (.*) (.*)',"",self.contents)
		self.contents = re.sub(r'typedef (.*) (.*);',"",self.contents)
		self.contents = re.sub(r'enum(.*){(.*)};',"",self.contents)
		# print(self.contents)

	#Scanner
	def scanner(self):
		#Preparation
		ch = self.contents[self.fp]
		#Identifier or Reserved words
		if(self.IsAlpha(ch)==1):
			word = ""
			word = word + ch
			self.fp += 1
			ch = self.contents[self.fp]

			while(self.IsNum(ch)==1 or self.IsAlpha(ch)==1 or ch=="_"):
				word = word + ch
				self.fp += 1
				ch = self.contents[self.fp]

			if(self.IsKeywords(word)==1):
				self.output = self.output + [["RESERVED_WORD",word]]
			else:
				self.output = self.output + [["IDENTIFIER",word]]
		# INT / FLOAT
		elif(self.IsNum(ch)==1):
			number = ""
			number = number + ch
			decimal_count = 0
			self.fp += 1
			ch = self.contents[self.fp]

			while(self.IsNum(ch)==1 or self.IsDecimal(ch)==1):
				number = number + ch
				if(self.IsDecimal(ch)==1):
					decimal_count += 1
				self.fp += 1
				ch = self.contents[self.fp]

			if(self.IsDecimal(self.contents[self.fp-1])==1):
				decimal_count += 1

			if(decimal_count==0):
				self.output = self.output + [["INT_CONST",number]]
			else:
				if(decimal_count==1):
					self.output = self.output + [["FLOAT_CONST",number]]
				else:
					self.output = self.output + [["ERROR_CONST",number]]
		# Symbol and Char/String-constant
		elif(self.IsSingleSymbol(ch)==1):
			if(ch=='\''):
				error_flag = 0
				char_constant = ""
				char_constant = char_constant + '\''
				self.fp += 1
				ch = self.contents[self.fp]
				while(ch!='\''):
					if(ch=='\\'):
						if(self.contents[self.fp+1]=='\n'):
							self.fp += 2
							ch = self.contents[self.fp]
							continue
						else:
							char_constant = char_constant + ch
							self.fp +=1
							ch = self.contents[self.fp]
							continue
					if(ch=='\n'):
						if(self.contents[self.fp-1]=='\\'):
							self.fp +=1
							ch = self.contents[self.fp]
							continue
						else:
							error_flag = 1
					char_constant = char_constant + ch
					self.fp += 1
					ch = self.contents[self.fp]
				char_constant = char_constant + '\''
				self.fp += 1
				if(error_flag==0):
					self.output = self.output + [["CHAR_CONST",char_constant]]
				else:
					self.output = self.output + [["ERROR_CONST",char_constant]]
			elif(ch=='\"'):
				error_flag = 0
				string_constant = ""
				string_constant = string_constant + '\"'
				self.fp += 1
				ch = self.contents[self.fp]
				while(ch!='\"'):
					if(ch=='\\'):
						if(self.contents[self.fp+1]=='\n'):
							self.fp += 2
							ch = self.contents[self.fp]
							continue
						else:
							string_constant = string_constant + ch
							self.fp +=1
							ch = self.contents[self.fp]
							continue
					if(ch=='\n'):
						if(self.contents[self.fp-1]=='\\'):
							self.fp +=1
							ch = self.contents[self.fp]
							continue
						else:
							error_flag = 1
					string_constant = string_constant + ch
					self.fp += 1
					ch = self.contents[self.fp]
				string_constant = string_constant + '\"'
				self.fp += 1
				if(error_flag==0):
					self.output = self.output + [["STRING_CONST",string_constant]]
				else:
					self.output = self.output + [["ERROR_CONST",string_constant]]
			else:
				mark = ""
				mark = mark + ch

				if(ch=='[' or ch==']' or ch=='(' or ch==')' or ch=='{' or ch=='}' or ch==')' or ch=='.' or ch==',' or ch==';' or ch=='~' or ch=='?' or ch==':' or ch=='\\' or ch=='#'):
					self.output = self.output + [["SYMBOL",mark]]
					self.fp += 1

				elif(ch=='-'):
					self.fp += 1
					ch = self.contents[self.fp]
					if(ch=='>' or ch=='=' or ch=='-'):
						mark = mark + ch
						self.output = self.output + [["SYMBOL",mark]]
						self.fp +=1
					else:
						self.output = self.output + [["SYMBOL",mark]]

				elif(ch=='+'):
					self.fp += 1
					ch = self.contents[self.fp]
					if(ch=='+' or ch=='='):
						mark = mark + ch
						self.output = self.output + [["SYMBOL",mark]]
						self.fp +=1
					else:
						self.output = self.output + [["SYMBOL",mark]]

				elif(ch=='*' or ch=='/' or ch=='%' or ch=='^' or ch=='!' or ch=='='):
					self.fp += 1
					ch = self.contents[self.fp]
					if(ch=='='):
						mark = mark + ch
						self.output = self.output + [["SYMBOL",mark]]
						self.fp +=1
					else:
						self.output = self.output + [["SYMBOL",mark]]

				elif(ch=='&'):
					self.fp += 1
					ch = self.contents[self.fp]
					if(ch=='&' or ch=='='):
						mark = mark + ch
						self.output = self.output + [["SYMBOL",mark]]
						self.fp +=1
					else:
						self.output = self.output + [["SYMBOL",mark]]

				elif(ch=='|'):
					self.fp += 1
					ch = self.contents[self.fp]
					if(ch=='|' or ch=='='):
						mark = mark + ch
						self.output = self.output + [["SYMBOL",mark]]
						self.fp +=1
					else:
						self.output = self.output + [["SYMBOL",mark]]

				elif(ch=='<'):
					self.fp += 1
					ch = self.contents[self.fp]
					if(ch=='<'):
						mark = mark + ch
						self.fp += 1
						ch = self.contents[self.fp]
						if(ch=='='):
							mark = mark + ch
							self.output = self.output + [["SYMBOL",mark]]
							self.fp +=1
						else:
							self.output = self.output + [["SYMBOL",mark]]
					elif(ch=='='):
						mark = mark + ch
						self.output = self.output + [["SYMBOL",mark]]
						self.fp +=1
					else:
						self.output = self.output + [["SYMBOL",mark]]

				elif(ch=='>'):
					self.fp += 1
					ch = self.contents[self.fp]
					if(ch=='>'):
						mark = mark + ch
						self.fp += 1
						ch = self.contents[self.fp]
						if(ch=='='):
							mark = mark + ch
							self.output = self.output + [["SYMBOL",mark]]
							self.fp +=1
						else:
							self.output = self.output + [["SYMBOL",mark]]
					elif(ch=='='):
						mark = mark + ch
						self.output = self.output + [["SYMBOL",mark]]
						self.fp +=1
					else:
						self.output = self.output + [["SYMBOL",mark]]
				else:
					print("Cannot analyze char " + ch + " .")

	def analyzer(self):
		self.fp = 0
		self.length = len(self.contents)
		while(self.fp<self.length):
			ch = self.contents[self.fp]
			if(ch == ' ' or ch == '\t' or ch == '\n'):
				self.fp +=1
			else:
				self.scanner()
		
		self.output_length = len(self.output)
		#print(self.output)
		# for word in self.output:
		# 	print(word)
		fw = open(self.file_output,"w", encoding = "utf-8")
		for word in self.output:
			fw.write(str(word)+"\n")

	def word_table(self,num):
		if(num<self.output_length):
			return self.output[num]
		else:
			return ["ERROR","NUM OUT OF RANGE"]

	def LL(self,n):
		if(self.word_iterator+n-1<self.output_length):
			return self.word_table(self.word_iterator+n-1)[1]
		else:
			return ["ERROR","NUM OUT OF RANGE"][1]

	def LL1(self):
		if(self.word_iterator<self.output_length):
			return self.word_table(self.word_iterator)[1]
		else:
			return ["ERROR","NUM OUT OF RANGE"][1]	

	def LL1type(self):
		if(self.word_iterator<self.output_length):
			return self.word_table(self.word_iterator)[0]
		else:
			return ["ERROR","NUM OUT OF RANGE"][0]	

	def advance(self):
		self.word_iterator = self.word_iterator + 1

if (__name__ == '__main__'):
	os.chdir(r"C:\Users\goldfish\PycharmProjects\Cparser\test")
	file = "mergesort.c"
	# create a object
	obj = C_Lexer(file)
	# pre-operation
	obj.preScanner()
	obj.preAnalyzer()
	# wording
	obj.analyzer()

	time.sleep(1000)