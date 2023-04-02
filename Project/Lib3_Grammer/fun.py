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

    def transformer(self):
        pass

def match(obj, t):
    if t.Token[1] == obj:
        t.get_next_token()
        return
    else:
        print('匹配错误')
        pass

"""
E 变量
F 函数调用
G 实参列表
H 实参
H1 实参'
I 语句
J 声明语句
K 值声明
L 常量声明
M 常量类型
N 常量声明表
N1 常量声明表'
O 变量声明
P 变量声明表
P1 变量声明表'
Q 单变量声明
Q1 单变量声明'
R 变量类型
S 函数声明
T 函数类型
U 函数声明形参列表
V 函数声明形参
V1 函数声明形参'
W 布尔表达式
W1 布尔表达式'
X 布尔项
X1 布尔项'
Y 布尔因子
Z 赋值表达式
A_ 表达式
B_ 执行语句
C_ 数据处理语句
D_ 赋值语句
E_ 函数调用语句
F_ 控制语句
G_ 复合语句
H_ 语句表
H1_ 语句表'
I_ if语句
I_1 if语句'
J_ for语句
K_ while语句
L_ dowhile语句
M_ 循环语句
N_ 循环用复合语句
O_ 循环语句表
O_1 循环语句表'
P_ 循环执行语句
Q_ 循环用if语句
Q_1 循环用if语句'
R_ return语句
R_1 return语句'
S_ break语句
T_ continue语句
U_ 关系表达式
V_ 关系运算符
W_ 函数定义
X_ 函数定义形参列表
Y_ 函数定义形参
Y_1 函数定义形参
Z_ 程序
A__ 函数块
"""

def A(t):
    """算术表达式"""
    B()
    A1()
    pass


def A1(t):
    """ 算术表达式' """
    if t.Token[1] == '+':
        match('+', t)
        A(t)
    elif t.Token[1] == '-':
        match('-', t)
        A(t)
    pass


def B(t):
    """项"""
    C(t)
    B1(t)
    pass


def B1(t):
    """ 项' """
    if t.Token[1] == '*':
        match('*', t)
        B(t)
    elif t.Token[1] == '/':
        match('/', t)
        B(t)
    elif t.Token[1] == '%':
        match('%', t)
        B(t)
    pass


def C(t):
    """因子"""
    if t.Token[1] == '(':
        match('(', t)
        A(t)
        if t.Token[1] == ')':
            match(')', t)
    elif t.Token[1] in t.firsts['con']:
        D(t)
    elif t.Token[1] in t.firsts['var']:
        E(t)
    elif t.Token[1] in t.firsts['fun_invoke']:
        F(t)
    else:
        pass


def D(t):
    """常量"""
    if t.Token[1] == 'num_con':
        match('num_con', t)
    elif t.Token[1] == 'sig_con':
        match('sig_con', t)
    else:
        pass


def E(t):
    """变量"""
    if t.Token[1] == 'signal':
        match('signal', t)
    else:
        pass


def F(t):
    """函数调用"""
    if t.Token[1] == 'signal':
        match('signal', t)
        if t.Token[1] == '(':
            match('(', t)
            G(t)
            if t.Token[1] == ')':
                match(')', t)
            else:
                pass
        else:
            pass
    else:
        pass


def G(t):
    """实参列表"""
    if t.Token[1] in t.firsts('real_par'):
        H(t)
    pass


def H(t):
    """实参"""
    A_(t)
    H1(t)
    pass


def H1(t):
    """ 实参' """
    if t.Token[1] == ',':
        match(',', t)
        H(t)
    pass


def I(t):
    """语句"""
    if t.Token[1] in t.firsts['declare_statement']:
        J(t)
    elif t.Token[1] in t.firsts['exe_statement']:
        B_(t)
    else:
        # error
        pass


def J(t):
    """声明语句"""
    if t.Token[1] in t.firsts['v_declare']:
        K(t)
    elif t.Token[1] in t.firsts['fun_declare']:
        S(t)
    pass


