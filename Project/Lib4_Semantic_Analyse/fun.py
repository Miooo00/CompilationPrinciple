import copy

from Project.Lib4_Semantic_Analyse.Tables import Constobj


class TokenBox:
    def __init__(self, tokens):
        self.tokens = tokens
        self.p = 0
        self.length = len(self.tokens)
        self.Token = ''
        self.transformer()

    def get_next_token(self):
        if self.p <= self.length-1:
            res = self.tokens[self.p]
            self.p += 1
            self.Token = res
            return res
        else:
            self.Token = [-1, 'None', 'None', -1]
            return None

    def transformer(self):
        # signal、num_con、sig_con
        for tok in self.tokens:
            if tok[0] == '700':
                tok.insert(1, 'signal')
                tok[1] = 'signal'
            elif tok[0] == '500' or tok[0] == '600':
                tok.insert(1, 'sig_con')
                tok[1] = 'sig_con'
            elif tok[0] == '400' or tok[0] == '800':
                tok.insert(1, 'num_con')
                tok[1] = 'num_con'
            else:
                tok.insert(1, tok[1])

def match(obj, t):
    if t.Token[1] == obj:
        t.get_next_token()
        return
    else:
        print('匹配错误')
        pass


def conditon(t):
    p = t.p
    simbol = ['>', '<', '>=', '<=', '==', '!=']
    wrong = t.tokens[p][3]
    while p < len(t.tokens) and t.tokens[p][1] != ')' and t.tokens[p][1] != ';':
        if wrong != t.tokens[p][3]:
            break
        if t.tokens[p][1] in simbol:
            return False
        p += 1

    return True


def conditon1(t):
    p = t.p
    simbol = ['&&', '||', '!']
    wrong = t.tokens[p][3]
    while (p < len(t.tokens) and t.tokens[p][1] != ')') and (p < len(t.tokens) and t.tokens[p][1] != ';'):
        if wrong != t.tokens[p][3]:
            break
        if t.tokens[p][1] in simbol:
            return False
        p += 1

    return True


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

def A(t, col):
    """算术表达式"""
    B(t, col)
    A1(t, col)
    pass


def A1(t, col):
    """ 算术表达式' """
    if t.Token[1] == '+':
        match('+', t)
        A(t, col)
    elif t.Token[1] == '-':
        match('-', t)
        A(t, col)
    pass


def B(t, col):
    """项"""
    C(t, col)
    B1(t, col)
    pass


def B1(t, col):
    """ 项' """
    if t.Token[1] == '*':
        match('*', t)
        B(t, col)
    elif t.Token[1] == '/':
        match('/', t)
        B(t, col)
    elif t.Token[1] == '%':
        match('%', t)
        B(t, col)
    pass


def C(t, col):
    """因子"""
    if t.Token[1] == '(':
        match('(', t)
        A(t, col)
        if t.Token[1] == ')':
            match(')', t)
    elif t.Token[1] in col.firsts['con']:
        D(t, col)
    elif t.Token[1] in col.firsts['var'] and (t.tokens[t.p][1] != '('):
        E(t, col)
    elif t.Token[1] in col.firsts['fun_invoke']:
        F(t, col)
    else:
        pass


def D(t, col, c_obj=None, c_table=None):
    """常量"""
    if t.Token[1] == 'num_con':
        if c_obj:
            c_obj.val = t.Token[2]
        match('num_con', t)
    elif t.Token[1] == 'sig_con':
        if c_obj:
            c_obj.val = t.Token[2]
        match('sig_con', t)
    if c_table:
        c_table.add_obj(c_obj)


def E(t, col):
    """变量"""
    if t.Token[1] == 'signal':
        match('signal', t)
    else:
        pass


def F(t, col):
    """函数调用"""
    if t.Token[1] == 'signal':
        match('signal', t)
        if t.Token[1] == '(':
            match('(', t)
            G(t, col)
            if t.Token[1] == ')':
                match(')', t)
            else:
                pass
        else:
            pass
    else:
        pass


def G(t, col):
    """实参列表"""
    if t.Token[1] in col.firsts['real_par']:
        H(t, col)
    pass


def H(t, col):
    """实参"""
    A_(t, col)
    H1(t, col)
    pass


