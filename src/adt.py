
class AbstractADT(object):
	def __init__(self, pos):
		self.pos_ = pos
		pass

	def accept(self, compPass):
		return compPass.visitAbstract("Cannot use abstract accept")

''' 
Top level file abstract data type 
Should contain all information for a single file of the language
'''
class ADTFile(AbstractADT):
	def __init__(self, pos, operations):
		super(ADTFile, self).__init__(pos)
		self.operations_ = operations

	def accept(self, compPass):
		return compPass.visitFile(self)

'''
The definition of a single program to be executed as a thread
It contains a sequence of operations to perform
'''
class ADTProgram(AbstractADT):
	def __init__(self, pos, name, sequence):
		super(ADTProgram, self).__init__(pos)
		self.name_ = name
		self.sequence_ = sequence

	def accept(self, compPass):
		return compPass.visitProgram(self)

class ADTFunctionDef(AbstractADT):
	def __init__(self, pos, args, sequence):
		super(ADTFunctionDef, self).__init__(pos)
		self.args_ = args
		self.sequence_ = sequence

	def accept(self, compPass):
		return compPass.visitFunctionDef(self)

class ADTSequence(AbstractADT):
	def __init__(self, pos, operations):
		super(ADTSequence, self).__init__(pos)
		self.operations_ = operations

	def accept(self, compPass):
		return compPass.visitSequence(self)

'''
operations
'''
'''
An assign operation for variables
'''
class ADTAssign(AbstractADT):
	def __init__(self, pos, name, expr):
		super(ADTAssign, self).__init__(pos)
		self.name_ = name
		self.expr_ = expr

	def accept(self, compPass):
		return compPass.visitAssign(self)

'''
An assign operation for variables
'''
class ADTDefine(AbstractADT):
	def __init__(self, pos, name, value):
		super(ADTDefine, self).__init__(pos)
		self.name_ = name
		self.value_ = value

	def accept(self, compPass):
		return compPass.visitDefine(self)

'''
ADT Types for if statements
'''
class ADTIf(AbstractADT):
	def __init__(self, pos, branches):
		super(ADTIf, self).__init__(pos)
		self.branches_ = branches

	def accept(self, compPass):
		return compPass.visitIf(self)

'''
ADT Type for loops
'''

class ADTLoop(AbstractADT):
	def __init__(self, pos, branches):
		super(ADTLoop, self).__init__(pos)
		self.branches_ = branches

	def accept(self, compPass):
		return compPass.visitLoop(self)

'''
Generic ADT for conditional branches
'''
class ADTBranch(AbstractADT):
	def __init__(self, pos, cond, sequence):
		super(ADTBranch, self).__init__(pos)
		self.cond_ = cond
		self.sequence_ = sequence

	def accept(self, compPass):
		return compPass.visitBranch(self)


'''
Expression ADT
'''

class ADTExpression(AbstractADT):
	def __init__(self, pos, op, e1, e2):
		super(ADTExpression, self).__init__(pos)
		self.op_ = op
		self.e1_ = e1
		self.e2_ = e2

	def accept(self, compPass):
		return compPass.visitExpr(self)

'''
Types
'''

'''
Num type
'''
class ADTNum(AbstractADT):
	def __init__(self, pos, value):
		super(ADTNum, self).__init__(pos)
		self.value_ = value

	def accept(self, compPass):
		return compPass.visitNum(self)

'''
String type
'''
class ADTString(AbstractADT):
	def __init__(self, pos, value):
		super(ADTString, self).__init__(pos)
		self.value_

	def accept(self, comPass):
		return comPass.visitStr(self)

'''
A name type that supports parameters
'''
class ADTName(AbstractADT):
	def __init__(self, pos, name, params):
		super(ADTName, self).__init__(pos)
		self.name_ = name
		self.params_ = params

	def accept(self, compPass):
		return compPass.visitName(self)