def K(t):
    """值声明"""
    if t.Token[1] in t.firsts['con_declare']:
        L(t)
    elif t.Token[1] in t.firsts['var_declare']:
        O(t)
    else:
        # error
        pass


def L(t):
    """常量声明"""
    if t.Token[1] == 'const':
        match('const', t)
        M(t)
        N(t)
    else:
        # error
        pass


def M(t):
    """常量类型"""
    if t.Token[1] == 'int':
        match('int', t)
    elif t.Token[1] == 'char':
        match('char', t)
    elif t.Token[1] == 'float':
        match('float', t)
    else:
        # error
        pass


def N(t):
    """常量声明表"""
    if t.Token[0] == 'signal':
        match('signal', t)
        if t.Token[1] == '=':
            match('=',t)
            if t.Token[1] == 'con':
                match('con', t)
                N1(t)
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass



def N1(t):
    """常量声明表'"""
    if t.Token[1] == ';':
        match(';', t)
    elif t.Token[1] == ',':
        match(',', t)
        N(t)
    else:
        # error
        pass


def O(t):
    """变量声明"""
    R(t)
    P(t)
    pass


def P(t):
    """变量声明表"""
    Q(t)
    P1(t)
    pass


def P1(t):
    """变量声明表'"""
    if t.Token[1] == ';':
        match(';', t)
    elif t.Token[1] == ',':
        match(',', t)
        P(t)
    else:
        # error
        pass


def Q(t):
    """单变量声明"""
    if t.Token[1] == 'var':
        match('var', t)
        Q1(t)
    else:
        # error
        pass


def Q1(t):
    """单变量声明'"""
    if t.Token[1] == '=':
        match('=', t)
        A_(t)
    pass


def R(t):
    """变量类型"""
    if t.Token[1] == 'int':
        match('int', t)
    elif t.Token[1] == 'char':
        match('char', t)
    elif t.Token[1] == 'float':
        match('float', t)
    else:
        # error
        pass


def S(t):
    """函数声明"""
    T(t)
    if t.Token[1] == 'signal':
        match('signal', t)
        if t.Token[1] == '(':
            match('(', t)
            U(t)
            if t.Token[1] == ')':
                match(')', t)
                if t.Token[1] == ';':
                    match(';', t)
                else:
                    # error
                    pass
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def T(t):
    """函数类型"""
    if t.Token[1] == 'int':
        match('int', t)
    elif t.Token[1] == 'char':
        match('char', t)
    elif t.Token[1] == 'float':
        match('float', t)
    elif t.Token[1] == 'void':
        match('void', t)
    else:
        # error
        pass


def U(t):
    """函数声明形参列表"""
    if t.Token[1] in t.firsts['fun_declare_fpar']:
        V(t)
    pass


def V(t):
    """函数声明形参"""
    R(t)
    V1(t)
    pass


def V1(t):
    """函数声明形参'"""
    if t.Token[1] == ',':
        match(',', t)
        V(t)
    pass


def W(t):
    """布尔表达式"""
    X(t)
    W1(t)
    pass


def W1(t):
    """布尔表达式'"""
    if t.Token[1] == '||':
        match('||', t)
        W(t)

    pass


def X(t):
    """布尔项"""
    Y(t)
    X1(t)
    pass


def X1(t):
    """布尔项'"""
    if t.Token[1] == '&&':
        match('&&', t)
        X(t)
    pass


def Y(t):
    """布尔因子"""
    if t.Token[1] in t.firsts['arg_exp']:
        A(t)
    elif t.Token[1] in t.firsts['rel_expression']:
        U_(t)
    elif t.Token[1] == '!':
        match('!', t)
        W1(t)
    else:
        # error
        pass


def Z(t):
    """赋值表达式"""
    if t.Token[1] == 'signal':
        match('signal', t)
        if t.Token[1] == '=':
            match('=', t)
            A_(t)
        else:
            # error
            pass
    else:
        # error
        pass


