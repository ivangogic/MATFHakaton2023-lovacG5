# -----------------------------------------------------------------
# pycparser: explore_ast.py
#
# This example demonstrates how to "explore" the AST created by
# pycparser to understand its structure. The AST is a n-nary tree
# of nodes, each node having several children, each with a name.
# Just read the code, and let the comments guide you. The lines
# beginning with #~ can be uncommented to print out useful
# information from the AST.
# It helps to have the pycparser/_c_ast.cfg file in front of you.
#
# Eli Bendersky [https://eli.thegreenplace.net/]
# License: BSD
# -----------------------------------------------------------------
from __future__ import print_function

import json
import sys

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

from backend.pycparser import c_parser
from backend.pycparser.c_ast import Node, FileAST

# This is some C source to parse. Note that pycparser must begin
# at the top level of the C file, i.e. with either declarations
# or function definitions (this is called "external declarations"
# in C grammar lingo)
#
# Also, a C parser must have all the types declared in order to
# build the correct AST. It doesn't matter what they're declared
# to, so I've inserted the dummy typedef in the code to let the
# parser know Hash and Node are types. You don't need to do it
# when parsing real, correct C code.

# text = r"""
# int main() {
#     int a = 5;
#     int *b = &a;
#     *b  =7;
#     int c = *b;
#     int **d = &b;
#     **d = 9;
# }
# """

text = r"""
int main() {
    int a = 5; 
    if (a > 3) {
    
    }
    while (a>5) {
        a = a + 1;
    }
}
"""

# int **c = &b;
# int d = 3 * (2 + **c);

# Create the parser and ask to parse the text. parse() will throw
# a ParseError if there's an error in the code
#
parser = c_parser.CParser()
ast: FileAST = parser.parse(text, filename='<none>')

# Uncomment the following line to see the AST in a nice, human
# readable way. show() is the most useful tool in exploring ASTs
# created by pycparser. See the c_ast.py file for the options you
# can pass it.

ast.show(showcoord=True)

main_compound = None


def ast_dfs(node: Node):
    global main_compound
    # print(node)
    # print(node.__class__.__name__)
    instruction = node.to_json()
    if instruction and type(instruction) == list:
        main_compound = json.dumps(instruction, indent=2)
        return
    # if json_text:
    #     print(node.to_json())
    # else:
    #     print(node.__class__.__name__)
    try:
        for _, child in node.children():
            ast_dfs(child)
    except Exception as e:
        # print(node.children())
        print("### CRASH ###", e)
        pass



ast_dfs(ast)

print("#############")
print(main_compound)
print("#############")
print(ast)
print("#############")

main_compound = json.loads(main_compound)

from parser import *

eval_expr(main_compound)

print('Memory')
print(memory)

print('Names')
print(names)

