from Project.Lib3_Grammer.main import *
from Tables import *


"""
1、声明不赋值产生多余 去除字典重复
2、变量作用域
3、常量必须赋值不用考虑多余
"""


regulation = '../Lib3_Grammer/test1'
content = read_file('../Lib3_Grammer/Token/target.reg')
tree, _ = entry(content, regulation)
print(tree.show(key=False))
d = tree.to_dict(sort=False)


"""div"""

a = {}
b = {}
res = []
con_res = []
fun_res = []


def var_type(tree, root, obj, start):
    typ = tree[root]['children'][0]
    obj[1] = typ


def var(tree, root, obj, start):
    name = tree[root]['children'][0]
    obj[2] = name
    if obj[2] not in b:
        b[obj[2]] = []
    b[obj[2]].append(obj[:])


def var_val(tree, root, obj, start):
    val = tree[root]['children'][0]
    obj[3] = val
    res.append(obj[:])
    if obj[2] not in b:
        b[obj[2]] = []
    b[obj[2]].append(obj[:])
    obj[3] = ''
    start[0] += 1
    obj[0] = start[0]


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


def con_type(tree, root, obj, start):
    typ = tree[root]['children'][0]
    obj[1] = typ


def con_declare_list(tree, root, obj, start):
    child = tree[root]['children']
    obj[2] = child[0]
    obj[3] = child[1]['con']['children'][0]
    if obj[2] not in a:
        a[obj[2]] = []
    a[obj[2]].append(obj[:])
    # con_res.append(obj[:])


def con_declare(tree, root, obj, start):
    child = tree[root]['children']
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'con_type':
                    con_type(c, k, obj, start)
                elif k == 'con_declare_list':
                    con_declare_list(c, k, obj, start)
                else:
                    con_declare(c, k, obj, start)


def fun_type(tree, root, obj, start):
    typ = tree[root]['children'][0]
    obj.append(typ)


def fun_declare_fpar(tree, root, obj, start, par):
    child = tree[root]['children']
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'var_type':
                    item = c[k]['children'][0]
                    par.append(item)
                else:
                    fun_declare_fpar(c, k, obj, start, par)


def fun_declare(tree, root, obj, start):
    child = tree[root]['children']
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'fun_type':
                    fun_type(c, k, obj, start)
                elif k == 'fun_declare_fpar':
                    par = []
                    fun_declare_fpar(c, k, obj, start, par)
                    obj.append(str(len(par)))
                    for i in par:
                        obj.append(i)
                    fun_res.append(obj[:])
                else:
                    fun_declare(c, k, obj, start)


root = 'program'


def create_sign_table(tree, root, start=[1]):
    child = tree[root]['children']
    for c in child:
        for k, _ in c.items():

            if k == 'global_var_declare':
                t = c[k]['children'][0]
                s = c[k]['children'][1]
                obj = [start[0], t, s, '']
                global_var_declare(c, k, obj, start)
                pass
            elif k == 'fun_declare':
                s = c[k]['children'][1]
                obj = [start[0], s]
                fun_declare(c, k, obj, start)
            elif k == 'var_declare':
                obj = [start[0], '', '', '']
                var_declare(c, k, obj, start)
            elif k == 'con_declare':
                obj = [start[0], '', '', '']
                con_declare(c, k, obj, start)
            else:
                create_sign_table(c, k)
    # print(len(child))
    pass


create_sign_table(d, root)
print(res)
print(a)
print(b)
print(fun_res)