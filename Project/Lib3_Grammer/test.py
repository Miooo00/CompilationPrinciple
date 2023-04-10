import copy

with open('test1', 'r', encoding='utf-8') as fp:
    content = fp.readlines()

mapping = {}
for line in content:
    items = line.strip().split('→')
    mapping[items[0]] = items[1]


def getSignal(src):
    t = set()
    n = set()
    for line in src:
        items = line.strip().split('→')
        n.add(items[0])
    for line in src:
        items = line.strip().split('→')
        if '|' in items[1]:
            divs_sub = items[1].split('|')
            for divs in divs_sub:
                divs = divs.split(' ')
                for div in divs:
                    if div not in n:
                        t.add(div)
        else:
            divs = items[1].split(' ')
            for div in divs:
                if div not in n:
                    t.add(div)

    t = list(t)
    n = list(n)
    return t, n

t, n = getSignal(content)

def getFirst(cur, first):
    nexts = mapping[cur]


    if '|' in nexts:
        nexts = nexts.split('|')
        # + arg_exp|- arg_exp|$
        for item in nexts:
            divs = item.split(' ')
            div = divs[0]
            if div in t:
                first.add(div)
            else:
                getFirst(div, first)
    else:
        nexts = nexts.split(' ')
        ch = nexts[0]
        if ch in t:
            first.add(ch)
        else:
            getFirst(ch, first)


def getFirsts():
    firsts = {}
    for item in n:
        cur_first = set()
        getFirst(item, cur_first)
        firsts[item] = [i for i in cur_first]
    print(firsts)
    return firsts


def isstop(src_dict, new_dict):
    src_str = ''
    new_str = ''
    TODO:"""用集合判断"""
    for _, v in src_dict.items():
        for item in v:
            src_str += item
    for _, v in new_dict.items():
        for item in v:
            new_str += item
    return src_str != new_str


def getLast(start, firsts):
    print('follow集合')
    table = []
    follows = dict.fromkeys(n)
    for k in follows:
        follows[k] = set()
    print(mapping)
    for k, v in mapping.items():
        if '|' in v:
            v = v.split('|')
            for i in v:
                s = k + '→' + i
                table.append(s)
        else:
            s = k + '→' + v
            table.append(s)
    print(table)
    new_f = copy.deepcopy(follows)
    follows[start].add('#')
    # 前后的两个follow集合相同结束循环
    while isstop(new_f, follows):
        new_f = copy.deepcopy(follows)
        print(new_f)
        print(follows)
        for i in n:
            # 遍历每个非终结符
            for chs in table:
                # 遍历每个情况的产生式
                div = chs.split('→')
                sec = div[-1].split(' ')
                head = div[0]
                for j in range(len(sec)):
                    # '|'拆分
                    while j < len(sec) and sec[j] != i:
                        j += 1
                    # 在产生式中找到与当前非终结符相同的字符
                    if sec[-1] in n:
                        for item in follows[head]:
                            follows[sec[-1]].add(item)
                    if j >= len(sec) - 1:
                        break
                    elif sec[j+1] in t:
                        follows[i].add(sec[j+1])
                    elif sec[j+1] in n:
                        for item in firsts[sec[j + 1]]:
                            if item != '$':
                                follows[i].add(item)
                    # print(sec)

    print(follows)
    return follows



