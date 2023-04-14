from Project.Lib3_Grammer.main import *
from Tables import *

regulation = '../Lib3_Grammer/test1'

content = read_file('../Lib3_Grammer/Token/target.reg')
tree, _ = entry(content, regulation)

print(tree.show(key=False))
print(tree.to_dict(sort=False))
d = tree.to_dict(sort=False)


def var_declare():
    pass

"""div"""
def var_type(tree, root, obj):
    typ = tree[root]['children'][0]
    obj[1] = typ

def var(tree, root, obj):
    name = tree[root]['children'][0]
    obj[2] = name

def var_val(tree, root, obj):
    val = tree[root]['children'][0]
    obj[3] = val


res = []
def global_var_declare(tree, root, obj):
    child = tree[root]['children']
    for c in child:
        if type(c) == 'dict':
            for k, _ in c.items():
                if k == 'var_type':
                    var_type(tree, k, obj)
                elif k == 'var':
                    var(tree, k, obj)
                elif k == 'con':
                    var_val(tree, k, obj)
                else:
                    global_var_declare(tree, k, obj)
                res.append(obj[:])


    pass


def con_declare():
    pass


def fun_declare():
    pass


root = 'program'
def create_sign_table(tree, root):
    child = tree[root]['children']
    for c in child:
        for k, _ in c.items():
            print(k)
            if k == 'global_var_declare':
                obj = ['', '', '', '']
                global_var_declare(c, k, obj)
                pass
    #         elif k == 'fun_declare':
    #             pass
    #         elif k == 'var_declare':
    #             pass
    #         elif k == 'con_declare':
    #             pass
    #         else:
    #             create_sign_table(tree, root)
    # print(len(child))
    pass

create_sign_table(d, root)
print(res)
