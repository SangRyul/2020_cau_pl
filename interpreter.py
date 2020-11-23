#interpreter

import math
import operator as op
from functools import reduce
from aparser import expression_parser

lisp_to_python_dic = {
    '+':lambda *x: reduce(op.add, *x), '-':lambda *x: reduce(op.sub, *x),
    '*':lambda *x: reduce(op.mul, *x), '/':lambda *x: reduce(op.truediv, *x),
    '>':lambda *x: reduce(op.gt, *x), '<':lambda *x: reduce(op.lt, *x),
    '>=':lambda *x: reduce(op.ge, *x), '<=':lambda *x: reduce(op.le, *x),
    '=':lambda *x: reduce(op.eq, *x),
    'abs':     abs,
    'append':  lambda *x: reduce(op.add, *x),
    'apply':   lambda x: x[0](x[1:]),
    'begin':   lambda *x: x[-1],
    'car':     lambda x: x[0],
    'cdr':     lambda x: x[1:],
    'cons':    lambda x, y: [x] + y,
    'reverse': lambda x: x[::-1],
    'eq?':     op.is_,
    'equal?':  op.eq,
    'length':  len,
    'list':    lambda *x: list(x),
    'list?':   lambda x: isinstance(x, list),
    'map':     map,
    'max':     max,
    'min':     min,
    'not':     op.not_,
    'null?':   lambda x: x == [],
    'number?': lambda x: isinstance(x, int) or isinstance(x, float),
    'procedure?': callable,
    'round':   round,
    'symbol?': lambda x: isinstance(x, str),
    'print' : lambda x : print(x),

    }

lisp_to_python_dic.update(vars(math))

dic_new2 = {}

def lambda_procedure(parms, body, *args):
    dic_new = {}
    for k, v in list(zip(parms, list(*args))):
        dic_new[k] = v
    dic_new2.update(lisp_to_python_dic)
    dic_new2.update(dic_new)
    return eval(body, dic_new2)

def eval(x, dic):

    if isinstance(x, str):
        return dic[x]
    elif isinstance(x, int):
        return x
    elif not isinstance(x, list):
        return x
    elif x[0] == 'quote':
        (_, exp) = x
        return exp
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        # print(x)
        exp = eval(conseq,dic) if eval(test, dic) else eval(alt,dic)
        return eval(exp, dic)
    elif x[0] == 'define':
        (_, var, exp) = x
        dic[var] = eval(exp, dic)
    elif x[0] == 'setq':
        (_, var, exp) = x
        dic[var] = eval(exp, dic)
    elif x[0] == 'set':
        (_, var, exp) = x
        # print(var, exp)
        dic[var[1]] = eval(exp, dic)
        # quote 붙을거 예상해서 1번으로 가야함
        # print(_, var, exp);

    elif x[0] == 'lambda':
        (_, parms, body, *args) = x
        return lambda_procedure(parms, body, args)
    elif x[0] == 'car':
        (_, var, exp) = x
        dic[var] = eval(exp, dic)
    elif x[0] == 'atom':
        (_, var) = x
        if str(type(var)) == "<class 'str'>":
            return "True"
        else:
            return "False"
    elif x[0] == 'null':
        (_, var) = x
        if str(type(var)) == "<class 'NoneType'>":
            return "T"
        else:
            return "F"
    elif x[0] == 'NUMBERP':
        (_, var) = x
        if str(type(var)) == "<class 'int'>":
            return "T"
        else:
            return "F"
    elif x[0] == 'ZEROP':
        (_, var) = x
        if var == 0 :
            return "T"
        else:
            return "ERROR"

    elif x[0] == 'minusp':
        try:
            (_, var, exp) = x
            if(var=='-'):
                if(isinstance(exp,int)):
                    return 'T'
        except:
                return 'Error'
    elif x[0] == 'equal':
        (_, var, exp) = x
        if(var==exp):
            return 'T'
        else:
            return 'NIL'
    elif x[0] == 'stringp':
        try:
            (_,dq1,*_,dq2)=x
            if(dq1=='"' and dq2=='"' ):
                return 'T'
        except:
            return 'NIL'

    else:
        proc = eval(x[0], dic)
        args = [eval(exp, dic) for exp in x[1:]]
        # print(proc)
        # print(args)

        # print(proc(args))

        if(args[0] is not None):
            return proc(args)
        else:
            return


# print(eval(['define', 'x', 100], lisp_to_python_dic))
#
# print(eval(['setq', 'x', 2], lisp_to_python_dic))
# print(eval(['define', 'y', 5], lisp_to_python_dic))
# print(eval(['print', ['+', 'x', 2]], lisp_to_python_dic))
# print(eval(['lambda', ['x', 'y'], ['*', 'x', 'y'], 5, 2], lisp_to_python_dic))
#
# print(eval(['*', ['+', 5, 7], ['/', 4, 2]], lisp_to_python_dic))
#
# print(eval(['*', 'x', 'x'], lisp_to_python_dic))
#
# print(eval(expression_parser('(+ 5 (* 3 2) )')[0], lisp_to_python_dic))
#
# print(eval(['>', 5 ,10], lisp_to_python_dic))
#
# print(eval(['if', ['<', 5 ,10], ['+', 10, 5],['-', 10, 5]], lisp_to_python_dic))

def main():
    # file_name = input()
    file_name = "example2.lsp"
    with open(file_name, 'r') as f:
        data = f.read().strip()
    # print(expression_parser(data))
    # print(expression_parser(data).pop(0))
    print(eval(expression_parser(data).pop(0), lisp_to_python_dic))
    # print(eval(expression_parser(data).pop(0), lisp_to_python_dic))

if __name__ == "__main__":
    main()

