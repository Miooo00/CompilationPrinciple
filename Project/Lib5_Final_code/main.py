import json
from Project.Lib4_Semantic_Analyse.Tables import *
from Project.Lib4_Semantic_Analyse.main import *

path_code = '../Lib5_Final_code/Code.json'
path_format_code = '../Lib5_Final_code/out.asm'
with open(path_code, 'r', encoding='utf-8') as fp:
    mapping = json.load(fp)
with open(path_format_code, 'r', encoding='utf-8') as fp:
    out_content = fp.read()




def get_var(var_table) -> str:
    declare_vars = ''
    for item in var_table.table:
        if item.val.isdigit():
            declare_vars += '\t' + '_' + item.name + ' ' + 'dw' + ' ' + item.val + '\n'
        else:
            declare_vars += '\t' + '_' + item.name + ' ' + 'dw' + ' ' + '0' + '\n'
    return declare_vars


def get_code(op_table, var_table, fun_table) -> str:
    code = ''
    index = 1
    the_format = '_{}:'
    var = get_var(var_table)
    for op in op_table.list:
        if op[0] == '+':
            per_code = the_format.format(index) + '\n'
            digit_fir = op[1]
            digit_sec = op[2]
            digit_thr = op[3]
            if not digit_fir.isdigit():
                digit_fir = '_' + digit_fir
            if not digit_sec.isdigit():
                digit_sec = '_' + digit_sec
            if not digit_thr.isdigit():
                digit_thr = '_' + digit_thr
            per_code += mapping[op[0]].format(A=digit_fir, B=digit_sec, T=digit_thr) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '-':
            per_code = the_format.format(index) + '\n'
            digit_fir = op[1]
            digit_sec = op[2]
            digit_thr = op[3]
            if not digit_fir.isdigit():
                digit_fir = '_' + digit_fir
            if not digit_sec.isdigit():
                digit_sec = '_' + digit_sec
            if not digit_thr.isdigit():
                digit_thr = '_' + digit_thr
            per_code += mapping[op[0]].format(A=digit_fir, B=digit_sec, T=digit_thr) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '*':
            per_code = the_format.format(index) + '\n'
            digit_fir = op[1]
            digit_sec = op[2]
            digit_thr = op[3]
            if not digit_fir.isdigit():
                digit_fir = '_' + digit_fir
            if not digit_sec.isdigit():
                digit_sec = '_' + digit_sec
            if not digit_thr.isdigit():
                digit_thr = '_' + digit_thr
            per_code += mapping[op[0]].format(A=digit_fir, B=digit_sec, T=digit_thr) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '/':
            per_code = the_format.format(index) + '\n'
            digit_fir = op[1]
            digit_sec = op[2]
            digit_thr = op[3]
            if not digit_fir.isdigit():
                digit_fir = '_' + digit_fir
            if not digit_sec.isdigit():
                digit_sec = '_' + digit_sec
            if not digit_thr.isdigit():
                digit_thr = '_' + digit_thr
            per_code += mapping[op[0]].format(A=digit_fir, B=digit_sec, T=digit_thr) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '%':
            per_code = the_format.format(index) + '\n'
            digit_fir = op[1]
            digit_sec = op[2]
            digit_thr = op[3]
            if not digit_fir.isdigit():
                digit_fir = '_' + digit_fir
            if not digit_sec.isdigit():
                digit_sec = '_' + digit_sec
            if not digit_thr.isdigit():
                digit_thr = '_' + digit_thr
            per_code += mapping[op[0]].format(A=digit_fir, B=digit_sec, T=digit_thr) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '=':
            per_code = the_format.format(index) + '\n'
            digit_sec = op[2]
            if digit_sec != 'AX' and not digit_sec.isdigit():
                digit_sec = '_' + digit_sec
            digit_thr = op[3]
            if not digit_thr.isdigit():
                digit_thr = '_' + digit_thr
            per_code += mapping[op[0]].format(B=digit_sec, T=digit_thr) + '\n'
            print(per_code)
            index += 1
        elif op[0] == 'j':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(P1='_'+str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == 'jnz':
            per_code = the_format.format(index) + '\n'
            digit_fir = op[1]
            if not digit_fir.isdigit():
                digit_fir = '_' + digit_fir
            per_code += mapping[op[0]].format(A=digit_fir, P1='_'+str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == 'para':
            per_code = the_format.format(index) + '\n'
            digit_fir = op[1]
            if not digit_fir.isdigit():
                digit_fir = '_' + digit_fir
            per_code += mapping[op[0]].format(A=digit_fir) + '\n'
            print(per_code)
            index += 1
        elif op[0] == 'call':
            per_code = the_format.format(index) + '\n'
            per_code += mapping[op[0]].format(A='_' + op[1]) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '>':
            per_code = the_format.format(index) + '\n'
            digit_fir = op[1]
            digit_sec = op[2]
            if not digit_fir.isdigit():
                digit_fir = '_' + digit_fir
            if not digit_sec.isdigit():
                digit_sec = '_' + digit_sec
            per_code += mapping[op[0]].format(A=digit_fir, B=digit_sec, P='_' + str(index+1), P1='_' + str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '>=':
            per_code = the_format.format(index) + '\n'
            digit_fir = op[1]
            digit_sec = op[2]
            if not digit_fir.isdigit():
                digit_fir = '_' + digit_fir
            if not digit_sec.isdigit():
                digit_sec = '_' + digit_sec
            per_code += mapping[op[0]].format(A=digit_fir, B=digit_sec, P='_' + str(index+1), P1='_' + str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '<':
            per_code = the_format.format(index) + '\n'
            digit_fir = op[1]
            digit_sec = op[2]
            if not digit_fir.isdigit():
                digit_fir = '_' + digit_fir
            if not digit_sec.isdigit():
                digit_sec = '_' + digit_sec
            per_code += mapping[op[0]].format(A=digit_fir, B=digit_sec, P='_' + str(index+1), P1='_' + str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '<=':
            per_code = the_format.format(index) + '\n'
            digit_fir = op[1]
            digit_sec = op[2]
            if not digit_fir.isdigit():
                digit_fir = '_' + digit_fir
            if not digit_sec.isdigit():
                digit_sec = '_' + digit_sec
            per_code += mapping[op[0]].format(A=digit_fir, B=digit_sec, P='_' + str(index+1), P1='_' + str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == '==':
            per_code = the_format.format(index) + '\n'
            digit_fir = op[1]
            digit_sec = op[2]
            if not digit_fir.isdigit():
                digit_fir = '_' + digit_fir
            if not digit_sec.isdigit():
                digit_sec = '_' + digit_sec
            per_code += mapping[op[0]].format(A=digit_fir, B=digit_sec, P='_' + str(index+1), P1='_' + str(op[3])) + '\n'
            print(per_code)
            index += 1
        elif op[0] == 'ret':
            per_code = the_format.format(index) + '\n'
            if op[3] != '':
                digit = op[3]
                if not digit.isdigit():
                    digit = '_' + digit
                per_code += mapping[op[0]].format(A=f'MOV AX,{digit}') + '\n'
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
    code = out_content.format(var=var, code=code)
    return code



# content = read_file('../Lib3_Grammer/Token/target.reg')
# const_table, var_table, fun_table, op_table, errors = entry(content, '../Lib3_Grammer/test1')
# var = get_var(var_table)
# code = get_code(op_table, var_table, fun_table)
# print(code)
# with open('out.asm', 'r', encoding='utf-8') as fp:
#     content = fp.read().format(var=var, code=code)
#
# with open('test2.asm', 'w', encoding='utf-8') as fp:
#     fp.write(content)