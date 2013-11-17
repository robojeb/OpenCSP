import sys


#Pretty printing data structure
class Printer:
	def __init__(self, file = sys.stdout):
		self.indentLevel = 0
		self.startLine = False
		self.file = file
	
	# Increase indentation level by one
	def indent(self):
		self.startLine = True
		self.indentLevel += 1

	#decrease indentation level by one
	def dedent(self):
		self.startLine = True
		self.indentLevel -= 1

	#If we are at the beginning of a line this prints the appropriate number of
	#tabs given the indentation level. It then prints the provided string.
	def out(self, string):
		if self.startLine == True:
			tabs = '\t'*self.indentLevel
			self.file.write(tabs + string)
		else:
			self.file.write(string)
		self.startLine = False
	#If we are at the beginning of a line this prints the appropriate number of
	#tabs given the indentation level. It then prints the provided string 
	#followed by a newline character.
	def outln(self, string):
		if self.startLine == True:
			tabs = '\t'*self.indentLevel
			self.file.write(tabs + string + '\n')
		else:
			self.file.write(string + '\n')
		self.startLine = True

	#Explicitly print a newline character
	def newline(self):
		self.startLine = True
		self.file.write('\n')

#ADT Classes

'''
These classes have only one required function. That function is compile
which takes in a printer and an environment. The function then returns
the environment with any modifications it made.
'''

#	
# Base level ADT structures for storing values
#   - Name (A name for a variable, semaphore, program, or channel)
#   - Number (float/int)
#   - String (for printing)
#

#ADT class for storing a variable, semaphore, program, or channel name
#Prefix is the mangler prefix V,S,P,C respectively
class ADTName:
	def __init__(self, name):
		#Default prefix is that this is a variable rather than other types
		self.prefix = "V"
		#Mangle the variable name to prevent conflicts with internal names
		self.name = str(len(name)) + "_" + name
		
	def setPrefix(self, prefix):
		self.prefix = prefix

	def compile(self, printer, environment):
		#For variables we only want to put the variable name down
		printer.out(self.prefix + self.name)
		return environment

#ADT class for numeric constants
class ADTNumber:
	def __init__(self, value):
		self.value = value

	def compile(self, printer, environment):
		#Simply print the value
		printer.out(self.value)
		return environment
	
#ADT class for string constants
class ADTString:
	def __init__(self, value):
		self.value = value
		
	def compile(self, printer, environment):
		#Print a quoted string
		printer.out("\"")
		printer.out(self.value)
		printer.out("\"")
		return environment
	
#
# ADT Strucures for operators
#   - Expression (Arithmetic operations +,-,/,*,())
#   - Assignment (Variable assighment, v := Expression)
#   - Semaphore (P, V operations on semaphores)
#

class ADTExpression:
	def __init__(self, operator, expr1, expr2):
		self.operator = operator
		self.expr1 = expr1
		self.expr2 = expr2
		
	def compile(self, printer, environment):
		pass

class ADTAssignment:
	def __init__(self, variable, expression):
		self.var = variable
		self.expr = expression

	def compile(self, printer, environment):
		pass

class ADTSemaphore:
	def __init__(self, semaphore):
		self.sem = semaphore

	def compile(self, printer, environment):
		pass
		
#
# ADT Control flow
#   - Sequence (A sequential run of operations)
#   - If (Conditional if)
#   - Loop (Conditional loop)
#   - Process (A sequence of actions that can be run as a process)
#   - Program (A restricted sequence of events for setting up the environment)
#   TODO: Parallel (Runing two sequences in parallel)
#

class ADTSequence:
	def __init__(self, operations):
		self.ops = operations

	def compile(self, printer, environment):
		pass

class ADTIf:
	def __init__(self, branches):
		self.branches = branches

	def compile(self, printer, environment):
		pass

class ADTLoop:
	def __init__(self, branches):
		self.branches = branches

	def compile(self, printer, environment):
		pass

class ADTProcess:
	def __init__(self, sequence):
		self.seq = sequence

	def compile(self, printer, environment):
		pass

class ADTProgram:
	def __init__(self, operations):
		self.ops = operations

	def compile(self, printer, environment):
		pass

# 
# ADT For Definitions
#   - Parameterized (Define a name to be parameterized over a set of numbers)
#

class ADTParameterized:
	def __init__(self, name, parameter_1):
		self.name = name
		self.param1 = parameter_1

	def compile(self, printer, environment):
		pass

class ADTSemaphoreDef:
	def __init__(self, process_1, process_2, channel_1, channel_2):
		self.proc1 = process_1
		self.proc2 = process_2
		self.chan1 = channel_1
		self.chan2 = channel_2

	def compile(self, printer, environment):
		pass