def A_(t):
    """表达式"""
    if t.Token[1] in t.firsts['arg_exp']:
        A(t)
    elif t.Token[1] in t.firsts['rel_expression']:
        U_(t)
    elif t.Token[1] in t.firsts['bool_expression']:
        W1(t)
    elif t.Token[1] in t.firsts['assign_expression']:
        Z(t)
    else:
        # error
        pass


def B_(t):
    """执行语句"""
    if t.Token[1] in t.firsts['digit_exe_statement']:
        C_(t)
    elif t.Token[1] in t.firsts['control_statement']:
        F_(t)
    elif t.Token[1] in t.firsts['complex_statement']:
        G_(t)
    else:
        # error
        pass


def C_(t):
    """数据处理语句"""
    if t.Token[1] in t.firsts['assign_statement']:
        D_(t)
    elif t.Token[1] in t.firsts['fun_invoke_statement']:
        E_(t)
    else:
        # error
        pass


def D_(t):
    """赋值语句"""
    Z(t)
    if t.Token[1] == ';':
        match(';', t)
    else:
        # error
        pass


def E_(t):
    """函数调用语句"""
    F(t)
    if t.Token[1] == ';':
        match(';', t)
    else:
        # error
        pass


def F_(t):
    """控制语句"""
    if t.Token[1] in t.firsts['if_statement']:
        I_(t)
    elif t.Token[1] in t.firsts['for_statement']:
        J_(t)
    elif t.Token[1] in t.firsts['while_statement']:
        K_(t)
    elif t.Token[1] in t.firsts['do_while_statement']:
        L_(t)
    elif t.Token[1] in t.firsts['return_statement']:
        R_(t)
    else:
        # error
        pass


def G_(t):
    """复合语句"""
    if t.Token[1] == '{':
        match('{', t)
        H_(t)
        if t.Token[1] == '}':
            match('}', t)
        else:
            # error
            pass
    else:
        # error
        pass


def H_(t):
    """语句表"""
    I(t)
    H_1(t)
    pass


def H_1(t):
    """语句表'"""
    if t.Token[1] in t.firsts['statement_list']:
        H_(t)
    pass


def I_(t):
    """if语句"""
    if t.Token[1] == 'if':
        match('if', t)
        if t.Token[1] == '(':
            match('(', t)
            A_(t)
            if t.Token[1] == ')':
                match(')', t)
                I(t)
                I_1(t)
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def I_1(t):
    """if语句'"""
    if t.Token[1] == 'else':
        match('else', t)
        I(t)
    pass


def J_(t):
    """for语句"""
    if t.Token[1] == 'for':
        match('for', t)
        if t.Token[1] == '(':
            match('(', t)
            A_(t)
            if t.Token[1] == ';':
                match(';', t)
                A_(t)
                if t.Token[1] == ';':
                    match(';', t)
                    A_(t)
                    if t.Token[1] == ')':
                        match(')', t)
                        M_(t)
                    else:
                        # error
                        pass
                else:
                    # error
                    pass
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def K_(t):
    """while语句"""
    if t.Token[1] == 'while':
        match('while', t)
        if t.Token[1] == '(':
            match('(', t)
            A_(t)
            if t.Token[1] == ')':
                match(')', t)
                M_(t)
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def L_(t):
    """dowhile语句"""
    if t.Token[1] == 'do':
        match('do', t)
        N_(t)
        if t.Token[1] == 'while':
            match('while', t)
            if t.Token[1] == '(':
                match('(', t)
                A_(t)
                if t.Token[1] == ')':
                    match(')', t)
                    if t.Token[1] == ';':
                        match(';', t)
                    else:
                        # error
                        pass
                else:
                    # error
                    pass
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def M_(t):
    """循环语句"""
    if t.Token[1] in t.firsts['declare_statement']:
        J(t)
    elif t.Token[1] in t.firsts['cir_exe_statement']:
        P_(t)
    elif t.Token[1] in t.firsts['cir_complex_statement']:
        N_(t)
    else:
        # error
        pass


