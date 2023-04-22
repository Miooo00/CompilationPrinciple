from treelib import Node


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
            # [种别码, token对应终结符(参考transformer), 当前token, 行号]
            self.Token = [-1, 'None', 'None', -1]
            return None

    def transformer(self):
        """
        700 标识符
        500,600 字符(串)常量
        400 数值常量
        """
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

def A(t, col, parent, tree, errors):
    """算术表达式"""

    sub1 = parent
    if t.Token[1] in col.firsts['item']:
        sub1 = Node('item')
        tree.add_node(sub1, parent)
    B(t, col, sub1, tree, errors)

    sub2 = parent
    if t.Token[1] in col.firsts["arg_exp'"]:
        sub2 = Node("arg_exp'")
        tree.add_node(sub2, parent)
    A1(t, col, sub2, tree, errors)


def A1(t, col, parent, tree, errors):
    """ 算术表达式' """
    if t.Token[1] == '+':
        tree.add_node(Node('+'), parent)
        match('+', t)
        A(t, col, parent, tree, errors)
    elif t.Token[1] == '-':
        tree.add_node(Node('-'), parent)
        match('-', t)
        A(t, col, parent, tree, errors)
    pass


def B(t, col, parent, tree, errors):
    """项"""

    sub1 = Node('factor')
    tree.add_node(sub1, parent)
    C(t, col, sub1, tree, errors)

    sub2 = Node("item'")
    if t.Token[1] in col.firsts["item'"]:
        tree.add_node(sub2, parent)
    B1(t, col, sub2, tree, errors)



def B1(t, col, parent, tree, errors):
    """ 项' """
    if t.Token[1] == '*':
        tree.add_node(Node('*'), parent)
        match('*', t)
        B(t, col, parent, tree, errors)
    elif t.Token[1] == '/':
        tree.add_node(Node('/'), parent)
        match('/', t)
        B(t, col, parent, tree, errors)
    elif t.Token[1] == '%':
        tree.add_node(Node('%'), parent)
        match('%', t)
        B(t, col, parent, tree, errors)
    elif t.Token[1] == '&':
        tree.add_node(Node('&'), parent)
        match('&', t)
        B(t, col, parent, tree, errors)
    elif t.Token[1] == '|':
        tree.add_node(Node('|'), parent)
        match('|', t)
        B(t, col, parent, tree, errors)
    pass


def C(t, col, parent, tree, errors):
    """因子"""
    if t.Token[1] == '(':
        match('(', t)

        sub1 = parent
        if t.Token[1] in col.firsts['arg_exp']:
            sub1 = Node('arg_exp')
            tree.add_node(sub1, parent)
        A(t, col, sub1, tree, errors)
        if t.Token[1] == ')':
            match(')', t)
    elif t.Token[1] in col.firsts['con']:
        sub2 = Node('con')
        tree.add_node(sub2, parent)
        D(t, col, sub2, tree, errors)
    elif t.Token[1] in col.firsts['var'] and (t.tokens[t.p][1] != '('):
        sub3 = Node('var')
        tree.add_node(sub3, parent)
        E(t, col, sub3, tree, errors)
    elif t.Token[1] in col.firsts['fun_invoke']:
        sub4 = Node('fun_invoke')
        tree.add_node(sub4, parent)
        F(t, col, sub4, tree, errors)
    else:
        errors.append(f'出现错误,缺少因子或者说数字?,第{t.tokens[t.p-2][3]}行')
        print(f'出现错误,缺少因子或者说数字?,第{t.tokens[t.p-2][3]}行')
        pass


def D(t, col, parent, tree, errors):
    """常量"""
    if t.Token[1] == 'num_con':
        tree.add_node(Node(t.Token[2]), parent)
        match('num_con', t)
    elif t.Token[1] == 'sig_con':
        tree.add_node(Node(t.Token[2]), parent)
        match('sig_con', t)
    else:
        errors.append(f'出现错误,常量未赋初值,第{t.tokens[t.p - 2][3]}行')
        print(f'出现错误,常量未赋初值,第{t.tokens[t.p - 2][3]}行')
        t.p -= 1
        t.Token = [-1, 'sig_con', 'None', -1]
        match('sig_con', t)
        pass


def E(t, col, parent, tree, errors):
    """变量"""
    if t.Token[1] == 'signal':
        tree.add_node(Node(t.Token[2]), parent)
        match('signal', t)
    else:
        pass


def F(t, col, parent, tree, errors):
    """函数调用"""
    if t.Token[1] == 'signal':
        tree.add_node(Node(t.Token[2]), parent)
        match('signal', t)
        if t.Token[1] == '(':
            match('(', t)
            G(t, col, parent, tree, errors)
            if t.Token[1] == ')':
                match(')', t)
            else:
                pass
        else:
            pass
    else:
        pass


def G(t, col, parent, tree, errors):
    """实参列表"""
    if t.Token[1] in col.firsts['real_par']:
        H(t, col, parent, tree, errors)
    pass


def H(t, col, parent, tree, errors):
    """实参"""
    A_(t, col, parent, tree, errors)
    H1(t, col, parent, tree, errors)
    pass


def H1(t, col, parent, tree, errors):
    """ 实参' """
    if t.Token[1] == ',':
        match(',', t)
        H(t, col, parent, tree, errors)
    pass


def I(t, col, parent, tree, errors):
    """语句"""
    if t.Token[1] in col.firsts['declare_statement']:
        sub1 = Node('declare_statement')
        tree.add_node(sub1, parent)
        J(t, col, sub1, tree, errors)
    elif t.Token[1] in col.firsts['exe_statement']:
        sub2 = Node('exe_statement')
        tree.add_node(sub2, parent)
        B_(t, col, sub2, tree, errors)
    else:
        # error
        pass


def J(t, col, parent, tree, errors):
    """声明语句"""
    if t.Token[1] in col.firsts['v_declare']:
        sub1 = Node('v_declare')
        tree.add_node(sub1, parent)
        K(t, col, sub1, tree, errors)
    elif t.Token[1] in col.firsts['fun_declare']:
        sub2 = Node('fun_declare')
        tree.add_node(sub2, parent)
        S(t, col, sub2, tree, errors)
    pass


def K(t, col, parent, tree, errors):
    """值声明"""
    if t.Token[1] in col.firsts['con_declare']:
        # sub1 = Node('con_declare')
        # tree.add_node(sub1, parent)
        L(t, col, parent, tree, errors)
    elif t.Token[1] in col.firsts['var_declare']:
        O(t, col, parent, tree, errors)
    else:
        # error
        pass


def L(t, col, parent, tree, errors):
    """常量声明"""
    sub = Node('con_declare')
    tree.add_node(sub, parent)
    if t.Token[1] == 'const':
        match('const', t)
        if t.Token[1] not in col.firsts['con_type']:
            if t.Token[2].startswith('i'):
                t.Token[1] = f = 'int'
            elif t.Token[2].startswith('c'):
                t.Token[1] = f = 'char'
            elif t.Token[2].startswith('f'):
                t.Token[1] = f = 'float'
            errors.append(f'出现函数声明错误:{t.Token[2]},第{t.tokens[t.p - 2][3]}行')
            print(f'出现函数声明错误:{t.Token[2]},第{t.tokens[t.p - 2][3]}行')


        sub1 = Node('con_type')
        tree.add_node(sub1, sub)
        M(t, col, sub1, tree, errors)

        sub2 = Node('con_declare_list')
        tree.add_node(sub2, sub)
        N(t, col, sub2, tree, errors)
    else:
        # error
        pass