def H1(t, col):
    """ 实参' """
    if t.Token[1] == ',':
        match(',', t)
        H(t, col)
    pass


def I(t, col):
    """语句"""
    if t.Token[1] in col.firsts['declare_statement']:
        J(t, col)
    elif t.Token[1] in col.firsts['exe_statement']:
        B_(t, col)
    else:
        # error
        pass


def J(t, col):
    """声明语句"""
    if t.Token[1] in col.firsts['v_declare']:
        K(t, col)
    elif t.Token[1] in col.firsts['fun_declare']:
        S(t, col)
    pass


def K(t, col):
    """值声明"""
    if t.Token[1] in col.firsts['con_declare']:
        L(t, col)
    elif t.Token[1] in col.firsts['var_declare']:
        O(t, col)
    else:
        # error
        pass


def L(t, col, c_table):
    """常量声明"""
    c_obj = Constobj()
    if t.Token[1] == 'const':
        match('const', t)
        M(t, col, c_obj, c_table)
        N(t, col, c_obj, c_table)
    else:
        # error
        pass


def M(t, col, c_obj, c_table):
    """常量类型"""
    if t.Token[1] == 'int':
        match('int', t)
        c_obj.type = 'int'
    elif t.Token[1] == 'char':
        match('char', t)
        c_obj.type = 'char'
    elif t.Token[1] == 'float':
        match('float', t)
        c_obj.type = 'float'


def N(t, col, c_obj, c_table):
    """常量声明表"""
    if t.Token[1] == 'signal':
        c_obj.name = t.Token[2]
        match('signal', t)
        if t.Token[1] == '=':
            match('=', t)
            D(t, col, c_obj, c_table)
            N1(t, col, c_obj, c_table)
    # 语义处理阶段应当是不存在语法错误



def N1(t, col, c_obj, c_table):
    """常量声明表'"""
    if t.Token[1] == ';':
        match(';', t)
    elif t.Token[1] == ',':
        match(',', t)
        next_cobj = copy.deepcopy(c_obj)
        next_cobj.name = ''
        next_cobj.val = ''
        N(t, col, next_cobj, c_table)
    else:
        # error
        pass


def O(t, col):
    """变量声明"""
    R(t, col)
    P(t, col)
    pass


def P(t, col):
    """变量声明表"""
    Q(t, col)
    P1(t, col)
    pass


def P1(t, col):
    """变量声明表'"""
    if t.Token[1] == ';' or t.Token[1] == ";":
        match(';', t)
    elif t.Token[1] == ',' or t.Token[1] == ",":
        match(',', t)
        P(t, col)
    else:
        # error
        pass


def Q(t, col):
    """单变量声明"""
    E(t, col)
    Q1(t, col)


def Q1(t, col):
    """单变量声明'"""
    if t.Token[1] == '=':
        match('=', t)
        A_(t, col)
    pass


def R(t, col):
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


def S(t, col):
    """函数声明"""
    if t.Token[1] == '(':
        match('(', t)
        U(t, col)
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
    # else:
    #     # error
    #     pass


def T(t, col):
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


def U(t, col):
    """函数声明形参列表"""
    if t.Token[1] in col.firsts['fun_declare_fpar']:
        V(t, col)
    pass


def V(t, col):
    """函数声明形参"""
    R(t, col)
    if t.Token[1] == 'signal':
        match('signal', t)
    V1(t, col)
    pass


def V1(t, col):
    """函数声明形参'"""
    if t.Token[1] == ',':
        match(',', t)
        V(t, col)
    pass


def W(t, col):
    """布尔表达式"""
    X(t, col)
    W1(t, col)
    pass


def W1(t, col):
    """布尔表达式'"""
    if t.Token[1] == '||':
        match('||', t)
        W(t, col)

    pass


def X(t, col):
    """布尔项"""
    Y(t, col)
    X1(t, col)
    pass


def X1(t, col):
    """布尔项'"""
    if t.Token[1] == '&&':
        match('&&', t)
        X(t, col)
    pass


