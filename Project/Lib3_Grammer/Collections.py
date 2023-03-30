import copy


class Collections:
    def __init__(self, regulation, start):
        self.mapping = {}
        self.t = set()
        self.n = set()
        self.firsts = {}
        self.follows = {}
        self.start = start
        with open(regulation, 'r', encoding='utf-8') as fp:
            content = fp.readlines()
        for line in content:
            items = line.strip().split('→')
            self.mapping[items[0]] = items[1]
        self.getSignal(content)


    def getSignal(self, src):
        for line in src:
            items = line.strip().split('→')
            self.n.add(items[0])
        for line in src:
            items = line.strip().split('→')
            if '|' in items[1]:
                divs_sub = items[1].split('|')
                for divs in divs_sub:
                    divs = divs.split(' ')
                    for div in divs:
                        if div not in self.n:
                            self.t.add(div)
            else:
                divs = items[1].split(' ')
                for div in divs:
                    if div not in self.n:
                        self.t.add(div)
        self.t = list(self.t)
        self.n = list(self.n)

    def getFirst(self, cur, first):
        nexts = self.mapping[cur]

        if '|' in nexts:
            nexts = nexts.split('|')
            # + arg_exp|- arg_exp|$
            for item in nexts:
                divs = item.split(' ')
                div = divs[0]
                if div in self.t:
                    first.add(div)
                else:
                    self.getFirst(div, first)
        else:
            nexts = nexts.split(' ')
            ch = nexts[0]
            if ch in self.t:
                first.add(ch)
            else:
                self.getFirst(ch, first)

    def getFirsts(self):
        for item in self.n:
            cur_first = set()
            self.getFirst(item, cur_first)
            self.firsts[item] = [i for i in cur_first]

    def isstop(self, src_dict, new_dict):
        src_str = ''
        new_str = ''
        TODO: """用集合判断"""
        for _, v in src_dict.items():
            for item in sorted(v):
                src_str += item
        for _, v in new_dict.items():
            for item in sorted(v):
                new_str += item
        return src_str != new_str

    def getLast(self, start, firsts):
        table = []
        self.follows = dict.fromkeys(self.n)
        for k in self.follows:
            self.follows[k] = set()
        for k, v in self.mapping.items():
            if '|' in v:
                v = v.split('|')
                for i in v:
                    s = k + '→' + i
                    table.append(s)
            else:
                s = k + '→' + v
                table.append(s)
        new_f = copy.deepcopy(self.follows)
        self.follows[start].add('#')
        # 前后的两个follow集合相同结束循环
        while self.isstop(new_f, self.follows):
            new_f = copy.deepcopy(self.follows)
            for i in self.n:
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
                        if sec[-1] in self.n:
                            for item in self.follows[head]:
                                self.follows[sec[-1]].add(item)
                        if j >= len(sec) - 1:
                            break
                        elif sec[j + 1] in self.t:
                            self.follows[i].add(sec[j + 1])
                        elif sec[j + 1] in self.n:
                            for item in firsts[sec[j + 1]]:
                                if item != '$':
                                    self.follows[i].add(item)
                        # print(sec)
        return self.follows


    def GET_FIRST_FOLLOW(self):
        self.getFirsts()
        self.getLast(self.start, self.firsts)

a = Collections('test1', 'arg_exp')
a.GET_FIRST_FOLLOW()

print(a.firsts)
print(a.follows)
print(a.t)