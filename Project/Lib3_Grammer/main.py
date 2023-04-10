"""
总控接口
需要:
词法分析结果文件: [种别码, 'obj', 行号]
语法规则:
    (递归下降,无左递归,无回溯.如A→B
    <div>取代|表示'或者', |用于逻辑运算或)
"""
from Project.Lib3_Grammer.fun import *
from Project.Lib3_Grammer.Collections import Collections


def entry(token_file, regulation, start='program'):
    """
    :param token_file: 词法分析结果
    :param regulation: 语法
    :param start: 开始符号
    :return: 错误信息
    """
    errors = []
    tokens = []
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
            L(tokenbox, col)
            pass
        elif tokenbox.Token[1] in ['int', 'char', 'float', 'void']:
            tokenbox.get_next_token()
            if tokenbox.Token[1] == 'main':
                break
            if tokenbox.Token[1] != 'signal':
                pass
                # 错误处理
            tokenbox.get_next_token()
            if tokenbox.Token[1] == '(':
                # 修改了文法的递归下降函数 解决了检测入口不对称
                S(tokenbox, col)
                if tokenbox.Token[1] == '{':
                    print(f'出现错误,在main函数前创建函数语句,或没有main函数,第{tokenbox.tokens[tokenbox.p-2][3]}行')
                    errors.append(f'出现错误,在main函数前创建函数语句,或没有main函数,第{tokenbox.tokens[tokenbox.p-2][3]}行')
                    G_(tokenbox, col)
                    break
                # 函数声明
            elif tokenbox.Token[1] == '=' or tokenbox.Token[1] == ',':
                O(tokenbox, col)
                # 变量声明
            else:
                print(f'出现错误,函数定义缺少左括号,第{tokenbox.tokens[tokenbox.p-2][3]}行')
                errors.append(f'出现错误,函数定义缺少左括号,第{tokenbox.tokens[tokenbox.p-2][3]}行')

                U(tokenbox, col)
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
            elif tokenbox.Token[2].startswith('c'):
                tokenbox.Token[1] = f = 'char'
            elif tokenbox.Token[2].startswith('f'):
                tokenbox.Token[1] = f = 'float'
            elif tokenbox.Token[2].startswith('m'):
                tokenbox.Token[1] = f = 'main'
            elif tokenbox.Token[2].startswith('v'):
                tokenbox.Token[1] = f = 'void'
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
    G_(tokenbox, col)
    while tokenbox.Token[1] in ['int', 'char', 'float', 'void']:
        W_(tokenbox, col)
        # 函数定义分析
    return errors



print(entry('Token/target.reg', 'test1'))