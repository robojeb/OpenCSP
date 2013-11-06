import sys
from threading import Semaphore


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
	
#ADT class for storing a variable name
class ADTVariable:
	def __init__(self, name):
		#Mangle the variable name to prevent conflicts with internal names
		self.name = "V" + str(len(name)) + "_" + name
		
	def compile(self, printer, environment):
		#For variables we only want to put the variable name down
		printer.out(self.name)
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
		
#ADT class for tuples
class ADTTuple:
	def __init__(self, values):
		self.values = values
		
	def compile(self, printer, environment):
		#create a python tuple
	