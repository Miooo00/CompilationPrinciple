from Project.Lib4_Semantic_Analyse.fun import *
from Project.Lib3_Grammer.Collections import Collections
from Project.Lib4_Semantic_Analyse.Tables import *



def entry(token_file, regulation, start='program'):
    tokens = []
    const_table = Table()
    var_table = Table()
    fun_table = Table()
    op_table = OPCODE()
    with open(token_file, 'r', encoding='utf-8') as fp:
        content = fp.readlines()
        for line in content:
            t = []
            divs = line.strip().split(' ')
            for div in divs:
                t.append(div)
            tokens.append(t)
    tokenbox = TokenBox(tokens)
    col = Collections(regulation, start)
    col.GET_FIRST_FOLLOW()

    tokenbox.get_next_token()

    while tokenbox.Token[1] != 'main':
        if tokenbox.Token[1] == 'const':
            # 常量声明
            L(tokenbox, col, None, const_table)
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
                f_i.name = t
                f_i.type = tpy
                fun_table.add_obj(f_i)
                S(tokenbox, col, f_i, fun_table)
                # 函数声明
            elif tokenbox.Token[1] == '=' or tokenbox.Token[1] == ',':
                v_i = VarItem()
                v_i.name = t
                v_i.type = tpy
                O(tokenbox, col, v_i, var_table, op_table)
                # 变量声明
    tokenbox.get_next_token()
    tokenbox.get_next_token()
    # 处理复合语句
    tokenbox.get_next_token()
    G_(tokenbox, col, None, var_table, op_table)
    while tokenbox.Token[1] in ['int', 'char', 'float', 'void']:
        W_(tokenbox, col)

    print('CONST TABLE:')
    for i in const_table.t:
        i.items_print()
    print('VAR TABLE:')
    for i in var_table.t:
        i.items_print()
    print('FUN TABLE:')
    for i in fun_table.t:
        i.items_print()

    op_table.show()


entry('../Lib3_Grammer/Token/target.reg', '../Lib3_Grammer/test1')
