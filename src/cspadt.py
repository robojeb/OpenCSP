import sys
from threading import Semaphore


#Pretty printing data structure
class Printer:
	def __init__(self, file = sys.stdout):
		self.indentLevel = 0
		self.startLine = False
		self.file = file

	def indent(self):
		#self.file.write('\n')
		self.startLine = True
		self.indentLevel += 1

	def dedent(self):
		#self.file.write('\n')
		self.startLine = True
		self.indentLevel -= 1

	def out(self, string):
		if self.startLine == True:
			tabs = '\t'*self.indentLevel
			self.file.write(tabs + string)
		else:
			self.file.write(string)
		self.startLine = False

	def outnl(self, string):
		if self.startLine == True:
			tabs = '\t'*self.indentLevel
			self.file.write(tabs + string + '\n')
		else:
			self.file.write(string + '\n')
		self.startLine = True

	def newline(self):
		self.startLine = True
		self.file.write('\n')

	def var(self, var):
		return var + self.indentLevel

# Channel class

header = "import random\n\
import threading\n\
class Channel:\n\
	def __init__(self):\n\
		self.readSem = threading.Semaphore(0)\n\
		self.writeSem = threading.Semaphore(0)\n\
		self.value = None\n\
\n\
	def write(self, value):\n\
		self.value = value\n\
		self.readSem.release()\n\
		self.writeSem.acquire()\n\
\n\
	def read(self):\n\
		self.readSem.acquire()\n\
		self.writeSem.release()\n\
		return self.value\n\
channels_ = {}\n"

#Global Variable List

globVar = []
activeThreads = []

# ADT

class Sequence:
	def __init__(self, commands):
		self.commands = commands

	def getGlobalVariables(self):
		global globVar
		for c in self.commands:
			if isinstance(c, Assign):
				globVar.append(c.var)

	def pp(self, printer):
		for c in self.commands:
			c.pp(printer)
			printer.newline()

class Assign:
	def __init__(self, var, expr):
		self.var = var
		self.expr = expr

	def pp(self, printer):
		varname = "V" + str(len(self.var)) + "_" + self.var
		printer.out(self.var + " =")
		self.expr.pp(printer)

class Operator:
	def __init__(self, op, val, expr):
		self.op = op
		self.val = val
		self.expr = expr

	def pp(self, printer):
		self.val.pp(printer)
		printer.out(self.op)
		self.expr.pp(printer)

	def getReplaceVars(self, guard):
		vars = []
		if self.val.var == True:
			vars.append(self.val.val)
			self.val.val = guard + self.val.val
		vars += self.expr.getReplaceVars(guard)
		return vars

class Value:
	def __init__(self, val):
		self.val = val
		if val[0] == "V":
			self.var = True
		else:
			self.var = False

	def pp(self, printer):
		printer.out(self.val)

	def getReplaceVars(self, guard):
		if self.var == True:
			temp = self.val
			self.val = guard + self.val
			return [temp]
		else:
			return []

class Program:
	def __init__(self, name, sequence):
		self.name = name
		self.sequence = sequence

	def pp(self, printer):
		progname = "P" + str(len(self.name)) + "_" + self.name
		printer.outnl("def " + progname + "():")
		printer.indent()
		printer.outnl("name_ = \"" + progname+ "\"")
		for v in globVar:
			printer.outnl("global " + v)
		self.sequence.pp(printer)
		printer.dedent()

class Run:
	def __init__(self, prog):
		self.prog = prog

	def pp(self, printer):
		progname = "P" + str(len(self.prog)) + "_" + self.prog
		printer.outnl(progname+ "_ = threading.Thread( target=" + progname +  ")" )
		printer.outnl(progname + "_.start()")
		activeThreads.append(progname)

class Write:
	def __init__(self, expr):
		self.expr = expr

	def pp(self, printer):
		printer.out("print (")
		self.expr.pp(printer)
		printer.out(")")

class Predicate:
	def __init__(self, op, expr1, expr2):
		self.op = op
		self.expr1 = expr1
		self.expr2 = expr2

	def pp(self, printer):
		printer.out("lambda: ")
		self.expr1.pp(printer)
		printer.out(self.op)
		self.expr2.pp(printer)


