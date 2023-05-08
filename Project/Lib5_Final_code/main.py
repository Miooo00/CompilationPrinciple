import json
from Project.Lib4_Semantic_Analyse.Tables import *
from Project.Lib4_Semantic_Analyse.main import *

with open('Code.json', 'r', encoding='utf-8') as fp:
    mapping = json.load(fp)
# print(content['+'].format(A='1', B='2', T='3'))
#



def get_var(var_table) -> str:
    declare_vars = ''
    for item in var_table.table:
        if item.val.isdigit():
            declare_vars += '\t' + item.name + ' ' + 'dw' + ' ' + item.val + '\n'
        else:
            declare_vars += '\t' + item.name + ' ' + 'dw' + ' ' + '0' + '\n'
    return declare_vars


def get_code(op_table, fun_table) -> str:
    code = ''
    index = 1
    the_format = '_{}:'
    for op in op_table.list:
        if op[0] == '+':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A=op[1], B=op[2], T=op[3]) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '-':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A=op[1], B=op[2], T=op[3]) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '*':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A=op[1], B=op[2], T=op[3]) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '/':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A=op[1], B=op[2], T=op[3]) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '%':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A=op[1], B=op[2], T=op[3]) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '=':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(B=op[2], T=op[3]) + '\n'
            print(per_code)
            index += 1
        elif op[0] == 'j':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(P1='_'+str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == 'jnz':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A=op[1], P1='_'+str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == 'para':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A=op[1]) + '\n'
            print(per_code)
            index += 1
        elif op[0] == 'call':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A='_' + op[1]) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '>':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A=op[1], B=str(op[2]), P='_' + str(index+1), P1='_' + str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '>=':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A=op[1], B=str(op[2]), P='_' + str(index+1), P1='_' + str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '<':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A=op[1], B=str(op[2]), P='_' + str(index+1), P1='_' + str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '<=':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A=op[1], B=str(op[2]), P='_' + str(index+1), P1='_' + str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '==':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A=op[1], B=str(op[2]), P='_' + str(index+1), P1='_' + str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == 'ret':
            per_code = the_format.format(index) + '\n'
            if op[3] != '':
                per_code += mapping[op[0]].format(A=f'MOV AX,{op[3]}') + '\n'
            else:
                per_code += mapping[op[0]].format(A='') + '\n'
            print(per_code)
            index += 1
        elif op[0] and not op[1] and not op[2] and not op[3]:
            reg = ['SI', 'DI']
            par_len = fun_table.get(op[0]).parLen
            startPos = 4
            getVal = ''
            for c in range(par_len):
                if c >= len(reg):
                    c = 0
                getVal += f'\tMOV {reg[c]},[BP+{startPos}]\n'
                startPos += 2
            p = index
            callFun = ''

            while p < len(op_table.list):
                if (op_table.list[p][0] and not op_table.list[p][1] and not op_table.list[p][2] and not op_table.list[p][3]) and op_table.list[p][0] != 'ret':
                    break
                else:
                    callFun += f'\tcall _{p+1}\n'
                p = p + 1

            print(callFun)
            per_code = the_format.format(op[0]) + '\n'
            getVal += callFun
            per_code += mapping['fun'].format(EX=getVal) + '\n'
            print(per_code)
            index += 1
        else:
            per_code = the_format.format(index) + '\n'
            index += 1
        code += per_code
    print(code)
    return code


content = read_file('../Lib3_Grammer/Token/target.reg')
const_table, var_table, fun_table, op_table, errors = entry(content, '../Lib3_Grammer/test1')
var = get_var(var_table)
code = get_code(op_table, fun_table)

with open('out.asm', 'r', encoding='utf-8') as fp:
    content = fp.read().format(var=var, code=code)

with open('test2.asm', 'w', encoding='utf-8') as fp:
    fp.write(content)