from Project.Lib4_Semantic_Analyse.fun import *
from Project.Lib3_Grammer.Collections import Collections
from Project.Lib4_Semantic_Analyse.Tables import *


def entry(token_file, regulation, start='program'):
    tokens = []
    const_table = Table()
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
            L(tokenbox, col, const_table)
        elif tokenbox.Token[1] in ['int', 'char', 'float', 'void']:
            tokenbox.get_next_token()
            if tokenbox.Token[1] == 'main':
                break
            tokenbox.get_next_token()
            if tokenbox.Token[1] == '(':
                # 修改了文法的递归下降函数 解决了检测入口不对称
                S(tokenbox, col)
                # 函数声明
            elif tokenbox.Token[1] == '=' or tokenbox.Token[1] == ',':
                O(tokenbox, col)
                # 变量声明
    tokenbox.get_next_token()
    tokenbox.get_next_token()
    # 处理复合语句
    tokenbox.get_next_token()
    G_(tokenbox, col)
    while tokenbox.Token[1] in ['int', 'char', 'float', 'void']:
        W_(tokenbox, col)

    for i in const_table.t:
        i.Tprint()


entry('../Lib3_Grammer/Token/target.reg', '../Lib3_Grammer/test1')