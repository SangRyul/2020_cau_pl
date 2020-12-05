#-*-coding utf-8-*-

import math
import itertools
import operator as op
from functools import reduce
from aparser import expression_parser
import numpy as np

lisp_to_python_dic = {
    '+': lambda *x: reduce(op.add, *x), '-': lambda *x: reduce(op.sub, *x),
    '*': lambda *x: reduce(op.mul, *x), '/': lambda *x: reduce(op.truediv, *x),
    '>': lambda x: op.gt(x[0], x[1]), '<': lambda x: op.lt(x[0], x[1]),
    '>=': lambda *x: op.ge(x[0], x[1]), '<=': lambda *x: op.le(x[0], x[1]),
    '=': lambda *x: reduce(op.eq, *x),
    'abs': abs,
    'append': lambda *x: reduce(op.add, *x),
    'apply': lambda x: x[0](x[1:]),
    'begin': lambda *x: x[-1],
    'car': lambda x: x[0][0],
    'cdr': lambda x: x[0][1:],
    'caddr': lambda x: ((x[0][1:])[1:])[0],
    'cons': lambda x: list(itertools.chain.from_iterable(x)),
    'nth': lambda x: nth_procedure(x),
    'reverse': lambda x: x[0][::-1],
    'eq?': op.is_,
    'equal?': op.eq,
    'length': lambda x: len(x[0]),
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
    'null': lambda x: print("T") if x == "NIL" else print("F"),
    'numberp': lambda x: number_procedure(x),
    'zerop': lambda x: print("T") if x[0] == 0 else print("F"), 
    'stringp' : lambda x : print("T") if(str(x[0]).startswith("\"")) else print("NIL"),
    'minusp': lambda x: minusp_procedure(x),
    'equal': lambda x: print("T") if x[0] == x[1] else print("F"),
    'member' : lambda x : x[1][x[1].index(x[0]):] if x[0] in x[1] else print("NIL"),
    'assoc' : lambda x : assoc_procedure(x),
    'remove' : lambda x : remove_procedure(x),
    'subst' : lambda x : subst_procedure(x)

}

lisp_to_python_dic.update(vars(math))
dic_new2 = {}

def cdr_procedure(x):
    list = x[0][1:]
    for i in list:
        print(i, end=' ')

def nth_procedure(x):
    lista = x[1]
    nth = x[0]

    if (isinstance(lista, list) == False):
        print('Error')
    elif nth >= len(lista):
        print('NIL')
    else:
        print(lista[nth])


def minusp_procedure(x):
    try:
        if str(type(int(str(x)[str(x).find("[") + 1: str(x).find("]")]))) == "<class 'int'>":
            if (int(str(x)[str(x).find("[") + 1: str(x).find("]")]) < 0):
                print("T")
            else:
                print("F")
    except ValueError:
        try:
            if str(type(float(str(x)[str(x).find("[") + 1: str(x).find("]")]))) == "<class 'float'>":
                if (float(str(x)[str(x).find("[") + 1: str(x).find("]")]) < 0):
                    print("T")
                else:
                    print("F")
        except ValueError:
            return print("Error")

def subst_procedure(x):
    if(x[1] in x[2]):
        for k in range(0,len(x[2])):
            if(x[1] == x[2][k]):
                x[2][k] = x[0]
        output_print(x[2])

        #print(x[2])
    else:
        print("NIL")

def remove_procedure(x):
    tmp = x[1][:]
    value = x[0] # 이게 제거 대상 요소
    if(value in tmp):
        for item in tmp:
            if item == value:
                tmp.remove(value)
        output_print(tmp)
        # print(type(tmp))
        # print(tmp)
    else:
        print("NIL")

def assoc_procedure(x):
    for k in x[1]:
        if(k[0] == x[0]):
            return k
    return "NIL"

def number_procedure(x):
    try:
        if str(type(int(str(x)[str(x).find("[") + 1: str(x).find("]")]))) == "<class 'int'>":
            return print("T")
    except ValueError:
        try:
            if str(type(float(str(x)[str(x).find("[") + 1: str(x).find("]")]))) == "<class 'float'>":
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

