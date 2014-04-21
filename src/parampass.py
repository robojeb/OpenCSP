from compilerpass import CompilerPass, CompileError, UndefError
from symboltable import SymbolTable
from varinfo import *
from ast import *

def isParam(x, params):
	if isinstance(x, ASTAssign) or isinstance(x, ASTDefine):
		return (x.name_.name_ in params.keys())
	return False


class ParamPass(CompilerPass):
	def __init__(self):
		self.symbols_ = SymbolTable()
		self.paramMap_ = {}

	def visitFile(self, f):
		#Build symbol table and gather parameter lists
		for op in f.operations_:
			op.accept(self)

		nonParam = [x for x in f.operations_ if not isParam(x, self.paramMap_)]
		for k in self.paramMap_.keys():
			param = self.paramMap_[k]
			param.check() #The parameter types will check themselves and error if needed
			nonParam.insert(0, param)
		
		return ASTFile(None, nonParam)


	def visitAssign(self, assign):
		name = assign.name_
		prevDecl, prevInfo = self.symbols_.lookup(name.name_)
		if(len(name.params_) == 0):
			if prevDecl and prevInfo.isParameterized():
				raise CompileError(name.printPos() + ":Redefinition of parameterized name as non-parameterized name")
			if prevDecl:
				raise CompileError(name.printPos() + ":Redefinition of non-parameterized type")
			self.symbols_.insert(name.name_, VarInfo(VarType.Unknown))
		else:
			if prevDecl and not prevInfo.isParameterized():
				raise CompileError(name.printPos() + ":Redefinition of non-parameterized name as parameterized name")
			self.symbols_.insert(name.name_, VarInfo(VarType.Unknown, True))
			if name.name_ in self.paramMap_:
				self.paramMap_[name.name_].addRawParam(name.pos_, name.params_, assign.expr_)
			else:
				self.paramMap_[name.name_] = ASTParams(0, name.name_)
				self.paramMap_[name.name_].addRawParam(name.pos_, name.params_, assign.expr_)

	def visitDefine(self, define):
		name = define.name_
		prevDecl, prevInfo = self.symbols_.lookup(name.name_)
		if(len(name.params_) == 0):
			if prevDecl and prevInfo.isParameterized():
				raise CompileError(name.printPos() + ":Redefinition of parameterized name as non-parameterized name")
			if prevDecl:
				raise CompileError(name.printPos() + ":Redefinition of non-parameterized type")
			self.symbols_.insert(name.name_, VarInfo(VarType.Unknown))
		else:
			if prevDecl and not prevInfo.isParameterized():
				raise CompileError(name.printPos() + ":Redefinition of non-parameterized name as parameterized name")
			self.symbols_.insert(name.name_, VarInfo(VarType.Unknown, True))
			if name.name_ in self.paramMap_:
				self.paramMap_[name.name_].addRawParam(name.pos_, name.params_, define.expr_)
			else:
				self.paramMap_[name.name_] = ASTParams(0, name.name_, define=True)
				self.paramMap_[name.name_].addRawParam(name.pos_, name.params_, define.expr_)


	def visitName(self, name):
		pass

	def visitSpawn(self, spawn):
		#We don't need to do anything with spawn at 
		#this point in the semantic pass
		pass

class ParamInitPass(CompilerPass):
	def __init__(self):
		self.symbols_ = SymbolTable()
		pass

	def visitFile(self, f):
		for op in f.operations_:
			op.accept(self)

	def visitExpr(self, expr):
		expr.e1_.accept(self)
		if not expr.e2_ == None:
			expr.e2_.accept(self)

	def visitNum(self, expr):
		pass

	def visitName(self, name):
		exists, data = self.symbols_.lookup(name.name_)
		if not exists:
			raise CompileError("Cannot use non-parameter variables in global initialization.")

	def visitAssign(self, assign):
		assign.expr_.accept(self)

	def visitDefine(self, define):
		pass

	def visitSpawn(self, spawn):
		pass

	def visitParams(self, params):
		if params.isDefine_:
			return
		self.symbols_.enterContext()
		for n in params.params_:
			self.symbols_.insert(n, None)
		for rp in params.rawParams_:
			e = rp[2]
			e.accept(self)
		self.symbols_.leaveContext()


