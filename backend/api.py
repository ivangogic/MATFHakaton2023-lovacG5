from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import Code, Memory, Names
import os, sys
import json
import uvicorn
# Now do your import

from pycparser import c_parser
from pycparser.c_ast import Node, FileAST
from ast_parser import *
import ast_parser_functions

app = FastAPI()
parser = None                                                                                               

@app.on_event('startup')
def init_data():
    print("init call")
    global parser 
    parser = c_parser.CParser()

@app.get("/get_data")
def get_memory(_text : str):
    text = _text

    ast_parser_functions.initialize()

    ast: FileAST =parser.parse(text, filename='<none>')

    ast_parser_functions.ast_dfs(ast)
    json_info = json.loads(ast_parser_functions.main_compound)

    evaluate_expression(json_info)

    response_data = {'memory': memory, 'names': names}

    response = JSONResponse(content=response_data)
    response.headers['Cache-Control'] = 'no-cache'
    
    return response

if __name__ == '__main__':
    uvicorn.run(f'api:app', host='localhost', port=8086)