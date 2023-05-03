import copy

from Project.Lib4_Semantic_Analyse.Tables import ConstItem, VarItem, Temp, ENTRY


# 临时变量创建器
temp_obj = Temp()
# 布尔变量标记 标记上一个出现的布尔运算符
bool_lastmark = ['']
# 出口补偿 忘了
entry_offset = [0]
# 循环内判断 1在循环中 0不在
cir_state = [0]


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
    while p < len(t.tokens) and t.tokens[p][1] != ';' and t.tokens[p][1] != '&&' and t.tokens[p][1] != '||':
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
    while (p < len(t.tokens) and t.tokens[p][1] != ';'):
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

def A(t, col, item, var_table, op_table, node, chain):
    """算术表达式"""
    # 算术操作[ , , ,T] 添加四元式
    next_node = node
    if node:
        if (node[0] in ['+', '-']) and (t.tokens[t.p][2] in ['*', '/']):
            temp = temp_obj.newtemp()
            if not node[1]:
                node[1] = temp
            elif not node[2]:
                node[2] = temp
            next_node = ['', '', '', temp]
            var_table.add_obj(VarItem(name=temp))
    B(t, col, item, var_table, op_table, next_node, chain)
    if node:
        if node[0] and node[1] and node[2] and node[3] and (t.Token[1] not in ['+', '-', '*', '/']):
            if not node[1].isdigit():
                if var_table.search(node[1]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass
            if not node[2].isdigit():
                if var_table.search(node[2]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass
            # if var_table.search(node[3]):
            #     var_temp = VarItem()
            #     var_temp.name = node[3]
            #     var_temp.type = 'None'
            #     if node[0] == '+':
            #         val_1 = node[1]
            #         val_2 = node[2]
            #         if not node[1].isdigit():
            #             val_1 = var_table.get_val(val_1)
            #         if not node[2].isdigit():
            #             val_2 = var_table.get_val(val_2)
            #         val = val_1 + val_2
            #         var_temp.val = val
            #         var_table.add_obj(var_temp)
            #     elif node[0] == '-':
            #         val_1 = node[1]
            #         val_2 = node[2]
            #         if not node[1].isdigit():
            #             val_1 = var_table.get_val(val_1)
            #         if not node[2].isdigit():
            #             val_2 = var_table.get_val(val_2)
            #         val = val_1 - val_2
            #         var_temp.val = val
            #         var_table.add_obj(var_temp)
            #     elif node[0] == '*':
            #         val_1 = node[1]
            #         val_2 = node[2]
            #         if not node[1].isdigit():
            #             val_1 = var_table.get_val(val_1)
            #         if not node[2].isdigit():
            #             val_2 = var_table.get_val(val_2)
            #         val = val_1 * val_2
            #         var_temp.val = val
            #         var_table.add_obj(var_temp)
            #     elif node[0] == '/':
            #         val_1 = node[1]
            #         val_2 = node[2]
            #         if not node[1].isdigit():
            #             val_1 = var_table.get_val(val_1)
            #         if not node[2].isdigit():
            #             val_2 = var_table.get_val(val_2)
            #         val = val_1 / val_2
            #         var_temp.val = val
            #         var_table.add_obj(var_temp)
            # else:
            #     pass
            op_table.add_node(node[:])
            if chain:
                chain.merge_real(op_table, op_table.length)
            temp_obj.last = node[3]
            node[0] = node[1] = node[2] = node[3] = ''
        elif node[0] and node[1] and node[2] and node[3]:
            if not node[1].isdigit():
                if var_table.search(node[1]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass
            if not node[2].isdigit():
                if var_table.search(node[2]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass
            op_table.add_node(node[:])
            chain.merge_real(op_table, op_table.length)
            t_var = node[3]
            node[0] = node[1] = node[3] = ''
            node[2] = t_var
            node[3] = temp_obj.newtemp()
            var_table.add_obj(VarItem(name=node[3]))
            temp_obj.last = node[3]
    # 若node填满加表
    A1(t, col, item, var_table, op_table, node, chain)



def A1(t, col, item, var_table, op_table, node, chain):
    """ 算术表达式' """
    if t.Token[1] == '+':
        node[0] = '+'
        match('+', t)
        A(t, col, item, var_table, op_table, node, chain)
    elif t.Token[1] == '-':
        node[0] = '-'
        match('-', t)
        A(t, col, item, var_table, op_table, node, chain)


def B(t, col, item, var_table, op_table, node, chain):
    """项"""
    C(t, col, item, var_table, op_table, node)
    B1(t, col, item, var_table, op_table, node, chain)
    if node:
        if node[0] and node[1] and node[2] and node[3] and (t.Token[1] not in ['+', '-', '*', '/']):
            if not node[1].isdigit():
                if var_table.search(node[1]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass
            if not node[2].isdigit():
                if var_table.search(node[2]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass
            if node[0] == '/' and int(node[2]) == 0:
                print(f'出现错误,除数为0,第{t.Token[3]}行')
                exit()
            op_table.add_node(node[:])
            if chain:
                chain.merge_real(op_table, op_table.length)
            temp_obj.last = node[3]
            node[0] = node[1] = node[2] = node[3] = ''
        elif node[0] and node[1] and node[2] and node[3]:
            if not node[1].isdigit():
                if var_table.search(node[1]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass
            if not node[2].isdigit():
                if var_table.search(node[2]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass
            if node[0] == '/' and int(node[2]) == 0:
                print(f'出现错误,除数为0,第{t.Token[3]}行')
                exit()
            op_table.add_node(node[:])
            if chain:
                chain.merge_real(op_table, op_table.length)
            t_var = node[3]
            node[0] = node[1] = node[3] = ''
            node[2] = t_var
            node[3] = temp_obj.newtemp()
            temp_obj.last = node[3]


def B1(t, col, item, var_table, op_table, node, chain):
    """ 项' """
    if t.Token[1] == '*':
        # 常量 [*, , con, T]
        if node[0] and node[1] and node[2] and node[3]:
            if not node[1].isdigit():
                if var_table.search(node[1]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass
            if not node[2].isdigit():
                if var_table.search(node[2]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass

            op_table.add_node(node[:])
            if chain:
                chain.merge_real(op_table, op_table.length)
            t_var = node[3]
            node[0] = node[1] = node[2] = node[3] = ''
            node[2] = t_var
            node[3] = temp_obj.newtemp()
        node[0] = '*'
        match('*', t)
        B(t, col, item, var_table, op_table, node, chain)
    elif t.Token[1] == '/':
        if node[0] and node[1] and node[2] and node[3]:
            if not node[1].isdigit():
                if var_table.search(node[1]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass
            if not node[2].isdigit():
                if var_table.search(node[2]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass
            if int(node[2]) == 0:
                print(f'出现错误,除数为0,第{t.Token[3]}行')
                exit()
            op_table.add_node(node[:])
            if chain:
                chain.merge_real(op_table, op_table.length)
            t_var = node[3]
            node[0] = node[1] = node[2] = node[3] = ''
            node[2] = t_var
            node[3] = temp_obj.newtemp()
        node[0] = '/'
        match('/', t)
        B(t, col, item, var_table, op_table, node, chain)
    elif t.Token[1] == '%':
        if node[0] and node[1] and node[2] and node[3]:
            if not node[1].isdigit():
                if var_table.search(node[1]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass
            if not node[2].isdigit():
                if var_table.search(node[2]):
                    print(f'变量或常量未声明,第{t.Token[3]}行')
                else:
                    pass

            op_table.add_node(node[:])
            if chain:
                chain.merge_real(op_table, op_table.length)
            t_var = node[3]
            node[0] = node[1] = node[2] = node[3] = ''
            node[2] = t_var
            node[3] = temp_obj.newtemp()
        node[0] = '%'
        match('%', t)
        B(t, col, item, var_table, op_table, node)


def C(t, col, item, var_table, op_table, node):
    """因子"""
    if t.Token[1] == '(':
        match('(', t)
        if node[3] != 0:
            p = temp_obj.newtemp()
            if not node[2]:
                node[2] = p
            elif not node[1]:
                node[1] = p
            node_pass = ['', '', '', p]
        else:
            node_pass = node
        A(t, col, item, var_table, op_table, node_pass)
        if t.Token[1] == ')':
            match(')', t)
    elif t.Token[1] in col.firsts['con']:
        # 常量 [, , con, T]  /1
        # 常量 [*, con1 , con, T] /2
        D(t, col, item, var_table, op_table, node)
    elif t.Token[1] in col.firsts['var'] and (t.tokens[t.p][1] != '('):
        # 变量 new = [, , var,T]
        E(t, col, item, var_table, op_table, node)
    elif t.Token[1] in col.firsts['fun_invoke']:
        F(t, col, item, var_table, op_table)


def D(t, col, item=None, table=None, op_table=None, node=None):
    """常量"""
    if t.Token[1] == 'num_con':
        if item:
            item.val = t.Token[2]
        if node:
            if not node[1]:
                node[1] = t.Token[2]
            elif not node[2]:
                node[2] = t.Token[2]
        temp_obj.last = t.Token[2]
        match('num_con', t)
    elif t.Token[1] == 'sig_con':
        if item:
            item.val = t.Token[2]
        if node:
            if not node[1]:
                node[1] = t.Token[2]
            elif not node[2]:
                node[2] = t.Token[2]
        temp_obj.last = t.Token[2]
        match('sig_con', t)


def E(t, col, item, var_table, op_table, node=None):
    """变量"""
    if t.Token[1] == 'signal':
        if item:
            if var_table.search(t.Token[2]):
                item.name = t.Token[2]
            else:
                print(f'变量重复声明错误,第{t.Token[3]}行')
                var_table.pop()
        if node:

            if not node[1]:
                node[1] = t.Token[2]
            elif not node[2]:
                node[2] = t.Token[2]
        temp_obj.last = t.Token[2]
        match('signal', t)


def F(t, col):
    """函数调用"""
    if t.Token[1] == 'signal':
        match('signal', t)
        if t.Token[1] == '(':
            match('(', t)
            G(t, col)
            if t.Token[1] == ')':
                match(')', t)


def G(t, col):
    """实参列表"""
    if t.Token[1] in col.firsts['real_par']:
        H(t, col)


def H(t, col):
    """实参"""
    A_(t, col)
    H1(t, col)


def H1(t, col):
    """ 实参' """
    if t.Token[1] == ',':
        match(',', t)
        H(t, col)


def I(t, col, item, var_table, const_table, op_table):
    """语句"""
    if t.Token[1] in col.firsts['declare_statement']:
        J(t, col, item, var_table, const_table, op_table)
    elif t.Token[1] in col.firsts['exe_statement']:
        B_(t, col, item, var_table, const_table, op_table)



def J(t, col, item, var_table, const_table, op_table):
    """声明语句"""
    if t.Token[1] in col.firsts['v_declare']:
        K(t, col, item, var_table, const_table, op_table)
    elif t.Token[1] in col.firsts['fun_declare']:
        S(t, col, item, var_table, const_table, op_table)


def K(t, col, item, var_table, const_table, op_table):
    """值声明"""
    if t.Token[1] in col.firsts['con_declare']:
        obj = ConstItem()
        L(t, col, obj, const_table, op_table)
    elif t.Token[1] in col.firsts['var_declare']:
        obj = VarItem()
        O(t, col, obj, var_table, op_table)


def L(t, col, item, c_table):
    """常量声明"""
    if not item:
        c_obj = ConstItem()
    else:
        c_obj = item
    c_table.add_obj(c_obj)
    if t.Token[1] == 'const':
        match('const', t)
        M(t, col, c_obj, c_table)
        N(t, col, c_obj, c_table)


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
        if c_table.search(t.Token[2]):
            c_obj.name = t.Token[2]
        else:
            print(f'常量重复声明错误,第{t.Token[3]}行')
            c_table.pop()
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
        next_cobj = ConstItem()
        next_cobj.type = c_obj.type
        c_table.add_obj(next_cobj)
        N(t, col, next_cobj, c_table)


def O(t, col, item, var_table, op_table):
    """变量声明"""
    if not item:
        obj = VarItem()
    else:
        obj = item
    var_table.add_obj(obj)
    R(t, col, obj)
    P(t, col, obj, var_table, op_table)


def P(t, col, item, var_table, op_table):
    """变量声明表"""
    Q(t, col, item, var_table, op_table)
    P1(t, col, item, var_table, op_table)


def P1(t, col, item, var_table, op_table):
    """变量声明表'"""
    if t.Token[1] == ';' or t.Token[1] == ";":
        match(';', t)
    elif t.Token[1] == ',' or t.Token[1] == ",":
        match(',', t)
        new_item = VarItem()
        new_item.type = item.type
        var_table.add_obj(new_item)
        P(t, col, new_item, var_table, op_table)


def Q(t, col, item, var_table, op_table):
    """单变量声明"""
    E(t, col, item, var_table, op_table)
    Q1(t, col, item, var_table, op_table)


def Q1(t, col, item, var_table, op_table):
    """单变量声明'"""
    if t.Token[1] == '=':
        match('=', t)
        A_(t, col, item, var_table, op_table)


def R(t, col, item):
    """变量类型"""
    if t.Token[1] == 'int':
        match('int', t)
        if isinstance(item, VarItem):
            item.type = 'int'
        else:
            item.parLen += 1
            item.para.append('int')
    elif t.Token[1] == 'char':
        match('char', t)
        if isinstance(item, VarItem):
            item.type = 'char'
        else:
            item.parLen += 1
            item.para.append('char')
    elif t.Token[1] == 'float':
        match('float', t)
        if isinstance(item, VarItem):
            item.type = 'float'
        else:
            item.parLen += 1
            item.para.append('float')


def S(t, col, item, fun_table):
    """函数声明"""
    if t.Token[1] == '(':
        match('(', t)
        U(t, col, item, fun_table)
        if t.Token[1] == ')':
            match(')', t)
            if t.Token[1] == ';':
                match(';', t)


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


def U(t, col, item, fun_table):
    """函数声明形参列表"""
    if t.Token[1] in col.firsts['fun_declare_fpar']:
        V(t, col, item, fun_table)


def V(t, col, item, fun_table):
    """函数声明形参"""
    R(t, col, item)
    if t.Token[1] == 'signal':
        match('signal', t)
    V1(t, col, item, fun_table)


def V1(t, col, item, fun_table):
    """函数声明形参'"""
    if t.Token[1] == ',':
        match(',', t)
        V(t, col, item, fun_table)


def W(t, col, item, var_table, op_table, node, chain):
    """布尔表达式"""
    X(t, col, item, var_table, op_table, node, chain)
    W1(t, col, item, var_table, op_table, node, chain)


def W1(t, col, item, var_table, op_table, node, chain):
    """布尔表达式'"""
    if t.Token[1] == '||':
        # a&&b||c
        if bool_lastmark[0] == '||':
            node[0] = 'jnz'
            if node[0] and (node[1] or node[2]):
                flag = 0
                for i in chain.realChain:
                    if i >= op_table.length:
                        flag = 1
                if chain and flag == 0:
                    chain.merge_real(op_table, op_table.length + 1)
                    chain.realChain.append(op_table.length)
                op_table.add_node(node[:])
                op_table.add_node(['j', '', '', 0])
                if chain:
                    chain.fakeChain.append(op_table.length - 1)
                node[1] = node[2] = ''
            else:
                chain.merge_real(op_table, op_table.length + 1)
                chain.realChain.append(op_table.length)
        else:
            node[0] = 'jnz'
            if node[0] and (node[1] or node[2]):
                flag = 0
                for i in chain.realChain:
                    if i >= op_table.length:
                        flag = 1
                if chain and flag == 0:
                    chain.merge_real(op_table, op_table.length + 1)
                    chain.realChain.append(op_table.length)
                op_table.add_node(node[:])
                op_table.add_node(['j', '', '', 0])
                if chain:
                    chain.fakeChain.append(op_table.length - 1)
                node[1] = node[2] = ''
            else:
                chain.merge_real(op_table, op_table.length + 1)
                chain.realChain.append(op_table.length)
        bool_lastmark[0] = '||'
        match('||', t)
        W(t, col, item, var_table, op_table, node, chain)



def X(t, col, item, var_table, op_table, node, chain):
    """布尔项"""
    Y(t, col, item, var_table, op_table, node, chain)
    X1(t, col, item, var_table, op_table, node, chain)


def X1(t, col, item, var_table, op_table, node, chain):
    """布尔项'"""
    if t.Token[1] == '&&':
        # a||b&&c
        if bool_lastmark[0] == '||':
            node[0] = 'jnz'
            if node[0] and (node[1] or node[2]):
                flag = 0
                for i in chain.realChain:
                    if i >= op_table.length:
                        flag = 1
                if chain and flag == 0:
                    chain.merge_real(op_table, op_table.length + 1)
                    # chain.realChain.append(op_table.length)
                    chain.fakeChain.append(op_table.length)
                op_table.add_node(node[:])
                op_table.add_node(['j', '', '', 0])
                if chain:
                    chain.fakeChain.append(op_table.length - 1)
                node[1] = node[2] = ''
            else:
                chain.merge_real(op_table, op_table.length + 1)
                chain.realChain.append(op_table.length)
        else:
            node[0] = 'jnz'
            if node[0] and (node[1] or node[2]):
                flag = 0
                for i in chain.realChain:
                    if i >= op_table.length:
                        flag = 1
                if chain and flag == 0:
                    chain.merge_real(op_table, op_table.length+1, True)
                    chain.realChain.append(op_table.length)
                op_table.add_node(node[:])
                op_table.add_node(['j', '', '', 0])
                if chain:
                    chain.fakeChain.append(op_table.length-1)
                node[1] = node[2] = ''
            else:
                chain.merge_real(op_table, op_table.length + 1, True)
                chain.realChain.append(op_table.length)
        bool_lastmark[0] = '&&'
        match('&&', t)
        X(t, col, item, var_table, op_table, node, chain)



def Y(t, col, item, var_table, op_table, node, chain):
    """布尔因子"""
    if t.Token[1] in col.firsts['arg_exp'] and conditon(t):
        A(t, col, item, var_table, op_table, node, chain)
    elif t.Token[1] in col.firsts['rel_expression']:
        U_(t, col, item, var_table, op_table, node, chain)
        node[0] = node[1] = node[2] = ''
        # f_node = ['j', '', '', 0]
        # op_table.add_node(f_node)
        # chain.fakeChain.append(op_table.length - 1)
    elif t.Token[1] == '!':
        match('!', t)
        W1(t, col, item, var_table, op_table, node)



def Z(t, col, item, var_table, op_table):
    """赋值表达式"""
    if t.Token[1] == 'signal':
        obj = t.Token[2]
        match('signal', t)
        if t.Token[1] == '=':
            match('=', t)
            temp = temp_obj.newtemp()
            # node = Node(op='=', b=temp, c=obj)
            # 赋值操作[=, ,T,signal] 需要A_返回值 , 传T的值
            # n = Node(c=temp)
            node = ['', '', '', temp]
            A_(t, col, item, var_table, op_table, node)
            node = ['=', '', temp_obj.last, obj]
            # 赋值操作
            # 临时变量是否在符号表中 不在就添加到符号表
            if var_table.search(obj):
                print(f'变量未声明,第{t.Token[3]}行')
            else:
                pass
                # if temp_obj.last.isdigit():
                #     var_table.update(obj, temp_obj.last)
                # else:
                #     var_table.update(obj, var_table.get_val(temp_obj.last))
            op_table.add_node(node[:])
            # 添加四元式


def A_(t, col, item, var_table, op_table, node=None, chain=None):
    """表达式"""
    if t.Token[1] in col.firsts['arg_exp'] and conditon(t) and conditon1(t) and (t.tokens[t.p][1] != '=') and (t.tokens[t.p][2] != ')' or t.tokens[t.p-2][2] != '('):
        # 赋值操作[=, ,T ,signal] 添加四元式
        A(t, col, item, var_table, op_table, node, chain)
    elif t.Token[1] in col.firsts['rel_expression'] and (t.tokens[t.p][1] != '=' and conditon1(t) and (t.tokens[t.p][2] != ')' or t.tokens[t.p-2][2] != '(')):
        chain.reset(r_chain=True)
        temp = temp_obj.newtemp()
        node[3] = temp
        temp_obj.last = temp
        U_(t, col, item, var_table, op_table, node, chain)
    elif t.Token[1] in col.firsts['bool_expression'] and (t.tokens[t.p][1] != '='):
        node[0] = 'jnz'
        W(t, col, item, var_table, op_table, node, chain)
    elif t.Token[1] in col.firsts['assign_expression']:
        Z(t, col, item, var_table, op_table)


def B_(t, col, item, var_table, const_table, op_table):
    """执行语句"""
    if t.Token[1] in col.firsts['digit_exe_statement']:
        C_(t, col, item, var_table, op_table)
    elif t.Token[1] in col.firsts['control_statement']:
        F_(t, col, item, var_table, const_table, op_table)
    elif t.Token[1] in col.firsts['complex_statement']:
        G_(t, col, item, var_table, const_table, op_table)
        if cir_state[0] == 0 and (t.Token[1] == 'break' or t.Token[1] == 'continue'):
            print(f'出现错误,在非循环语句中使用break或者continue,第{t.Token[3]}行')
            exit(-1)



def C_(t, col, item, var_table, op_table):
    """数据处理语句"""
    if t.Token[1] in col.firsts['assign_statement'] and (t.tokens[t.p][1] != '('):
        D_(t, col, item, var_table, op_table)
    elif t.Token[1] in col.firsts['fun_invoke_statement']:
        E_(t, col, item, var_table, op_table)


def D_(t, col, item, var_table, op_table):
    """赋值语句"""
    Z(t, col, item, var_table, op_table)
    if t.Token[1] == ';':
        match(';', t)


def E_(t, col):
    """函数调用语句"""
    F(t, col)
    if t.Token[1] == ';':
        match(';', t)


def F_(t, col, item, var_table, const_table, op_table):
    """控制语句"""
    if t.Token[1] in col.firsts['if_statement']:
        I_(t, col, item, var_table, const_table, op_table)
        if cir_state[0] == 0 and (t.Token[1] == 'break' or t.Token[1] == 'continue'):
            print(f'出现错误,在非循环语句中使用break或者continue,第{t.Token[3]}行')
            exit(-1)
    elif t.Token[1] in col.firsts['for_statement']:
        cir_state[0] = 1
        J_(t, col, item, var_table, const_table, op_table)
        cir_state[0] = 0
    elif t.Token[1] in col.firsts['while_statement']:
        cir_state[0] = 1
        K_(t, col, item, var_table, const_table, op_table)
        cir_state[0] = 0
    elif t.Token[1] in col.firsts['do_while_statement']:
        cir_state[0] = 1
        L_(t, col, item, var_table, const_table, op_table)
        cir_state[0] = 0
    elif t.Token[1] in col.firsts['return_statement']:
        R_(t, col)



def G_(t, col, item, var_table, const_table, op_table):
    """复合语句"""
    if t.Token[1] == '{':
        match('{', t)
        H_(t, col, item, var_table, const_table, op_table)
        if t.Token[1] == '}':
            match('}', t)
        else:
            if cir_state[0] == 0 and (t.Token[1] == 'break' or t.Token[1] == 'continue'):
                print(f'出现错误,在非循环语句中使用break或者continue,第{t.Token[3]}行')
                exit(-1)


def H_(t, col, item, var_table, const_table, op_table):
    """语句表"""
    I(t, col, item, var_table, const_table, op_table)
    H_1(t, col, item, var_table, const_table, op_table)


def H_1(t, col, item, var_table, const_table, op_table):
    """语句表'"""
    if t.Token[1] in col.firsts['statement_list']:
        H_(t, col, item, var_table, const_table, op_table)


def I_(t, col, item, var_table, const_table, op_table):
    """if语句"""
    chain = ENTRY()
    if t.Token[1] == 'if':
        match('if', t)
        if t.Token[1] == '(':
            match('(', t)
            node = ['', '', '', 0]
            chain.realChain.append(op_table.length)
            A_(t, col, item, var_table, op_table, node, chain)
            if entry_offset[0] != 0:
                chain.realChain[-1] = entry_offset[0]
                # print(entry_offset[0])
                entry_offset[0] = 0

            # print(chain.realChain)
            if bool_lastmark[0] in ['&&', '||']:
                if node[0] == 'jnz' and (node[1] or node[2]):
                    if bool_lastmark[0] == '||':
                        bool_reset = False
                    else:
                        bool_reset = True
                    flag = 0
                    for i in chain.realChain:
                        if i >= op_table.length:
                            flag = 1
                    if flag == 0:
                        chain.merge_real(op_table, op_table.length + 1, bool_reset)
                    chain.realChain.append(op_table.length)
                    op_table.add_node(node[:])
                    f_node = ['j', '', '', 0]
                    op_table.add_node(f_node)
                    chain.fakeChain.append(op_table.length - 1)
                    node[1] = node[2] = ''
            elif node[0] == 'jnz':
                op_table.add_node(node[:])
                chain.merge_real(op_table, op_table.length + 2, False)
                f_node = ['j', '', '', 0]
                op_table.add_node(f_node)
                chain.fakeChain.append(op_table.length - 1)
                node[1] = node[2] = ''
                # 假出口未知

            if t.Token[1] == ')':
                match(')', t)
                chain.merge_real(op_table, op_table.length+1, True)
                I(t, col, item, var_table, const_table, op_table)


                # 回填假出口
                chain.merge_fake(op_table, op_table.length+2)
                chain.reset(f_chain=True)
                op_table.add_node(['j', '', '', 0])
                chain.fakeChain.append(op_table.length - 1)


                I_1(t, col, item, var_table, const_table, op_table)
                chain.merge_fake(op_table, op_table.length+1)


def I_1(t, col, item, var_table, const_table, op_table):
    """if语句'"""
    if t.Token[1] == 'else':
        match('else', t)
        I(t, col, item, var_table, const_table, op_table)


def J_(t, col, item, var_table, const_table, op_table):
    """for语句"""
    chain = ENTRY()
    entry = [0, 0]
    if t.Token[1] == 'for':
        match('for', t)
        if t.Token[1] == '(':
            match('(', t)
            node = ['', '', '', '']
            A_(t, col, item, var_table, op_table, node, chain)
            if t.Token[1] == ';':
                match(';', t)
                node = ['', '', '', 0]
                chain.realChain.append(op_table.length)
                A_(t, col, item, var_table, op_table, node, chain)
                # f_node = ['j', '', '', 0]
                # op_table.add_node(f_node)
                # chain.fakeChain.append(op_table.length - 1)
                if t.Token[1] == ';':
                    match(';', t)
                    node = ['', '', '', '']
                    entry[0] = op_table.length-1
                    A_(t, col, item, var_table, op_table, node, chain)
                    entry[1] = op_table.length-1
                    op_table.add_node(['j', '', '', entry[0]])

                    if t.Token[1] == ')':
                        match(')', t)
                        chain.merge_real(op_table, op_table.length+1, True)
                        M_(t, col, item, var_table, const_table, op_table, chain, op_table.length+1)
                        op_table.add_node(['j', '', '', entry[1]])
                        chain.merge_fake(op_table, op_table.length+1)


def K_(t, col, item, var_table, const_table, op_table):
    """while语句"""
    chain = ENTRY()
    entry = [0]
    if t.Token[1] == 'while':
        match('while', t)
        if t.Token[1] == '(':
            match('(', t)
            node = ['', '', '', 0]
            entry[0] = op_table.length+1
            chain.realChain.append(op_table.length)
            A_(t, col, item, var_table, op_table, node, chain)

            # f_node = ['j', '', '', 0]
            # op_table.add_node(f_node)
            # chain.fakeChain.append(op_table.length - 1)
            if t.Token[1] == ')':
                match(')', t)
                chain.merge_real(op_table, op_table.length+1)
                M_(t, col, item, var_table, const_table, op_table, chain, entry[0])
                chain.merge_fake(op_table, op_table.length+2)
                op_table.add_node(['j', '', '', entry[0]])
                entry[0] = 0


def L_(t, col, item, var_table, const_table, op_table):
    """dowhile语句"""
    chain = ENTRY()
    entry = [0]
    if t.Token[1] == 'do':
        match('do', t)
        entry[0] = op_table.length + 1
        N_(t, col, item, var_table, const_table, op_table, chain, entry[0])
        if t.Token[1] == 'while':
            match('while', t)
            if t.Token[1] == '(':
                match('(', t)
                node = ['', '', '', 0]
                chain.realChain.append(op_table.length)
                A_(t, col, item, var_table, op_table, node, chain)
                chain.merge_real(op_table, entry[0])
                entry[0] = 0
                chain.merge_fake(op_table, op_table.length+1)

                # f_node = ['j', '', '', op_table.length+2]
                # op_table.add_node(f_node)
                # chain.fakeChain.append(op_table.length - 1)
                if t.Token[1] == ')':
                    match(')', t)
                    if t.Token[1] == ';':
                        match(';', t)


def M_(t, col, item, var_table, const_table, op_table, chain, continue_entry):
    """循环语句"""
    # 书上给的词法在循环语句中没有执行语句,在循环内的执行语句如赋值无法正确识别 ----
    # if t.Token[1] in col.firsts['exe_statement']:
    #     B_(t, col, item, var_table, const_table, op_table)
    if t.Token[1] in col.firsts['declare_statement']:
        J(t, col)
    elif t.Token[1] in col.firsts['cir_exe_statement']:
        P_(t, col, item, var_table, const_table, op_table, chain, continue_entry)
    elif t.Token[1] in col.firsts['cir_complex_statement']:
        N_(t, col, item, var_table, const_table, op_table, chain, continue_entry)


def N_(t, col, item, var_table, const_table, op_table, chain, continue_entry):
    """循环用复合语句"""
    if t.Token[1] == '{':
        match('{', t)
        O_(t, col, item, var_table, const_table, op_table, chain, continue_entry)
        if t.Token[1] == '}':
            match('}', t)


def O_(t, col, item, var_table, const_table, op_table, chain, continue_entry):
    """循环语句表"""
    M_(t, col, item, var_table, const_table, op_table, chain, continue_entry)
    O_1(t, col, item, var_table, const_table, op_table, chain, continue_entry)


def O_1(t, col, item, var_table, const_table, op_table, chain, continue_entry):
    """循环语句表'"""
    if t.Token[1] in col.firsts['cir_statement_list']:
        O_(t, col, item, var_table, const_table, op_table, chain, continue_entry)


def P_(t, col, item, var_table, const_table, op_table, chain, continue_entry):
    """循环执行语句"""
    if t.Token[1] in col.firsts['digit_exe_statement']:
        C_(t, col, item, var_table, op_table)
    elif t.Token[1] in col.firsts['cir_if_statement']:
        Q_(t, col, item, var_table, const_table, op_table, chain, continue_entry)
    elif t.Token[1] in col.firsts['for_statement']:
        J_(t, col)
    elif t.Token[1] in col.firsts['while_statement']:
        K_(t, col)
    elif t.Token[1] in col.firsts['do_while_statement']:
        L_(t, col)
    elif t.Token[1] in col.firsts['return_statement']:
        R_(t, col)
    elif t.Token[1] in col.firsts['break_statement']:
        S_(t, col, op_table, chain)
    elif t.Token[1] in col.firsts['continue_statement']:
        T_(t, col, op_table, continue_entry)


def Q_(t, col, item, var_table, const_table, op_table, for_chain, continue_entry):
    """循环用if语句"""
    chain = ENTRY()
    if t.Token[1] == 'if':
        match('if', t)
        if t.Token[1] == '(':
            match('(', t)
            node = ['', '', '', 0]
            chain.realChain.append(op_table.length)
            A_(t, col, item, var_table, op_table, node, chain)
            # if entry_offset[0] != 0:
            #     chain.realChain[-1] = entry_offset[0]
            #     # print(entry_offset[0])
            #     entry_offset[0] = 0

            # print(chain.realChain)
            if bool_lastmark[0] in ['&&', '||']:
                if node[0] == 'jnz' and (node[1] or node[2]):
                    if bool_lastmark[0] == '||':
                        bool_reset = False
                    else:
                        bool_reset = True
                    chain.merge_real(op_table, op_table.length + 1, bool_reset)
                    chain.realChain.append(op_table.length)
                    op_table.add_node(node[:])
                    f_node = ['j', '', '', 0]
                    op_table.add_node(f_node)
                    chain.fakeChain.append(op_table.length - 1)
                    node[1] = node[2] = ''
            elif node[0] == 'jnz':
                op_table.add_node(node[:])
                chain.merge_real(op_table, op_table.length + 2, False)
                # f_node = ['j', '', '', 0]
                # op_table.add_node(f_node)
                # chain.fakeChain.append(op_table.length - 1)
                node[1] = node[2] = ''
            else:
                chain.merge_real(op_table, op_table.length + 2, False)
                # f_node = ['j', '', '', 0]
                # op_table.add_node(f_node)
                # chain.fakeChain.append(op_table.length - 1)
                node[1] = node[2] = ''
                # 假出口未知

            if t.Token[1] == ')':
                match(')', t)
                chain.merge_real(op_table, op_table.length + 1, True)
                M_(t, col, item, var_table, const_table, op_table, for_chain, continue_entry)
                # 回填假出口
                chain.merge_fake(op_table, op_table.length + 2)
                chain.reset(f_chain=True)
                op_table.add_node(['j', '', '', 0])
                chain.fakeChain.append(op_table.length - 1)

                Q_1(t, col, item, var_table, const_table, op_table, chain, continue_entry)
                chain.merge_fake(op_table, op_table.length + 1)



def Q_1(t, col, item, var_table, const_table, op_table, chain, continue_entry):
    """循环用if语句'"""
    if t.Token[1] == 'else':
        match('else', t)
        M_(t, col, item, var_table, const_table, op_table, chain, continue_entry)


def R_(t, col):
    """return语句"""
    if t.Token[1] == 'return':
        match('return', t)
        R_1(t, col)


def R_1(t, col):
    """return语句"""
    if t.Token[1] == ';':
        match('return', t)
    elif t.Token[1] in col.firsts['expression']:
        A_(t, col)
        if t.Token[1] == ';':
            match(';', t)



def S_(t, col, op_table, chain):
    """break语句"""
    if t.Token[1] == 'break':
        op_table.add_node(['j', '', '', 0])
        chain.fakeChain.append(op_table.length-1)
        match('break', t)
        if t.Token[1] == ';':
            match(';', t)



def T_(t, col, op_table, continue_entry):
    """continue语句"""
    if t.Token[1] == 'continue':
        op_table.add_node(['j', '', '', continue_entry])
        match('continue', t)
        if t.Token[1] == ';':
            match(';', t)



def U_(t, col, item, var_table, op_table, node, chain):
    """关系表达式"""
    A(t, col, item, var_table, op_table, node, chain)
    if node[0] and node[1] and node[2] and node[3]:
        n_t = node[3]
        op_table.add_node(node[:])
        node = ['', n_t, '', 0]

    else:
        node = ['', temp_obj.last, '', 0]



    V_(t, col, item, var_table, op_table, node)
    only_const = ''
    const_index = 0
    arg_or_con = []
    if not node[1]:
        temp = temp_obj.newtemp()
        node[1] = temp
        const_index = 1
        arg_or_con = node[:]
        node = ['', '', '', temp]

    elif not node[2]:
        temp = temp_obj.newtemp()
        node[2] = temp
        const_index = 2
        arg_or_con = node[:]
        node = ['', '', '', temp]
    A(t, col, item, var_table, op_table, node, chain)
    if not node[1] and not node[2]:
        chain.merge_real(op_table, op_table.length + 1, True)
        chain.realChain.append(op_table.length)
        op_table.add_node(arg_or_con[:])
        entry_offset[0] = op_table.length-1
        op_table.add_node(['j', '', '', 0])
        chain.fakeChain.append(op_table.length-1)
    elif (not node[1]) or (not node[2]):
        if node[1]:
            only_const = node[1]
        elif node[2]:
            only_const = node[2]
        arg_or_con[const_index] = only_const
        flag = 0
        for i in chain.realChain:
            if i >= op_table.length:
                flag = 1
        if flag == 0:
            chain.merge_real(op_table, op_table.length+1, True)
        chain.realChain.append(op_table.length)
        op_table.add_node(arg_or_con[:])
        op_table.add_node(['j', '', '', 0])
        chain.fakeChain.append(op_table.length - 1)
    else:
        chain.merge_real(op_table, op_table.length+1, True)
        chain.realChain.append(op_table.length)
        op_table.add_node(arg_or_con[:])
        entry_offset[0] = op_table.length-1
        op_table.add_node(['j', '', '', 0])
        chain.fakeChain.append(op_table.length - 1)



def V_(t, col, item, var_table, op_table, node):
    """关系运算符"""
    if t.Token[1] == '>':
        node[0] = '>'
        match('>', t)
    elif t.Token[1] == '<':
        node[0] = '<'
        match('<', t)
    elif t.Token[1] == '>=':
        node[0] = '>='
        match('>=', t)
    elif t.Token[1] == '<=':
        node[0] = '<='
        match('<=', t)
    elif t.Token[1] == '==':
        node[0] = '=='
        match('==', t)
    elif t.Token[1] == '!=':
        node[0] = '!='
        match('!=', t)



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



def X_(t, col):
    """函数定义形参列表"""
    if t.Token[1] in col.firsts['fun_define_fpar']:
        Y_(t, col)



def Y_(t, col):
    """函数定义形参"""
    R(t, col)
    if t.Token[1] == 'signal':
        match('signal', t)
        Y_1(t, col)


def Y_1(t, col):
    """函数定义形参'"""
    if t.Token[1] == ',':
        match(',', t)
        Y_(t, col)


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


def A__(t, col):
    """函数块"""
    if t.Token[1] in col.firsts['fun_define']:
        W_(t, col)
        A__(t, col)

