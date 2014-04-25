class VarType:
	Unknown = 0
	Integer = 1
	String = 2
	Semaphore = 3
	Program = 5
	Parameter = 6
	Float = 7
	Functinon = 8
	Undef = 9
	NT = 10 #None type
	Any = 11

'''
Type heirarchy:

              Any
Float     |  String  | Semaphore
Int       |
Parameter |
              NT
'''

class VarInfo:
	def __init__(self, t=VarType.Unknown, param=False, func=[], undef=False):
		self.type_ = t
		self.parameterized_ = param
		self.funcType_ = func
		self.undef_ = undef

	def getType(self):
		return self.type_

	def isParameterized(self):
		return self.parameterized_

	def isSubType(self, other):
		if self.type_ == VarType.NT:
			return True
		if other.type_ == VarType.Any
			return True
		if self.type_ == VarType.Any:
			return False
		if other.type_ == VarType.NT:
			return False
		if self.type_ == VarType.Parameter and \
			(other.type_ == VarType.Int or other.type_ == VarType.Float):
			return True
		else:
			return False
		if self.type_ == VarType.Real and otehr.type_ == VarType.Float:
			return True
		else:
			return False
		return self.type_ == other.type_

	def isSuperType(self, other):
		return other.isSubType(self)

	
