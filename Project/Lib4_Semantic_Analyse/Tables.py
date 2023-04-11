class Tables:
    def __init__(self):
        self.entry = 1
        self.name = ''


class Constobj(Tables):
    def __init__(self):
        super().__init__()
        self.type = ''
        self.val = ''

    def Tprint(self):
        print(self.entry, self.name, self.type, self.val)


class Table:
    def __init__(self):
        self.t = []
        self.entry = 1

    def add_obj(self, obj):
        obj.entry = self.entry
        self.entry += 1
        self.t.append(obj)