def Y(t, col):
    """布尔因子"""
    # 同样存在相同firsts集合优先情况考虑
    if t.Token[1] in col.firsts['arg_exp'] and conditon(t):
        A(t, col)
    elif t.Token[1] in col.firsts['rel_expression']:
        U_(t, col)
    elif t.Token[1] == '!':
        match('!', t)
        W1(t, col)
    else:
        # error
        pass


def Z(t, col):
    """赋值表达式"""
    if t.Token[1] == 'signal':
        match('signal', t)
        if t.Token[1] == '=':
            match('=', t)
            A_(t, col)
        else:
            # error
            pass
    else:
        # error
        pass


def A_(t, col):
    """表达式"""
    if t.Token[1] in col.firsts['arg_exp'] and conditon(t) and conditon1(t) and (t.tokens[t.p][1] != '='):
        A(t, col)
    elif t.Token[1] in col.firsts['rel_expression'] and (t.tokens[t.p][1] != '=' and conditon1(t)):
        U_(t, col)
    elif t.Token[1] in col.firsts['bool_expression'] and (t.tokens[t.p][1] != '='):
        W(t, col)
    elif t.Token[1] in col.firsts['assign_expression']:
        Z(t, col)
    else:
        # error
        pass


def B_(t, col):
    """执行语句"""
    if t.Token[1] in col.firsts['digit_exe_statement']:
        C_(t, col)
    elif t.Token[1] in col.firsts['control_statement']:
        F_(t, col)
    elif t.Token[1] in col.firsts['complex_statement']:
        G_(t, col)
    else:
        # error
        pass


def C_(t, col):
    """数据处理语句"""
    if t.Token[1] in col.firsts['assign_statement'] and (t.tokens[t.p][1] != '('):
        D_(t, col)
    elif t.Token[1] in col.firsts['fun_invoke_statement']:
        E_(t, col)
    else:
        # error
        pass


def D_(t, col):
    """赋值语句"""
    Z(t, col)
    if t.Token[1] == ';':
        match(';', t)
    else:
        # error
        pass


def E_(t, col):
    """函数调用语句"""
    F(t, col)
    if t.Token[1] == ';':
        match(';', t)
    else:
        # error
        pass


def F_(t, col):
    """控制语句"""
    if t.Token[1] in col.firsts['if_statement']:
        I_(t, col)
    elif t.Token[1] in col.firsts['for_statement']:
        J_(t, col)
    elif t.Token[1] in col.firsts['while_statement']:
        K_(t, col)
    elif t.Token[1] in col.firsts['do_while_statement']:
        L_(t, col)
    elif t.Token[1] in col.firsts['return_statement']:
        R_(t, col)
    else:
        # error
        pass


def G_(t, col):
    """复合语句"""
    if t.Token[1] == '{':
        match('{', t)
        H_(t, col)
        if t.Token[1] == '}':
            match('}', t)
        else:
            # error
            pass
    else:
        # error
        pass


def H_(t, col):
    """语句表"""
    I(t, col)
    H_1(t, col)
    pass


def H_1(t, col):
    """语句表'"""
    if t.Token[1] in col.firsts['statement_list']:
        H_(t, col)
    pass


def I_(t, col):
    """if语句"""
    if t.Token[1] == 'if':
        match('if', t)
        if t.Token[1] == '(':
            match('(', t)
            A_(t, col)
            if t.Token[1] == ')':
                match(')', t)
                I(t, col)
                I_1(t, col)
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def I_1(t, col):
    """if语句'"""
    if t.Token[1] == 'else':
        match('else', t)
        I(t, col)
    pass


def J_(t, col):
    """for语句"""
    if t.Token[1] == 'for':
        match('for', t)
        if t.Token[1] == '(':
            match('(', t)
            A_(t, col)
            if t.Token[1] == ';':
                match(';', t)
                A_(t, col)
                if t.Token[1] == ';':
                    match(';', t)
                    A_(t, col)
                    if t.Token[1] == ')':
                        match(')', t)
                        M_(t, col)
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


def K_(t, col):
    """while语句"""
    if t.Token[1] == 'while':
        match('while', t)
        if t.Token[1] == '(':
            match('(', t)
            A_(t, col)
            if t.Token[1] == ')':
                match(')', t)
                M_(t, col)
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def L_(t, col):
    """dowhile语句"""
    if t.Token[1] == 'do':
        match('do', t)
        N_(t, col)
        if t.Token[1] == 'while':
            match('while', t)
            if t.Token[1] == '(':
                match('(', t)
                A_(t, col)
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