def M(t, col, parent, tree, errors):
    """常量类型"""
    if t.Token[1] == 'int':
        match('int', t)
        sub1 = Node('int')
        tree.add_node(sub1, parent)
    elif t.Token[1] == 'char':
        match('char', t)
        sub1 = Node('char')
        tree.add_node(sub1, parent)
    elif t.Token[1] == 'float':
        match('float', t)
        sub1 = Node('float')
        tree.add_node(sub1, parent)
    else:
        # errors.append(f'出现函数声明错误:{t.Token[2]},第{t.Token[3]}行')
        # error
        pass


def N(t, col, parent, tree, errors):
    """常量声明表"""
    if t.Token[1] == 'signal':
        tree.add_node(Node(t.Token[2]), parent)
        match('signal', t)
        if t.Token[1] == '=':
            match('=', t)

            sub = Node('con')
            tree.add_node(sub, parent)
            D(t, col, sub, tree, errors)

            sub1 = Node('con_declare_list')
            tree.add_node(sub1, parent)
            N1(t, col, sub1, tree, errors)
        else:
            print(f'出现常量声明错误,未赋初值，第{t.tokens[t.p - 2][3]}行')
            errors.append(f'出现常量声明错误,未赋初值，第{t.tokens[t.p - 2][3]}行')
            if t.Token[1] == ';':
                match(';', t)
            pass
    else:
        # error
        pass



def N1(t, col, parent, tree, errors):
    """常量声明表'"""
    if t.Token[1] == ';':
        match(';', t)
    elif t.Token[1] == ',':
        match(',', t)
        N(t, col, parent, tree, errors)
    else:
        errors.append(f'出现常量声明错误,缺少,号或;号，第{t.tokens[t.p - 2][3]}行')
        if t.Token[1] in col.firsts['con_list']:
            N(t, col, parent, tree, errors)
        pass


def O(t, col, parent, tree, errors):
    """变量声明"""
    sub = Node('var_declare')
    tree.add_node(sub, parent)

    sub1 = Node('var_type')
    tree.add_node(sub1, sub)
    R(t, col, sub1, tree, errors)

    sub2 = Node('var_list')
    tree.add_node(sub2, sub)
    P(t, col, sub2, tree, errors)


def P(t, col, parent, tree, errors):
    """变量声明表"""

    sub = Node('one_var_declare')
    tree.add_node(sub, parent)
    Q(t, col, sub, tree, errors)

    sub1 = parent
    if t.Token[1] in col.firsts["var_list'"]:
        sub1 = Node("var_list'")
        tree.add_node(sub1, parent)
    P1(t, col, sub1, tree, errors)
    pass


def P1(t, col, parent, tree, errors):
    """变量声明表'"""
    if t.Token[1] == ';' or t.Token[1] == ";":
        tree.add_node(Node(';'), parent)
        match(';', t)
    elif t.Token[1] == ',' or t.Token[1] == ",":
        match(',', t)
        if t.Token[1] in col.firsts['var_list']:
            sub1 = Node('var_list')
            tree.add_node(sub1, parent)
            P(t, col, sub1, tree, errors)
        else:
            errors.append(f'出现错误:,号后面是否声明变量或者结束该行语句?,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误:,号后面是否声明变量或者结束该行语句?,第{t.tokens[t.p - 2][3]}行')
    else:
        # error
        errors.append(f'出现错误:缺少;号,第{t.tokens[t.p-2][3]}行')
        print(f'出现错误:缺少;号,第{t.tokens[t.p-2][3]}行')
        pass


def Q(t, col, parent, tree, errors):
    """单变量声明"""

    sub = Node('var')
    tree.add_node(sub, parent)
    E(t, col, sub, tree, errors)

    sub1 = Node("one_var_declare'")
    tree.add_node(sub1, parent)
    Q1(t, col, sub1, tree, errors)


def Q1(t, col, parent, tree, errors):
    """单变量声明'"""
    if t.Token[1] == '=':
        tree.add_node(Node('='), parent)
        match('=', t)
        sub = Node('expression')
        tree.add_node(sub, parent)
        A_(t, col, sub, tree, errors)
    pass


def R(t, col, parent, tree, errors):
    """变量类型"""
    if t.Token[1] == 'int':
        match('int', t)
        tree.add_node(Node('int'), parent)
    elif t.Token[1] == 'char':
        match('char', t)
        tree.add_node(Node('char'), parent)
    elif t.Token[1] == 'float':
        match('float', t)
        tree.add_node(Node('float'), parent)
    else:
        # error
        pass


def S(t, col, parent, tree, errors):
    """函数声明"""

    sub1 = parent
    if t.Token[1] == '(':
        match('(', t)
        sub2 = Node('fun_declare_fpar_list')
        tree.add_node(sub2, sub1)
        U(t, col, sub2, tree, errors)

        if t.Token[1] == ')':
            match(')', t)
            if t.Token[1] == ';':
                match(';', t)
            else:
                # error
                errors.append(f'出现函数声明错误,函数声明缺少;号,第{t.tokens[t.p-2][3]}行')
                print(f'出现函数声明错误,函数声明缺少;号,第{t.tokens[t.p-2][3]}行')
                pass
        else:
            errors.append(f'出现函数声明错误,函数声明缺少右括号,第{t.tokens[t.p - 2][3]}行')
            print(f'出现函数声明错误,函数声明缺少右括号,第{t.tokens[t.p - 2][3]}行')
            if t.Token[1] == ';':
                match(';', t)
            else:
                errors.append(f'出现函数声明错误,函数声明缺少;号,第{t.tokens[t.p-2][3]}行')
                print(f'出现函数声明错误,函数声明缺少;号,第{t.tokens[t.p-2][3]}行')
                pass
    else:
        errors.append(f'出现函数声明错误,函数声明缺少左括号,第{t.tokens[t.p-2][3]}行')
        print(f'出现函数声明错误,函数声明缺少左括号,第{t.tokens[t.p-2][3]}行')
        if t.Token[1] in col.firsts['fun_define_fpar_list']:
            sub2 = Node('fun_declare_fpar_list')
            tree.add_node(sub2, sub1)
            U(t, col, sub2, tree, errors)

            if t.Token[1] == ')':
                match(')', t)
                if t.Token[1] == ';':
                    match(';', t)
                else:
                    errors.append(f'出现函数声明错误,函数声明缺少;号,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现函数声明错误,函数声明缺少;号,第{t.tokens[t.p - 2][3]}行')
            else:
                errors.append(f'出现函数声明错误,函数声明缺少右括号,第{t.tokens[t.p - 2][3]}行')
                print(f'出现函数声明错误,函数声明缺少右括号,第{t.tokens[t.p - 2][3]}行')
                if t.Token[1] == ';':
                    match(';', t)
                else:
                    errors.append(f'出现函数声明错误,函数声明缺少;号,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现函数声明错误,函数声明缺少;号,第{t.tokens[t.p - 2][3]}行')
                    pass
        else:
            if t.Token[1] == ')':
                match(')', t)
                if t.Token[1] == ';':
                    match(';', t)
                else:
                    errors.append(f'出现函数声明错误,函数声明缺少;号,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现函数声明错误,函数声明缺少;号,第{t.tokens[t.p - 2][3]}行')
                    pass
            else:
                errors.append(f'出现函数声明错误,函数声明缺少右括号,第{t.tokens[t.p - 2][3]}行')
                print(f'出现函数声明错误,函数声明缺少右括号,第{t.tokens[t.p - 2][3]}行')
                if t.Token[1] == ';':
                    match(';', t)
                else:
                    errors.append(f'出现函数声明错误,函数声明缺少;号,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现函数声明错误,函数声明缺少;号,第{t.tokens[t.p - 2][3]}行')


