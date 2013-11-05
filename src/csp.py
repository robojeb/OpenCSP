# coding=UTF-8

from cspadt import *
from pyparsing import *
import sys


#Convert to ADT

def stripSemiColon(str, pos, tok):
	return tok[0]

def makeSequence(str, pos, tok):
	return Sequence(tok)

def makeAssign(str, pos, tok):
	return Assign(tok[0], tok[2])

def makeProgram(str, pos, tok):
	return Program(tok[0], tok[3])

def makeValue(str, pos, tok):
	return Value(tok[0])

def makeOperator(str, pos, tok):
	return Operator(tok[1], tok[0], tok[2])

def makeRun(str, pos, tok):
	return Run(tok[1])

def makePrint(str, pos, tok):
	return Write(tok[1])

def makeBoolean(str, pos, tok):
	if str == "true":
		return "True"
	else:
		return "False"

def makeIf(str, pos, tok):
	return IF(tok[1])

def makeBranch(str, pos, tok):
	if len(tok) == 4:
		return (tok[1], tok[3])
	else:
		return (tok[0], tok[2])

def makePredicate(str, pos, tok):
	return Predicate(tok[1], tok[0], tok[2])

def stripBar(str, pos, tok):
	return tok[1]

def makeBinOp(str, pos, tok):
	if tok[0] == "=":
		return "=="
	else:
		return tok[0]

def makeLoop(str, pos, tok):
	return LOOP(tok[1])

def makeSemaphoreAction(str, pos, tok):
	return SemAct(tok[0], tok[2])

def makeSemaphore(str, pos, tok):
	return Sem(tok[1], tok[3])

#def makeVar(str, pos, tok):
#	return "V" + str(len(tok[0])) + "_" + tok[0]

def mangle(string, type):
	return type + str(len(string)) + "_" + string

def makeChannel(str, pos, tok):
	procName0 = mangle(tok[1], "P")
	procName1 = mangle(tok[5], "P")
	return ChannelDef(procName0, tok[3], procName1, tok[7])

def makeChannelAction(str, pos, tok):
	read = False
	if tok[1] == "?":
		read = True
	return ChannelAct(read, tok[0], tok[2])

#Parsing instrucitons

PFile = Forward()
PCmd = Forward()
PProg = Forward()
PSeq = Forward()
PExp = Forward()
PProd = Forward()
PPred = Forward()
PIf = Forward()
PLoop = Forward()
#PEndIf = Forward()
PVar = Word(alphas, alphanums).setParseAction(lambda s,p,t: mangle(t[0], "V"))
PChan = Word(alphas, alphanums).setParseAction(lambda s,p,t: mangle(t[0], "C"))
PName = Word(alphas, alphanums)
PBool = (Keyword("true") | Keyword("false")).setParseAction(makeBoolean)
PVal = (PBool | PVar | Word(nums)).setParseAction(makeValue)
PBinOp = (Keyword("=") | Keyword("<=") | Keyword(">=") | Keyword("&") | Keyword("|") | Keyword("!=") | Keyword("<") | Keyword(">")).setParseAction(makeBinOp)
PSemAct = ((Literal("P") | Literal("V")) + "(" + PName + ")").setParseAction(makeSemaphoreAction)
PSem = (Keyword("semaphore") + PName + ":=" + PVal).setParseAction(makeSemaphore)

PChanDef = (Keyword("channel") + PName + ":" + PName + "->" + PName + ":" + PName).setParseAction(makeChannel)
PChanAct = (PName + (Literal("?") | Literal("!")) + PExp).setParseAction(makeChannelAction)

PFile << (OneOrMore((PCmd + ";").setParseAction(stripSemiColon) | (PProg + ";").setParseAction(stripSemiColon)).setParseAction(makeSequence))

PCmd << (PChanDef | PChanAct | (PVar + ":=" + PExp).setParseAction(makeAssign) | ("run(" + PName + ")").setParseAction(makeRun) | ("print(" + PExp + ")").setParseAction(makePrint) | PSem | PSemAct)

PProg << (PName + "::=" + "[" + PSeq + "]").setParseAction(makeProgram)

PSeq << (OneOrMore((PIf + ";").setParseAction(stripSemiColon) | (PLoop + ";").setParseAction(stripSemiColon) | (PCmd + ";").setParseAction(stripSemiColon)).setParseAction(makeSequence))

PExp << (((PProd + "+" + PExp) | (PProd + "-" + PExp)).setParseAction(makeOperator) | PProd)

PProd << (((PVal + "*" + PProd) | (PVal + "/" + PProd)).setParseAction(makeOperator) | PVal)

PBranch = (Optional("|") + PPred + "->" + PSeq).setParseAction(makeBranch)

PIf << ("[" + OneOrMore(PBranch).setParseAction(lambda s,p,t:[t]) + "]").setParseAction(makeIf)

PLoop << ("*[" + OneOrMore(PBranch).setParseAction(lambda s,p,t:[t]) + "]").setParseAction(makeLoop)

#PEndIf << (OneOrMore(("|" + PPred + "->" + PSeq).setParseAction(makeBranch)) | Empty().setParseAction(lambda: []))

PPred << (PExp + PBinOp + PExp).setParseAction(makePredicate)


# Read and compile the file

if not len(sys.argv) == 3:
	print "Must provide: python csp.py <input> <output>"
	sys.exit(0)

in_file = open(sys.argv[1], "r")
out_file = open(sys.argv[2], "w")

in_string = in_file.read()

ADT = PFile.parseString(in_string)[0]

p = Printer(out_file)

#print ADT.commands
#print test

p.outnl(header)
ADT.getGlobalVariables()
ADT.pp(p)
for prog in activeThreads:
	p.outnl(prog + "_.join()")


