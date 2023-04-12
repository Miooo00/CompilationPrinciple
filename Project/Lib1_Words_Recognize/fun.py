
def read_dict():
    category = {}
    with open('../Lib1_Words_Recognize/Category', 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
        for line in lines:
            item = line.split(' ')
            category[item[0]] = item[1].strip()
    return category


col = ['(', ')', '[', ']', '!', '*', '/', '%', '+', '-', '<', '>', '&', '|', '=', ',', ';', '{', '}', ' ']
border = ['(', ')', '[', ']', ',', ';', '{', '}', ' ']
hex_c = ['a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F']
cat = read_dict()


def digit_reg(src, i):
    """
    实数的识别
    :param src: 待分析源
    :param i: 指针，指向待判断的元素
    :return: 种别码 识别的串
    """
    state = 0
    start = i
    while state != 4 and state != 7 and state != 13 and state != 14 and state != 15 and state != 16:
        if state == 0:
            if src[i] == '0':
                state = 3
                i += 1
            elif src[i] != '0' and str.isdigit(src[i]):
                state = 1
                i += 1
        elif state == 1:
            if str.isdigit(src[i]):
                state = 1
                i += 1
            elif src[i] == 'e' or src[i] == 'E':
                state = 10
                i += 1
            elif src[i] == '.':
                state = 8
                i += 1
            elif src[i] in col:
                state = 15
            else:
                state = 16
            pass
        elif state == 3:
            if (src[i] != '8' and src[i] != '9' and src[i] != '0') and str.isdigit(src[i]):
                state = 17
                i += 1
            elif src[i] == 'x' or src[i] == 'X':
                state = 5
                i += 1
            elif src[i] == '.':
                state = 8
                i += 1
            elif src[i] != '.' and src[i] in col:
                state = 15
            else:
                state = 16
                i += 1
            pass
        elif state == 17:
            if (src[i] != '8' and src[i] != '9') and str.isdigit(src[i]):
                state = 17
                i += 1
            elif src[i] == '8' or src[i] == '9' or src[i] == '.':
                state = 16
                i += 1
            else:
                state = 4
                i += 1
        elif state == 5:
            if str.isdigit(src[i]) or src[i] in hex_c:
                state = 6
                i += 1
            else:
                state = 16
                i += 1
        elif state == 6:
            if str.isdigit(src[i]) or src[i] in hex_c:
                state = 6
                i += 1
            elif str.isdigit(src[i]) and (src[i] not in hex_c):
                state = 16
                i += 1
            else:
                state = 7
                i += 1
        elif state == 8:
            if str.isdigit(src[i]):
                state = 9
                i += 1
            else:
                state = 16
                i += 1
            pass
        elif state == 9:
            if str.isdigit(src[i]):
                state = 9
                i += 1
            elif src[i] == 'e' or src[i] == 'E':
                state = 10
                i += 1
            elif src[i] in col or src[i] == ' ':
                state = 14
            else:
                state = 16
                i += 1
            pass
        elif state == 10:
            if src[i] == '+' or src[i] == '-':
                state = 11
                i += 1
            elif str.isdigit(src[i]):
                state = 12
                i += 1
            else:
                state = 16
            pass
        elif state == 11:
            if str.isdigit(src[i]):
                state = 12
                i += 1
            else:
                state = 16
            pass
        elif state == 12:
            if str.isdigit(src[i]):
                state = 12
                i += 1
            elif src[i] == ' ':
                state = 13
                i += 1
            else:
                state = 16
                i += 1
            pass
    syn = -1
    if state == 4 or state == 7 or state == 13:
        syn = 800
        return syn, src[start:i-1], i
    elif state == 14:
        syn = 800
        return syn, src[start:i], i
    elif state == 15:
        syn = 400
        return syn, src[start:i], i
    else:
        tail = i
        while tail < len(src) and src[tail] != ' ':
            tail += 1
        return -1, src[start:tail], tail


def word_reg(src, i):
    state = 0
    start = i
    while state != 2:
        if state == 0:
            if str.isalpha(src[i]) or src[i] == '_':
                state = 1
                i += 1
        elif state == 1:
            if str.isalpha(src[i]) or src[i] == '_' or str.isdigit(src[i]):
                state = 1
                i += 1
            else:
                state = 2

    res = src[start: i]
    if res in cat:
        return cat[res], res, i
    else:
        return 700, res, i


def chr_cons_reg(src, i):
    state = 0
    start = i
    while state != 3 and state != 4:
        if state == 0:
            if src[i] == "'":
                state = 1
                i += 1
        elif state == 1:
            if str.isascii(src[i]):
                state = 2
                i += 1
        elif state == 2:
            if src[i] == "'":
                state = 3
                i += 1
            else:
                state = 4
                i += 1

    res = src[start: i]
    if state == 3:
        res = res.replace("'", '')
        return 500, res, i
    elif state == 4:
        return -3, res, i

# print(chr_cons_reg("'abc' ", 0))


def chrs_cons_reg(src, i):
    state = 0
    start = i
    while state != 3 and state != 4 and state != 6:
        if state == 0:
            if src[i] == '"':
                state = 1
                i += 1
        elif state == 1:
            if str.isascii(src[i]):
                state = 2
                i += 1
        elif state == 2:
            if src[i] == '"':
                state = 3
                i += 1
            elif src[i] == '/':
                state = 5
                i += 1
            elif str.isascii(src[i]):
                if i == len(src)-1:
                    state = 4
                    i += 1
                else:
                    state = 2
                    i += 1
            else:
                state = 4
                i += 1
        elif state == 5:
            if src[i] == '*':
                state = 6
                i -= 1
            else:
                state = 2
                i += 1

    res = src[start: i]
    if state == 3:
        res = res.replace('"', '')
        return 600, res, i
    elif state == 4 or state == 6:
        return -4, res, i


def expl_div_reg(src, i, pre_state):
    state = pre_state
    start = i
    while state != 2 and state != 5 and state != 6 and state != 7:
        if state == 0:
            if src[i] == '/':
                state = 1
                i += 1
        elif state == 1:
            if src[i] == '*':
                state = 3
                i += 1
            else:
                state = 2
                i += 1
        elif state == 3:
            if i < len(src):
                if src[i] != '*':
                    state = 3
                    i += 1
                elif src[i] == '*':
                    state = 4
                    i += 1
                else:
                    state = 6
                    i += 1
            else:
                state = 7
                i += 1
        elif state == 4:
            if src[i] == '*':
                state = 4
                i += 1
            elif src[i] != '*' and src[i] != '/':
                state = 3
                i += 1
            elif src[i] == '/':
                state = 5
                i += 1
            else:
                state = 6
                i += 1

    if state == 2:
        res = src[start: i-1]
        return 207, res, i-1
    elif state == 5:
        res = src[start: i]
        return -5, res, i
    elif state == 6:
        res = src[start: i]
        return -2, res, i
    elif state == 7:
        res = src[start: i]
        return -9, res, i


def sig_reg(src, i):
    state = 0
    start = i
    while state != 2 and state != 4 and state != 5 and state != 6:
        if state == 0:
            if src[i] == '>':
                state = 1
                i += 1
        elif state == 1:
            if src[i] == '=':
                state = 2
                i += 1
            elif src[i] == '>':
                state = 3
                i += 1
            else:
                state = 6
                i += 1
        elif state == 3:
            if src[i] == '=':
                state = 4
                i += 1
            else:
                state = 5
                i += 1
    if state == 2:
        res = src[start: i]
        return 214, res, i
    elif state == 4:
        res = src[start: i]
        return 221, res, i
    elif state == 5:
        res = src[start: i-1]
        return 222, res, i-1
    elif state == 6:
        res = src[start: i-1]
        return 213, res, i-1


def sig_reg2(src, i):
    state = 0
    start = i
    while state != 2 and state != 4 and state != 5 and state != 6:
        if state == 0:
            if src[i] == '<':
                state = 1
                i += 1
        elif state == 1:
            if src[i] == '=':
                state = 2
                i += 1
            elif src[i] == '<':
                state = 3
                i += 1
            else:
                state = 6
                i += 1
        elif state == 3:
            if src[i] == '=':
                state = 4
                i += 1
            else:
                state = 5
                i += 1
    if state == 2:
        res = src[start: i]
        return 212, res, i
    elif state == 4:
        res = src[start: i]
        return 223, res, i
    elif state == 5:
        res = src[start: i-1]
        return 224, res, i-1
    elif state == 6:
        res = src[start: i-1]
        return 211, res, i-1


def double_sig_rec(src, i):
    state = 0
    start = i
    while state != 2 and state != 3 and state != 6 and state != 9 and state != 12 and state != 14:
        if state == 0:
            if src[i] == '+':
                state = 1
                i += 1
            elif src[i] == '&':
                state = 5
                i += 1
            elif src[i] == '|':
                state = 8
                i += 1
            elif src[i] == '-':
                state = 11
                i += 1
            elif src[i] == '=':
                state = 13
                i += 1
        elif state == 1:
            if src[i] == '+' or src[i] == '=':
                state = 3
                i += 1
            elif str.isdigit(src[i]) or str.isalpha(src[i]) or (src[i] in border):
                state = 2
        elif state == 5:
            if src[i] == '&' or src[i] == '=':
                state = 6
                i += 1
            elif str.isdigit(src[i]) or str.isalpha(src[i]) or (src[i] in border):
                state = 2
        elif state == 8:
            if src[i] == '|' or src[i] == '=':
                state = 9
                i += 1
            elif str.isdigit(src[i]) or str.isalpha(src[i]) or (src[i] in border):
                state = 2
        elif state == 11:
            if src[i] == '-' or src[i] == '=':
                state = 12
                i += 1
            elif str.isdigit(src[i]) or str.isalpha(src[i]) or (src[i] in border):
                state = 2
        elif state == 13:
            if src[i] == '=':
                state = 14
                i += 1
            elif str.isdigit(src[i]) or str.isalpha(src[i]) or (src[i] in border) or src[i] == '"' or src[i] == "'":
                state = 2

    res = src[start: i]
    if state == 2:
        return cat[src[start]], res, i
    elif state == 3:
        return cat[res], res, i
    elif state == 6:
        return cat[res], res, i
    elif state == 9:
        return cat[res], res, i
    elif state == 12:
        return cat[res], res, i
    elif state == 14:
        return cat[res], res, i

# print(digit_reg('1.45e5 + 5', 0))
# print(word_reg('int ', 0))
# print(chr_cons_reg("'b'", 0))
# print(chrs_cons_reg('"abc"', 0))

# print(digit_reg('12355b.2 ', 0))
# print(expl_div_reg('/*2 ', 0))
# print(sig_reg('>>= ', 0))
# print(word_reg('_abc ', 0))