from Project.Lib3_Grammer.fun import Collections

"""
A→BF
F→+A|-A|$
B→CG
G→*B|/B|%B|$
C→(A)|D|E
D→H|I
E→J
H:数值型常量
I:字符型常量
J:标识符
"""

operation_mapping = {800: 'H', 400: 'H', 700: 'J', 500: 'I', 600: 'I'}


class TokenBox:
    def __init__(self, tokens):
        self.tokens = tokens
        self.p = 0
        self.length = len(self.tokens)
        self.Token = ''

    def get_next_token(self):
        if self.p <= self.length-1:
            res = self.tokens[self.p]
            self.p += 1
            self.Token = res
            return res
        else:
            return None


def transform(tokens):
    for token in tokens:
        if token[1] in operation_mapping:
            token[1] = operation_mapping[token[1]]
        else:
            token[1] = token[0]
    return tokens


src_tokens = [['5', 800], ['+', 209], ['2', 800], ['+', 209], ['10', 800]]
tokens = transform(src_tokens)
collection = Collections('operation', 'A')
collection.GET_FIRST_FOLLOW()
t = TokenBox(tokens)


def match(obj):
    if t.Token[1] == obj:
        t.get_next_token()
        return
    else:
        print('匹配错误')
        pass


def A():
    B()
    F()


def F():
    if t.Token[1] == '+':
        match('+')
        A()
    elif t.Token[1] == '-':
        match('-')
        A()


def B():
    C()
    G()


def G():
    if t.Token[1] == '*':
        match('*')
        B()
    elif t.Token[1] == '/':
        match('/')
        B()
    elif t.Token[1] == '%':
        match('%')
        B()


def C():
    if t.Token[1] == '(':
        match('(')
        A()
        if t.Token[1] == ')':
            match(')')
        else:
            print('错误')
            pass
    elif t.Token[1] == 'H':
        match('H')
    elif t.Token[1] == 'I':
        match('I')
    elif t.Token[1] == 'J':
        match('J')
    else:
        print('匹配错误')
        pass


def operation():
    token = t.get_next_token()
    if token[1] in collection.firsts['A']:
        A()
    elif token[1] in collection.firsts['F']:
        F()
    elif token[1] in collection.firsts['B']:
        B()
    elif token[1] in collection.firsts['G']:
        G()
    elif token[1] in collection.firsts['C']:
        C()
    else:
        print("匹配错误")
        pass


operation()