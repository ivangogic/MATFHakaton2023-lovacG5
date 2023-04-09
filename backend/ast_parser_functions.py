import json
# from pycparser.c_ast import Node, FileAST
from backend.pycparser.c_ast import Node

def initialize():
    global main_compound
    main_compound = None


def ast_dfs(node: Node):
    global main_compound
    instruction = node.to_json()
    if instruction and type(instruction) == list:
        main_compound = json.dumps(instruction, indent=2)
        return
    try:
        for _, child in node.children():
            ast_dfs(child)
    except Exception as e:
        pass