def output_print(x):
    if (isinstance(x, list)):
        x = np.array(x)
        x = x.flatten()

        # for item in x:
        #     return
        new_output = '(' + ' '.join(map(str,x)) + ')'
        print(new_output)
    else:
        print(x)

def eval(x, dic):

    global flaga
    flaga = 0
    if isinstance(x, str):
        if(x.startswith("\"")):
            return x
        try:
            '''
            if(isinstance(dic[x], int)):
                print(dic[x])
            '''
            #print(dic[x])
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
        return eval(exp, dic)

    elif x[0] == 'define':
        (_, var, exp) = x
        dic[var] = eval(exp, dic)
    elif x[0] == 'setq':
        (_, var, exp) = x

        if(isinstance(exp, list)):
            output_print(exp[1])
        else:
            print(exp)

        # if(exp[0] == 'quote'):
        #     print(exp[1])
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
    elif x[0] == 'cond':
        if (len(x) == 4):
            (_, test1, test2, test3) = x
            if eval(test1[0], dic):
                exp = eval(test1[1], dic)
                return eval(exp, dic)
                #print(eval(exp, dic))
            elif eval(test2[0], dic):
                exp = eval(test2[1], dic)
                return eval(exp, dic)
                #print(eval(exp, dic))
            elif eval(test3[0], dic):
                exp = eval(test3[1], dic)
                return eval(exp, dic)
                #print(eval(exp, dic))

    else:

        proc = eval(x[0], dic)
        args = [eval(exp, dic) for exp in x[1:]]
        print(args)
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


    '''
    if (isinstance(x, list)== True) :
        try:
            # return ('('+' '.join(x)+')')
            return (' '.join(x))

        except TypeError:
            x_ints = [str(int) for int in x]
            return ('('+' '.join(x_ints)+')')
    elif (isinstance(x, list) == False):
        return x
    '''
def run(data):
    tmp = expression_parser(data)

    if (tmp == None):
        print("NIL")
        return

    input_data = list(itertools.chain(*tmp))
    input_data = [x for x in input_data if x != ';']


    output = eval(input_data, lisp_to_python_dic)

    erase = [[None], "", None, [], [None, None], [[]]]
    if (output not in erase):

        output_print(output)
        # print(output)

repl_mode_buffer = []
def input_check_valid(data, user_input):

    multi_line_data_buffer = ""
    count_left_bracket = 0
    count_right_bracket = 0

    if(user_input == 1):
        pass
        # file mode
    elif(user_input == 2):
        repl_mode_buffer.append(data)
        data = repl_mode_buffer
        # repl mode

    for data in data:
        # multiline 받는 명령어도 축가해야함
        # (의 숫자와 )의 숫자를 비교할것
        if (data.startswith(";") or data == ''):
            continue
        for x in data:
            if (x == '('):
                count_left_bracket += 1
            elif (x == ')'):
                count_right_bracket += 1

        if (count_left_bracket == count_right_bracket):
            multi_line_data_buffer += data
            run(multi_line_data_buffer)
            # initialize again
            # no bracket
            if(count_left_bracket == 0):
                try:
                    print(lisp_to_python_dic[data])
                except:
                    print("The Variable IS UNBOUND")
            multi_line_data_buffer = ""
            repl_mode_buffer.clear()
            count_left_bracket, count_right_bracket = (0, 0)
        else:

            multi_line_data_buffer += data
            multi_line_data_buffer += " "

        # (의 숫자와 )자의 숫자가 동일해 졌을때 run에 data를 날려야 한다.
        # run(data)
def main():

    print("---- lisp interpreter -----")
    print("Please input a number")
    user_input = int(input("1: file mode / 2: repl mode / other number: quit program => "))
    while(True):
        data = None
        if(user_input == 1):
            file_name = "input.lsp"
            with open(file_name, 'r', encoding='UTF8') as f:
                data = f.read().splitlines()
                input_check_valid(data, user_input)
            break;

        elif(user_input == 2):
            data = input(">>> ")
            input_check_valid(data, user_input)
        else:
            print("bye")
            break

if __name__ == "__main__":
    main()
