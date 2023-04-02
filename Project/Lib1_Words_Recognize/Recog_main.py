from Project.Lib1_Words_Recognize.fun import *
c_dict = read_dict()
col = ['(', ')', '[', ']', '!', '*', '/', '%', '+', '-', '<', '>', '&', '|', '=', '.', ',', ';', '{', '}', '"']


def rec(src, i, isrecheck):
    if isrecheck:
        code, res, n_i = expl_div_reg(src, i, 3)
        return code, res, n_i
    if src[i] == ' ':
        i += 1
        return -10, None, i
    elif src[i] == '@' or src[i] == '$':
        while src[i] != ' ':
            i += 1
        return -6, src[:i], len(src)
    elif src[i] == '+' or src[i] == '-' or src[i] == '&' or src[i] == '|' or src[i] == '=':
        code, res, n_i = double_sig_rec(src, i)
        return code, res, n_i
    elif src[i] == '/':
        code, res, n_i = expl_div_reg(src, i, 0)
        return code, res, n_i
    elif src[i] == '_' or str.isalpha(src[i]):
        code, res, n_i = word_reg(src, i)
        return code, res, n_i
    elif str.isdigit(src[i]):
        code, res, n_i = digit_reg(src, i)
        return code, res, n_i
    elif src[i] == '>':
        code, res, n_i = sig_reg(src, i)
        return code, res, n_i
    elif src[i] == '<':
        code, res, n_i = sig_reg2(src, i)
        return code, res, n_i
    elif src[i] == "'":
        code, res, n_i = chr_cons_reg(src, i)
        return code, res, n_i
    elif src[i] == '"':
        code, res, n_i = chrs_cons_reg(src, i)
        return code, res, n_i
    elif src[i] in col:
        return c_dict[src[i]], src[i], i+1
    else:
        return -10, None, i+1


def op(src, row, e_str, e_start, isrecheck, max_row):
    res = []
    err = []
    index = 0
    next_line = 0
    last_str = ''
    while index <= len(src) - 1:
        code, item, index = rec(src, index, isrecheck)
        if code == -1:
            tip = f'数值规范错误, 位置:第{row}行, 出错串:{item}'
            err.append(tip)
        elif code == -2 or (row >= max_row and code == -9):
            err_str = e_str + item
            tip = f'注释规范错误, 位置:第{e_start}:{row}行, 出错串:{err_str}'
            next_line = 0
            isrecheck = 0
            err.append(tip)
        elif code == -3:
            tip = f'字符常量错误, 位置:第{row}行, 出错串:{item}'
            err.append(tip)
        elif code == -4:
            tip = f'字符串常量错误, 位置:第{row}行, 出错串:{item}'
            err.append(tip)
        elif code == -6:
            tip = f'非法字符, 位置:第{row}行, 出错串:{item}'
            err.append(tip)
        elif code == -9:
            next_line = 1
            last_str = item
        elif e_str and item:
            # res.append([e_str + item, code])
            isrecheck = 0
            next_line = 0
        elif item and code != -5:
            res.append([item, code])
    return res, err, next_line, last_str


def entry1(content):
    content = content.split('\n')
    # 识别每一行
    c_row = 1
    info = []
    ex_str = ''
    ex_start = ''
    recheck = 0
    max_crow = len(content)
    for line in content:
        line += ' '
        pos, neg, f_line, l_str = op(line, c_row, ex_str, ex_start, recheck, max_crow)
        if f_line:
            recheck = 1
            ex_str += l_str + '\n'
            if not ex_start:
                ex_start = c_row
            else:
                ex_start = min(c_row, ex_start)
        else:
            ex_str = ''
            ex_start = ''
            recheck = 0
        info.append([pos, neg, c_row])
        c_row += 1
    return info
