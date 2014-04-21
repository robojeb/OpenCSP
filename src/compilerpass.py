from symboltable import SymbolTable
from varinfo import *
from ast import *

# Define an exception to show if something is undefined
class UndefError(Exception):
	def __init__(self, value):
		self.value_ = value

	def __str__(self):
		return repr(self.value)

class CompileError(Exception):
	def __init__(self, value):
		self.value_ = value

	def __str__(self):
		return repr(self.value)

# Define the generic compiler pass type
class CompilerPass:
	def __init__(self):
		pass

	def visitAbstract(self, str):
		raise UndefError(str)

	def visitFile(self, f):
		raise UndefError("visitFile not defined")

	def visitProgram(self, prog):
		raise UndefError("visitProgram not defined")

	def visitFunctionDef(self, func):
		raise UndefError("visitFunctionDef not defined")

	def visitSequence(self, seq):
		raise UndefError("visitSequence not defined")

	def visitAssign(self, assign):
		raise UndefError("visitAssign not defined")

	def visitDefine(self, define):
		raise UndefError("visitDefine not defined")

	def visitIf(self, If):
		raise UndefError("visitIf not defined")

	def visitLoop(self, loop):
		raise UndefError("visitLoop not defined")

	def visitBranch(self, branch):
		raise UndefError("visitBranch not defined")

	def visitExpr(self, expr):
		raise UndefError("visitExpr not defined")

	def visitNum(self, num):
		raise UndefError("visitNum not defined")

	def visitName(self, name):
		raise UndefError("visitName not defined")

	def visitRange(self, name):
		raise UndefError("visitRange not defined")

	def visitSemDef(self, semdef):
		raise UndefError("visitSemDef not defined")

	def visitSemOp(self, semop):
		raise UndefError("visitSemOp not defined")

	def visitSpawn(self, spawn):
		raise UndefError("visitSpawn not defined")

	def visitParams(self, params):
		raise UndefError("visitParams not defined")
