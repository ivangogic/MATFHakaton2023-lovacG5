
from __future__ import print_function

import json
import sys

sys.path.extend(['.', '..'])

from backend.pycparser import c_parser
from backend.pycparser.c_ast import Node, FileAST


text = r"""
int main() {
    int *ptr=malloc(4);  
    int a=560;  
    ptr=&a;  
    free(ptr);  
}
"""



parser = c_parser.CParser()
ast: FileAST = parser.parse(text, filename='<none>')

ast.show(showcoord=True)

import ast_parser_functions

ast_parser_functions.initialize()
ast_parser_functions.ast_dfs(ast)

code_json = json.loads(ast_parser_functions.main_compound)

from ast_parser import *

evaluate_expression(code_json)

print('Memory')
print(memory)

print('Names')
print(names)