def T(t, col, parent, tree, errors):
    """函数类型"""
    if t.Token[1] == 'int':
        tree.add_node(Node('int'), parent)
        match('int', t)
    elif t.Token[1] == 'char':
        tree.add_node(Node('char'), parent)
        match('char', t)
    elif t.Token[1] == 'float':
        tree.add_node(Node('float'), parent)
        match('float', t)
    elif t.Token[1] == 'void':
        tree.add_node(Node('void'), parent)
        match('void', t)
    else:
        # error
        pass


def U(t, col, parent, tree, errors):
    """函数声明形参列表"""
    if t.Token[1] in col.firsts['fun_declare_fpar']:
        sub1 = Node('fun_declare_fpar')
        tree.add_node(sub1, parent)
        V(t, col, sub1, tree, errors)
    pass


def V(t, col, parent, tree, errors):
    """函数声明形参"""

    sub1 = Node('var_type')
    tree.add_node(sub1, parent)
    R(t, col, sub1, tree, errors)
    if t.Token[1] == 'signal':
        match('signal', t)
    else:
        errors.append(f'出现函数声明错误,函数声明形式参数不完整,第{t.tokens[t.p - 2][3]}行')
        print(f'出现函数声明错误,函数声明形式参数不完整,第{t.tokens[t.p - 2][3]}行')

    sub2 = Node("fun_declare_fpar'")
    tree.add_node(sub2, parent)
    V1(t, col, sub2, tree, errors)
    pass


def V1(t, col, parent, tree, errors):
    """函数声明形参'"""
    if t.Token[1] == ',':
        match(',', t)
        sub1 = Node('fun_declare_fpar')
        tree.add_node(sub1, parent)
        V(t, col, sub1, tree, errors)
    elif t.Token[1] in col.firsts['fun_declare_fpar']:
        errors.append(f'出现函数声明错误,函数声明形式参数之间缺少,号,第{t.tokens[t.p - 2][3]}行')
        print(f'出现函数声明错误,函数声明形式参数之间缺少,号,第{t.tokens[t.p - 2][3]}行')
        sub1 = Node('fun_declare_fpar')
        tree.add_node(sub1, parent)
        V(t, col, sub1, tree, errors)
    pass


def W(t, col, parent, tree, errors):
    """布尔表达式"""
    X(t, col, parent, tree, errors)
    W1(t, col, parent, tree, errors)
    pass


def W1(t, col, parent, tree, errors):
    """布尔表达式'"""
    if t.Token[1] == '||':
        match('||', t)
        W(t, col, parent, tree, errors)

    pass


def X(t, col, parent, tree, errors):
    """布尔项"""
    Y(t, col, parent, tree, errors)
    X1(t, col, parent, tree, errors)
    pass


def X1(t, col, parent, tree, errors):
    """布尔项'"""
    if t.Token[1] == '&&':
        match('&&', t)
        X(t, col, parent, tree, errors)
    pass


def Y(t, col, parent, tree, errors):
    """布尔因子"""
    # 同样存在相同firsts集合优先情况考虑
    if t.Token[1] in col.firsts['arg_exp'] and conditon(t):
        A(t, col, parent, tree, errors)
    elif t.Token[1] in col.firsts['rel_expression']:
        U_(t, col, parent, tree, errors)
    elif t.Token[1] == '!':
        match('!', t)
        W1(t, col, parent, tree, errors)
    else:
        # error
        pass


def Z(t, col, parent, tree, errors):
    """赋值表达式"""
    if t.Token[1] == 'signal':
        tree.add_node(Node(t.Token[2]), parent)
        match('signal', t)
        if t.Token[1] == '=':
            tree.add_node(Node('='), parent)
            match('=', t)
            A_(t, col, parent, tree, errors)
        else:
            errors.append(f'出现赋值错误,可能是声明语句出错,第{t.tokens[t.p-2][3]}行')
            print(f'出现赋值错误,可能是声明语句出错,第{t.tokens[t.p-2][3]}行')
            t.p -= 1
            t.Token = [-1, '=', 'None', -1]

            match('=', t)
            A_(t, col, parent, tree, errors)
            pass
    else:
        # error
        pass


def A_(t, col, parent, tree, errors):
    """表达式"""
    if t.Token[1] in col.firsts['arg_exp'] and conditon(t) and conditon1(t) and (t.tokens[t.p][1] != '='):
        sub1 = Node('arg_exp')
        tree.add_node(sub1, parent)
        A(t, col, sub1, tree, errors)
    elif t.Token[1] in col.firsts['rel_expression'] and (t.tokens[t.p][1] != '=' and conditon1(t)):
        sub2 = Node('rel_expression')
        tree.add_node(sub2, parent)
        U_(t, col, sub2, tree, errors)
    elif t.Token[1] in col.firsts['bool_expression'] and (t.tokens[t.p][1] != '='):
        sub3 = Node('bool_expression')
        tree.add_node(sub3, parent)
        W(t, col, sub3, tree, errors)
    elif t.Token[1] in col.firsts['assign_expression']:
        sub4 = Node('assign_expression')
        tree.add_node(sub4, parent)
        Z(t, col, sub4, tree, errors)
    else:
        errors.append(f'出现错误,缺少表达式?,第{t.tokens[t.p-2][3]}行')
        print(f'出现错误,缺少表达式?,第{t.tokens[t.p-2][3]}行')



def B_(t, col, parent, tree, errors):
    """执行语句"""
    if t.Token[1] in col.firsts['digit_exe_statement']:
        sub1 = Node('digit_exe_statement')
        tree.add_node(sub1, parent)
        C_(t, col, sub1, tree, errors)
    elif t.Token[1] in col.firsts['control_statement']:
        sub2 = Node('control_statement')
        tree.add_node(sub2, parent)
        F_(t, col, sub2, tree, errors)
    elif t.Token[1] in col.firsts['complex_statement']:
        G_(t, col, parent, tree, errors)
    else:
        # error
        pass


def C_(t, col, parent, tree, errors):
    """数据处理语句"""
    if t.Token[1] in col.firsts['assign_statement'] and (t.tokens[t.p][1] != '('):
        sub1 = Node('assign_statement')
        tree.add_node(sub1, parent)
        D_(t, col, sub1, tree, errors)
    elif t.Token[1] in col.firsts['fun_invoke_statement']:
        sub2 = Node('fun_invoke_statement')
        tree.add_node(sub2, parent)
        E_(t, col, sub2, tree, errors)
    else:
        # error
        pass


def D_(t, col, parent, tree, errors):
    """赋值语句"""

    sub1 = Node('assign_expression')
    tree.add_node(sub1, parent)
    Z(t, col, sub1, tree, errors)
    if t.Token[1] == ';':
        match(';', t)
    else:
        errors.append(f'出现错误,赋值语句缺少;号,第{t.tokens[t.p - 2][3]}行')
        print(f'出现错误,赋值语句缺少;号,第{t.tokens[t.p - 2][3]}行')



def E_(t, col, parent, tree, errors):
    """函数调用语句"""
    F(t, col, parent, tree, errors)
    if t.Token[1] == ';':
        match(';', t)
    else:
        errors.append('出现错误,赋值调用缺少;号,第{t.tokens[t.p - 2][3]}行')
        print(f'出现错误,赋值调用缺少;号,第{t.tokens[t.p - 2][3]}行')



