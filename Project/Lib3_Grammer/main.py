"""
语法分析入口
需要:
    词法分析结果文件行格式: [种别码, 'obj', 行号]
    语法规则:
        (递归下降,无左递归,无回溯.如A→B
        <div>取代|表示'或者', |用于逻辑运算或)

能够:
    1、能检查大部分语法错误
不能:
    2、缺少for语句左大括号缺失判断,
        循环语句嵌套复合语句时后一个语句的大括号会被前一个识别,仅出现在大括号相邻情况
    3、缺少error信息收集

"""
import os

import pydot
from treelib import Tree
from graphviz import Source
from Project.Lib3_Grammer.fun import *
from Project.Lib3_Grammer.Collections import Collections


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
    """
    :param token_file: 词法分析结果
    :param regulation: 语法
    :param start: 开始符号
    :return: 错误信息
    """
    tree = Tree()
    root = tree.create_node('program')
    errors = []

    tokenbox = init_tokenbox1(content)
    print(regulation)
    col = Collections(regulation, start)
    print(col)

    col.GET_FIRST_FOLLOW()
    tokenbox.get_next_token()


    while tokenbox.Token[1] != 'main':
        if tokenbox.Token[1] == 'const':
            # 常量声明
            L(tokenbox, col, root, tree, errors)
        elif tokenbox.Token[1] in ['int', 'char', 'float', 'void']:
            typ = tokenbox.Token[2]
            tokenbox.get_next_token()
            if tokenbox.Token[1] == 'main':
                break
            if tokenbox.Token[1] != 'signal':
                pass
                # 错误处理
            name = tokenbox.Token[2]
            tokenbox.get_next_token()
            if tokenbox.Token[1] == '(':
                # 修改了文法的递归下降函数 解决了检测入口不对称

                sub1 = Node('fun_declare')
                tree.add_node(sub1, root)
                t = Node('fun_type')
                tree.add_node(t, sub1)
                tree.add_node(Node(typ), t)
                tree.add_node(Node(name), sub1)

                # tree
                S(tokenbox, col, sub1, tree, errors)
                if tokenbox.Token[1] == '{':
                    print(f'出现错误,在main函数前创建函数语句,或没有main函数,第{tokenbox.tokens[tokenbox.p-2][3]}行')
                    errors.append(f'出现错误,在main函数前创建函数语句,或没有main函数,第{tokenbox.tokens[tokenbox.p-2][3]}行')
                    G_(tokenbox, col, root, tree, errors)
                    break
                # 函数声明
            elif tokenbox.Token[1] == '=' or tokenbox.Token[1] == ',':

                sub1 = Node('global_fun_declare')
                tree.add_node(sub1, root)
                tree.add_node(Node(typ), sub1)
                tree.add_node(Node(name), sub1)
                print(sub1.data)
                O(tokenbox, col, sub1, tree, errors)
                # 变量声明
            else:
                print(f'出现错误,函数定义缺少左括号,第{tokenbox.tokens[tokenbox.p-2][3]}行')
                errors.append(f'出现错误,函数定义缺少左括号,第{tokenbox.tokens[tokenbox.p-2][3]}行')

                U(tokenbox, col, root, tree, errors)
                if tokenbox.Token[1] == ')':
                    match(')', tokenbox)
                    if tokenbox.Token[1] == ';':
                        match(';', tokenbox)
                    else:
                        print(f'出现错误,函数定义缺少;号,第{tokenbox.tokens[tokenbox.p-2][3]}行')
                        errors.append(f'出现错误,函数定义缺少;号,第{tokenbox.tokens[tokenbox.p-2][3]}行')
                else:
                    print(f'出现错误,函数定义缺少右括号,第{tokenbox.tokens[tokenbox.p-2][3]}行')
                    errors.append(f'出现错误,函数定义缺少右括号,第{tokenbox.tokens[tokenbox.p-2][3]}行')
                    if tokenbox.Token[1] == ';':
                        match(';', tokenbox)
                    else:
                        print(f'出现错误,函数定义缺少;号,第{tokenbox.tokens[tokenbox.p-2][3]}行')
                        errors.append(f'出现错误,函数定义缺少;号,第{tokenbox.tokens[tokenbox.p-2][3]}行')
                # 错误
        else:
            if tokenbox.Token[2].startswith('i'):
                tokenbox.Token[1] = f = 'int'
            elif tokenbox.Token[2].startswith('ch'):
                tokenbox.Token[1] = f = 'char'
            elif tokenbox.Token[2].startswith('f'):
                tokenbox.Token[1] = f = 'float'
            elif tokenbox.Token[2].startswith('m'):
                tokenbox.Token[1] = f = 'main'
            elif tokenbox.Token[2].startswith('v'):
                tokenbox.Token[1] = f = 'void'
            elif tokenbox.Token[2].startswith('co'):
                tokenbox.Token[1] = f = 'const'
            print(f'出现函数声明错误:{tokenbox.Token[2]},第{tokenbox.Token[3]}行')
            errors.append(f'出现函数声明错误:{tokenbox.Token[2]},第{tokenbox.Token[3]}行')
    tokenbox.get_next_token()
    if tokenbox.Token[1] != '(':
        print(f'出现错误,main函数未左闭合,第{tokenbox.tokens[tokenbox.p - 2][3]}行')
        errors.append(f'出现错误,main函数未左闭合,第{tokenbox.tokens[tokenbox.p - 2][3]}行')
        tokenbox.p -= 1
        tokenbox.Token = [-1, '(', 'None', -1]
        # 错误
    tokenbox.get_next_token()
    if tokenbox.Token[1] != ')':
        print(f'出现错误,main函数未右闭合,第{tokenbox.tokens[tokenbox.p - 2][3]}行')
        errors.append(f'出现错误,main函数未右闭合,第{tokenbox.tokens[tokenbox.p - 2][3]}行')
        tokenbox.p -= 1
        tokenbox.Token = [-1, ')', 'None', -1]
        # 错误
    # 处理复合语句
    tokenbox.get_next_token()
    if tokenbox.Token[1] != '{':
        print(f'出现错误,复合语句缺少左大括号,第{tokenbox.tokens[tokenbox.p-2][3]}行')
        errors.append(f'出现错误,复合语句缺少左大括号,第{tokenbox.tokens[tokenbox.p-2][3]}行')
        tokenbox.p -= 1
        tokenbox.Token = [-1, '{', 'None', -1]


    G_(tokenbox, col, root, tree, errors)
    while tokenbox.Token[1] in ['int', 'char', 'float', 'void']:
        W_(tokenbox, col, root, tree, errors)
        # 函数定义分析
    if not errors:
        tree.show()

    return tree, errors


# 测试
content = read_file('Token/target.reg')
print(entry(content, 'test1'))