def N_(t):
    """循环用复合语句"""
    if t.Token[1] == '{':
        match('{', t)
        O_(t)
        if t.Token[1] == '}':
            match('}', t)
        else:
            # error
            pass
    else:
        # error
        pass


def O_(t):
    """循环语句表"""
    M_(t)
    O_1(t)
    pass


def O_1(t):
    """循环语句表'"""
    if t.Token[1] in t.firsts['cir_statement_list']:
        O_(t)
    pass


def P_(t):
    """循环执行语句"""
    if t.Token[1] in t.firsts['cir_if_statement']:
        Q_(t)
    elif t.Token[1] in t.firsts['for_statement']:
        J_(t)
    elif t.Token[1] in t.firsts['while_statement']:
        K_(t)
    elif t.Token[1] in t.firsts['do_while_statement']:
        L_(t)
    elif t.Token[1] in t.firsts['return_statement']:
        R_(t)
    elif t.Token[1] in t.firsts['break_statement']:
        S_(t)
    elif t.Token[1] in t.firsts['continue_statement']:
        T_(t)
    else:
        # error
        pass


def Q_(t):
    """循环用if语句"""
    if t.Token[1] == 'if':
        match('if', t)
        if t.Token[1] == '(':
            match('(', t)
            A_(t)
            if t.Token[1] == ')':
                match(')', t)
                Q_1(t)
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def Q_1(t):
    """循环用if语句'"""
    if t.Token[1] == 'else':
        match('else', t)
        M_(t)
    pass


def R_(t):
    """return语句"""
    if t.Token[1] == 'return':
        match('return', t)
        R_1(t)
    pass


def R_1(t):
    """return语句"""
    if t.Token[1] == ';':
        match('return', t)
    elif t.Token[1] in t.firsts['expression']:
        A_(t)
        if t.Token[1] == ';':
            match(';', t)
        else:
            # error
            pass
    else:
        # error
        pass


def S_(t):
    """break语句"""
    if t.Token[1] == 'break':
        match('break', t)
        if t.Token[1] == ';':
            match(';', t)
        else:
            # error
            pass
    else:
        # error
        pass


def T_(t):
    """continue语句"""
    if t.Token[1] == 'continue':
        match('continue', t)
        if t.Token[1] == ';':
            match(';', t)
        else:
            # error
            pass
    else:
        # error
        pass


def U_(t):
    """关系表达式"""
    A(t)
    V_(t)
    A(t)
    pass


def V_(t):
    """关系运算符"""
    if t.Token[1] == '>':
        match('>', t)
    elif t.Token[1] == '<':
        match('<', t)
    elif t.Token[1] == '>=':
        match('>=', t)
    elif t.Token[1] == '<=':
        match('<=', t)
    elif t.Token[1] == '==':
        match('==', t)
    elif t.Token[1] == '!=':
        match('!=', t)
    else:
        # error
        pass


def W_(t):
    """函数定义"""
    T(t)
    if t.Token[1] == 'signal':
        match('signal', t)
        if t.Token[1] == '(':
            match('(', t)
            X_(t)
            if t.Token[1] == ')':
                match(')', t)
                G_(t)
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def X_(t):
    """函数定义形参列表"""
    if t.Token[1] in t.firsts['fun_define_fpar']:
        Y_(t)
    pass


def Y_(t):
    """函数定义形参"""
    R(t)
    if t.Token[1] == 'signal':
        match('signal', t)
        Y_1(t)
    else:
        # error
        pass


def Y_1(t):
    """函数定义形参'"""
    if t.Token[1] == ',':
        match(',', t)
        Y_(t)
    pass


def Z_(t):
    """程序"""
    J(t)
    if t.Token[1] == 'main':
        match('main', t)
        if t.Token[1] == '(':
            match('(', t)
            if t.Token[1] == ')':
                match(')', t)
                G_(t)
                A__(t)
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def A__(t):
    """函数块"""
    if t.Token[1] in t.firsts['fun_define']:
        W_(t)
        A__(t)
    pass





