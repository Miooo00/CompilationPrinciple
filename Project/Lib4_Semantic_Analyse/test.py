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

index = [1]
res = []
inter_c = []
v_tc = [1]

def merge(table):
    """去重 除去声明未赋值可能产生的冗余"""
    i = 0
    length = len(table)
    if length == 1:
        return table
    while i < length:
        if table[i][0] == table[i-1][0]:
            table.pop(i-1)
            length -= 1
        i += 1
    return table


def visit_node(obj):
    flag = obj[1]
    name = obj[3]
    for node in res:
        if node[1] == flag and node[3] == name:
            if flag == 'F':
                print("出现函数重名!")
                return False
            elif flag == 'V' or flag == 'GV':
                print("重复声明变量!")
                return False
            elif flag == 'C':
                print("重复声明常量!")
                return False
    return True


def has_item(table, flag, name):
    for i in table:
        if flag != i[1]:
            continue
        if name == i[3]:
            return True
    return False



def search_symbol(table, flag, name):
    if flag == 'V':
        for i in table:
            if i[1] != 'V':
                continue
            if i[4] and i[3] == name:
                return i[4]
    return ''


def update_symbol(table, flag, name, val):
    for i in table:
        if i[1] != flag:
            continue
        if i[3] == name:
            i[4] = val


def var_type(tree, root, obj):
    typ = tree[root]['children'][0]
    obj[2] = typ


def var(tree, root, obj):
    name = tree[root]['children'][0]['var']['children'][0]
    obj[3] = name


def var_val(tree, root, obj):
    val = tree[root]['children'][0]
    obj[4] = val


def get_val(tree, root, obj):
    child = tree[root]['children']
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'con':
                    obj[4] = int(c['con']['children'][0])
                elif k == 'var':
                    obj[4] = search_symbol(res, 'V', c['var']['children'][0])
                else:
                    get_val(c, k, obj)

def global_var_declare(tree, root, obj):
    child = tree[root]['children']
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'var_type':
                    var_type(c, k, obj)
                elif k == 'var':
                    var(c, k, obj)
                elif k == 'con':
                    var_val(c, k, obj)
                else:
                    global_var_declare(c, k, obj)


def var_declare(tree, root, obj, str_d):
    child = tree[root]['children']
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'var_type':
                    var_type(c, k, obj)
                elif k == 'expression':
                    get_val(c, k, obj)
                # elif k == 'con':
                #     var_val(c, k, obj)
                elif k == 'one_var_declare':
                    var(c, k, obj)
                    var_declare(c, k, obj, str_d)
                    if visit_node(obj):
                        obj[-1] = str_d
                        res.append(obj[:])
                        index[0] += 1
                        obj[0] = index[0]
                else:
                    var_declare(c, k, obj, str_d)


def con_type(tree, root, obj):
    typ = tree[root]['children'][0]
    obj[2] = typ


def con_declare_list(tree, root, obj, str_d):
    child = tree[root]['children']
    obj[3] = child[0]
    obj[4] = child[1]['con']['children'][0]
    if visit_node(obj):
        obj[-1] = str_d
        res.append(obj[:])
        index[0] += 1
        obj[0] = index[0]
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'con_declare_list':
                    con_declare_list(c, k, obj)


def con_declare(tree, root, obj, str_d):
    child = tree[root]['children']
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'con_type':
                    con_type(c, k, obj)
                elif k == 'con_declare_list':
                    con_declare_list(c, k, obj, str_d)
                else:
                    con_declare(c, k, obj)


def fun_type(tree, root, obj):
    typ = tree[root]['children'][0]
    obj[2] = typ


def fun_declare_fpar(tree, root, obj, par):
    child = tree[root]['children']
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'var_type':
                    item = c[k]['children'][0]
                    par.append(item)
                else:
                    fun_declare_fpar(c, k, obj, par)


def fun_declare(tree, root, obj):

    child = tree[root]['children']
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'fun_type':
                    fun_type(c, k, obj)
                elif k == 'fun_declare_fpar':
                    par = []
                    fun_declare_fpar(c, k, obj, par)
                    obj.append(str(len(par)))
                    for i in par:
                        obj.append(i)
                else:
                    fun_declare(c, k, obj)


