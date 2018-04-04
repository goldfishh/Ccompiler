# Main函数
# int main()           -> (lable, main, -, -)
# {
# 	initialization();  -> (call, initialization, parameters, -)
# 	Sleep(1000);       -> (Sleep, 1000, -, -)
# 	round();           -> (call, round, params, -)
# 	return 0;          -> (return, 0, -, -)
# }

# if-else
#   if (roundcount == 0)          (==, roundcount, 0, tmp1)
# 	{                             (jmp, funcname_if, funcname_else, tmp1)
# 		block = firstblock;       (label, funcname_if, -, -)
# 	}                             ......
# 	else
# 	{
# 		block = nextblock;
# 	}

# while / for

# letstatement


# dostatement √
#                              -> (call, )

#    jmp>
#    jmp>=
#    jmp
#    jmpZ
#    jmp<
#    jmp<=

# printf()
# scanf()
# srand()
# rand()
# Sleep()
# kbhit()  检测键盘是否有输入
# getch()
# system()
class QuadrupleWriter:
	def __init__(self, fname):
		self.foutname = fname.split('.')[0] + ".qpl"
		self.fout = open(self.foutname, "a+", encoding = "utf-8")
		self.tempnum = 0

	def utility(self,a1, a2="-", a3="-", a4="-"):
		self.fout.write("({}, {}, {}, {})\n".format(a1, a2, a3, a4))
	#C库函数
	def writePrintf(self, expressionnum):
		self.utility("printf", expressionnum)

	def writeScanf(self, expressionnum):
		self.utility("scanf", expressionnum)
	def writeSrand(self, expressionnum):
		#import random
		#random.seed()
		self.utility("srand", expressionnum)
	def writeTime(self, expressionnum):
		#import time
		#time.time(0)
		self.utility("time", expressionnum)
	def writeRand(self, expressionnum):
		#import random
		#random.random()
		self.utility("rand", expressionnum)
	def writeSleep(self, expressionnum):
		#time.sleep()
		self.utility("sleep", expressionnum)
	def writeKbhit(self, expressionnum):
		#import msvcrt
		#msvcrt.kbhit()
		self.utility("kbhit", expressionnum)
	def writeGetch(self, expressionnum):
		#import msvcrt
		#msvcrt.getch()
		self.utility("getch", expressionnum)
	def writeSystem(self, expressionnum):
		#import sys
		self.utility("system", expressionnum)

#type == 1 : jmp>=
#type == 2 : jmp>
#type == 3 : jmp
# 注: label == "-" 时 结果成立也不跳转
	def writeJmp(self, type, label1, label2, value):
		if(type == 1):
			self.utility("jmp>=", label1, label2, value)
		elif(type == 2):
			self.utility("jmp>", label1, label2, value)
		elif(type == 3):
			self.utility("jmp", label1, label2, value)
		else:
			print("ERROR\n")
	def writeGoto(self,label):
		self.utility("goto", label)

	def writeCall(self, routinename, expressionnum):
		self.utility("call", routinename, expressionnum)

	def writeReturn(self, flag = True):
		if(flag):
			self.utility("return", "TMP"+str(self.tempnum-1))
		else:
			self.utility("return")

	def writeLabel(self, labelname):
		self.utility("label",labelname)

	def writeunaryop(self, unaryop,object):
		self.utility(unaryop, object, "-", "TMP"+str(self.tempnum))
		self.tempnum = self.tempnum + 1

	def writearyop(self, aryop,object1, object2):
		self.utility(aryop, object1, object2, "TMP"+str(self.tempnum))
		self.tempnum = self.tempnum + 1
#type == 1 ++vaname
#type == 2 vname++
	def writeselfop(self, aryop, vname, type):
		if(type == 1):
			self.utility(aryop, vname, "-", vname)
		elif(type == 2):
			self.utility("=", vname, "-", "TMP"+str(self.tempnum))
			self.tempnum = self.tempnum + 1
			self.utility(aryop, "-", vname, vname)
		else:
			print("ERROR\n")
	def writelet(self, receiver = None, sender = None):
		if(not sender):
			self.utility("=", "TMP"+str(self.tempnum-1), "-", receiver)
		elif(not receiver):
			self.utility("=", sender, "-", "TMP"+str(self.tempnum))
			self.tempnum = self.tempnum + 1
	# 形参
	def writereceiveparams(self, receiver):
		self.utility("FORMAL", "-", "-", receiver)
	# 实参
	def writepassparams(self, num):
		self.utility("ACTUAL", "TMP"+str(self.tempnum-1), num)
#type == 1 IN
#type == 2 OUT
	def writeinout(self, type):
		if(type == 1):
			self.utility("IN")
		elif(type == 2):
			self.utility("OUT")
		else:
			print("ERROR\n")
