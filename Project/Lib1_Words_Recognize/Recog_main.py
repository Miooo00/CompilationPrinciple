from Readcategory import rCategory

c_dict = rCategory()
path = './Test'


def recognize(src, s, i):
    syn = -1
    state = 0
    index = i
    start = s
    while state != 3:
        if len(src)-1 == index:
            break
        if state == 0:
            if str.isalpha(src[index]):
                state = 1
            elif str.isdigit(src[index]):
                state = 2
            else:
                start += 1
            index += 1
        elif state == 1:
            if str.isalpha(src[index]):
                index += 1
            else:
                state = 3
                syn = 700
        elif state == 2:
            if str.isdigit(src[index]):
                index += 1
            else:
                state = 3
                syn = 400
    # print(src[start:index])
    if index == len(src)-1:
        return index, src[start:], syn
    return index, src[start:index], syn


def find_all(src):
    res = []
    start = index = 0
    while index != len(src)-1:
        index, item, code = recognize(src, start, index)
        start = index
        res.append([item, code])
    return res
    # print(res)




def operate_file(path):
    with open(path, 'r', encoding='utf-8') as fp:
        content = fp.readlines()
    row_c = 0
    info = []
    for line in content:
        items = find_all(line)
        for item in items:
            c = str(item[1])
            if c in c_dict:
                info.append([c, c_dict[c], item[0], row_c])
            else:
                info.append([-1, 'none', item[0], row_c])
        row_c += 1
    for l in info:
        print(l)


# chracters = find_all('%^*abc((aac&ssd123//123')
operate_file(path)


