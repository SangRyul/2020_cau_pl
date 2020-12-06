
# 프로그래밍 언어론 04분반 PL Team Project
# Lisp Interpreter 구현 프로젝트

# 참여자:
# 창의ICT공과대학 컴퓨터공학부(컴퓨터공학전공) 20165020 김상렬
# 창의ICT공과대학 소프트웨어학부 20181154 선민승
# 소프트웨어대학 소프트웨어학부 20190143 고은서

# 파일 정보:
# 프로그램 명: interpreter.py
# 역할: interpreter
# 생성 날짜: 2020.11.10

import math
import itertools
import operator as op
from functools import reduce
from aparser import expression_parser
import numpy as np

# eval 함수가 입력받는 x에 따라 실핼시킬 세부 함수(procedures).
lisp_to_python_dic = {
    '+': lambda *x: reduce(op.add, *x), '-': lambda *x: reduce(op.sub, *x),
    '*': lambda *x: reduce(op.mul, *x), '/': lambda *x: reduce(op.truediv, *x),
    '>': lambda x: op.gt(x[0], x[1]), '<': lambda x: op.lt(x[0], x[1]),
    '>=': lambda *x: op.ge(x[0], x[1]), '<=': lambda *x: op.le(x[0], x[1]),
    '=': lambda *x: reduce(op.eq, *x),

    # append - 주어진 여러 개의 리스트들을 하나의 리스트로 만듬, add 사용
    'append': lambda *x: reduce(op.add, *x),

    # car 함수 - 리스트의 첫번째 원소를 리턴
    'car': lambda x: x[0][0],
    # cdr 함수 - 리스트의 첫번째 원소를 제외한 나머지 값들을 리스트로 리턴
    'cdr': lambda x: x[0][1:],
    # caddr 함수 - CAR과 CDR을 혼합 사용한 경우
    'caddr': lambda x: ((x[0][1:])[1:])[0],
    # CONS 함수 - 기존의 리스트에 새로운 원소 추가하여 리스트 생성
    'cons': lambda x: list(itertools.chain.from_iterable(x)),
    # NTH 함수 - N번째 원소 리턴
    'nth': lambda x: nth_procedure(x),
    # REVERSE 함수 - 리스트 안의 원소의 순서를 거꾸로 바꿈
    'reverse': lambda x: x[0][::-1],
    # LENGTH 함수 - 주어진 리스트 내의 원소 개수 리턴
    'length': lambda x: len(x[0]),
    # LIST 함수 - 원소들을 모아서 새로운 리스트 구조 생성
    'list': lambda *x: list(x),
    # PRINT 함수 - 원소 출력
    'print': lambda x: print(x[0]),
    # NULL 함수 - X가 NIL일때만 참을 반환
    'null': lambda x: print("T") if x[0] == "NIL" else print("F"),
    # NUMBERP 함수 - X가 숫자일 때만 참을 반환
    'numberp': lambda x: number_procedure(x),
    # ZEROP 함수 - X가 0일 때만 참을 반환
    'zerop': lambda x: print("T") if x[0] == 0 else print("F"),
    # STRINGP 함수 - X가 STRINGP일 때 참을 반환
    'stringp' : lambda x : print("T") if(str(x[0]).startswith("\"")) else print("NIL"),
    # MINUSP 함수 - X가 음수일 때만 참을 반환
    'minusp': lambda x: minusp_procedure(x),
    # EQUAL 함수 - X와 Y가 같으면 참을 반환
    'equal': lambda x: print("T") if x[0] == x[1] else print("F"),
    # MEMBER 함수 - 주어진 리스트 내에 어떤 원소가 있는지 확인
    'member' : lambda x : x[1][x[1].index(x[0]):] if x[0] in x[1] else print("NIL"),
    # ASSOC 함수 -  리스트를 원소로 갖는 리스트에서 원소 리스트의 첫번째 원소를 DB에서의 KEY처럼 사용하여 원하는 리스트를 찾음
    'assoc' : lambda x : assoc_procedure(x),
    # REMOVE 함수 - 첫번째 인자를 두번째 인자로 받는 리스트에서 찾아 모두 제거하는 함수
    'remove' : lambda x : remove_procedure(x),
    # SUBST 함수 - 세번째 인자에서 두번째 인자를 찾아 첫번째 인자로 대치
    'subst' : lambda x : subst_procedure(x)
}

