from compilerpass import CompileError

class AbstractAST(object):
	def __init__(self, pos):
		self.pos_ = pos

	def accept(self, compPass):
		return compPass.visitAbstract("Cannot use abstract accept")

	def printPos(self):
		if self.pos_ == None:
			return "No position"
		else:
			return "Line: " + self.pos_[0] + " Col: " + self.pos_[1]

''' 
Top level file abstract data type 
Should contain all information for a single file of the language
'''
class ASTFile(AbstractAST):
	def __init__(self, pos, operations):
		super(ASTFile, self).__init__(pos)
		self.operations_ = operations

	def accept(self, compPass):
		return compPass.visitFile(self)

	def __repr__(self):
		return str(self.operations_)

'''
The definition of a single program to be executed as a thread
It contains a sequence of operations to perform
'''
class ASTProgram(AbstractAST):
	def __init__(self, pos, sequence):
		super(ASTProgram, self).__init__(pos)
		self.sequence_ = sequence

	def accept(self, compPass):
		return compPass.visitProgram(self)

class ASTFunctionDef(AbstractAST):
	def __init__(self, pos, args, sequence):
		super(ASTFunctionDef, self).__init__(pos)
		self.args_ = args
		self.sequence_ = sequence

	def accept(self, compPass):
		return compPass.visitFunctionDef(self)

class ASTSequence(AbstractAST):
	def __init__(self, pos, operations):
		super(ASTSequence, self).__init__(pos)
		self.operations_ = operations

	def accept(self, compPass):
		return compPass.visitSequence(self)

	def __repr__(self):
		return str(self.operations_)

'''
operations
'''
'''
An assign operation for variables
'''
class ASTAssign(AbstractAST):
	def __init__(self, pos, name, expr):
		super(ASTAssign, self).__init__(pos)
		self.name_ = name
		self.expr_ = expr

	def accept(self, compPass):
		return compPass.visitAssign(self)

	def __repr__(self):
		return str(self.name_) + "=" + str(self.expr_) 

'''
An assign operation for variables
'''
class ASTDefine(AbstractAST):
	def __init__(self, pos, name, expr):
		super(ASTDefine, self).__init__(pos)
		self.name_ = name
		self.expr_ = expr

	def accept(self, compPass):
		return compPass.visitDefine(self)

	def __repr__(self):
		return str(self.name_) + "<-" + str(self.expr_) 

'''
AST Types for if statements
'''
class ASTIf(AbstractAST):
	def __init__(self, pos, branches):
		super(ASTIf, self).__init__(pos)
		self.branches_ = branches

	def accept(self, compPass):
		return compPass.visitIf(self)

	def __repr__(self):
		return "if\n" + str(self.branches_)

'''
AST Type for loops
'''

class ASTLoop(AbstractAST):
	def __init__(self, pos, branches):
		super(ASTLoop, self).__init__(pos)
		self.branches_ = branches

	def accept(self, compPass):
		return compPass.visitLoop(self)

	def __repr__(self):
		return "loop\n" + str(self.branches_)

'''
Generic AST for conditional branches
'''
class ASTBranch(AbstractAST):
	def __init__(self, pos, cond, sequence):
		super(ASTBranch, self).__init__(pos)
		self.cond_ = cond
		self.sequence_ = sequence

	def accept(self, compPass):
		return compPass.visitBranch(self)

	def __repr__(self):
		return str(self.cond_) + "=>" + str(self.sequence_)


'''
Expression AST
'''

class ASTExpression(AbstractAST):
	def __init__(self, pos, op, e1, e2):
		super(ASTExpression, self).__init__(pos)
		self.op_ = op
		self.e1_ = e1
		self.e2_ = e2

	def accept(self, compPass):
		return compPass.visitExpr(self)

	def __repr__(self):
		if self.e2_ == None:
			return "(" + self.op_ + str(self.e1_) + ")"
		else:
			return "(" + str(self.e1_) + " " + self.op_ + " " + str(self.e2_) + ")"

'''
Types
'''

