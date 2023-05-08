
class FunctionItem:
    def __init__(self):
        self.entry = 1
        self.name = ''
        self.type = ''
        self.parLen = 0
        self.para = []

    def items_print(self):
        print(self.entry, self.name, self.type, self.parLen, self.para, sep='\t\t   ')

    def to_string(self):
        res_str = str(self.entry) + ' ' + self.name + ' ' + self.type + ' ' + str(self.parLen) + ' '
        for par in self.para:
            res_str += par + ' '
        res_str += '\n'
        return res_str

class VarItem:
    def __init__(self, name='null', type='null', val='null', field='null'):
        self.entry = 1
        self.name = name
        self.type = type
        self.val = val
        self.field = field

    def items_print(self):
        print(self.entry, self.name, self.type, self.val, self.field, sep='\t\t   ')

    def to_string(self):
        res_str = str(self.entry) + ' ' + self.name + ' ' + self.type + ' ' + self.val + ' ' + self.field
        res_str += '\n'
        return res_str



class ConstItem:
    def __init__(self):
        self.entry = 1
        self.name = ''
        self.type = ''
        self.val = ''
        self.field = ''

    def items_print(self):
        print(self.entry, self.name, self.type, self.val, self.field, sep='\t\t   ')

    def to_string(self):
        res_str = str(self.entry) + ' ' + self.name + ' ' + self.type + ' ' + self.val + ' ' + self.field
        res_str += '\n'
        return res_str



class Table:
    def __init__(self, flag):
        self.table = []
        self.entry = 1
        self.flag = flag

    def add_obj(self, obj):
        obj.entry = self.entry
        self.entry += 1
        self.table.append(obj)

    def get_val(self, name):
        if self.flag == 'C':
            for item in self.table:
                if item.name == name:
                    return item.val
        elif self.flag == 'V':
            for item in self.table:
                if item.name == name:
                    return item.val
        return 114514

    def search_in_field(self, name, cur_field):
        if self.flag == 'C':
            for item in self.table:
                if item.name == name and (item.field == '<all>' or cur_field.startswith(item.field)):
                    return True
            return False
        elif self.flag == 'V':
            for item in self.table:
                if item.name == name and (item.field == '<all>' or cur_field.startswith(item.field)):
                    return True
            return False
        elif self.flag == 'F':
            for item in self.table:
                if item.name == name and (item.field == '<all>' or cur_field.startswith(item.field)):
                    return True
            return False

    def search(self, name):
        if self.flag == 'C':
            for item in self.table:
                if item.name == name:
                    return False
            return True
        elif self.flag == 'V':
            for item in self.table:
                if item.name == name:
                    return False
            return True
        elif self.flag == 'F':
            for item in self.table:
                if item.name == name:
                    return False
            return True

    def get(self, name):
        if self.flag == 'C':
            for item in self.table:
                if item.name == name:
                    return item
        elif self.flag == 'V':
            for item in self.table:
                if item.name == name:
                    return item
        elif self.flag == 'F':
            for item in self.table:
                if item.name == name:
                    return item
        return None

    def update(self, name, val):
        if self.flag == 'C':
            for item in self.table:
                if item.name == name:
                    item.val = val
                    return
        elif self.flag == 'V':
            for item in self.table:
                if item.name == name:
                    item.val = val
                    return
        elif self.flag == 'F':
            for item in self.table:
                if item.name == name:
                    item.val = val
                    return

    def pop(self):
        self.table.pop()






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
        self.length = 0

    def add_node(self, node):
        self.list.append(node)
        self.length = len(self.list)

    def show(self):
        index = 1
        res = ''
        for item in self.list:
            line = str(index)+':' + '('
            for i in item:
                line += str(i) + ','
            line = line +')'
            print(line)
            res += line + '\n'
            index += 1
        return res


class ENTRY:
    def __init__(self):
        self.realChain = []
        self.fakeChain = []

    def merge_real(self, op_table, exit, reset=False):
        table = op_table.list
        # print(len(table), self.realChain)
        for i in self.realChain:
            table[i][3] = exit
        if reset:
            self.realChain = []

    def merge_fake(self, op_table, exit, reset=False):
        table = op_table.list
        for i in self.fakeChain:
            table[i][3] = exit
        if reset:
            self.fakeChain = []

    def reset(self, r_chain=False, f_chain=False):
        if r_chain:
            self.realChain = []
        if f_chain:
            self.fakeChain = []

