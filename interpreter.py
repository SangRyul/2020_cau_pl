# interpreter

import math
import itertools
import operator as op
from functools import reduce
from aparser import expression_parser

lisp_to_python_dic = {
    '+': lambda *x: reduce(op.add, *x), '-': lambda *x: reduce(op.sub, *x),
    '*': lambda *x: reduce(op.mul, *x), '/': lambda *x: reduce(op.truediv, *x),
    '>': lambda *x: reduce(op.gt, *x), '<': lambda *x: reduce(op.lt, *x),
    '>=': lambda *x: reduce(op.ge, *x), '<=': lambda *x: reduce(op.le, *x),
    '=': lambda *x: reduce(op.eq, *x),
    'abs': abs,
    'append': lambda *x: reduce(op.add, *x),
    'apply': lambda x: x[0](x[1:]),
    'begin': lambda *x: x[-1],
    'car': lambda x: x[0],
    'cdr': lambda x: x[1:],
    'cons': lambda x: print(x),
    'reverse': lambda x: x[::-1],
    'eq?': op.is_,
    'equal?': op.eq,
    'length': len,
    'list': lambda *x: list(x),
    'list?': lambda x: isinstance(x, list),
    'map': map,
    'max': max,
    'min': min,
    'not': op.not_,
    'null?': lambda x: x == [],
    'number?': lambda x: isinstance(x, int) or isinstance(x, float),
    'procedure?': callable,
    'round': round,
    'symbol?': lambda x: isinstance(x, str),
    'print': lambda x: print(x[0]),
    'null': lambda x: print("T") if x == "NIL" else print("F" + str(x)),
    'numberp': lambda x: number_procedure(x),
    'zerop': lambda x: print("T") if str(x) == "[0]" else print("F" + str(x)),
    'stringp' : lambda x : print("T") if(str(x[0]).startswith("\"")) else print("F"),
    'member' : lambda x : x[1][x[1].index(x[0]):] if x[0] in x[1] else print("NIL"),
    'assoc' : lambda x : assoc_procedure(x),
    'remove' : lambda x : remove_procedure(x),
    'subst' : lambda x : subst_procedure(x)

}

lisp_to_python_dic.update(vars(math))

dic_new2 = {}

def subst_procedure(x):
    if(x[1] in x[2]):
        for k in range(0,len(x[2])):
            if(x[1] == x[2][k]):
                x[2][k] = x[0]
        print(x[2])
    else:
        print("NIL")

def remove_procedure(x):
    tmp = x[1][:]
    value = x[0]
    if(value in tmp):
        tmp.remove(value)
        print(tmp)
        return
    else:
        print("NIL")

def assoc_procedure(x):
    for k in x[1]:
        if(k[0] == x[0]):
            return k
    return "NIL"

def number_procedure(x):
    try:
        print(str(type(int(str(x)[str(x).find("[") + 1: str(x).find("]")]))))
        if str(type(int(str(x)[str(x).find("[") + 1: str(x).find("]")]))) == "<class 'int'>":
            return print("T")
    except ValueError:
        return print("F")



def lambda_procedure(parms, body, *args):
    dic_new = {}
    for k, v in list(zip(parms, list(*args))):
        dic_new[k] = v
    dic_new2.update(lisp_to_python_dic)
    dic_new2.update(dic_new)
    return eval(body, dic_new2)


def eval(x, dic):
    # print(x)
    global flaga
    flaga = 0
    if isinstance(x, str):
        if(x.startswith("\"")):
            return x
        try:
            return dic[x]
        except:
            return x
    elif isinstance(x, int):
        return x
    elif not isinstance(x, list):
        return x
    elif x[0] == 'quote':
        flaga = 1
        # quote 다음에 하나라면 변수로 취급해야한다.
        # quote 다음에 문자열 변수가 오면 문자열 취급
        # qoute 다음에 괄호안에 둘러싸인 리스트 형태로 오면 괄호 취급
        # if isinstance(x[1],str):
        #     dic[x[1]] = x[1]
        #     print(dic[x[1]])
        #     return dic[x[1]]
        # else:
        (_, exp) = x
        return exp
    elif x[0] == 'if':
        if (len(x) == 3):
            (_, test, conseq) = x
            exp = eval(conseq, dic) if eval(test, dic) else print("NIL")
        elif (len(x) == 4):
            (_, test, conseq, alt) = x
            exp = eval(conseq, dic) if eval(test, dic) else eval(alt, dic)
        # print(x)
        return eval(exp, dic)

    elif x[0] == 'define':
        (_, var, exp) = x
        dic[var] = eval(exp, dic)
    elif x[0] == 'setq':
        (_, var, exp) = x
        # print(var)
        # print(exp)

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
    # elif x[0] == 'car':
    #     (_, var, exp) = x
    #     dic[var] = eval(exp, dic)
    elif x[0] == 'atom':
        (_, var) = x
        if var[0] == "quote":
            return "True"
        else:
            return "False"
    # elif x[0] == 'null':
    #     (_, var) = x
    #     if var == "NIL":
    #         return "T"
    #     else:
    #         return "F"
    # elif x[0] == 'NUMBERP':
    #     (_, var) = x
    #     if str(type(var)) == "<class 'int'>":
    #         return "T"
    #     else:
    #         return "F"
    # elif x[0] == 'ZEROP':
    #     (_, var) = x
    #     if var == 0 :
    #         return "T"
    #     else:
    #         return "ERROR"

    elif x[0] == 'minusp':
        try:
            (_, var, exp) = x
            if (var == '-'):
                if (isinstance(exp, int)):
                    return 'T'
        except:
            return 'Error'
    elif x[0] == 'equal':
        (_, var, exp) = x
        if (var == exp):
            return 'T'
        else:
            return 'NIL'
    # elif x[0] == 'stringp':
    #
    #     try:
    #         (_, dq1, *_, dq2) = x
    #         print(_, dq1, *_, dq2)
    #         print("ASdf")
    #         if (dq1 == '"' and dq2 == '"'):
    #             return 'T'
    #     except:
    #         return 'NIL'

    else:

        proc = eval(x[0], dic)
        args = [eval(exp, dic) for exp in x[1:]]

        # return proc(args)
        try:
            # if(type(args) == list and args[0] is not None):
            #    return proc(sum(args,[]))
            try:
                return proc(args)
            except:
                return proc(list(itertools.chain(*args)))
                #if (len(args)!=0 and args[0] is not None and flaga):
                    #return proc(list(itertools.chain(*args)))
        except TypeError:
            return args
            pass


# print(eval([['setq', 'foo', ['quote', [1, 2, 3]]], ['print', 'foo']], lisp_to_python_dic))
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
    a = []
    file_name = "example2.lsp"
    with open(file_name, 'r') as f:
        data = f.read().strip()

    tmp = expression_parser(data)

    if(tmp == None):
        print("NIL")
        return
    input_data = list(itertools.chain(*tmp))
    print(input_data)
    output = eval(input_data, lisp_to_python_dic)

    # useless part
    erase = [[None], "", None, [], [None, None]]
    if(output not in erase):
        print(output)
    # print(eval(input_data, lisp_to_python_dic))


if __name__ == "__main__":
    main()