'''
Num type
'''
class ASTNum(AbstractAST):
	def __init__(self, pos, value):
		super(ASTNum, self).__init__(pos)
		self.value_ = value

	def accept(self, compPass):
		return compPass.visitNum(self)

	def __repr__(self):
		return str(self.value_)

'''
String type
'''
class ASTString(AbstractAST):
	def __init__(self, pos, value):
		super(ASTString, self).__init__(pos)
		self.value_

	def accept(self, comPass):
		return comPass.visitStr(self)

	def __repr__(self):
		return self.value_

'''
A name type that supports parameters
'''
class ASTName(AbstractAST):
	def __init__(self, pos, name, params):
		super(ASTName, self).__init__(pos)
		self.name_ = name
		self.params_ = params

	def accept(self, compPass):
		return compPass.visitName(self)

	def __repr__(self):
		return self.name_ + str(self.params_)

'''
Range parameter type
'''
class ASTRange(AbstractAST):
	def __init__(self, pos, start, end):
		super(ASTRange, self).__init__(pos)
		self.start_ = start
		self.end_ = end

	def accept(self, compPass):
		return compPass.visitRange(self)

	def __repr__(self):
		return "[" + str(self.start_) + "->" + str(self.end_) + "]"

'''
Semaphore stuff
'''
'''
semaphore definition
'''
class ASTSemDef(AbstractAST):
	def __init__(self, pos, value):
		super(ASTSemDef, self).__init__(pos)
		self.value_ = value

	def accept(self, compPass):
		return compPass.visitSemDef(self)

'''
semaphore operation
'''
class ASTSemOp(AbstractAST):
	def __init__(self, pos, op, name):
		super(ASTSemOp, self).__init__(pos)
		self.name_ = name
		self.op_ = op

	def accept(self, compPass):
		return compPass.visitSemDef(self)

'''
Spawn operation
'''

class ASTSpawn(AbstractAST):
	def __init__(self, pos, prog):
		super(ASTSpawn, self).__init__(pos)
		self.prog_ = prog

	def accept(self, compPass):
		return compPass.visitSpawn(self)

	def __repr__(self):
		return "spawn:" + str(self.prog_)

'''
Second level structure
'''

class ASTParams(AbstractAST):
	def __init__(self, pos, name, define=False):
		super(ASTParams, self).__init__(pos)
		self.name_ = name
		self.rawParams_ = []
		self.params_ = []
		self.isDefine_ = define

	def addRawParam(self, pos, param, expr):
		self.rawParams_.append((pos, param, expr))

	def check(self):
		baseLen = len(self.rawParams_[0][1])
		#verify all params same length
		for rp in self.rawParams_:
			p = rp[1]
			if not len(p) == baseLen:
				raise CompileError("Parameterized variable " + self.name_ + " contains two different length parameter lists: " + str(baseLen) + " and " + str(len(p)))
		#verify same name for all parameters in each definition
		self.params_ = [None]*baseLen
		hasGeneric = False
		for rp in self.rawParams_:
			p = rp[1]
			allGeneric = True
			for i, param in enumerate(p):
				if isinstance(param, ASTName):
					if self.params_[i] == None:
						self.params_[i] = param.name_
					else:
						if self.params_[i] != param.name_:
							raise CompileError("Parameterized variable " + self.name_ + " has two different paramter names at index " + str(i) + ": " + str(self.params_[i]) + " and " + str(param.name_))
				elif isinstance(param, ASTRange) or isinstance(param, ASTNum):
					allGeneric = False
				else:
					raise CompileError("Parameterized variable " + self.name_ + " can only use names, numbers, and ranges in its definition")
			hasGeneric |= allGeneric

		if not hasGeneric:
			raise CompileError("Parameterized variable " + self.name_ + " does not have a generic invocation (all named parameters)")

	def accept(self, compPass):
		return compPass.visitParams(self)

	def __repr__(self):
		if len(self.params_) > 0:
			return str(self.name_) + ":" + str(self.params_)
		else:
			return str(self.name_) + ":" + str(len(self.rawParams_))