lisp_to_python_dic.update(vars(math))
dic_new2 = {}

# CDR 처리 함수
def cdr_procedure(x):
    list = x[0][1:]
    for i in list:
        print(i, end=' ')

# NTH 처리 함수
def nth_procedure(x):
    lista = x[1]
    nth = x[0]
    # list인지 확인
    if (isinstance(lista, list) == False):
        print('Error')
    # list 범위 넘어 있는 것이 n으로 들어오게 되는지 확인
    elif nth >= len(lista):
        print('NIL')
    else:
        print(lista[nth])

# minusp 처리 함수
def minusp_procedure(x):
    try:
        if str(type(int(str(x)[str(x).find("[") + 1: str(x).find("]")]))) == "<class 'int'>":
            if (int(str(x)[str(x).find("[") + 1: str(x).find("]")]) < 0):
                print("T")
            else:
                print("F")
    # float 이면 value error 가 나기 때문에 예외 처리
    except ValueError:
        try:
            # float 형에 대한 처리
            if str(type(float(str(x)[str(x).find("[") + 1: str(x).find("]")]))) == "<class 'float'>":
                if (float(str(x)[str(x).find("[") + 1: str(x).find("]")]) < 0):
                    print("T")
                else:
                    print("F")
            # int, float 도 아니면 에러 처리
        except ValueError:
            return print("Error")
# subst 에 대한 함수
# 리스트의 길이동안 반복문을 사용하여 차례 로 리스트의 원소들에 접근해보면서 대치 될 data와 같을 때 x[0]로 값을 대치
def subst_procedure(x):
    if(x[1] in x[2]):
        for k in range(0,len(x[2])):
            if(x[1] == x[2][k]):
                x[2][k] = x[0]
        output_print(x[2])

    else:
        print("NIL")

# remove 실행을 위한 함수
# for문을 통해 Value가 여러 개 있어도 모두 삭제
def remove_procedure(x):
    tmp = x[1][:]
    value = x[0] # 제거 대상 요소
    if(value in tmp):
        for item in tmp:
            if item == value:
                tmp.remove(value)
        output_print(tmp)
    else:
        print("NIL")

# Assoc 실행 함수
# for문을 통해 이차원리스트의 원소(1 차원리스트)들을 반복시키고 k[0]의 인덱 스값에 해당하는 리스트를 반환함
def assoc_procedure(x):
    for k in x[1]:
        if(k[0] == x[0]):
            return k
    # 인덱스가 리스트의 인덱스값을 벗어나면 NIL 을 반환
    return "NIL"

# number 함수
def number_procedure(x):
    try:
        # x를 string형 변환후 [ 와 ] 를 제거
        # 다시 int형으로 형변환 후 해당 값의 type이 int형이라면 참을 반환
        if str(type(int(str(x)[str(x).find("[") + 1: str(x).find("]")]))) == "<class 'int'>":
            return print("T")
        # float 형에 대해서도 위와 같이 처리해줌
    except ValueError:
        try:
            if str(type(float(str(x)[str(x).find("[") + 1: str(x).find("]")]))) == "<class 'float'>":
                return print("T")
        # float, int 모두 아니면 F 반환
        except ValueError:
            return print("F")

# lambda 처리를 위한 함수
def lambda_procedure(parms, body, *args):
    dic_new = {}
    for k, v in list(zip(parms, list(*args))):
        dic_new[k] = v
    dic_new2.update(lisp_to_python_dic)
    dic_new2.update(dic_new)
    return eval(body, dic_new2)

# 최종 출력을 위한 함수
# LISP 언어 형식대로 출력이 될 수 있도록 중괄호, 1차원배열로 만드는 과정(np, flatten) 등을 처리해줌
def output_print(x):
    if (isinstance(x, list)):
        # 1차원으로 처리
        x = np.array(x)
        x = x.flatten()
        # 중괄호 처리
        new_output = '(' + ' '.join(map(str,x)) + ')'
        print(new_output)
    else:
        print(x)