def assign_expression(tree, root, node, name):
    child = tree[root]['children'][::-1]
    flag = 0
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'arg_exp':

                    if len(c[k]['children']) == 1:
                        flag = 1
                        v_name = f'T{v_tc[0]}'
                        assign_expression(c, k, node, v_name)
                    else:
                        v_name = f'T{v_tc[0]}'
                        v_tc[0] += 1
                        if not node[2] and node[3]:
                            node[2] = v_name
                        elif not node[1] and node[3]:
                            node[1] = v_name
                        node = ['', '', '', v_name]
                        assign_expression(c, k, node, v_name)
                        if flag == 0:
                            inter_c.append(node[:])

                    if not has_item(res, 'V', v_name):
                        if node[0] and node[1] and node[2]:
                            # 添加临时变量到符号表
                            n1 = node[1]
                            n2 = node[2]
                            if not n1.isdigit():
                                n1 = int(search_symbol(res, 'V', node[1]))
                            if not n2.isdigit():
                                n2 = int(search_symbol(res, 'V', node[2]))
                            n1 = int(n1)
                            n2 = int(n2)
                            if node[0] == '+':
                                t = n1 + n2
                            elif node[0] == '-':
                                t = n1 - n2
                            elif node[0] == '*':
                                t = n1 * n2
                            elif node[0] == '/':
                                t = n2 / n1
                            res.append([index[0], 'V', 'int', v_name, t, ''])
                            index[0] += 1
                elif k == "arg_exp'":
                    if len(c[k]['children'])>=3:
                        v_name = f'T{v_tc[0]}'
                        v_tc[0] += 1
                        if not node[2]:
                            node[2] = v_name
                        elif not node[1]:
                            node[1] = v_name
                        node[0] = c[k]['children'][0]
                        node1 = ['', '', '', v_name]
                        assign_expression(c, k, node1, v_name)
                        inter_c.append(node1[:])

                        if not has_item(res, 'V', v_name):
                            if node1[0] and node1[1] and node1[2]:
                                # 添加临时变量到符号表
                                n1 = node1[1]
                                n2 = node1[2]
                                if not n1.isdigit():
                                    n1 = int(search_symbol(res, 'V', node1[1]))
                                if not n2.isdigit():
                                    n2 = int(search_symbol(res, 'V', node1[2]))
                                n1 = int(n1)
                                n2 = int(n2)

                                if node1[0] == '+':
                                    t = n1 + n2
                                elif node1[0] == '-':
                                    t = n1 - n2
                                elif node1[0] == '*':
                                    t = n1 * n2
                                elif node1[0] == '/':
                                    t = n2 / n1
                                res.append([index[0], 'V', 'int', v_name, t, ''])
                                index[0] += 1

                    else:
                        assign_expression(c, k, node, name)

                elif k == 'item':
                    if len(c[k]['children']) >= 2:
                        v_name = f'T{v_tc[0]}'
                        v_tc[0] += 1
                        if v_name == node[3]:
                            node = ['', '', '', v_name]
                            assign_expression(c, k, node, v_name)
                            inter_c.append(node[:])
                            if not has_item(res, 'V', v_name):
                                if not node[0] and (c in ['+', '-', '*', '/']):
                                    node[0] = c
                                elif not node[1]:
                                    node[1] = c
                                elif not node[2]:
                                    node[2] = c

                                if node[0] and node[1] and node[2]:
                                    # 添加临时变量到符号表
                                    n1 = node[1]
                                    n2 = node[2]
                                    if not n1.isdigit():
                                        n1 = int(search_symbol(res, 'V', node[1]))
                                    if not n2.isdigit():
                                        n2 = int(search_symbol(res, 'V', node[2]))
                                    n1 = int(n1)
                                    n2 = int(n2)

                                    if node[0] == '+':
                                        t = n1 + n2
                                    elif node[0] == '-':
                                        t = n1 - n2
                                    elif node[0] == '*':
                                        t = n1 * n2
                                    elif node[0] == '/':
                                        t = n2 / n1
                                    res.append([index[0], 'V', 'int', name, t, ''])
                                    index[0] += 1
                        else:
                            if not node[2]:
                                node[2] = v_name
                            elif not node[1]:
                                node[1] = v_name
                            node1 = ['', '', '', v_name]
                            assign_expression(c, k, node1, v_name)
                            inter_c.append(node1[:])
                            if not has_item(res, 'V', v_name):
                                if not node1[0] and (c in ['+', '-', '*', '/']):
                                    node1[0] = c
                                elif not node1[1]:
                                    node1[1] = c
                                elif not node1[2]:
                                    node1[2] = c

                                if node1[0] and node1[1] and node1[2]:
                                    # 添加临时变量到符号表
                                    n1 = node1[1]
                                    n2 = node1[2]
                                    if not n1.isdigit():
                                        n1 = int(search_symbol(res, 'V', node1[1]))
                                    if not n2.isdigit():
                                        n2 = int(search_symbol(res, 'V', node1[2]))
                                    n1 = int(n1)
                                    n2 = int(n2)

                                    if node1[0] == '+':
                                        t = n1 + n2
                                    elif node1[0] == '-':
                                        t = n1 - n2
                                    elif node1[0] == '*':
                                        t = n1 * n2
                                    elif node1[0] == '/':
                                        t = n2 / n1
                                    res.append([index[0], 'V', 'int', name, t, ''])
                                    index[0] += 1
                    else:
                        assign_expression(c, k, node, name)

                else:
                    assign_expression(c, k, node, name)
        else:
            if node[0] and (c in ['+', '-', '*', '/']):
                continue
            elif c == '=':
                if flag != 1:
                    node = ['', '', '', '']
                    node[0] = '='
                    node[2] = v_name
                    node[3] = child[-1]
                else:
                    node[0] = '='
                    node[3] = child[-1]
                inter_c.append(node[:])
                if node[1].isdigit():
                    t = int(node[1])
                elif node[2].isdigit():
                    t = int(node[2])
                elif node[1] and not node[1].isdigit():
                    t = int(search_symbol(res, 'V', node[1]))
                elif node[2] and not node[2].isdigit():
                    t = int(search_symbol(res, 'V', node[2]))
                update_symbol(res, 'V', node[3], t)

                node[0] = ''
                node[1] = ''
                node[2] = ''
                node[3] = ''
                break
            elif not node[0] and (c in ['+', '-', '*', '/']):
                node[0] = c
            elif not node[1]:
                node[1] = c
            elif not node[2]:
                node[2] = c
            if node[0] and node[1] and node[2]:
                # 添加临时变量到符号表
                n1 = node[1]
                n2 = node[2]
                if not n1.isdigit():
                    n1 = int(search_symbol(res, 'V', node[1]))
                if not n2.isdigit():
                    n2 = int(search_symbol(res, 'V', node[2]))
                n1 = int(n1)
                n2 = int(n2)

                if node[0] == '+':
                    t = n1 + n2
                elif node[0] == '-':
                    t = n1 - n2
                elif node[0] == '*':
                    t = n1 * n2
                elif node[0] == '/':
                    t = n2 / n1
                res.append([index[0], 'V', 'int', name, t, ''])
                index[0] += 1



