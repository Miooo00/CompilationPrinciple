class Tables:
    def __init__(self):
        self.entry = 1
        self.name = ''


class FunctionItem:
    def __init__(self):
        self.entry = 1
        self.name = ''
        self.type = ''
        self.val = ''


class VarItem:
    def __init__(self):
        self.entry = 1
        self.name = ''
        self.type = ''
        self.val = ''
        self.varList = []

    def items_print(self):
        print(self.entry, self.name, self.type, self.val)


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






