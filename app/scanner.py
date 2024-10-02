from .lexer import Lexer
from .token import Token, TOKEN_TYPE
import sys

class Scanner:
    def __init__(self, source: str):
        self.lexer = Lexer(source)
        self.tokens = []
        self.errors = []

    def scan(self):
        while True:
            token = self.lexer.next_token()
            if token.type == TOKEN_TYPE.EOF:
                break
            self.tokens.append(token)

    def print_tokens(self):
        for token in self.tokens:
            print(token)

    def has_errors(self):
        return len(self.errors) > 0

    def print_errors(self):
        for error in self.errors:
            print(error, file=sys.stderr)