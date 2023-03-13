from Project.Lib1_Words_Recognize.Readcategory import rCategory
from Project.Lib1_Words_Recognize.fun import *
c_dict = rCategory()
path = './Test'
col = ['(', ')', '[', ']', '!', '*', '/', '%', '+', '-', '<', '>', '&', '|', '=', '.', ',', ';', '{', '}']


def rec(src, i):
    if src[i] == ' ':
        i += 1
        return -2, None, i
    elif src[i] == '/':
        code, res, n_i = expl_div_reg(src, i)
        return code, res, n_i
    elif src[i] == '_' or str.isalpha(src[i]):
        code, res, n_i = word_reg(src, i)
        return code, res, n_i
    elif str.isdigit(src[i]):
        code, res, n_i = digit_reg(src, i)
        return code, res, n_i
    elif src[i] in col:
        return c_dict[src[i]], src[i], i+1
    elif src[i] == "'":
        code, res, n_i = chr_cons_reg(src, i)
        return code, res, n_i
    elif src[i] == '"':
        code, res, n_i = chrs_cons_reg(src, i)
        return code, res, n_i
    else:
        return -2, None, i+1

def op(src, row):
    res = []
    err = []
    index = 0
    while index <= len(src) - 1:
        code, item, index = rec(src, index)
        if code == -1:
            tip = f'数值规范错误, 位置:第{row}行, 出错串:{item}'
            err.append(tip)
        elif item:
            res.append([item, code])
    return res, err


def entry1(content):
    # with open(path, 'r', encoding='utf-8') as fp:
    #     content = fp.readlines()
    content = content.split('\n')
    # 识别每一行
    c_row = 1
    info = []
    for line in content:
        if line.strip():
            line += ' '
            pos, neg = op(line, c_row)
            info.append([pos, neg, c_row])
        c_row += 1
    return info