# evaluation 과정
def eval(x, dic):

    global flaga
    flaga = 0
    # string 형에 대한 처리
    if isinstance(x, str):
        if(x.startswith("\"")):
            return x
        try:
            return dic[x]
        except:
            return x

    # int 형일 경우 그대로 반환
    elif isinstance(x, int):
        return x
    # list 형일 경우 그대로 반환
    elif not isinstance(x, list):
        return x
    # quote 에 대한 처리
    elif x[0] == 'quote':
        flaga = 1
        # quote 다음에 하나라면 변수로 취급해야한다.
        # quote 다음에 문자열 변수가 오면 문자열 취급
        # qoute 다음에 괄호안에 둘러싸인 리스트 형태로 오면 괄호 취급
        (_, exp) = x
        return exp
    # if 에 대한 처리
    elif x[0] == 'if':
        if (len(x) == 3):
            (_, test, conseq) = x
            exp = eval(conseq, dic) if eval(test, dic) else print("NIL")
        elif (len(x) == 4):
            (_, test, conseq, alt) = x
            exp = eval(conseq, dic) if eval(test, dic) else eval(alt, dic)
        return eval(exp, dic)
    # define 에 대한 처리
    elif x[0] == 'define':
        (_, var, exp) = x
        dic[var] = eval(exp, dic)
    # setq 에 대한 처리
    elif x[0] == 'setq':
        (_, var, exp) = x

        if(isinstance(exp, list)):
            output_print(exp[1])
        else:
            print(exp)

        dic[var] = eval(exp, dic)
    # set 에 대한 처리
    elif x[0] == 'set':
        (_, var, exp) = x
        dic[var[1]] = eval(exp, dic)
    # lamda 에 대한 처리
    elif x[0] == 'lambda':
        (_, parms, body, *args) = x
        return lambda_procedure(parms, body, args)
    # atom 에 대한 처리
    elif x[0] == 'atom':
        (_, var) = x
        # 각각의 데이터 자료형에 따른 반환 값
        # atom 인지 아닌지에 대하여 처리해줌
        if (str(type(var))) == "<class 'int'>":
            print("True")
        elif (str(type(var))) == "<class 'float'>":
            print("True")
        elif (str(type(var))) == "<class 'str'>" and len(var) > 1 \
                and var[0] == '"':
            print("True")
        else:
            if var[0] == "quote" and (len(x[1][1]) == 1):
                return "True"
            else:
                return "NIL"
    # cond 에 대한 처리
    elif x[0] == 'cond':
        if (len(x) == 4):
            (_, test1, test2, test3) = x
            if eval(test1[0], dic):
                exp = eval(test1[1], dic)
                return eval(exp, dic)

            elif eval(test2[0], dic):
                exp = eval(test2[1], dic)
                return eval(exp, dic)

            elif eval(test3[0], dic):
                exp = eval(test3[1], dic)
                return eval(exp, dic)


    else:

        proc = eval(x[0], dic)
        args = [eval(exp, dic) for exp in x[1:]]

        try:
            try:
                return proc(args)
            except:
                return proc(list(itertools.chain(*args)))

        except TypeError:
            return args
            pass


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
# main 함수
def main():
    #interface 내용
    print("---- lisp interpreter -----")
    print("Please input a number")
    user_input = int(input("1: file mode / 2: repl mode / other number: quit program => "))
    while(True):
        data = None
        # 1번 모드 작동 (file mode)
        if(user_input == 1):
            file_name = "input.lsp"
            with open(file_name, 'r', encoding='UTF8') as f:
                data = f.read().splitlines()
                input_check_valid(data, user_input)
            break;
        # 2번 모드 작동 ( repl mode )
        elif(user_input == 2):
            data = input(">>> ")
            input_check_valid(data, user_input)
        else:
            print("bye")
            break

if __name__ == "__main__":
    main()
