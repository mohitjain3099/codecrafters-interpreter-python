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
    def __init__(self, type: TOKEN_TYPE, name: str, value, line: int):
        self.type = type
        self.name = name
        self.value = value
        self.line = line
    def __str__(self):
        return f"{str(self.type)} {self.name} {self.value}"
    def __repr__(self):
        return str(self)
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
                next = Token(TOKEN_TYPE.EOF, "", "null", self.line)
            case "(":
                next = self.advance_with(
                    Token(TOKEN_TYPE.LEFT_PAREN, "(", "null", self.line)
                )
            case ")":
                next = self.advance_with(
                    Token(TOKEN_TYPE.RIGHT_PAREN, ")", "null", self.line)
                )
            case "{":
                next = self.advance_with(
                    Token(TOKEN_TYPE.LEFT_BRACE, "{", "null", self.line)
                )
            case "}":
                next = self.advance_with(
                    Token(TOKEN_TYPE.RIGHT_BRACE, "}", "null", self.line)
                )
            case ",":
                next = self.advance_with(
                    Token(TOKEN_TYPE.COMMA, ",", "null", self.line)
                )
            case ".":
                next = self.advance_with(Token(TOKEN_TYPE.DOT, ".", "null", self.line))
            case "-":
                next = self.advance_with(
                    Token(TOKEN_TYPE.MINUS, "-", "null", self.line)
                )
            case "+":
                next = self.advance_with(Token(TOKEN_TYPE.PLUS, "+", "null", self.line))
            case ";":
                next = self.advance_with(
                    Token(TOKEN_TYPE.SEMICOLON, ";", "null", self.line)
                )
            case "*":
                next = self.advance_with(Token(TOKEN_TYPE.STAR, "*", "null", self.line))
            case "/":
                next = self.advance_with(
                    Token(TOKEN_TYPE.SLASH, "/", "null", self.line)
                )
            case "=":
                next = self.advance_with(
                    Token(TOKEN_TYPE.EQUAL, "=", "null", self.line)
                )
            case "!":
                next = self.advance_with(Token(TOKEN_TYPE.BANG, "!", "null", self.line))
            case "<":
                next = self.advance_with(Token(TOKEN_TYPE.LESS, "<", "null", self.line))
            case ">":
                next = self.advance_with(
                    Token(TOKEN_TYPE.GREATER, ">", "null", self.line)
                )
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
                    next = self.advance_with(Token(TOKEN_TYPE.NONE, "", "", self.line))
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
                return Token(TOKEN_TYPE.AND, i, "null", self.line)
            case "or":
                return Token(TOKEN_TYPE.OR, i, "null", self.line)
            case "if":
                return Token(TOKEN_TYPE.IF, i, "null", self.line)
            case "else":
                return Token(TOKEN_TYPE.ELSE, i, "null", self.line)
            case "for":
                return Token(TOKEN_TYPE.FOR, i, "null", self.line)
            case "while":
                return Token(TOKEN_TYPE.WHILE, i, "null", self.line)
            case "true":
                return Token(TOKEN_TYPE.TRUE, i, "null", self.line)
            case "false":
                return Token(TOKEN_TYPE.FALSE, i, "null", self.line)
            case "class":
                return Token(TOKEN_TYPE.CLASS, i, "null", self.line)
            case "super":
                return Token(TOKEN_TYPE.SUPER, i, "null", self.line)
            case "this":
                return Token(TOKEN_TYPE.THIS, i, "null", self.line)
            case "var":
                return Token(TOKEN_TYPE.VAR, i, "null", self.line)
            case "fun":
                return Token(TOKEN_TYPE.FUN, i, "null", self.line)
            case "return":
                return Token(TOKEN_TYPE.RETURN, i, "null", self.line)
            case "print":
                return Token(TOKEN_TYPE.PRINT, i, "null", self.line)
            case "nil":
                return Token(TOKEN_TYPE.NIL, i, "null", self.line)
        return Token(TOKEN_TYPE.IDENTIFIER, i, "null", self.line)
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
                return self.advance_with(Token(TOKEN_TYPE.EOF, "", "null", self.line))
        return self.advance_with(Token(TOKEN_TYPE.STRING, f'"{s}"', s, self.line))
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
        return Token(TOKEN_TYPE.NUMBER, n, value, self.line)
    def next_token(self) -> Token:
        self.skip_whitespace()
        if self.i >= self.size:
            self.advance()
            return Token(TOKEN_TYPE.EOF, "", "null", self.line)
        global exit_code
        match self.c:
            case "(":
                return self.advance_with(
                    Token(TOKEN_TYPE.LEFT_PAREN, "(", "null", self.line)
                )
            case ")":
                return self.advance_with(
                    Token(TOKEN_TYPE.RIGHT_PAREN, ")", "null", self.line)
                )
            case "{":
                return self.advance_with(
                    Token(TOKEN_TYPE.LEFT_BRACE, "{", "null", self.line)
                )
            case "}":
                return self.advance_with(
                    Token(TOKEN_TYPE.RIGHT_BRACE, "}", "null", self.line)
                )
            case ",":
                return self.advance_with(
                    Token(TOKEN_TYPE.COMMA, ",", "null", self.line)
                )
            case ".":
                return self.advance_with(Token(TOKEN_TYPE.DOT, ".", "null", self.line))
            case "-":
                return self.advance_with(
                    Token(TOKEN_TYPE.MINUS, "-", "null", self.line)
                )
            case "+":
                return self.advance_with(Token(TOKEN_TYPE.PLUS, "+", "null", self.line))
            case ";":
                return self.advance_with(
                    Token(TOKEN_TYPE.SEMICOLON, ";", "null", self.line)
                )
            case "*":
                return self.advance_with(Token(TOKEN_TYPE.STAR, "*", "null", self.line))
            case "/":
                if self.peek().type == TOKEN_TYPE.SLASH:
                    while self.i < self.size and self.c != "\n":
                        self.advance()
                    return Token(TOKEN_TYPE.NONE, "", "", self.line)
                else:
                    return self.advance_with(
                        Token(TOKEN_TYPE.SLASH, "/", "null", self.line)
                    )
            case "=":
                if self.peek().type == TOKEN_TYPE.EQUAL:
                    self.advance()
                    return self.advance_with(
                        Token(TOKEN_TYPE.EQUAL_EQUAL, "==", "null", self.line)
                    )
                else:
                    return self.advance_with(
                        Token(TOKEN_TYPE.EQUAL, "=", "null", self.line)
                    )
            case "!":
                if self.peek().type == TOKEN_TYPE.EQUAL:
                    self.advance()
                    return self.advance_with(
                        Token(TOKEN_TYPE.BANG_EQUAL, "!=", "null", self.line)
                    )
                else:
                    return self.advance_with(
                        Token(TOKEN_TYPE.BANG, "!", "null", self.line)
                    )
            case "<":
                if self.peek().type == TOKEN_TYPE.EQUAL:
                    self.advance()
                    return self.advance_with(
                        Token(TOKEN_TYPE.LESS_EQUAL, "<=", "null", self.line)
                    )
                else:
                    return self.advance_with(
                        Token(TOKEN_TYPE.LESS, "<", "null", self.line)
                    )
            case ">":
                if self.peek().type == TOKEN_TYPE.EQUAL:
                    self.advance()
                    return self.advance_with(
                        Token(TOKEN_TYPE.GREATER_EQUAL, ">=", "null", self.line)
                    )
                else:
                    return self.advance_with(
                        Token(TOKEN_TYPE.GREATER, ">", "null", self.line)
                    )
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
                return self.advance_with(Token(TOKEN_TYPE.NONE, "", "", self.line))
