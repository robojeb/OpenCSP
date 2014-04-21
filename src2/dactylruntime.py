class ParamDict(object):
	def __init__(self, default):
		self.default_ = default
		self.dict_ = {}

	def __getitem__(self, index):
		if index in self.dict_:
			return self.dict_[index]
		else:
			return self.default_(index)

	def __setitem__(self, index, val):
		self.dict_[index] = val


class ParamExpr(object):
	def __init__(self):
		pass

	def __call__(self, arg):
		if isinstance(arg, tuple):
			return arg[0]
		else:
			return arg