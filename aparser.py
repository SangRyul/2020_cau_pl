### Lisp Intrepreter in Python
## Parser

from functools import reduce
import re

def bracket_parser(data):
    if data[0] == '(':
        return [data[0], data[1:]]

def space_parser(data):
    space_reg_ex = re.compile('\s+')
    space_match = space_reg_ex.match(data)
    if space_match:
        return [data[:space_match.end()], data[space_match.end():]]

def number_parser(data):
    number_reg_ex = re.compile('[+-]?([0-9]*[.])?[0-9]+')
    number_match = number_reg_ex.match(data)
    if number_match:
        return[data[:number_match.end()], data[number_match.end():]]

def identifier_parser(data):
    identifier_reg_ex = re.compile('\w+')
    identifier_match = identifier_reg_ex.match(data)
    if identifier_match:
        return[data[:identifier_match.end()], data[identifier_match.end():]]

keywords_li = ['reverse','car','define','lambda', '*', '+', '-', '/', '<', '>','=','<=', '>=', '%', 'if',
               'length', 'abs', 'append', 'pow', 'min', 'max', 'round', 'not', 'quote',
               'atom','null','NUMBERP','ZEROP','minusp','equal','stringp', 'member', '\'']

def keyword_parser(data):
    for item in keywords_li:
        if data.startswith(item):
            return key_parser(data)
def single_quote_parser(data):
    #현재는 안쓰는 함수임
    if data[:1] == "\'":
        point = data.index("\'")
        print(data[:data.index(')', point+1)])
        return[data[:data.index(')', point+1)], data[data.index(")", point+1):]]
def double_quote_parser(data):
    if data[:1] == "\"":
        point = data.index("\"")
        return[data[:data.index('\"', point+1)+1], data[data.index("\"", point+1)+1:]]

def declarator_parser(data):
    if data[:6] == 'define':
        return ['define', data[6:]]

def lambda_parser(data):
    if data[:6] == 'lambda':
        return ['lambda', data[6:]]

# def car_parser(data):
#     if data[:3] == 'car':
#         return ['car', data[3:]]

arithmetic_operators = ['*', '+', '/', '%']

def arithemetic_parser(data):
    for item in arithmetic_operators:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]


    if data[:1] == "\"":
        point = data.index("\"")
        return[data[:data.index('\"', point+1)+1], data[data.index("\"", point+1)+1:]]

def minus_parser(data):
    if data[:1] == "-":
        if(data[1:2] == ' '):
            #-연산을 위한 경우
            return [data[:1], data[1:]]
        else:
            #부호가 음수일경우
            number_parser(data)

binary_operations = ['<=', '>=', '<', '>', 'pow', 'append', '=']

def binary_parser(data):
    for item in binary_operations:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

unary_operations = ['length', 'abs', 'round', 'not','\'']

def unary_parser(data):
    for item in unary_operations:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

def if_parser(data):
    if data[:2] == 'if':
        return [data[:2], data[2:]]

def atom(s):
    try: return int(s)
    except TypeError:
        return s
    except ValueError:
        try: return float(s)
        except ValueError:
            return str(s)

def expression_parser(data):

        res = value_parser(data)
        rest = res.pop(1)
        token = res.pop(0)

        if token == '(':
            L = []

            while(len(rest)!=0 and rest[0] != ')'):
                nex = expression_parser(rest)
                rest = nex.pop(1)
                token = nex.pop(0)


                if token[0] == ' ' or token == '\n':
                    continue
                # elif (token == '\"'):
                #     pass

                elif (token == '\''):

                    # print(expression_parser(rest))
                    tmp_quote = expression_parser(rest)[0]
                    rest = list(rest)
                    tmp_arr = []
                    mode = 0
                    if (rest[0] == '('):
                        # 리스트 들어오는 경우
                        mode = 1
                        tmp_arr.append(rest[0])
                    else:
                        # 일반 변수 들어오는 경우
                        tmp_arr.append(rest[0])
                        mode = 2

                    for x in range(1, len(rest)-1):
                        if(rest[x] == ")" and mode == 1):
                            tmp_arr.append(rest[x])
                            break
                        elif(rest[x] == " " and mode == 2):
                            break
                        elif(mode == 1 or mode == 2):
                            tmp_arr.append(rest[x])

                    rest = ''.join(rest[len(tmp_arr):])

                    L.append(['quote', tmp_quote])
                else:

                    L.append(atom(token))

            rest = rest[1:]
            return [L, rest]

        else:
            return [token, rest]

def any_one_parser_factory(*args):
    return lambda data: (reduce(lambda f, g: f if f(data)  else g, args)(data))

value_parser = any_one_parser_factory(space_parser, bracket_parser, keyword_parser,
                                      number_parser, identifier_parser,double_quote_parser)
key_parser = any_one_parser_factory(declarator_parser, lambda_parser, if_parser,
                                    binary_parser, arithemetic_parser, unary_parser, minus_parser)

def main():
    # file_name = input()
    file_name = "example2.lsp"
    with open(file_name, 'r') as f:
        data = f.read().strip()
    print(expression_parser(data))
# 마지막에 flatten 하고 공백 제거해야함 --> interperter에서는 함

if __name__ == "__main__":
    main()

