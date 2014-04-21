from ast import *

class DactylASTSemantics(object):
    def file(self, ast):
        if isinstance(ast['oper'], list):
            return ASTFile(None, ast['oper'])
        return ASTFile(None, [ast['oper']])

    def assign(self, ast):
        return ASTAssign(None, ast["n"], ast["e"])

    def define(self, ast):
        return ASTDefine(None, ast["n"], ast["p"])

    def expr(self, ast):
        if isinstance(ast, dict):
            if "op" in ast and ast["op"] != None:
                return ASTExpression(None, ast["op"], ast["e1"], ast["e2"])
            else:
                return ast["e1"]
        return ast

    def exprAnd(self, ast):
        if isinstance(ast, dict):
            if "op" in ast and ast["op"] != None:
                return ASTExpression(None, ast["op"], ast["e1"], ast["e2"])
            else:
                return ast["e1"]
        return ast

    def exprEq(self, ast):
        if isinstance(ast, dict):
            if "op" in ast and ast["op"] != None:
                return ASTExpression(None, ast["op"], ast["e1"], ast["e2"])
            else:
                return ast["e1"]
        return ast

    def exprComp(self, ast):
        if isinstance(ast, dict):
            if "op" in ast and ast["op"] != None:
                return ASTExpression(None, ast["op"], ast["e1"], ast["e2"])
            else:
                return ast["e1"]
        return ast

    def exprAdd(self, ast):
        if isinstance(ast, dict):
            if "op" in ast and ast["op"] != None:
                return ASTExpression(None, ast["op"], ast["e1"], ast["e2"])
            else:
                return ast["e1"]
        return ast

    def exprMul(self, ast):
        if isinstance(ast, dict):
            if "op" in ast and ast["op"] != None:
                return ASTExpression(None, ast["op"], ast["e1"], ast["e2"])
            else:
                return ast["e1"]
        return ast

    def exprUni(self, ast):
        if isinstance(ast, dict):
            if "op" in ast and ast["op"] != None:
                return ASTExpression(None, ast["op"], ast["e1"], None)
            else:
                return ast["e1"]
        return ast

    def exprParen(self, ast):
        if isinstance(ast, dict):
            return ast["e1"]
        return ast

    def value(self, ast):
        return ast

    def number(self, ast):
        if isinstance(ast, list):
            return ASTNum(None, float(ast[0] + ast[1] + ast[2]))
        return ASTNum(None, int(ast))

    def string(self, ast):
        return ASTNum(None, ast)

    def identifier(self, ast):
        return ast

    def name(self, ast):
        if "param" in ast:
            return ASTName(None, ast["ident"], ast["param"])
        return ASTName(None, ast["ident"], [])

    def parameters(self, ast):
        if isinstance(ast, list):
            return [ast[0]] + ast[2]
        return [ast]

    def program(self, ast):
        return ASTProgram(None, ast["s"])

    def sequence(self, ast):
        if isinstance(ast["oper"], list):
            return ASTSequence(None, ast["oper"])
        return ASTSequence(None, [ast["oper"]])

    def ifblk(self, ast):
        return ASTIf(None, ast[1])

    def loop(self, ast):
        return ASTLoop(None, ast[1])

    def branches(self, ast):
        if "bl" in ast:
            if isinstance(ast["bl"], list):
                ast["bl"].append(ast["b1"])
                return ast["bl"]
            else:
                return [ast["b1"], ast["bl"]]
        return [ast["b1"]]

    def branch(self, ast):
        return ASTBranch(None, ast["cond"], ast["op"])

    def semdef(self, ast):
        return ast

    def semop(self, ast):
        return ast

    def spawnop(self, ast):
        return ASTSpawn(None, ast["n"])

    def range(self, ast):
        return ASTRange(None, int(ast[1]), int(ast[3]))

    def int(self, ast):
        return ast["num"]
