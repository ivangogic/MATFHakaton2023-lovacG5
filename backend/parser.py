memory = {}
names = {}


def eval_unaryop(json):
    operation = json['operation']
    operand = json['operand']
    operand_type = operand['class']

    if operation == '&':
        if operand_type == 'variable':
            return names[operand['name']][0]
        else:
            return -1
    elif operation == '*':
        if operand_type == 'binary_op':
            number = eval_binaryop(operand)
        elif operand_type == 'unary_op':
            number = eval_unaryop(operand)
        elif operand_type == 'variable':
            number = names[operand['name']][0]
        elif operand_type == 'const':
            number = operand['value']
        else:
            return -1

        return memory[number] if number in memory else -1


def eval_binaryop(eval_dict : dict):
    operand_1 = eval_dict['operand1']
    operand_2 = eval_dict['operand2']

    op_code = eval_dict['operation']

    evaluated_operand_1 = eval(operand_1)
    evaluated_operand_2 = eval(operand_2)

    if op_code == '+':
        return evaluated_operand_1 + evaluated_operand_2
    elif op_code == '-':
        return evaluated_operand_1 - evaluated_operand_2
    elif op_code == '*':
        return evaluated_operand_1 * evaluated_operand_2
    elif op_code == '/':
        return evaluated_operand_1 / evaluated_operand_2
    else:
        raise Exception("eval_binaryop : not supported operation")


def eval_const(eval_dict : dict):
    value = eval_dict['value']
    type = eval_dict['type']

    return value


def eval_assign(instr):
    if instr['class'] == 'assign':
        left = instr['left']

        right = eval(instr['right'])

        if left['class'] == 'variable':
            var_name = instr['name']
            names[var_name][0] = right

        elif left['class'] == 'unary_op':
            memory_addr = eval_unaryop(left)
            if memory_addr in memory:
                memory[memory_addr] = right
            else:
                return -1