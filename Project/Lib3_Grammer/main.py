"""
总控
"""
from Project.Lib3_Grammer.fun import *


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
            L(tokenbox)
            pass
        elif tokenbox.Token[1] in ['int', 'char', 'float', 'void']:
            tokenbox.get_next_token()
            if tokenbox.Token[1] != 'signal':
                pass
                # 错误处理
            tokenbox.get_next_token()
            if tokenbox.Token[1] == '(':
                S(tokenbox)
                # 函数声明
            elif tokenbox.Token[1] == '=' or tokenbox.Token[1] == ',':
                O(tokenbox)
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
    G_(tokenbox)
    tokenbox.get_next_token()
    while tokenbox.Token[1] in ['int', 'char', 'float', 'void']:
        W_(tokenbox)
        pass
        # 函数定义分析
        tokenbox.get_next_token()


# def main(token_file):
#     tokens = []
#     with open(token_file, 'r', encoding='utf-8') as fp:
#         content = fp.readlines()
#         for line in content:
#             t = []
#             divs = line.strip().split(',')
#             for div in divs:
#                 t.append(div)
#             tokens.append(t)
#     tokenbox = TokenBox(tokens)
#     tokenbox.get_next_token()
#     print(tokenbox.Token)



entry('Token/Test.reg')