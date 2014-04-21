#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DactylParser import DactylParser
from DactylSemant import DactylASTSemantics
from compilerpass import CompileError, UndefError
from parampass import ParamPass, ParamInitPass
from usedefpass import UseDef

p = DactylParser()

with open("test.dac") as f:
	text = f.read()

ast = p.parse(text, rule_name="file", semantics=DactylASTSemantics(), comments_re="\(\*.*?\*\)")

paramPass = ParamPass()

try:
	ast1 = ast.accept(paramPass)
	print ast1
	ast1.accept(ParamInitPass())
	ast1.accept(UseDef())
	#useDefPass = UseDef()
	#ast1.accept(useDefPass)
except CompileError as e:
	print(e.value_)
except UndefError as e:
	print(e.value_)

#print ast1
#print str(preDecl.paramMap_)