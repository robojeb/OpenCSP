from cspadt import *
from pyparsing import *
import sys

#Parse a list of objects deliminated by a specified character
# e.g. ListParser(Literal("A"), Literal(",")) should parse
# A, A, A
def ListParser(parsephrase, delimiter):
	return (OneOrMore(parsephrase + Suppress(Optional(delimiter))))

# -- Forward declarations of parsers for use later --
PExpression = Forward()

# -- Base data values --
# Parser and ADT constructors for the following
# Name -> [a-zA-Z]+[a-zA-Z0-9]?
# String -> A quoted string
# Number -> [0-9]+\.[0-9]?

def makeName(string, pos, tok):
	return ADTName(tok[0])

PName = Word(alphas, alphanums).setParseAction(makeName)

def makeString(string, pos, tok):
	return ADTString(tok[0])

PString = (quotedString).setParseAction(makeString)

def makeNumber(string, pos, tok):
	if len(tok) == 1:
		return ADTNumber(tok[0])
	elif len(tok) == 3:
		return ADTNumber(tok[0] + tok[1] + tok[2])
	else:
		#Either we have a decimal or we don't otherwise die
		sys.stderr.write()
		sys.exit(1)

PNumber = (Word(nums) + Optional(Literal(".") + OneOrMore(nums))).setParseAction(makeName)

# -- Parameterization options --
# Parameterized -> Name<Expression,Expression> | Name<Expression>
PParameterized = PName + Literal("<") + (PExpression + ZeroOrMore(Literal(",") + PExpression)) + Literal(">")

# -- Arithmetic --
# Expression -> Product + Expression | Product - Expression | Product
# Product -> Value / Product | Value * Product | Value

# Forward declare Expression and Product so that we can do recursive definitions
PProduct = Forward()
PValue = PName | PString | PName

PExpression << ((PProduct + (Literal("+") | Literal("-")) + PExpression) | PProduct)

PProduct << ((PValue + (Literal("*") | Literal("/")) + PProduct) | PValue)

# -- Basic operations --
# Assignment -> PName := Expression
# SemaphoreOp -> P(Name) | V(Name)

PAssign = PName + Literal(":=") + PExpression
PSemaphoreOp = (Literal("P") | Literal("V")) + Literal("(") + PName + Literal(")")

# -- ControlFlow Operations --
# Sequence -> ListDelimitedBy((Assignment | If | Loop), ";")
# If -> []

PSequence = ListParser((PAssign | PSemaphoreOp), Literal(";"))

# -- Arithmetic --
# Program -> (Assignment; | SemaphoreDef; | ProcessDef; | ProcessExec;)+
# Assignment -> Variable := Expression
# 