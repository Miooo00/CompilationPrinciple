"""
编写Lex源程序，其功能是统计文本文件中的字符数和行数。
请分析Lex生成的C语言代码，找出“统计字符数和行数”的代码

！需要安装依赖ply ---- pip install ply

"""

import ply.lex as lex


tokens = (
    'CHRACTER',
)


t_CHRACTER = r'.'


t_ignore = '\t'


def t_error(t):
    t.lexer.skip(1)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def read_file(path):
    with open(path, 'r', encoding='utf-8') as fp:
        content = fp.read()
    return content


lexer = lex.lex()


def chr_line_counter(path):
    data = read_file(path)
    lexer.input(data)
    c_chr = 0
    while True:
        tok = lexer.token()
        c_chr += 1
        if not tok:
            break
        print(tok)
    print(f'字符数:{c_chr}')
    print(f'行数:{lexer.lineno}')


chr_line_counter('../Lib1_Words_Recognize/Test1.txt')