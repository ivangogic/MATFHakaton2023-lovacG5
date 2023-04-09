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
    final_states = []
    states.append([0,0,0,-1])
    print(*states,sep='\n')
    for i in range(len(states)-1):
        ind1 = states[len(states)-1-i][3]
        ind2 = states[len(states)-1-(i+1)][3]
        if ind1!=ind2:
            final_states.append(states[i])
    # final_states.reverse()
    print(*final_states,sep='\n')
    return final_states
