from Project.Lib4_Semantic_Analyse.fun import *
from Project.Lib3_Grammer.Collections import Collections
from Project.Lib4_Semantic_Analyse.Tables import *



def read_file(token_file):
    with open(token_file, 'r', encoding='utf-8') as fp:
        content = fp.readlines()
    return content


def init_tokenbox(content) -> TokenBox:
    tokens = []
    content = content.split('\n')
    for line in content:
        if line:
            t = []
            divs = line.strip().split(' ')
            for div in divs:
                t.append(div)
            tokens.append(t)
    tokenbox = TokenBox(tokens)
    return tokenbox


def init_tokenbox1(content) -> TokenBox:
    tokens = []
    for line in content:
        if line:
            t = []
            divs = line.strip().split(' ')
            for div in divs:
                t.append(div)
            tokens.append(t)
    tokenbox = TokenBox(tokens)
    return tokenbox


def entry(content, regulation, start='program'):
    # tokens = []
    const_table = Table('C')
    var_table = Table('V')
    fun_table = Table('F')
    op_table = OPCODE()
    errors = []
    field = [0]
    # with open(token_file, 'r', encoding='utf-8') as fp:
    #     content = fp.readlines()
    #     for line in content:
    #         t = []
    #         divs = line.strip().split(' ')
    #         for div in divs:
    #             t.append(div)
    #         tokens.append(t)
    # tokenbox = TokenBox(tokens)
    tokenbox = init_tokenbox1(content)
    col = Collections(regulation, start)
    col.GET_FIRST_FOLLOW()

    tokenbox.get_next_token()
    op_table.add_node(['main', '', '', ''])
    while tokenbox.Token[1] != 'main':
        if tokenbox.Token[1] == 'const':
            # 常量声明
            L(tokenbox, col, None, const_table, '<all>', errors)
        elif tokenbox.Token[1] in ['int', 'char', 'float', 'void']:
            tpy = tokenbox.Token[1]
            tokenbox.get_next_token()
            t = tokenbox.Token[2]
            if tokenbox.Token[1] == 'main':
                break
            tokenbox.get_next_token()
            if tokenbox.Token[1] == '(':
                # 修改了文法的递归下降函数 解决了检测入口不对称
                f_i = FunctionItem()
                if fun_table.search(t):
                    # 没有找到同名函数 就创建
                    f_i.name = t
                    f_i.type = tpy
                    fun_table.add_obj(f_i)
                else:
                    errors.append(f'函数重复声明错误,第{tokenbox.Token[3]}行')
                    print(f'函数重复声明错误,第{tokenbox.Token[3]}行')
                S(tokenbox, col, f_i, fun_table)
                # 函数声明
            elif tokenbox.Token[1] == '=' or tokenbox.Token[1] == ',':
                v_i = VarItem()
                v_i.name = t
                v_i.type = tpy
                v_i.field = '<all>'
                O(tokenbox, col, v_i, var_table, op_table, '<all>', errors)
                # 变量声明
    tokenbox.get_next_token()
    tokenbox.get_next_token()
    # 处理复合语句
    tokenbox.get_next_token()
    field[0] += 1
    f_str = f'{field[0]}/'
    G_(tokenbox, col, None, var_table, const_table, op_table, field[:], f_str, errors)
    op_table.add_node(['', '', '', ''])
    while tokenbox.Token[1] in ['int', 'char', 'float', 'void']:
        field[0] += 1
        f_str = f'{field[0]}/'
        W_(tokenbox, col, None, var_table, const_table, op_table, field, f_str, errors)
    op_table.add_node(['sys', '', '', ''])
    print('CONST TABLE:')
    for i in const_table.table:
        i.items_print()
    print('VAR TABLE:')
    for i in var_table.table:
        i.items_print()
    print('FUN TABLE:')
    for i in fun_table.table:
        i.items_print()

    op_table.show()

    return const_table, var_table, fun_table, op_table, errors



# 测试
content = read_file('../Lib3_Grammer/Token/target.reg')
entry(content, '../Lib3_Grammer/test1')

