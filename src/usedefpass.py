from compilerpass import CompilerPass, CompileError, UndefError
from symboltable import SymbolTable
from varinfo import *
from ast import *

class UseDef(CompilerPass):
	def __init__(self):
		self.symbols_ = SymbolTable()

	def visitFile(self, f):
		for op in f.operations_:
			op.accept(self)

	def visitProgram(self, prog):
		prog.sequence_.accept(self)

	def visitFunctionDef(self, func):
		raise UndefError("visitFunctionDef not defined")

	def visitSequence(self, seq):
		for o in seq.operations_:
			o.accept(self)

	def visitAssign(self, assign):
		# we have already checked all of the variable assignemnts
		# just check for conflicts
		exists, data = self.symbols_.lookup(assign.name_.name_)
		if not exists:
			assign.expr_.accept(self)
			self.symbols_.insert(assign.name_.name_, VarInfo())
		else:
			assign.expr_.accept(self)

	def visitDefine(self, define):
		exists, data = self.symbols_.lookup(define.name_.name_)
		if not exists:
			self.symbols_.insert(define.name_.name_, VarInfo())
			self.symbols_.enterContext()
			define.expr_.accept(self)
			self.symbols_.leaveContext()
		elif not data.undef_:
			raise CompileError("Cannot redefine non-parameterized variable")

	def visitIf(self, If):
		for b in If.branches_:
			b.accept(self)

	def visitLoop(self, loop):
		for b in loop.branches_:
			b.accept(self)

	def visitBranch(self, branch):
		branch.cond_.accept(self)
		branch.sequence_.accept(self)

	def visitExpr(self, expr):
		expr.e1_.accept(self)
		if not expr.e2_ == None:
			expr.e2_.accept(self)

	def visitNum(self, num):
		#Nothing to do here
		pass

	def visitName(self, name):
		inDict, data = self.symbols_.lookup(name.name_)
		if not inDict:
			if len(name.params_) > 0:
				self.symbols_.insert(name.name_, VarInfo(undef=True, param=True))
			else:
				self.symbols_.insert(name.name_, VarInfo(undef=True))

	def visitRange(self, name):
		raise UndefError("visitRange not defined")

	def visitSemDef(self, semdef):
		raise UndefError("visitSemDef not defined")

	def visitSemOp(self, semop):
		raise UndefError("visitSemOp not defined")

	def visitSpawn(self, spawn):
		spawn.prog_.accept(self)

	def visitParams(self, params):
		if params.isDefine_:
			self.symbols_.insert(params.name_, VarInfo(param=True))
			self.symbols_.enterContext()
			for par in params.params_:
					self.symbols_.insert(par.name_)
			for p in params.rawParms_:
				self.symbols_.enterContext()
				expr = p[2]
				expr.accept(self)
				self.symbols_.leaveContext()
			self.symbols_.leaveContext()
		else:
			self.symbols_.insert(params.name_, VarInfo(param=True))

class UseDefSecondPass(CompilerPass):
	def __init__(self, sym):
		self.symbols_ = sym
		pass

	def visitFile(self, f):
		for op in f.operations_:
			op.accept(self)

	def visitProgram(self, prog):
		prog.sequence_.accept(self)

	def visitFunctionDef(self, func):
		raise UndefError("visitFunctionDef not defined")

	def visitSequence(self, seq):
		for o in seq.operations_:
			o.accept(self)

	def visitAssign(self, assign):
		# we have already checked all of the variable assignemnts
		# just check for conflicts
		exists, data = self.symbols_.lookup(assign.name_.name_)
		if not exists and len(assign.name_.parameters_) == 0:
			assign.expr_.accept(self)
			self.symbols_.insert(assign.name_.name_, VarInfo())
		elif not exists and len(assign.name_.parameters_) == 0:
			raise CompileError("Parameterized variable can only be declared globally")
		else:
			assign.expr_.accept(self)

	def visitDefine(self, define):
		self.symbols_.enterContext()
		define.expr_.accept(self)
		self.symbols_.leaveContext()

	def visitIf(self, If):
		for b in If.branches_:
			b.accept(self)

	def visitLoop(self, loop):
		for b in loop.branches_:
			b.accept(self)

	def visitBranch(self, branch):
		branch.cond_.accept(self)
		branch.sequence_.accept(self)

	def visitExpr(self, expr):
		expr.e1_.accept(self)
		if not expr.e2_ == None:
			expr.e2_.accept(self)

	def visitNum(self, num):
		#Nothing to do here
		pass

	def visitName(self, name):
		inDict, data = self.symbols_.lookup(name.name_)
		if not inDict:
			raise CompileError("Symbol: " + name.name_ + " not defined")
		elif (len(name.params_) > 0 and not data.parameterized_):
			raise CompileError("Using non-parameterized variable " + name.name_ + " with parameter")
		elif (name.params_ == [] and data.parameterized_):
			raise CompileError("Using parameterized variable " + name.name_ + " without parameter")

		# We need to usedef check the parameters of a variable too
		for p in name.params_:
			p.accept(self)


	def visitRange(self, name):
		raise UndefError("visitRange not defined")

	def visitSemDef(self, semdef):
		raise UndefError("visitSemDef not defined")

	def visitSemOp(self, semop):
		raise UndefError("visitSemOp not defined")

	def visitSpawn(self, spawn):
		spawn.prog_.accept(self)

	def visitParams(self, params):
		if params.isDefine_:
			self.symbols_.insert(params.name_, VarInfo(param=True))
			self.symbols_.enterContext()
			for par in params.params_:
					self.symbols_.insert(par.name_)
			for p in params.rawParms_:
				self.symbols_.enterContext()
				expr = p[2]
				expr.accept(self)
				self.symbols_.leaveContext()
			self.symbols_.leaveContext()
