"""
算术表达式
"""
import copy

with open('operation', 'r', encoding='utf-8') as fp:
    content = fp.readlines()

mapping = {}
for line in content:
    items = line.strip().split('→')
    mapping[items[0]] = items[1]




"""
→
"""
def getSignal(src):
    t = set()
    n = set()
    for i in range(len(src)):
        n.add(src[i][0])
    for line in src:
        right = line.strip().split('→')[-1]
        for ch in right:
            if ch != '|' and (ch not in n):
                t.add(ch)
    t = list(t)
    n = list(n)
    return t, n


t, n = getSignal(content)


def getFirst(cur, first):
    nexts = mapping[cur]
    if '|' in nexts:
        nexts = nexts.split('|')
        for i in nexts:
            ch = i[0]
            if ch in t:
                first.add(ch)
            else:
                getFirst(ch, first)
    else:
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

firsts = getFirsts()

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

# print(mapping)
def getLast(start):
    table = []
    follows = dict.fromkeys(n)
    for k in follows:
        follows[k] = set()

    print(follows)
    # follows = sorted(follows.items(), key=lambda x: x[0])
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
                sec = chs.split('→')[-1]
                head = chs[0]
                for j in range(len(sec)):
                    # '|'拆分
                    while j < len(sec) and sec[j] != i:
                        j += 1
                    # 在产生式中找到与当前非终结符相同的字符
                    if j > len(sec) - 1:
                        break
                    elif j == len(sec) - 1:
                        for item in follows[i]:
                            follows[head].add(item)
                    elif sec[j+1] in t:
                        follows[i].add(sec[j+1])
                    elif sec[j+1] in n:
                        for item in firsts[sec[j + 1]]:
                            if item != '$':
                                follows[i].add(item)
    print(follows)

getLast('A')