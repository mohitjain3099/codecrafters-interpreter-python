import sys
import re
from enum import Enum
exit_code: int = 0
class TOKEN_TYPE(Enum):
    NONE = -2
    EOF = -1
    STRING = 0
    NUMBER = 1
    IDENTIFIER = 2
    LEFT_PAREN = 3
    RIGHT_PAREN = 4
    LEFT_BRACE = 5
    RIGHT_BRACE = 6
    COMMA = 7
    DOT = 8
    MINUS = 9
    PLUS = 10
    SEMICOLON = 11
    STAR = 12
    SLASH = 13
    EQUAL_EQUAL = 14
    EQUAL = 15
    BANG_EQUAL = 16
    BANG = 17
    LESS_EQUAL = 18
    LESS = 19
    GREATER_EQUAL = 20
    GREATER = 21
    AND = 22
    OR = 23
    IF = 24
    ELSE = 25
    FOR = 26
    WHILE = 27
    TRUE = 28
    FALSE = 29
    CLASS = 30
    SUPER = 31
    THIS = 32
    VAR = 33
    FUN = 34
    RETURN = 35
    PRINT = 36
    NIL = 37
    def __str__(self):
        return self.name
class Token:
    def __init__(self, type: TOKEN_TYPE, name: str, value):
        self.type = type
        self.name = name
        self.value = value
    def __str__(self):
        return f"{str(self.type)} {self.name} {self.value}"
    def __repr__(self):
        return str(self)