def Binary(left, operator, right):
    if not right:
        global exit_code
        exit_code = 65
        return ""
    return f"({operator.name} {left} {right})"
def Grouping(expression):
    if not expression:
        global exit_code
        exit_code = 65
        return ""
    return f"(group {expression})"
def Literal(value):
    if value is None:
        return "nil"
    return str(value).lower()
def Unary(operator, right):
    return f"({operator.name} {right})"
class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.current = 0
        
    def parser(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.match(TOKEN_TYPE.PRINT):
            return self.print_statement()
        return self.expression_statement()

    def print_statement(self):
        if self.check(TOKEN_TYPE.SEMICOLON):
            self.consume(TOKEN_TYPE.SEMICOLON, "Expect ';' after value.")
            return {"type": "print", "value": None}
        value = self.expression()
        self.consume(TOKEN_TYPE.SEMICOLON, "Expect ';' after value.")
        return {"type": "print", "value": value}

    def expression_statement(self):
        expr = self.expression()
        self.consume(TOKEN_TYPE.SEMICOLON, "Expect ';' after expression.")
        return {"type": "expression", "expression": expr}
    def parse(self):
        return self.expression()
    def expression(self):
        return self.equality()
    def equality(self):
        expr = self.comparison()
        while self.match(TOKEN_TYPE.BANG_EQUAL, TOKEN_TYPE.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr
    def match(self, *types) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    def check(self, token_type) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == token_type
    def is_at_end(self) -> bool:
        return self.peek().type == TOKEN_TYPE.EOF
    def peek(self) -> Token:
        if self.current < len(self.tokens):
            return self.tokens[self.current]
    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    def previous(self) -> Token:
        return self.tokens[self.current - 1]
    def comparison(self):
        expr = self.term()
        while self.match(
            TOKEN_TYPE.GREATER,
            TOKEN_TYPE.GREATER_EQUAL,
            TOKEN_TYPE.LESS,
            TOKEN_TYPE.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr
    def term(self):
        expr = self.factor()
        while self.match(TOKEN_TYPE.MINUS, TOKEN_TYPE.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr
    def factor(self):
        expr = self.unary()
        while self.match(TOKEN_TYPE.SLASH, TOKEN_TYPE.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr
    def unary(self):
        if self.match(TOKEN_TYPE.BANG, TOKEN_TYPE.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()
    def primary(self):
        if self.match(TOKEN_TYPE.FALSE):
            return Literal(False)
        if self.match(TOKEN_TYPE.TRUE):
            return Literal(True)
        if self.match(TOKEN_TYPE.NIL):
            return Literal(None)
        if self.match(TOKEN_TYPE.PRINT):
            return Literal("print")
        if self.match(TOKEN_TYPE.NUMBER, TOKEN_TYPE.STRING):
            return Literal(self.previous().value)
        if self.match(TOKEN_TYPE.LEFT_PAREN):
            expr = self.expression()
            if not expr:
                return self.error(self.peek(), "Expect expression.")
            self.consume(TOKEN_TYPE.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        global exit_code
        exit_code = 65
        return self.error(self.peek(), "Expect expression.")
    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        global exit_code
        exit_code = 65
        print(message, file=sys.stderr)
        exit(exit_code)
    def error(self, token: Token, message: str):
        print(
            f"[line {token.line}] Error at '{token.name}': {message}", file=sys.stderr
        )
        return None

class Interpreter:
    def interpret(self, statements):
        for statement in statements:
            self.execute(statement)

    def execute(self, statement):
        global exit_code
        if statement["type"] == "print":
            if statement["value"] is None:
                exit_code = 65
                print("")
            else:
                value = self.evaluate(statement["value"])
                print(self.stringify(value))
        elif statement["type"] == "expression":
            self.evaluate(statement["expression"])

    def stringify(self, value):
        if value is None:
            return "nil"
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)
    
    def evaluate(self, expression: str):
        """Evaluate a given expression with nested subexpressions."""
        if isinstance(expression, (int, float)):
            return expression
        elif isinstance(expression, str):
            try:
                return float(expression)
            except ValueError:
                pass
            
            if expression.startswith("("):
                stack = []
                tokenexpression = expression.replace("(", " ( ").replace(")", " ) ").split()
                i = 0
                unary_or_binary = None
                while i < len(tokenexpression):
                    token = tokenexpression[i]                    
                    if token == "(":
                        i += 1
                        continue  # Skip the open parenthesis
                    elif token == ")":
                        # Pop two operands and one operator from the stack
                        right = stack.pop()
                        if not isinstance(right, bool):
                            if not self.is_integer(right):
                                try:
                                    right = float(right)
                                except:
                                    pass
                        left = stack.pop()
                        if not isinstance(left, bool):
                            if not self.is_integer(left):
                                try:
                                    left = float(left)
                                    operator = stack.pop()
                                    unary_or_binary = "binary"
                                except:
                                    if left in ["!", "-"]:
                                        unary_or_binary = "unary"
                                        operator = left
                                    else:
                                        unary_or_binary = "binary"
                                        operator = stack.pop()
                            else:
                                unary_or_binary = "binary"
                                operator = stack.pop()
                        else:
                            unary_or_binary = "binary"
                            operator = stack.pop()
                        if unary_or_binary == "unary":
                            stack.append(self.do_unary(operator, right))
                        elif unary_or_binary == "binary":
                            stack.append(self.do_operation(left, operator, right))
                        # Perform the operation and push the result back to the stack
                    elif token == "group":
                        i += 1
                        subexpression = []
                        depth = 1
                        while depth > 0:
                            subtoken = tokenexpression[i]
                            if subtoken == "(":
                                depth += 1
                            elif subtoken == ")":
                                depth -= 1
                            if depth > 0:
                                subexpression.append(subtoken)
                            i += 1
                        # Recursively evaluate the subexpression and push the result
                        subexpression_str = " ".join(subexpression)
                        stack.append(self.evaluate(f"{subexpression_str}"))
                        i -= 1
                    elif token in {"true", "false", "nil"}:
                        # Handle boolean literals
                        stack.append(True if token == "true" else False)
                    else:
                        stack.append(token)
                    i += 1
                
                if len(stack) != 1:
                    raise ValueError("Invalid expression, stack not fully reduced")
                
                return stack[0]
            else:
                return expression

    def do_operation(self, left, operator, right):
        """Perform basic arithmetic operations.""" 
        global exit_code
        if operator in ["+", "-", "*", "/"]:
            op_type= "arithmetic"
        else:
            op_type = "comparison"
        def handle_comparison(left, operator, right):
            global exit_code
            if operator == "==":
                return left == right
            elif operator == "!=":
                return left != right
            elif operator == "<":
                return left < right
            elif operator == ">":
                return left > right
            elif operator == "<=":
                return left <= right
            elif operator == ">=":
                return left >= right
            else:
                exit_code = 70
                return ""
        def handle_arithmetic(left, operator, right):
            global exit_code
            if operator == "+":
                return left + right
            elif operator == "-":
                return left - right
            elif operator == "*":
                return left * right
            elif operator == "/":
                if right == 0:
                    raise ZeroDivisionError("Division by zero is undefined")
                return left / right
            else:
                exit_code = 70
                return ""
        if isinstance(left, bool) and isinstance(right, bool):
            exit_code = 70
            return ""
        elif isinstance(left, (int,float)) and isinstance(right, bool):
            exit_code = 70
            return ""
        elif isinstance(left, bool) and isinstance(right, (int,float)):
            exit_code = 70
            return ""
        elif isinstance(left, str) and isinstance(right, str):
            if operator == "+":
                return left + right
            else:
                return handle_comparison(left, operator, right)
        elif isinstance(left, (int,float)) and isinstance(right, (int,float)):
            if op_type == "arithmetic":
                return handle_arithmetic(left, operator, right)
            elif op_type == "comparison":
                return handle_comparison(left, operator, right)
        elif type(left) != type(right):
            if operator == "==":
                return False
            elif operator == "!=":
                return True
            else:
                exit_code = 70
                return ""
        
        
        
        
    def do_unary(self, operator, right):
        """Perform unary operations."""
        global exit_code
        if isinstance(right, bool):
            if operator == "!":
                return not right
            else:
                exit_code = 70
                return ""
        if not isinstance(right, int) and not isinstance(right, float):
            exit_code = 70
            return ""
        if operator == "-":
            return -right
        elif operator == "!":
            return not right
        else:
            raise ValueError(f"Unknown unary operator: {operator}")
        
    def is_integer(self, value: str):
        try:
            int(value)
            return True
        except ValueError:
            return False
    def visit_literal(self, literal):
        return literal

    def visit_grouping(self, grouping):
        return self.evaluate(grouping[7:-1])  # Remove "(group " and ")"

    def visit_unary(self, unary):
        parts = unary[1:-1].split(maxsplit=1)
        operator, right = parts[0], parts[1]
        right_value = self.evaluate(right)
        if operator == "-":
            return -right_value
        elif operator == "!":
            return not right_value
        raise ValueError(f"Unknown unary operator: {operator}")

    def visit_binary(self, binary):
        return self.evaluate(binary)
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)
    command: str = sys.argv[1]
    filename: str = sys.argv[2]
    commands = ["tokenize", "parse", "evaluate", "run"]
    if command not in commands:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)
    with open(filename) as file:
        file_contents = file.read()
        if command == "tokenize":
            lex = Lexer(file_contents)
            token: Token = Token(TOKEN_TYPE.NONE, "", "", 0)
            while token.type != TOKEN_TYPE.EOF:
                token = lex.next_token()
                if token.type != TOKEN_TYPE.NONE:
                    print(token)
        elif command == "parse":
            lex = Lexer(file_contents)
            tokens = []
            while lex.i <= lex.size:
                token = lex.next_token()
                if token.type != TOKEN_TYPE.NONE:
                    tokens.append(token)
            par = Parser(tokens)
            expression = par.parse()
            if expression:
                print(expression)
        elif command == "evaluate":
            lex = Lexer(file_contents)
            tokens = []
            while lex.i <= lex.size:
                token = lex.next_token()
                if token.type != TOKEN_TYPE.NONE:
                    tokens.append(token)
            par = Parser(tokens)
            expression = par.parse()
            if expression:
                interpreter = Interpreter()
                value = interpreter.evaluate(expression)
                if value is None:
                    print("nil")
                elif isinstance(value, bool):
                    print(str(value).lower())
                elif isinstance(value, float) and value.is_integer():
                    print(int(value))
                else:
                    print(value)
        elif command == "run":
            lex = Lexer(file_contents)
            tokens = []
            while lex.i <= lex.size:
                token = lex.next_token()
                if token.type != TOKEN_TYPE.NONE:
                    tokens.append(token)
            par = Parser(tokens)
            statements = par.parser()
            if statements:
                interpreter = Interpreter()
                interpreter.interpret(statements)
    if exit_code != 0:
        sys.exit(exit_code)  # Exit with error code
    # Default success exit
    sys.exit(0)
if __name__ == "__main__":
    # lex = Lexer("print;")
    # tokens = []
    # while lex.i <= lex.size:
    #     token = lex.next_token()
    #     if token.type != TOKEN_TYPE.NONE:
    #         tokens.append(token)
    # par = Parser(tokens)
    # statements = par.parser()
    # if statements:
    #     interpreter = Interpreter()
    #     interpreter.interpret(statements)
    
    main()