def M_(t, col):
    """循环语句"""
    # 书上给的词法在循环语句中没有执行语句,在循环内的执行语句如赋值无法正确识别 ----
    if t.Token[1] in col.firsts['exe_statement']:
        B_(t, col)
    elif t.Token[1] in col.firsts['declare_statement']:
        J(t, col)
    elif t.Token[1] in col.firsts['cir_exe_statement']:
        P_(t, col)
    elif t.Token[1] in col.firsts['cir_complex_statement']:
        N_(t, col)
    else:
        # error
        pass


def N_(t, col):
    """循环用复合语句"""
    if t.Token[1] == '{':
        match('{', t)
        O_(t, col)
        if t.Token[1] == '}':
            match('}', t)
        else:
            # error
            pass
    else:
        # error
        pass


def O_(t, col):
    """循环语句表"""
    M_(t, col)
    O_1(t, col)
    pass


def O_1(t, col):
    """循环语句表'"""
    if t.Token[1] in col.firsts['cir_statement_list']:
        O_(t, col)
    pass


def P_(t, col):
    """循环执行语句"""
    if t.Token[1] in col.firsts['cir_if_statement']:
        Q_(t, col)
    elif t.Token[1] in col.firsts['for_statement']:
        J_(t, col)
    elif t.Token[1] in col.firsts['while_statement']:
        K_(t, col)
    elif t.Token[1] in col.firsts['do_while_statement']:
        L_(t, col)
    elif t.Token[1] in col.firsts['return_statement']:
        R_(t, col)
    elif t.Token[1] in col.firsts['break_statement']:
        S_(t, col)
    elif t.Token[1] in col.firsts['continue_statement']:
        T_(t, col)
    else:
        # error
        pass


def Q_(t, col):
    """循环用if语句"""
    if t.Token[1] == 'if':
        match('if', t)
        if t.Token[1] == '(':
            match('(', t)
            A_(t, col)
            if t.Token[1] == ')':
                match(')', t)
                Q_1(t, col)
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def Q_1(t, col):
    """循环用if语句'"""
    if t.Token[1] == 'else':
        match('else', t)
        M_(t, col)
    pass


def R_(t, col):
    """return语句"""
    if t.Token[1] == 'return':
        match('return', t)
        R_1(t, col)
    pass


def R_1(t, col):
    """return语句"""
    if t.Token[1] == ';':
        match('return', t)
    elif t.Token[1] in col.firsts['expression']:
        A_(t, col)
        if t.Token[1] == ';':
            match(';', t)
        else:
            # error
            pass
    else:
        # error
        pass


def S_(t, col):
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


def T_(t, col):
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


def U_(t, col):
    """关系表达式"""
    A(t, col)
    V_(t, col)
    A(t, col)
    pass


def V_(t, col):
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


def W_(t, col):
    """函数定义"""
    T(t, col)
    if t.Token[1] == 'signal':
        match('signal', t)
        if t.Token[1] == '(':
            match('(', t)
            X_(t, col)
            if t.Token[1] == ')':
                match(')', t)
                G_(t, col)
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def X_(t, col):
    """函数定义形参列表"""
    if t.Token[1] in col.firsts['fun_define_fpar']:
        Y_(t, col)
    pass


def Y_(t, col):
    """函数定义形参"""
    R(t, col)
    if t.Token[1] == 'signal':
        match('signal', t)
        Y_1(t, col)
    else:
        # error
        pass


def Y_1(t, col):
    """函数定义形参'"""
    if t.Token[1] == ',':
        match(',', t)
        Y_(t, col)
    pass


def Z_(t, col):
    """程序"""
    J(t, col)
    if t.Token[1] == 'main':
        match('main', t)
        if t.Token[1] == '(':
            match('(', t)
            if t.Token[1] == ')':
                match(')', t)
                G_(t, col)
                A__(t, col)
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def A__(t, col):
    """函数块"""
    if t.Token[1] in col.firsts['fun_define']:
        W_(t, col)
        A__(t, col)
    pass
