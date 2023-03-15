"""
编写Lex源程序，其功能是输出文本文件中Sample语言的标识符和整数。
并分析生成的C语言代码，找出 “识别标识符和整数”的代码

"""
import ply.lex as lex

tokens = (
    'SIGNAL',
    'NUMBER',
)


t_SIGNAL = r'[_|a-z|A-Z][_|a-z|A-Z|0-9]*'
t_NUMBER = r'0|[1-9][0-9]*'


t_ignore = '\t'


def t_error(t):
    t.lexer.skip(1)


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


chr_line_counter('../Lib1_Words_Recognize/Test')