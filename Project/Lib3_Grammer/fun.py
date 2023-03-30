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


def match(obj, t):
    if t.Token[1] == obj:
        t.get_next_token()
        return
    else:
        print('匹配错误')
        pass


def norm_statement():
    pass


def for_statement():
    pass


def if_statement(tokenbox_obj):
    if tokenbox_obj.Token[1] != 'if':
        syntax_error()
    tokenbox_obj.get_next_token()
    if tokenbox_obj.Token[1] != '(':
        syntax_error()



def while_statement():
    pass


def do_statement():
    pass


def const_declare_analyzer():
    pass


def syntax_error():
    pass


def fun_declare_analyzer():
    pass


def variable_declare_analyzer():
    pass


def complex_sentence_analyzer():
    pass



