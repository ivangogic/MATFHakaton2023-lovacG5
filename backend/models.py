from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Tuple

class Code(BaseModel):
    text : str

class Memory(BaseModel):
    memory : Dict[int, int]

class Names(BaseModel):
    names: Dict[str, Tuple[int, bool, str]]