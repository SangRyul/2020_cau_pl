
# 프로그래밍 언어론 04분반 PL Team Project
# Lisp Interpreter 구현 프로젝트

# 참여자:
# 창의ICT공과대학 컴퓨터공학부(컴퓨터공학전공) 20165020 김상렬
# 창의ICT공과대학 소프트웨어학부 20181154 선민승
# 소프트웨어대학 소프트웨어학부 20190143 고은서

# 파일 정보:
# 프로그램 명: aparser.py
# 역할: Parser
# 생성 날짜: 2020.11.10


from functools import reduce
import re

# 괄호 처리에 대한 함수
def bracket_parser(data):
    if data[0] == '(':
        return [data[0], data[1:]]
# 띄어쓰기에 대한 함수
def space_parser(data):
    space_reg_ex = re.compile('\s+')
    space_match = space_reg_ex.match(data)
    if space_match:
        return [data[:space_match.end()], data[space_match.end():]]
# 숫자 입력에 대한 처리 함수
def number_parser(data):
    number_reg_ex = re.compile('[+-]?([0-9]*[.])?[0-9]+')
    number_match = number_reg_ex.match(data)
    if number_match:
        return[data[:number_match.end()], data[number_match.end():]]
# 식별자가 들어오게 되면 식별자에 대해 처리를 해주는 함수
def identifier_parser(data):
    identifier_reg_ex = re.compile('\w+')
    identifier_match = identifier_reg_ex.match(data)
    if identifier_match:
        return[data[:identifier_match.end()], data[identifier_match.end():]]
# keyword_parser를 위한 데이터 배열
keywords_li = ['reverse','car', 'cdr', 'caddr', 'cons', 'nth', 'reverse','length','define','lambda', '*', '+', '-', '/', '<', '>','=','<=', '>=', '%', 'if',';',
               'length', 'append', 'quote', 'list',
               'atom','null','equal','member', '\'',
               'print', 'numberp', 'zerop',
               'stringp', 'minusp', 'equal', 'assoc', 'remove', 'subst', 'setq', 'set', 'cond']
upper_token = [x.upper() for x in keywords_li]
keywords_li.extend(upper_token)
# 위의 배열에 해당하는 키워드에 대해 처리를 하는 함수.
def keyword_parser(data):
    for item in keywords_li:
        if data.startswith(item):
            return key_parser(data)

# 아래부터는 quote에 대한 처리 함수.
def double_quote_parser(data):
    if data[:1] == "\"":
        point = data.index("\"")
        return[data[:data.index('\"', point+1)+1], data[data.index("\"", point+1)+1:]]
# define 처리 함수
def declarator_parser(data):
    if data[:6] == 'define':
        return ['define', data[6:]]
# lamda 처리 파서 함수
def lambda_parser(data):
    if data[:6] == 'lambda':
        return ['lambda', data[6:]]

# arithemetic_parser를 위한 배열
arithmetic_operators = ['*', '+', '/', '%']

# 위의 배열에 해당하는 수식들을 처리하는 파서 함수
def arithemetic_parser(data):
    for item in arithmetic_operators:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

    if data[:1] == "\"":
        point = data.index("\"")
        return[data[:data.index('\"', point+1)+1], data[data.index("\"", point+1)+1:]]

# Minus 처리 파서 함수
def minus_parser(data):
    if data[:1] == "-":
        if(data[1:2] == ' '):
            #-연산을 위한 경우
            return [data[:1], data[1:]]
        else:
            #부호가 음수일경우
            number_parser(data)

# binary 수식 파서를 위한 배열
binary_operations = ['<=', '>=', '<', '>', 'pow', 'append', '=', ';']

# binary 수식 파서 함수
def binary_parser(data):
    for item in binary_operations:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]
# unary 수식을 위한 배열
unary_operations = ['length', 'round', 'not','\'']

# unary 계산을 위한 파서 함수
def unary_parser(data):
    for item in unary_operations:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

# if 처리를 위한 파서 함수
def if_parser(data):
    if data[:2] == 'if':
        return [data[:2], data[2:]]

# atom 처리를 위한 파서 함수
def atom(s):
    try: return int(s)
    except TypeError:
        return s
    except ValueError:
        try: return float(s)
        except ValueError:
            return str(s)

# parser의 시작점
def expression_parser(data):
    try:
        #각 토큰을 value_parser에서 토크나이즈해서 token과 나머지 부분으로 나눈다.
        res = value_parser(data)
        rest = res.pop(1)
        token = res.pop(0)
        # 받은 token의 대소문자 구별을 없애기 위해서 소문자로 모두 바꾼다.
        if(token in keywords_li):
            token = token.lower()
        if token == '':
            rest = rest[rest.index('\n') + 1:]

            return [token, rest]
        #토큰이 (로 시작하면
        elif token == '(':
            L = []

            while(len(rest)!=0 and rest[0] != ')'):
                nex = expression_parser(rest)
                rest = nex.pop(1)
                token = nex.pop(0)

                if token[0] == ' ' or token == '\n':
                    continue
                #토큰이 '로 시작하면 quote로 바꾸어줘야 한다.
                elif (token == '\''):
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
            #남은 문자열에 대해서도 위와 같은 과정 반복
            return [L, rest]

        else:
            return [token, rest]
    except:
        pass

def any_one_parser_factory(*args):
    return lambda data: (reduce(lambda f, g: f if f(data)  else g, args)(data))

value_parser = any_one_parser_factory(space_parser, bracket_parser, keyword_parser,
                                      number_parser, identifier_parser,double_quote_parser)
key_parser = any_one_parser_factory(declarator_parser, lambda_parser, if_parser,
                                    binary_parser, arithemetic_parser, unary_parser, minus_parser)


def main():
    file_name = "input.lsp"
    with open(file_name, 'r', encoding='UTF8') as f:
        data = f.read().splitlines()
        for data in data:
            if (data.startswith(";")):
                continue

if __name__ == "__main__":
    main()

