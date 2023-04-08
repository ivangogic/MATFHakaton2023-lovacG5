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