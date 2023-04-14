from Project.Lib3_Grammer.main import *
from Tables import *

regulation = '../Lib3_Grammer/test1'

content = read_file('../Lib3_Grammer/Token/target.reg')
tree, _ = entry(content, regulation)

print(tree.show(key=False))

d = tree.to_dict(sort=False)




"""div"""


def var_type(tree, root, obj, start):
    typ = tree[root]['children'][0]
    obj[1] = typ


def var(tree, root, obj, start):
    name = tree[root]['children'][0]
    obj[2] = name
    res.append(obj[:])


def var_val(tree, root, obj, start):
    val = tree[root]['children'][0]
    obj[3] = val
    res.append(obj[:])
    obj[3] = ''
    start[0] += 1
    obj[0] = start[0]


res = []
def global_var_declare(tree, root, obj, start):
    child = tree[root]['children']
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'var_type':
                    var_type(c, k, obj, start)
                elif k == 'var':
                    var(c, k, obj, start)
                elif k == 'con':
                    var_val(c, k, obj, start)
                else:
                    global_var_declare(c, k, obj, start)



def var_declare(tree, root, obj, start):
    child = tree[root]['children']
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'var_type':
                    var_type(c, k, obj, start)
                elif k == 'var':
                    var(c, k, obj, start)
                elif k == 'con':
                    var_val(c, k, obj, start)
                else:
                    var_declare(c, k, obj, start)

def con_declare():
    pass


def fun_declare():
    pass


root = 'program'
def create_sign_table(tree, root, start=[1]):
    child = tree[root]['children']
    for c in child:
        for k, _ in c.items():

            if k == 'global_var_declare':
                obj = [start[0], '', '', '']
                global_var_declare(c, k, obj, start)
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
