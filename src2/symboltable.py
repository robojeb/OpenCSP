class SymbolTable:
	def __init__(self):
		self.stack_ = []
		self.stack_.append({})

	def enterContext(self):
		self.stack_.append({})

	def leaveContext(self):
		self.stack_.pop()

	def insert(self, name, data):
		self.stack_[-1][name] = data

	def lookup(self, name):
		for i in reversed(range(0, len(self.stack_))):
			if name in self.stack_[i]:
				return True, self.stack_[i][name]
		return False, None

