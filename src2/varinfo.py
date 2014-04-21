class VarType:
	Unknown = 0
	Integer = 1
	String = 2
	Semaphore = 3
	Program = 5
	Parameter = 6
	Float = 7
	Functino = 8
	Undef = 9

class VarInfo:
	def __init__(self, t=VarType.Unknown, param=False, func=[]):
		self.type_ = t
		self.parameterized_ = param
		self.funcType = func

	def getType(self):
		return self.type_

	def isParameterized(self):
		return self.parameterized_

