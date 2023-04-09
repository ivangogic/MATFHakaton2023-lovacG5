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


def get_all_states(json1):
    eval_expr(json1)
    return all_states


def get_next_state(all_states1, curr_state_cnt):
    if curr_state_cnt < len(all_states1):
        curr_state = all_states1[curr_state_cnt]
        return curr_state
    else:
        print("Nema vise stanja")


def get_open_memory():
    return

