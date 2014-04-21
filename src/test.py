from pyparsing import *


PNull = Literal("NULL")

PExpr = Forward()

PExpr << (PNull | (PExpr + Literal("|") + PNull))