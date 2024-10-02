from .token import Token, TOKEN_TYPE
import sys
class Lexer:
    def __init__(self, program: str):
        self.program: str = program
        self.size: int = len(self.program)
        self.i: int = 0
        if self.size >= 1:
            self.c: str = self.program[self.i]
        self.line: int = 1
    def advance(self):
        self.i += 1
        if self.i < self.size:
            self.c = self.program[self.i]
    def advance_with(self, token: Token) -> Token:
        self.advance()
        return token
    def skip_whitespace(self):
        while self.i < self.size and self.c.isspace():
            match self.c:
                case self.c if self.c in [" ", "\r", "\t"]:
                    self.advance()
                case "\n":
                    self.advance()
                    self.line += 1
    def peek(self) -> Token:
        i = self.i
        c = self.c
        self.advance()
        next: Token
        self.skip_whitespace()
        match self.c:
            case self.c if self.i >= self.size:
                next = Token(TOKEN_TYPE.EOF, "", "null")
            case "(":
                next = self.advance_with(Token(TOKEN_TYPE.LEFT_PAREN, "(", "null"))
            case ")":
                next = self.advance_with(Token(TOKEN_TYPE.RIGHT_PAREN, ")", "null"))
            case "{":
                next = self.advance_with(Token(TOKEN_TYPE.LEFT_BRACE, "{", "null"))
            case "}":
                next = self.advance_with(Token(TOKEN_TYPE.RIGHT_BRACE, "}", "null"))
            case ",":
                next = self.advance_with(Token(TOKEN_TYPE.COMMA, ",", "null"))
            case ".":
                next = self.advance_with(Token(TOKEN_TYPE.DOT, ".", "null"))
            case "-":
                next = self.advance_with(Token(TOKEN_TYPE.MINUS, "-", "null"))
            case "+":
                next = self.advance_with(Token(TOKEN_TYPE.PLUS, "+", "null"))
            case ";":
                next = self.advance_with(Token(TOKEN_TYPE.SEMICOLON, ";", "null"))
            case "*":
                next = self.advance_with(Token(TOKEN_TYPE.STAR, "*", "null"))
            case "/":
                next = self.advance_with(Token(TOKEN_TYPE.SLASH, "/", "null"))
            case "=":
                next = self.advance_with(Token(TOKEN_TYPE.EQUAL, "=", "null"))
            case "!":
                next = self.advance_with(Token(TOKEN_TYPE.BANG, "!", "null"))
            case "<":
                next = self.advance_with(Token(TOKEN_TYPE.LESS, "<", "null"))
            case ">":
                next = self.advance_with(Token(TOKEN_TYPE.GREATER, ">", "null"))
            case '"':
                next = self.next_string()
            case "_":
                next = self.next_id()
            case _:
                if self.c.isalpha():
                    next = self.next_id()
                if self.c.isdigit():
                    next = self.next_number()
                else:
                    next = self.advance_with(Token(TOKEN_TYPE.NONE, "", ""))
        self.i = i
        self.c = c
        return next
    def next_id(self) -> Token:
        i = ""
        while self.i < self.size and (self.c.isalnum() or self.c == "_"):
            i += self.c
            self.advance()
        match i:
            case "and":
                return Token(TOKEN_TYPE.AND, i, "null")
            case "or":
                return Token(TOKEN_TYPE.OR, i, "null")
            case "if":
                return Token(TOKEN_TYPE.IF, i, "null")
            case "else":
                return Token(TOKEN_TYPE.ELSE, i, "null")
            case "for":
                return Token(TOKEN_TYPE.FOR, i, "null")
            case "while":
                return Token(TOKEN_TYPE.WHILE, i, "null")
            case "true":
                return Token(TOKEN_TYPE.TRUE, i, "null")
            case "false":
                return Token(TOKEN_TYPE.FALSE, i, "null")
            case "class":
                return Token(TOKEN_TYPE.CLASS, i, "null")
            case "super":
                return Token(TOKEN_TYPE.SUPER, i, "null")
            case "this":
                return Token(TOKEN_TYPE.THIS, i, "null")
            case "var":
                return Token(TOKEN_TYPE.VAR, i, "null")
            case "fun":
                return Token(TOKEN_TYPE.FUN, i, "null")
            case "return":
                return Token(TOKEN_TYPE.RETURN, i, "null")
            case "print":
                return Token(TOKEN_TYPE.PRINT, i, "null")
            case "nil":
                return Token(TOKEN_TYPE.NIL, i, "null")
        return Token(TOKEN_TYPE.IDENTIFIER, i, "null")
    def next_string(self) -> Token:
        global exit_code
        s = ""
        self.advance()
        while self.c != '"':
            s += self.c
            self.advance()
            if self.i >= self.size:
                print(
                    f"[line {self.line}] Error: Unterminated string.", file=sys.stderr
                )
                exit_code = 65
                return self.advance_with(Token(TOKEN_TYPE.NONE, "", ""))
        return self.advance_with(Token(TOKEN_TYPE.STRING, f'"{s}"', s))
    def next_number(self) -> Token:
        dot: bool = False
        n: str = ""
        while self.i < self.size:
            if self.c == ".":
                next: Token = self.peek()
                if next.type != TOKEN_TYPE.NUMBER or dot:
                    break
                dot = True
            elif not self.c.isdigit():
                break
            n += self.c
            self.advance()
        value: float = float(n)
        return Token(TOKEN_TYPE.NUMBER, n, value)
    def next_token(self) -> Token:
        self.skip_whitespace()
        if self.i >= self.size:
            self.advance()
            return Token(TOKEN_TYPE.EOF, "", "null")
        global exit_code
        match self.c:
            case "(":
                return self.advance_with(Token(TOKEN_TYPE.LEFT_PAREN, "(", "null"))
            case ")":
                return self.advance_with(Token(TOKEN_TYPE.RIGHT_PAREN, ")", "null"))
            case "{":
                return self.advance_with(Token(TOKEN_TYPE.LEFT_BRACE, "{", "null"))
            case "}":
                return self.advance_with(Token(TOKEN_TYPE.RIGHT_BRACE, "}", "null"))
            case ",":
                return self.advance_with(Token(TOKEN_TYPE.COMMA, ",", "null"))
            case ".":
                return self.advance_with(Token(TOKEN_TYPE.DOT, ".", "null"))
            case "-":
                return self.advance_with(Token(TOKEN_TYPE.MINUS, "-", "null"))
            case "+":
                return self.advance_with(Token(TOKEN_TYPE.PLUS, "+", "null"))
            case ";":
                return self.advance_with(Token(TOKEN_TYPE.SEMICOLON, ";", "null"))
            case "*":
                return self.advance_with(Token(TOKEN_TYPE.STAR, "*", "null"))
            case "/":
                if self.peek().type == TOKEN_TYPE.SLASH:
                    while self.i < self.size and self.c != "\n":
                        self.advance()
                    return Token(TOKEN_TYPE.NONE, "", "")
                else:
                    return self.advance_with(Token(TOKEN_TYPE.SLASH, "/", "null"))
            case "=":
                if self.peek().type == TOKEN_TYPE.EQUAL:
                    self.advance()
                    return self.advance_with(
                        Token(TOKEN_TYPE.EQUAL_EQUAL, "==", "null")
                    )
                else:
                    return self.advance_with(Token(TOKEN_TYPE.EQUAL, "=", "null"))
            case "!":
                if self.peek().type == TOKEN_TYPE.EQUAL:
                    self.advance()
                    return self.advance_with(Token(TOKEN_TYPE.BANG_EQUAL, "!=", "null"))
                else:
                    return self.advance_with(Token(TOKEN_TYPE.BANG, "!", "null"))
            case "<":
                if self.peek().type == TOKEN_TYPE.EQUAL:
                    self.advance()
                    return self.advance_with(Token(TOKEN_TYPE.LESS_EQUAL, "<=", "null"))
                else:
                    return self.advance_with(Token(TOKEN_TYPE.LESS, "<", "null"))
            case ">":
                if self.peek().type == TOKEN_TYPE.EQUAL:
                    self.advance()
                    return self.advance_with(
                        Token(TOKEN_TYPE.GREATER_EQUAL, ">=", "null")
                    )
                else:
                    return self.advance_with(Token(TOKEN_TYPE.GREATER, ">", "null"))
            case '"':
                return self.next_string()
            case _:
                if self.c.isalpha() or self.c == "_":
                    return self.next_id()
                if self.c.isdigit():
                    return self.next_number()
                print(
                    f"[line {self.line}] Error: Unexpected character: {self.c}",
                    file=sys.stderr,
                )
                exit_code = 65
                return self.advance_with(Token(TOKEN_TYPE.NONE, "", ""))