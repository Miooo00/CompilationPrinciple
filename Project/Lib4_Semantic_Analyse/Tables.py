class Tables:
    def __init__(self):
        self.entry = 1
        self.name = ''


class FunctionItem:
    def __init__(self):
        self.entry = 1
        self.name = ''
        self.type = ''
        self.parLen = 0
        self.para = []

    def items_print(self):
        print(self.entry, self.name, self.type, self.parLen, self.para)


class VarItem:
    def __init__(self):
        self.entry = 1
        self.name = ''
        self.type = ''
        self.val = ''

    def items_print(self):
        print(self.entry, self.name, self.type, self.val)

    def format_output(self):
        print("------------------------------------------")
        print("index\tname\ttype\tval\t")


class ConstItem:
    def __init__(self):
        self.entry = 1
        self.name = ''
        self.type = ''
        self.val = ''

    def items_print(self):
        print(self.entry, self.name, self.type, self.val)


class Table:
    def __init__(self):
        self.t = []
        self.entry = 1

    def add_obj(self, obj):
        obj.entry = self.entry
        self.entry += 1
        self.t.append(obj)


class Node:
    def __init__(self, op='', a='', b='', c=''):
        self.op = op
        self.obja = a
        self.objb = b
        self.res = c

    def ready2add(self):
        if self.op and self.obja and self.objb and self.res:
            return True
        return False

    def reset(self):
        self.op = self.obja = self.objb = self.res = ''


class Temp:
    def __init__(self):
        self.count = 1
        self.table = {}
        self.last = ''

    def newtemp(self, val=0):
        temp = f'T{self.count}'
        self.count += 1
        self.table[temp] = val
        return temp


class OPCODE:
    def __init__(self):
        self.list = []

    def add_node(self, node):
        self.list.append(node)

    def show(self):
        index = 1
        for item in self.list:
            line = str(index)+':'+'\t' + '('
            for i in item:
                line += str(i) + ',' + '\t'
            line = line +')'
            print(line)
            index += 1


class ENTRY:
    def __init__(self):
        self.realChain = []
        self.fakeChain = []

    def merge(self, exit):
        for item in self.realChain:
            item[3] = exit





