memory = {}
names = {}
heap_memory = {}
stack_pos = 1000
stack_size = 1000
heap_pos = 2000
heap_size = 1000

def evaluate_expression(data):
    memory.clear()
    names.clear()

    return eval_expr(data)

def eval_expr(data):
    functions = {
        'assign': eval_assign,
        'declare': eval_declare,
        'unary_op': eval_unaryop,
        'binary_op': eval_binaryop,
        'const': eval_const,
        'variable': eval_variable,
        'while': eval_while,
        'if': eval_if,
        'malloc': eval_malloc,
        'free': eval_free
    }
    if type(data) == list:
        for instruction in data:
            eval_expr(instruction)
    else:
        return functions[data['class']](data)


def eval_unaryop(json, flag=False):
    # print('unary', json)
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
    elif op_code == '>':
        return 1 if evaluated_operand_1 > evaluated_operand_2 else 0
    elif op_code == '<':
        return 1 if evaluated_operand_1 < evaluated_operand_2 else 0
    elif op_code == '==':
        return 1 if evaluated_operand_1 == evaluated_operand_2 else 0
    elif op_code == '!=':
        return 1 if evaluated_operand_1 != evaluated_operand_2 else 0
    elif op_code == '>=':
        return 1 if evaluated_operand_1 >= evaluated_operand_2 else 0
    elif op_code == '<=':
        return 1 if evaluated_operand_1 <= evaluated_operand_2 else 0
    elif op_code == '&&':
        return 1 if evaluated_operand_1 != 0 and evaluated_operand_2 != 0 else 0
    elif op_code == '||':
        return 1 if evaluated_operand_1 != 0 or evaluated_operand_2 != 0 else 0
    else:
        raise Exception("eval_binary_op : not supported operation")


def eval_const(eval_dict: dict):
    value = eval_dict['value']
    type = eval_dict['type']

    return value


def eval_assign(instr):
    # ("assign", instr)
    if instr['class'] == 'assign':
        left = instr['left']

        right = eval_expr(instr['right'])
        # print("right", right)

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


def eval_declare(data):
    if data['class'] != 'declare':
        return -1

    if data['name'] in names.keys():
        return -1

    for i in range(stack_pos, stack_pos + stack_size):
        if i not in memory.keys():
            memory[i] = None
            if 'init' in data:
                memory[i] = eval_expr(data['init'])
            strelice = '*' in data['type']
            names[data['name']] = [i, strelice, data['type']]
            break


def eval_variable(data):
    return memory[ names[data['name']][0] ]


def eval_if(instr):
    cond = eval_expr(instr['cond'])
    print(cond)
    if cond == 1:
        print(instr)
        for data in instr['iftrue']:
            eval_expr(data)
    else:
        for data in instr['iffalse']:
            eval_expr(data)


def eval_while(instr):
    while eval_expr(instr['cond']):
        local_variables = []
        for data in instr['compound']:
            if data['class'] == 'declare':
                local_variables.append(data['name'])
            eval_expr(data)
        for local_variable in local_variables:
            memory.pop(names[local_variable][0])
            names.pop(local_variable)


def eval_malloc(instr):
    # print(instr)
    space = []
    n_instr = instr['n']
    n = eval_expr(n_instr)
    for i in range(heap_pos, heap_pos + heap_size):
        if i not in memory.keys():
            space.append(i)
            if len(space) == n:
                break
        else:
            space.clear()

    # print(space)
    if len(space) == n:
        for pos in space:
            memory[pos] = 0
        heap_memory[space[0]] = n
        return space[0]
    else:
        return -1


def eval_free(instr):
    print(instr)
    var_name = instr['name']
    var_addr = memory[names[var_name][0]]
    print(var_addr)
    print(memory)
    if var_addr in heap_memory.keys():
        n = heap_memory.get(var_addr)
        for i in range(var_addr, var_addr + n):
            memory.pop(i)
        heap_memory.pop(var_addr)
    else:
        return -1
