memory = {}
names = {}


def eval_expr(data):
    # print(data)
    functions = {
        'assign': eval_assign,
        'declare': eval_declare,
        'unary_op': eval_unaryop,
        'binary_op': eval_binaryop,
        'const': eval_const,
        'variable': eval_variable
    }
    if type(data) == list:
        for instruction in data:
            eval_expr(instruction)
    else:
        return functions[data['class']](data)


def eval_unaryop(json, flag=False):
    print('unary', json)
    operation = json['operation']
    operand = json['operand']
    operand_type = operand['class']

    if operation == '&':
        if operand_type == 'variable':
            return names[operand['name']][0]
        else:
            return -1
    elif operation == '*':
        evaluated_expr =  eval_expr(operand)
        return memory[evaluated_expr] if not flag else evaluated_expr

def eval_binaryop(eval_dict: dict):
    operand_1 = eval_dict['operand1']
    operand_2 = eval_dict['operand2']

    op_code = eval_dict['operation']

    evaluated_operand_1 = eval_expr(operand_1)
    evaluated_operand_2 = eval_expr(operand_2)

    if op_code == '+':
        return evaluated_operand_1 + evaluated_operand_2
    elif op_code == '-':
        return evaluated_operand_1 - evaluated_operand_2
    elif op_code == '*':
        return evaluated_operand_1 * evaluated_operand_2
    elif op_code == '/':
        if type(evaluated_operand_1) == type(evaluated_operand_2) == int:
            return evaluated_operand_1 // evaluated_operand_2
        else:
            return evaluated_operand_1 / evaluated_operand_2
    else:
        raise Exception("eval_binary_op : not supported operation")


def eval_const(eval_dict: dict):
    value = eval_dict['value']
    type = eval_dict['type']

    return value


def eval_assign(instr):
    print("assign", instr)
    if instr['class'] == 'assign':
        left = instr['left']

        right = eval_expr(instr['right'])
        print("right", right)

        if left['class'] == 'variable':
            var_name = left['name']
            if '*' not in names[var_name][2]:
                right = eval(f"{names[var_name][2]}({right})")
            memory[names[var_name][0]] = right

        elif left['class'] == 'unary_op':
            memory_addr = eval_unaryop(left, True)
            if memory_addr in memory:
                memory[memory_addr] = right
            else:
                raise Exception("dzaras po memoriji dje nesmije", memory_addr)
                return -1


def eval_declare(data):
    if data['class'] != 'declare':
        return -1

    if data['name'] in names.keys():
        return -1

    for i in range(100,1000):
        if i not in memory.keys():
            memory[i] = None
            if 'init' in data:
                memory[i] = eval_expr(data['init'])
            strelice = '*' in data['type']
            names[data['name']] = [i, strelice, data['type']]
            break


def eval_variable(data):
    return memory[ names[data['name']][0] ]