class IF:
	def __init__(self, branches):
		self.branches = branches

	def pp(self, printer):
		vvar = "valid" + str(printer.indentLevel) + "_"
		bvar = "branches" + str(printer.indentLevel) + "_"
		cvar = "choice" + str(printer.indentLevel) + "_"
		gvar = "guard" + str(printer.indentLevel) + "_"

		vars = []
		for branch in self.branches:
			vars += branch[0].expr1.getReplaceVars(gvar)
			vars += branch[0].expr2.getReplaceVars(gvar)

		vars = set(vars)
		for v in vars:
			printer.outnl(gvar + v + "=" + v)

		printer.outnl("#Branches printed here")
		printer.out(bvar + "=[")
		for i, branch in enumerate(self.branches):
			printer.out("(" + str(i) + ",")
			branch[0].pp(printer)
			printer.out(")")
			if not i == len(self.branches )-1:
				printer.out(",")
		printer.outnl("]")
		printer.outnl("while True:")
		printer.indent()
		for v in vars:
			printer.outnl(gvar + v + "=" + v)
		printer.outnl(vvar + "= filter(lambda x: x[1](), "+ bvar + ")")
		printer.outnl("if len("+ vvar + ") == 0: continue")
		printer.outnl(cvar + "= random.choice(" + vvar + ")")
		printer.outnl(cvar + "=" + cvar + "[0]")
		for i, branch in enumerate(self.branches):
			printer.outnl("if " + cvar + "==" + str(i) + ":")
			printer.indent()
			branch[1].pp(printer)
			printer.dedent()
		printer.outnl("break")
		printer.dedent()

class LOOP:
	def __init__(self, branches):
		self.branches = branches

	def pp(self, printer):
		vvar = "valid" + str(printer.indentLevel) + "_"
		bvar = "branches" + str(printer.indentLevel) + "_"
		cvar = "choice" + str(printer.indentLevel) + "_"
		gvar = "guard" + str(printer.indentLevel) + "_"

		vars = []
		for branch in self.branches:
			vars += branch[0].expr1.getReplaceVars(gvar)
			vars += branch[0].expr2.getReplaceVars(gvar)

		vars = set(vars)
		for v in vars:
			printer.outnl(gvar + v + "=" + v)

		printer.outnl("#Branches printed here")
		printer.out(bvar + "=[")
		for i, branch in enumerate(self.branches):
			printer.out("(" + str(i) + ",")
			branch[0].pp(printer)
			printer.out(")")
			if not i == len(self.branches )-1:
				printer.out(",")
		printer.outnl("]")
		printer.outnl(vvar + "= filter(lambda x: x[1](), "+ bvar + ")")
		printer.outnl("while len(" + vvar + ") != 0:")
		printer.indent()
		printer.outnl(cvar + "= random.choice(" + vvar + ")")
		printer.outnl(cvar + "=" + cvar + "[0]")
		for i, branch in enumerate(self.branches):
			printer.outnl("if " + cvar + "==" + str(i) + ":")
			printer.indent()
			branch[1].pp(printer)
			printer.dedent()
		
		for v in vars:
			printer.outnl(gvar + v + "=" + v)
		printer.outnl(vvar + "= filter(lambda x: x[1](), "+ bvar + ")")
		printer.dedent()

class Sem:
	def __init__(self, name, val):
		self.val = val
		self.name = name

	def pp(self, printer):
		semname = "S" + str(len(self.name)) + "_" + self.name
		printer.out(semname + "= threading.Semaphore(")
		self.val.pp(printer)
		printer.outnl(")")

class SemAct:
	def __init__(self, op, var):
		self.op = op
		self.var = var

	def pp(self, printer):
		semname = "S" + str(len(self.var)) + "_" + self.var
		printer.out(semname)
		if self.op == "P":
			printer.out(".acquire()")
		else:
			printer.out(".release()")

class ChannelDef:
	def __init__(self, fromProc, fromName, toProc, toName):
		self.fromProc = fromProc
		self.fromName = fromName
		self.toProc = toProc
		self.toName = toName

	def pp(self, printer):
		printer.outnl("channels_[(\"" + self.fromProc + "\",\"" + self.fromName + "\")] = Channel()")
		printer.outnl("channels_[(\"" + self.toProc + "\",\"" + self.toName + "\")] = channels_[(\""+ self.fromProc + "\",\"" + self.fromName + "\")]")

class ChannelAct:
	def __init__(self, read, name, var):
		self.read = read
		self.name = name
		self.var = var

	def pp(self, printer):
		if self.read:
			self.var.pp(printer)
			printer.outnl("=channels_[(name_,\"" + self.name + "\")].read()")
		else:
			printer.out("channels_[(name_,\"" + self.name + "\")].write(")
			self.var.pp(printer)
			printer.outnl(")")