depth = [0]
def create_sign_table(tree, root, str_d=''):
    child = tree[root]['children']
    for c in child:
        if isinstance(c, dict):
            for k, _ in c.items():
                if k == 'global_var_declare':
                    t = c[k]['children'][0]
                    s = c[k]['children'][1]
                    obj = [index[0], 'V', t, s, '', 0]
                    global_var_declare(c, k, obj)
                    if visit_node(obj):
                        res.append(obj[:])
                        index[0] += 1
                elif k == 'fun_declare':
                    s = c[k]['children'][1]
                    obj = [index[0], 'F', '', s]
                    fun_declare(c, k, obj)
                    if visit_node(obj):
                        res.append(obj[:])
                        index[0] += 1
                elif k == 'var_declare':
                    obj = [index[0], 'V', '', '', '', 0]
                    var_declare(c, k, obj, str_d)
                    # print(str_d)
                elif k == 'con_declare':
                    obj = [index[0], 'C', '', '', '', 0]
                    con_declare(c, k, obj, str_d)
                    # print(str_d)
                elif k == 'complex_statement' or k == 'cir_complex_statement':
                    depth[0] += 1
                    create_sign_table(c, k, str_d+str(depth[0]) + '/')
                elif k == 'assign_expression':
                    node = ['', '', '', '']
                    assign_expression(c, k, node, '')
                else:
                    create_sign_table(c, k, str_d)



create_sign_table(d, 'program')
res = merge(res)
print(res)
for i in res:
    print(i)

print(inter_c)