def F_(t, col, parent, tree, errors):
    """控制语句"""
    if t.Token[1] in col.firsts['if_statement']:
        sub1 = Node('if_statement')
        tree.add_node(sub1, parent)
        I_(t, col, sub1, tree, errors)
    elif t.Token[1] in col.firsts['for_statement']:
        sub2 = Node('for_statement')
        tree.add_node(sub2, parent)
        J_(t, col, sub2, tree, errors)
    elif t.Token[1] in col.firsts['while_statement']:
        sub3 = Node('while_statement')
        tree.add_node(sub3, parent)
        K_(t, col, sub3, tree, errors)
    elif t.Token[1] in col.firsts['do_while_statement']:
        sub4 = Node('do_while_statement')
        tree.add_node(sub4, parent)
        L_(t, col, sub4, tree, errors)
    elif t.Token[1] in col.firsts['return_statement']:
        R_(t, col, parent, tree, errors)
    else:
        # error
        pass


def G_(t, col, parent, tree, errors):
    """复合语句"""

    sub1 = Node('complex_statement')
    tree.add_node(sub1, parent)
    if t.Token[1] == '{':
        match('{', t)

        sub2 = Node('statement_list')
        tree.add_node(sub2, sub1)
        H_(t, col, sub2, tree, errors)
        if t.Token[1] == '}':
            match('}', t)
        else:
            errors.append(f'出现错误,缺少右大括号,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误,缺少右大括号,第{t.tokens[t.p - 2][3]}行')
    else:
        errors.append(f'出现错误,复合语句缺少左大括号,第{t.tokens[t.p - 2][3]}行')
        print(f'出现错误,复合语句缺少左大括号,第{t.tokens[t.p - 2][3]}行')
        t.p -= 1
        t.Token = [-1, '{', 'None', -1]
        match('{', t)
        H_(t, col, parent, tree, errors)
        if t.Token[1] == '}':
            match('}', t)
        else:
            errors.append(f'出现错误,缺少右大括号,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误,缺少右大括号,第{t.tokens[t.p - 2][3]}行')


def H_(t, col, parent, tree, errors):
    """语句表"""

    sub1 = parent
    if t.Token[1] in col.firsts['statement']:
        sub1 = Node('statement')
        tree.add_node(sub1, parent)
    I(t, col, sub1, tree, errors)

    sub2 = parent
    if t.Token[1] in col.firsts["statement_list'"]:
        sub2 = Node("statement_list'")
        tree.add_node(sub2, parent)
    H_1(t, col, sub2, tree, errors)
    pass


def H_1(t, col, parent, tree, errors):
    """语句表'"""
    if t.Token[1] in col.firsts['statement_list']:
        H_(t, col, parent, tree, errors)
    pass


def I_(t, col, parent, tree, errors):
    """if语句"""
    if t.Token[1] == 'if':
        match('if', t)
        if t.Token[1] == '(':
            match('(', t)
            if t.Token[1] != 'signal':
                errors.append(f'出现错误,if语句表达式异常,第{t.tokens[t.p-2][3]}行')
                print(f'出现错误,if语句表达式异常,第{t.tokens[t.p-2][3]}行')
                t.p -= 1
                t.Token = [-1, 'signal', 'None', -1]

            sub1 = Node('expression')
            tree.add_node(sub1, parent)
            A_(t, col, sub1, tree, errors)
            if t.Token[1] == ')':
                match(')', t)
                # 如何解决复合函数左{号遗漏情况
                if t.Token[1] != '{':
                    left = t.Token[3]
                else:
                    left = 0

                sub2 = Node('statement')
                tree.add_node(sub2, parent)
                I(t, col, sub2, tree, errors)

                sub3 = Node("if_statement'")
                tree.add_node(sub3, parent)
                I_1(t, col, sub3, tree, errors)
                if t.Token[1] == '}' and left != 0 and t.p != len(t.tokens):
                    errors.append(f'出现错误,复合语句缺少左大括号,第{left}行')
                    print(f'出现错误,复合语句缺少左大括号,第{left}行')
                    match('}', t)
            else:
                errors.append(f'出现错误,if语句未右闭合,第{t.tokens[t.p-2][3]}行')
                print(f'出现错误,if语句未右闭合,第{t.tokens[t.p-2][3]}行')
                if t.Token[1] in col.firsts['statement']:
                    if t.Token[1] != '{':
                        left = t.Token[3]
                    else:
                        left = 0
                    I(t, col, parent, tree, errors)
                    I_1(t, col, parent, tree, errors)
                    if t.Token[1] == '}' and left != 0 and t.p != len(t.tokens):
                        errors.append(f'出现错误,复合语句缺少左大括号,第{left}行')
                        print(f'出现错误,复合语句缺少左大括号,第{left}行')
                        match('}', t)
                else:
                    return
        else:
            errors.append(f'出现错误,if语句未左闭合,第{t.tokens[t.p-2][3]}行')
            print(f'出现错误,if语句未左闭合,第{t.tokens[t.p-2][3]}行')
            if t.Token[1] in col.firsts['expression']:
                A_(t, col, parent, tree, errors)
                if t.Token[1] == ')':
                    match(')', t)
                    if t.Token[1] != '{':
                        left = t.Token[3]
                    else:
                        left = 0
                    I(t, col, parent, tree, errors)
                    I_1(t, col, parent, tree, errors)
                    if t.Token[1] == '}' and left != 0 and t.p != len(t.tokens):
                        errors.append(f'出现错误,复合语句缺少左大括号,第{left}行')
                        print(f'出现错误,复合语句缺少左大括号,第{left}行')
                        match('}', t)
                else:
                    errors.append(f'出现错误,if语句未右闭合,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现错误,if语句未右闭合,第{t.tokens[t.p - 2][3]}行')
                    if t.Token[1] in col.firsts['statement']:
                        if t.Token[1] != '{':
                            left = t.Token[3]
                        else:
                            left = 0
                        I(t, col, parent, tree, errors)
                        I_1(t, col, parent, tree, errors)
                        if t.Token[1] == '}' and left != 0 and t.p != len(t.tokens):
                            errors.append(f'出现错误,复合语句缺少左大括号,第{left}行')
                            print(f'出现错误,复合语句缺少左大括号,第{left}行')
                            match('}', t)
                    else:
                        return
            else:
                errors.append(f'出现错误,if语句缺少表达式,第{t.tokens[t.p - 2][3]}行')
                print(f'出现错误,if语句缺少表达式,第{t.tokens[t.p - 2][3]}行')
                if t.Token[1] == ')':
                    match(')', t)
                else:
                    errors.append(f'出现错误,if语句未右闭合,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现错误,if语句未右闭合,第{t.tokens[t.p - 2][3]}行')
                if t.Token[1] in col.firsts['statement']:
                    if t.Token[1] != '{':
                        left = t.Token[3]
                    else:
                        left = 0
                    I(t, col, parent, tree, errors)
                    I_1(t, col, parent, tree, errors)
                    if t.Token[1] == '}' and left != 0 and t.p != len(t.tokens):
                        errors.append(f'出现错误,复合语句缺少左大括号,第{left}行')
                        print(f'出现错误,复合语句缺少左大括号,第{left}行')
                        match('}', t)
                else:
                    return
    else:
        # error
        pass


def I_1(t, col, parent, tree, errors):
    """if语句'"""
    if t.Token[1] == 'else':
        match('else', t)
        I(t, col, parent, tree, errors)
    pass


