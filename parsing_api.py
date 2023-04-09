import json
from backend.pycparser import c_parser
from backend.pycparser.c_ast import Node, FileAST
from backend import ast_parser_functions
from backend.ast_parser import *


def get_json_from_textarea(text):
    parser = c_parser.CParser()
    # print(text)
    ast: FileAST = parser.parse(text, filename='<none>')

    ast_parser_functions.initialize()
    ast_parser_functions.ast_dfs(ast)

    code_json = json.loads(ast_parser_functions.main_compound)

    # print(code_json)
    return code_json


def get_all_states1(json1):
    eval_expr(json1)
    return all_states


def get_all_states(json1):
    eval_expr(json1)
    return get_final_states(all_states)


def get_final_states(states):
    states_index = []
    final_states = []

    for i in reversed(states):
        ind = i[3]
        if ind not in states_index:
            states_index.append(ind)
            final_states.append(i)
            print(i)
    #print(*reversed(final_states), sep='\n')
    return reversed(final_states)