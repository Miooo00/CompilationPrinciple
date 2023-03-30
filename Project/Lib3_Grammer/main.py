"""
总控
"""
from fun import *


def entry(token_file):
    tokens = []
    with open(token_file, 'r', encoding='utf-8') as fp:
        content = fp.readlines()
        for line in content:
            t = []
            divs = line.strip().split(',')
            for div in divs:
                t.append(div)
            tokens.append(t)
    tokenbox = TokenBox(tokens)
    # tokenbox.get_next_token()
    # print(tokenbox.Token)

    tokenbox.get_next_token()
    while tokenbox.Token[1] != 'main':
        if tokenbox.Token[1] == 'const':
            # 常量声明
            pass
        elif tokenbox.Token[1] in ['int', 'char', 'float', 'void']:
            tokenbox.get_next_token()
            if tokenbox.Token[1] != 'signal':
                pass
                # 错误处理
            tokenbox.get_next_token()
            if tokenbox.Token[1] == '(':
                pass
                # 函数声明
            elif tokenbox.Token[1] == '=' or tokenbox.Token[1] == ',':
                pass
                # 变量声明
            else:
                pass
                # 错误
    tokenbox.get_next_token()
    if tokenbox.Token[1] != '(':
        pass
        # 错误
    tokenbox.get_next_token()
    if tokenbox.Token[1] != ')':
        pass
        # 错误
    # 处理复合语句
    tokenbox.get_next_token()
    while tokenbox.Token[1] in ['int', 'char', 'float', 'void']:
        pass
        # 函数定义分析
        tokenbox.get_next_token()


entry('./Token/Test1.txt.reg')