def J_(t, col, parent, tree, errors):
    """for语句"""
    if t.Token[1] == 'for':
        match('for', t)
        if t.Token[1] == '(':
            match('(', t)

            sub1 = Node('expression')
            tree.add_node(sub1, parent)
            A_(t, col, sub1, tree, errors)
            if t.Token[1] == ';':
                match(';', t)

                sub2 = Node('expression')
                tree.add_node(sub2, parent)
                A_(t, col, sub2, tree, errors)
                if t.Token[1] == ';':
                    match(';', t)

                    sub3 = Node('expression')
                    tree.add_node(sub3, parent)
                    A_(t, col, sub3, tree, errors)
                    if t.Token[1] == ')':
                        match(')', t)
                        sub4 = Node('cir_statement')
                        tree.add_node(sub4, parent)
                        M_(t, col, sub4, tree, errors)
                    else:
                        errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p-2][3]}行')
                        print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p-2][3]}行')
                        if t.Token[1] in col.firsts['cir_statement']:
                            M_(t, col, parent, tree, errors)
                else:
                    errors.append(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                    if t.Token[1] in col.firsts['expression']:
                        A_(t, col, parent, tree, errors)
                        if t.Token[1] == ')':
                            match(')', t)
                            M_(t, col, parent, tree, errors)
                        else:
                            errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                            if t.Token[1] in col.firsts['cir_statement']:
                                M_(t, col, parent, tree, errors)
                    else:
                        if t.Token[1] == ')':
                            match(')', t)

                            M_(t, col, parent, tree, errors)
                        else:
                            errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                            if t.Token[1] in col.firsts['cir_statement']:
                                M_(t, col, parent, tree, errors)
            else:
                errors.append(f'出现错误,for语句缺少第1个;号,第{t.tokens[t.p-2][3]}行')
                print(f'出现错误,for语句缺少第1个;号,第{t.tokens[t.p-2][3]}行')
                if t.Token[1] in col.firsts['expression']:
                    A_(t, col, parent, tree, errors)
                    if t.Token[1] == ';':
                        match(';', t)
                        A_(t, col, parent, tree, errors)
                        if t.Token[1] == ')':
                            match(')', t)
                            M_(t, col, parent, tree, errors)
                        else:
                            errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                            if t.Token[1] in col.firsts['cir_statement']:
                                M_(t, col, parent, tree, errors)
                    else:
                        errors.append(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                        print(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                        if t.Token[1] in col.firsts['expression']:
                            A_(t, col, parent, tree, errors)
                            if t.Token[1] == ')':
                                match(')', t)
                                M_(t, col, parent, tree, errors)
                            else:
                                errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                if t.Token[1] in col.firsts['cir_statement']:
                                    M_(t, col, parent, tree, errors)
                        else:
                            if t.Token[1] == ')':
                                match(')', t)
                                M_(t, col, parent, tree, errors)
                            else:
                                errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                if t.Token[1] in col.firsts['cir_statement']:
                                    M_(t, col, parent, tree, errors)
                else:
                    if t.Token[1] == ';':
                        match(';', t)
                        A_(t, col, parent, tree, errors)
                        if t.Token[1] == ')':
                            match(')', t)
                            M_(t, col, parent, tree, errors)
                        else:
                            errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                            if t.Token[1] in col.firsts['cir_statement']:
                                M_(t, col, parent, tree, errors)
                    else:
                        errors.append(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                        print(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                        if t.Token[1] in col.firsts['expression']:
                            A_(t, col, parent, tree, errors)
                            if t.Token[1] == ')':
                                match(')', t)
                                M_(t, col, parent, tree, errors)
                            else:
                                errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                if t.Token[1] in col.firsts['cir_statement']:
                                    M_(t, col, parent, tree, errors)
                        else:
                            if t.Token[1] == ')':
                                match(')', t)
                                M_(t, col, parent, tree, errors)
                            else:
                                errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                if t.Token[1] in col.firsts['cir_statement']:
                                    M_(t, col, parent, tree, errors)
        else:
            errors.append(f'出现错误,for语句左括号未闭合,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误,for语句左括号未闭合,第{t.tokens[t.p - 2][3]}行')
            if t.Token[1] in col.firsts['expression']:
                A_(t, col, parent, tree, errors)
                if t.Token[1] == ';':
                    match(';', t)
                    A_(t, col, parent, tree, errors)
                    if t.Token[1] == ';':
                        match(';', t)
                        A_(t, col, parent, tree, errors)
                        if t.Token[1] == ')':
                            match(')', t)
                            M_(t, col, parent, tree, errors)
                        else:
                            errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                            if t.Token[1] in col.firsts['cir_statement']:
                                M_(t, col, parent, tree, errors)
                    else:
                        errors.append(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                        print(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                        if t.Token[1] in col.firsts['expression']:
                            A_(t, col, parent, tree, errors)
                            if t.Token[1] == ')':
                                match(')', t)
                                M_(t, col, parent, tree, errors)
                            else:
                                errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                if t.Token[1] in col.firsts['cir_statement']:
                                    M_(t, col, parent, tree, errors)
                        else:
                            if t.Token[1] == ')':
                                match(')', t)
                                M_(t, col, parent, tree, errors)
                            else:
                                errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                if t.Token[1] in col.firsts['cir_statement']:
                                    M_(t, col, parent, tree, errors)
                else:
                    errors.append(f'出现错误,for语句缺少第1个;号,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现错误,for语句缺少第1个;号,第{t.tokens[t.p - 2][3]}行')
                    if t.Token[1] in col.firsts['expression']:
                        A_(t, col, parent, tree, errors)
                        if t.Token[1] == ';':
                            match(';', t)
                            A_(t, col, parent, tree, errors)
                            if t.Token[1] == ')':
                                match(')', t)
                                M_(t, col, parent, tree, errors)
                            else:
                                errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                if t.Token[1] in col.firsts['cir_statement']:
                                    M_(t, col, parent, tree, errors)
                        else:
                            errors.append(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                            if t.Token[1] in col.firsts['expression']:
                                A_(t, col, parent, tree, errors)
                                if t.Token[1] == ')':
                                    match(')', t)
                                    M_(t, col, parent, tree, errors)
                                else:
                                    errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    if t.Token[1] in col.firsts['cir_statement']:
                                        M_(t, col, parent, tree, errors)
                            else:
                                if t.Token[1] == ')':
                                    match(')', t)
                                    M_(t, col, parent, tree, errors)
                                else:
                                    errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    if t.Token[1] in col.firsts['cir_statement']:
                                        M_(t, col, parent, tree, errors)
                    else:
                        if t.Token[1] == ';':
                            match(';', t)
                            A_(t, col, parent, tree, errors)
                            if t.Token[1] == ')':
                                match(')', t)
                                M_(t, col, parent, tree, errors)
                            else:
                                errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                if t.Token[1] in col.firsts['cir_statement']:
                                    M_(t, col, parent, tree, errors)
                        else:
                            errors.append(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                            if t.Token[1] in col.firsts['expression']:
                                A_(t, col, parent, tree, errors)
                                if t.Token[1] == ')':
                                    match(')', t)
                                    M_(t, col, parent, tree, errors)
                                else:
                                    errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    if t.Token[1] in col.firsts['cir_statement']:
                                        M_(t, col, parent, tree, errors)
                            else:
                                if t.Token[1] == ')':
                                    match(')', t)
                                    M_(t, col, parent, tree, errors)
                                else:
                                    errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    if t.Token[1] in col.firsts['cir_statement']:
                                        M_(t, col, parent, tree, errors)
            else:
                if t.Token[1] == ';':
                    match(';', t)
                    A_(t, col, parent, tree, errors)
                    if t.Token[1] == ';':
                        match(';', t)
                        A_(t, col, parent, tree, errors)
                        if t.Token[1] == ')':
                            match(')', t)
                            M_(t, col, parent, tree, errors)
                        else:
                            errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                            if t.Token[1] in col.firsts['cir_statement']:
                                M_(t, col, parent, tree, errors)
                    else:
                        errors.append(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                        print(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                        if t.Token[1] in col.firsts['expression']:
                            A_(t, col, parent, tree, errors)
                            if t.Token[1] == ')':
                                match(')', t)
                                M_(t, col, parent, tree, errors)
                            else:
                                errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                if t.Token[1] in col.firsts['cir_statement']:
                                    M_(t, col, parent, tree, errors)
                        else:
                            if t.Token[1] == ')':
                                match(')', t)
                                M_(t, col, parent, tree, errors)
                            else:
                                errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                if t.Token[1] in col.firsts['cir_statement']:
                                    M_(t, col, parent, tree, errors)
                else:
                    errors.append(f'出现错误,for语句缺少第1个;号,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现错误,for语句缺少第1个;号,第{t.tokens[t.p - 2][3]}行')
                    if t.Token[1] in col.firsts['expression']:
                        A_(t, col, parent, tree, errors)
                        if t.Token[1] == ';':
                            match(';', t)
                            A_(t, col, parent, tree, errors)
                            if t.Token[1] == ')':
                                match(')', t)
                                M_(t, col, parent, tree, errors)
                            else:
                                errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                if t.Token[1] in col.firsts['cir_statement']:
                                    M_(t, col, parent, tree, errors)
                        else:
                            errors.append(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                            if t.Token[1] in col.firsts['expression']:
                                A_(t, col, parent, tree, errors)
                                if t.Token[1] == ')':
                                    match(')', t)
                                    M_(t, col, parent, tree, errors)
                                else:
                                    errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    if t.Token[1] in col.firsts['cir_statement']:
                                        M_(t, col, parent, tree, errors)
                            else:
                                if t.Token[1] == ')':
                                    match(')', t)
                                    M_(t, col, parent, tree, errors)
                                else:
                                    errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    if t.Token[1] in col.firsts['cir_statement']:
                                        M_(t, col, parent, tree, errors)
                    else:
                        if t.Token[1] == ';':
                            match(';', t)
                            A_(t, col, parent, tree, errors)
                            if t.Token[1] == ')':
                                match(')', t)
                                M_(t, col, parent, tree, errors)
                            else:
                                errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                if t.Token[1] in col.firsts['cir_statement']:
                                    M_(t, col, parent, tree, errors)
                        else:
                            errors.append(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,for语句缺少第2个;号,第{t.tokens[t.p - 2][3]}行')
                            if t.Token[1] in col.firsts['expression']:
                                A_(t, col, parent, tree, errors)
                                if t.Token[1] == ')':
                                    match(')', t)
                                    M_(t, col, parent, tree, errors)
                                else:
                                    errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    if t.Token[1] in col.firsts['cir_statement']:
                                        M_(t, col, parent, tree, errors)
                            else:
                                if t.Token[1] == ')':
                                    match(')', t)
                                    M_(t, col, parent, tree, errors)
                                else:
                                    errors.append(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    print(f'出现错误,for语句右括号未闭合,第{t.tokens[t.p - 2][3]}行')
                                    if t.Token[1] in col.firsts['cir_statement']:
                                        M_(t, col, parent, tree, errors)
    else:
        # error
        pass


def K_(t, col, parent, tree, errors):
    """while语句"""
    if t.Token[1] == 'while':
        match('while', t)
        if t.Token[1] == '(':
            match('(', t)
            sub1 = Node('expression')
            tree.add_node(sub1, parent)
            A_(t, col, sub1, tree, errors)
            if t.Token[1] == ')':
                match(')', t)
                if t.Token[1] != '{':
                    left = t.Token[3]
                else:
                    left = 0
                sub2 = Node('cir_statement')
                tree.add_node(sub2, parent)
                M_(t, col, sub2, tree, errors)
                if t.Token[1] == '}' and left != 0 and t.p != len(t.tokens):
                    errors.append(f'出现错误,while语句缺少左大括号,第{left}行')
                    print(f'出现错误,while语句缺少左大括号,第{left}行')
                    match('}', t)
            else:
                errors.append(f'出现错误,while语句括号未右闭合,第{t.tokens[t.p-2][3]}行')
                print(f'出现错误,while语句括号未右闭合,第{t.tokens[t.p-2][3]}行')
                if t.Token[1] in col.firsts['cir_statement']:
                    M_(t, col, parent, tree, errors)
                # error
                pass
        else:
            errors.append(f'出现错误,while语句括号未左闭合,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误,while语句括号未左闭合,第{t.tokens[t.p - 2][3]}行')
            if t.Token[1] == ')':
                match(')', t)
                M_(t, col, parent, tree, errors)
            else:
                errors.append(f'出现错误,while语句括号未右闭合,第{t.tokens[t.p-2][3]}行')
                print(f'出现错误,while语句括号未右闭合,第{t.tokens[t.p-2][3]}行')
                if t.Token[1] in col.firsts['cir_statement']:
                    M_(t, col, parent, tree, errors)
    else:
        # error
        pass


def L_(t, col, parent, tree, errors):
    """dowhile语句"""
    if t.Token[1] == 'do':
        match('do', t)
        if t.Token[1] != '{':
            errors.append(f'出现错误,复合语句缺少左大括号,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误,复合语句缺少左大括号,第{t.tokens[t.p - 2][3]}行')
            t.p -= 1
            t.Token = [-1, '{', 'None', -1]

        sub1 = Node('cir_complex_statement')
        tree.add_node(sub1, parent)
        N_(t, col, sub1, tree, errors)
        if t.Token[1] == 'while':
            match('while', t)
            if t.Token[1] == '(':
                match('(', t)

                sub2 = Node('expression')
                tree.add_node(sub2, parent)
                A_(t, col, sub2, tree, errors)
                if t.Token[1] == ')':
                    match(')', t)
                    if t.Token[1] == ';':
                        match(';', t)
                    else:
                        errors.append(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p-2][3]}行')
                        print(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p-2][3]}行')
                else:
                    errors.append(f'出现错误,dowhile语句括号未右闭合,第{t.tokens[t.p-2][3]}行')
                    print(f'出现错误,dowhile语句括号未右闭合,第{t.tokens[t.p-2][3]}行')
                    if t.Token[1] == ';':
                        match(';', t)
                    else:
                        errors.append(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p-2][3]}行')
                        print(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p-2][3]}行')
            else:
                errors.append(f'出现错误,dowhile语句括号未左闭合,第{t.tokens[t.p - 2][3]}行')
                print(f'出现错误,dowhile语句括号未左闭合,第{t.tokens[t.p - 2][3]}行')
                if t.Token[1] in col.firsts['expression']:
                    A_(t, col, parent, tree, errors)
                    if t.Token[1] == ')':
                        match(')', t)
                        if t.Token[1] == ';':
                            match(';', t)
                        else:
                            errors.append(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                    else:
                        errors.append(f'出现错误,dowhile语句括号未右闭合,第{t.tokens[t.p - 2][3]}行')
                        print(f'出现错误,dowhile语句括号未右闭合,第{t.tokens[t.p - 2][3]}行')
                        if t.Token[1] == ';':
                            match(';', t)
                        else:
                            errors.append(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                else:
                    errors.append(f'出现错误,dowhile语句缺少表达式,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现错误,dowhile语句缺少表达式,第{t.tokens[t.p - 2][3]}行')
                    if t.Token[1] == ')':
                        match(')', t)
                        if t.Token[1] == ';':
                            match(';', t)
                        else:
                            errors.append(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                    else:
                        errors.append(f'出现错误,dowhile语句括号未右闭合,第{t.tokens[t.p - 2][3]}行')
                        print(f'出现错误,dowhile语句括号未右闭合,第{t.tokens[t.p - 2][3]}行')
                        if t.Token[1] == ';':
                            match(';', t)
                        else:
                            errors.append(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
        else:
            errors.append(f'出现错误,dowhile语句末尾缺少while,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误,dowhile语句末尾缺少while,第{t.tokens[t.p - 2][3]}行')
            if t.Token[1] == '(':
                match('(', t)
                A_(t, col, parent, tree, errors)
                if t.Token[1] == ')':
                    match(')', t)
                    if t.Token[1] == ';':
                        match(';', t)
                    else:
                        errors.append(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                        print(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                else:
                    errors.append(f'出现错误,dowhile语句括号未右闭合,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现错误,dowhile语句括号未右闭合,第{t.tokens[t.p - 2][3]}行')
                    if t.Token[1] == ';':
                        match(';', t)
                    else:
                        errors.append(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                        print(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
            else:
                errors.append(f'出现错误,dowhile语句括号未左闭合,第{t.tokens[t.p - 2][3]}行')
                print(f'出现错误,dowhile语句括号未左闭合,第{t.tokens[t.p - 2][3]}行')
                if t.Token[1] in col.firsts['expression']:
                    A_(t, col, parent, tree, errors)
                    if t.Token[1] == ')':
                        match(')', t)
                        if t.Token[1] == ';':
                            match(';', t)
                        else:
                            errors.append(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                    else:
                        errors.append(f'出现错误,dowhile语句括号未右闭合,第{t.tokens[t.p - 2][3]}行')
                        print(f'出现错误,dowhile语句括号未右闭合,第{t.tokens[t.p - 2][3]}行')
                        if t.Token[1] == ';':
                            match(';', t)
                        else:
                            errors.append(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                else:
                    errors.append(f'出现错误,dowhile语句缺少表达式,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现错误,dowhile语句缺少表达式,第{t.tokens[t.p - 2][3]}行')
                    if t.Token[1] == ')':
                        match(')', t)
                        if t.Token[1] == ';':
                            match(';', t)
                        else:
                            errors.append(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                    else:
                        errors.append(f'出现错误,dowhile语句括号未右闭合,第{t.tokens[t.p - 2][3]}行')
                        print(f'出现错误,dowhile语句括号未右闭合,第{t.tokens[t.p - 2][3]}行')
                        if t.Token[1] == ';':
                            match(';', t)
                        else:
                            errors.append(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
                            print(f'出现错误,dowhile语句末尾缺少;号,第{t.tokens[t.p - 2][3]}行')
    else:
        # error
        pass


def M_(t, col, parent, tree, errors):
    """循环语句"""
    # 书上给的词法在循环语句中没有执行语句,在循环内的执行语句如赋值无法正确识别 ----
    # if t.Token[1] in col.firsts['exe_statement']:
    #     B_(t, col, parent, tree, errors)
    # 新增2个文法右部
    if t.Token[1] in col.firsts['digit_exe_statement']:
        sub1 = Node('digit_exe_statement')
        tree.add_node(sub1, parent)
        C_(t, col, sub1, tree, errors)
    elif t.Token[1] in col.firsts['fun_invoke_statement']:
        sub2 = Node('fun_invoke_statement')
        tree.add_node(sub2, parent)
        E_(t, col, sub2, tree, errors)
    elif t.Token[1] in col.firsts['declare_statement']:
        sub3 = Node('declare_statement')
        tree.add_node(sub3, parent)
        J(t, col, sub3, tree, errors)
    elif t.Token[1] in col.firsts['cir_exe_statement']:
        sub4 = Node('cir_exe_statement')
        tree.add_node(sub4, parent)
        P_(t, col, sub4, tree, errors)
    elif t.Token[1] in col.firsts['cir_complex_statement']:
        sub5 = Node('cir_complex_statement')
        tree.add_node(sub5, parent)
        N_(t, col, sub5, tree, errors)
    elif t.Token[1] == ';':
        match(';', t)
    else:
        # error
        pass


def N_(t, col, parent, tree, errors):
    """循环用复合语句"""
    if t.Token[1] == '{':
        match('{', t)
        O_(t, col, parent, tree, errors)
        if t.Token[1] == '}':
            match('}', t)
        else:
            errors.append(f'出现错误,复合语句缺少右大括号,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误,复合语句缺少右大括号,第{t.tokens[t.p - 2][3]}行')
    else:
        # error
        pass


def O_(t, col, parent, tree, errors):
    """循环语句表"""
    M_(t, col, parent, tree, errors)
    # 书上的循环语句无函数调用语句
    O_1(t, col, parent, tree, errors)
    pass


def O_1(t, col, parent, tree, errors):
    """循环语句表'"""
    if t.Token[1] in col.firsts['cir_statement_list']:
        O_(t, col, parent, tree, errors)


def P_(t, col, parent, tree, errors):
    """循环执行语句"""
    if t.Token[1] in col.firsts['cir_if_statement']:
        sub1 = Node('cir_if_statement')
        tree.add_node(sub1, parent)
        Q_(t, col, sub1, tree, errors)
    elif t.Token[1] in col.firsts['for_statement']:
        sub2 = Node('for_statement')
        tree.add_node(sub2, parent)
        J_(t, col, sub2, tree, errors)
    elif t.Token[1] in col.firsts['while_statement']:
        sub3 = Node('while_statement')
        tree.add_node(sub3, parent)
        K_(t, col, sub3, tree, errors)
    elif t.Token[1] in col.firsts['do_while_statement']:
        sub4 = Node('do_while_statement')
        tree.add_node(sub4, parent)
        L_(t, col, sub4, tree, errors)
    elif t.Token[1] in col.firsts['return_statement']:
        sub5 = Node('return_statement')
        tree.add_node(sub5, parent)
        R_(t, col, sub5, tree, errors)
    elif t.Token[1] in col.firsts['break_statement']:
        sub6 = Node('break_statement')
        tree.add_node(sub6, parent)
        S_(t, col, sub6, tree, errors)
    elif t.Token[1] in col.firsts['continue_statement']:
        sub7 = Node('continue_statement')
        tree.add_node(sub7, parent)
        T_(t, col, sub7, tree, errors)
    else:
        # error
        pass


def Q_(t, col, parent, tree, errors):
    """循环用if语句"""
    if t.Token[1] == 'if':
        match('if', t)
        if t.Token[1] == '(':
            match('(', t)
            A_(t, col, parent, tree, errors)
            if t.Token[1] == ')':
                match(')', t)
                if t.Token[1] != '{':
                    left = t.Token[3]
                else:
                    left = 0
                # 书上文法无语句
                I(t, col, parent, tree, errors)
                Q_1(t, col, parent, tree, errors)
                if t.Token[1] == '}' and left != 0 and t.p != len(t.tokens):
                    errors.append(f'出现错误,复合语句缺少左大括号,第{left}行')
                    print(f'出现错误,复合语句缺少左大括号,第{left}行')
                    match('}', t)
            else:
                errors.append(f'出现错误,if语句未右闭合,第{t.tokens[t.p - 2][3]}行')
                print(f'出现错误,if语句未右闭合,第{t.tokens[t.p - 2][3]}行')
                if t.Token[1] in col.firsts["cir_if_statement'"]:
                    Q_1(t, col, parent, tree, errors)
                else:
                    return
        else:
            errors.append(f'出现错误,if语句未左闭合,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误,if语句未左闭合,第{t.tokens[t.p - 2][3]}行')
            if t.Token[1] in col.firsts['expression']:
                A_(t, col, parent, tree, errors)
                if t.Token[1] == ')':
                    match(')', t)
                    Q_1(t, col, parent, tree, errors)
                else:
                    errors.append(f'出现错误,if语句未右闭合,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现错误,if语句未右闭合,第{t.tokens[t.p - 2][3]}行')
                    if t.Token[1] in col.firsts["cir_if_statement'"]:
                        Q_1(t, col, parent, tree, errors)
                    else:
                        return
            else:
                errors.append(f'出现错误,if语句缺少表达式,第{t.tokens[t.p - 2][3]}行')
                print(f'出现错误,if语句缺少表达式,第{t.tokens[t.p - 2][3]}行')
                if t.Token[1] == ')':
                    match(')', t)
                else:
                    errors.append(f'出现错误,if语句未右闭合,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现错误,if语句未右闭合,第{t.tokens[t.p - 2][3]}行')
                if t.Token[1] in col.firsts["cir_if_statement'"]:
                    Q_1(t, col, parent, tree, errors)
                else:
                    return
    else:
        # error
        pass


def Q_1(t, col, parent, tree, errors):
    """循环用if语句'"""
    if t.Token[1] == 'else':
        match('else', t)
        M_(t, col, parent, tree, errors)
    pass


def R_(t, col, parent, tree, errors):
    """return语句"""
    if t.Token[1] == 'return':
        match('return', t)
        sub1 = Node('return_statement')
        tree.add_node(sub1, parent)
        R_1(t, col, sub1, tree, errors)
    pass


def R_1(t, col, parent, tree, errors):
    """return语句"""
    if t.Token[1] == ';':
        match(';', t)
        if t.Token[1] != '}':
            errors.append(f'出现错误,复合语句缺少右大括号,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误,复合语句缺少右大括号,第{t.tokens[t.p - 2][3]}行')
            t.p -= 1
            t.Token = [-1, '}', 'None', -1]
    elif t.Token[1] in col.firsts['expression']:
        sub1 = Node('expression')
        tree.add_node(sub1, parent)
        A_(t, col, sub1, tree, errors)
        if t.Token[1] == ';':
            match(';', t)
        else:
            errors.append(f'出现错误,return语句缺少;号,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误,return语句缺少;号,第{t.tokens[t.p - 2][3]}行')
    else:
        # error
        pass


def S_(t, col, parent, tree, errors):
    """break语句"""
    if t.Token[1] == 'break':
        match('break', t)
        if t.Token[1] == ';':
            match(';', t)
        else:
            errors.append(f'出现错误,break语句缺少;号,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误,break语句缺少;号,第{t.tokens[t.p - 2][3]}行')
    else:
        # error
        pass


def T_(t, col, parent, tree, errors):
    """continue语句"""
    if t.Token[1] == 'continue':
        match('continue', t)
        if t.Token[1] == ';':
            match(';', t)
        else:
            errors.append(f'出现错误,continue语句缺少;号,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误,continue语句缺少;号,第{t.tokens[t.p - 2][3]}行')
    else:
        # error
        pass


def U_(t, col, parent, tree, errors):
    """关系表达式"""
    sub1 = Node('arg_exp')
    tree.add_node(sub1, parent)
    A(t, col, sub1, tree, errors)

    sub2 = parent
    if t.Token[1] in col.firsts['rel_expression']:
        sub2 = Node('rel_expression')
        tree.add_node(sub2, parent)
    V_(t, col, sub2, tree, errors)

    sub3 = parent
    if t.Token[1] in col.firsts['arg_exp']:
        sub3 = Node('arg_exp')
        tree.add_node(sub3, parent)
    A(t, col, sub3, tree, errors)
    pass


def V_(t, col, parent, tree, errors):
    """关系运算符"""
    if t.Token[1] == '>':
        tree.add_node(Node('>'), parent)
        match('>', t)
    elif t.Token[1] == '<':
        tree.add_node(Node('<'), parent)
        match('<', t)
    elif t.Token[1] == '>=':
        tree.add_node(Node('>='), parent)
        match('>=', t)
    elif t.Token[1] == '<=':
        tree.add_node(Node('<='), parent)
        match('<=', t)
    elif t.Token[1] == '==':
        tree.add_node(Node('=='), parent)
        match('==', t)
    elif t.Token[1] == '!=':
        tree.add_node(Node('!='), parent)
        match('!=', t)
    else:
        # error
        pass


def W_(t, col, parent, tree, errors):
    """函数定义"""
    sub1 = Node('fun_define')
    tree.add_node(sub1, parent)

    sub2 = Node('fun_type')
    tree.add_node(sub2, sub1)
    T(t, col, sub2, tree, errors)
    if t.Token[1] == 'signal':
        tree.add_node(Node(t.Token[2]), sub1)
        match('signal', t)
        if t.Token[1] == '(':
            match('(', t)
            sub3 = Node('fun_define_fpar_list')
            tree.add_node(sub3, sub1)
            X_(t, col, sub3, tree, errors)
            if t.Token[1] == ')':
                match(')', t)
                G_(t, col, sub1, tree, errors)
            else:
                errors.append(f'出现错误,函数定义语句缺少右括号,第{t.tokens[t.p - 2][3]}行')
                print(f'出现错误,函数定义语句缺少右括号,第{t.tokens[t.p - 2][3]}行')
                if t.Token[1] in col.firsts['complex_statement']:
                    G_(t, col, parent, tree, errors)
        else:
            errors.append(f'出现错误,函数定义语句缺少左括号,第{t.tokens[t.p - 2][3]}行')
            print(f'出现错误,函数定义语句缺少左括号,第{t.tokens[t.p - 2][3]}行')
            if t.Token[1] in col.firsts['fun_define_fpar_list']:
                X_(t, col, parent, tree, errors)
                if t.Token[1] == ')':
                    match(')', t)
                    G_(t, col, parent, tree, errors)
                else:
                    errors.append(f'出现错误,函数定义语句缺少右括号,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现错误,函数定义语句缺少右括号,第{t.tokens[t.p - 2][3]}行')
                    if t.Token[1] in col.firsts['complex_statement']:
                        G_(t, col, parent, tree, errors)
            else:
                if t.Token[1] == ')':
                    match(')', t)
                    G_(t, col, parent, tree, errors)
                else:
                    errors.append(f'出现错误,函数定义语句缺少右括号,第{t.tokens[t.p - 2][3]}行')
                    print(f'出现错误,函数定义语句缺少右括号,第{t.tokens[t.p - 2][3]}行')
                    if t.Token[1] in col.firsts['complex_statement']:
                        G_(t, col, parent, tree, errors)

    else:
        # error
        pass


def X_(t, col, parent, tree, errors):
    """函数定义形参列表"""
    if t.Token[1] in col.firsts['fun_define_fpar']:
        Y_(t, col, parent, tree, errors)
    pass


def Y_(t, col, parent, tree, errors):
    """函数定义形参"""
    R(t, col, parent, tree, errors)
    if t.Token[1] == 'signal':
        tree.add_node(Node(t.Token[2]), parent)
        match('signal', t)
        Y_1(t, col, parent, tree, errors)
    else:
        # error
        pass


def Y_1(t, col, parent, tree, errors):
    """函数定义形参'"""
    if t.Token[1] == ',':
        match(',', t)
        Y_(t, col, parent, tree, errors)
    pass


def Z_(t, col, parent, tree, errors):
    """程序"""
    J(t, col, parent, tree, errors)
    if t.Token[1] == 'main':
        match('main', t)
        if t.Token[1] == '(':
            match('(', t)
            if t.Token[1] == ')':
                match(')', t)
                G_(t, col, parent, tree, errors)
                A__(t, col, parent, tree, errors)
            else:
                # error
                pass
        else:
            # error
            pass
    else:
        # error
        pass


def A__(t, col, parent, tree, errors):
    """函数块"""
    if t.Token[1] in col.firsts['fun_define']:
        W_(t, col, parent, tree, errors)
        A__(t, col, parent, tree, errors)






