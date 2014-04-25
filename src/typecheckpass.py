from compilerpass import CompilerPass, CompileError, UndefError
from symboltable import SymbolTable
from varinfo import *
from ast import *

class TypeDef(CompilerPass):
	def __init__(self):
		self.symbols_ = SymbolTable()

	def visitFile(self, f):
		for op in f.operations_:
			op.accept(self)

	def visitProgram(self, prog):
		prog.sequence_.accept(self)

	def visitSequence(self, seq):
		for op in seq.operations_:
			op.accept(self)

	def visitAssign(self, assign):
		exists, data = self.symbols_.lookup(assign.name_.name_)
		pass
