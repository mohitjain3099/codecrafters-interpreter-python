from app.token import Token,TOKEN_TYPE
from app.parser import Parser,ParserError
import pytest # type: ignore
# (5 - (3 - 1)) + -1
# // expect: (+ (group (- 5.0 (group (- 3.0 1.0)))) (- 1.0))
class TestPrint:
    def test_print_token(self, capfd):
        print(Token(TOKEN_TYPE.FALSE, "to_be_printed", "dont_print"), end="")
        print(Token(TOKEN_TYPE.TRUE, "to_be_printed", "dont_print"), end="")
        print(Token(TOKEN_TYPE.NIL, "to_be_printed", "dont_print"), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == 3 * "to_be_printed"
    @pytest.mark.parametrize(
        "token, expected_stdout",
        [
            (Token(TOKEN_TYPE.NUMBER, "5", "5.0"), "5.0"),
            (Token(TOKEN_TYPE.NUMBER, "79.20", "79.2"), "79.2"),
        ],
    )
    def test_print_number_literal(self, capfd, token, expected_stdout):
        print(token, end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == expected_stdout
    def test_string_literal(self, capfd):
        print(Token.create_string_literal("hello"), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "hello"  # without quotes, so not '"hello"'
class TestGrouping:
    def test_double_parenthesis(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.LEFT_PAREN, "(", "null"),
            Token(TOKEN_TYPE.LEFT_PAREN, "(", "null"),
            Token(TOKEN_TYPE.TRUE, "true", "true"),
            Token(TOKEN_TYPE.RIGHT_PAREN, ")", "null"),
            Token(TOKEN_TYPE.RIGHT_PAREN, ")", "null"),
        ]
        print(Parser(tokens)._parse_primary(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(group (group true))"
    def test_empty_group(self):
        tokens = [
            Token(TOKEN_TYPE.LEFT_PAREN, "(", "null"),
            Token(TOKEN_TYPE.RIGHT_PAREN, ")", "null"),
        ]
        with pytest.raises(ParserError) as e:
            Parser(tokens)._parse_primary()
class TestUnary:
    def test_negation(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.MINUS, "-", "null"),
            Token(TOKEN_TYPE.NUMBER, "5", "5.0"),
        ]
        print(Parser(tokens)._parse_unary(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(- 5.0)"
    def test_logical_not(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.BANG, "!", "null"),
            Token(TOKEN_TYPE.TRUE, "true", "null"),
        ]
        print(Parser(tokens)._parse_unary(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(! true)"
    def test_nested_logical_not(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.BANG, "!", "null"),
            Token(TOKEN_TYPE.BANG, "!", "null"),
            Token(TOKEN_TYPE.TRUE, "true", "null"),
        ]
        print(Parser(tokens)._parse_unary(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(! (! true))"
    def test_combined_with_groupping(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.BANG, "!", "null"),
            Token(TOKEN_TYPE.LEFT_PAREN, "(", "null"),
            Token(TOKEN_TYPE.TRUE, "true", "null"),
            Token(TOKEN_TYPE.RIGHT_PAREN, ")", "null"),
        ]
        print(Parser(tokens)._parse_unary(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(! (group true))"
class TestFactor:
    def test_multiplication(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.NUMBER, "5", "5.0"),
            Token(TOKEN_TYPE.STAR, "*", "null"),
            Token(TOKEN_TYPE.NUMBER, "2", "2.0"),
        ]
        print(Parser(tokens)._parse_factor(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(* 5.0 2.0)"
    def test_division(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.NUMBER, "5", "5.0"),
            Token(TOKEN_TYPE.SLASH, "/", "null"),
            Token(TOKEN_TYPE.NUMBER, "2", "2.0"),
        ]
        print(Parser(tokens)._parse_factor(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(/ 5.0 2.0)"
    def test_division_with_multiplication(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.NUMBER, "5", "5.0"),
            Token(TOKEN_TYPE.SLASH, "/", "null"),
            Token(TOKEN_TYPE.NUMBER, "2", "2.0"),
            Token(TOKEN_TYPE.STAR, "*", "null"),
            Token(TOKEN_TYPE.NUMBER, "2", "2.0"),
        ]
        print(Parser(tokens)._parse_factor(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(* (/ 5.0 2.0) 2.0)"
class TestTerm:
    def test_addition(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.NUMBER, "5", "5.0"),
            Token(TOKEN_TYPE.PLUS, "+", "null"),
            Token(TOKEN_TYPE.NUMBER, "2", "2.0"),
        ]
        print(Parser(tokens)._parse_term(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(+ 5.0 2.0)"
    def test_subtraction(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.NUMBER, "5", "5.0"),
            Token(TOKEN_TYPE.PLUS, "-", "null"),
            Token(TOKEN_TYPE.NUMBER, "2", "2.0"),
        ]
        print(Parser(tokens)._parse_term(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(- 5.0 2.0)"
class TestComparison:
    def test_single_comparison(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.NUMBER, "5", "5.0"),
            Token(TOKEN_TYPE.GREATER, ">", "null"),
            Token(TOKEN_TYPE.NUMBER, "2", "2.0"),
        ]
        print(Parser(tokens)._parse_comparison(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(> 5.0 2.0)"
    def test_multiple_comparison(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.NUMBER, "83", "83.0"),
            Token(TOKEN_TYPE.LESS, "<", "null"),
            Token(TOKEN_TYPE.NUMBER, "99", "99.0"),
            Token(TOKEN_TYPE.LESS, "<", "null"),
            Token(TOKEN_TYPE.NUMBER, "115", "115.0"),
        ]
        print(Parser(tokens)._parse_comparison(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(< (< 83.0 99.0) 115.0)"
class TestEquality:
    def test_single_equality(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.NUMBER, "5", "5.0"),
            Token(TOKEN_TYPE.EQUAL_EQUAL, "==", "null"),
            Token(TOKEN_TYPE.NUMBER, "2", "2.0"),
        ]
        print(Parser(tokens)._parse_equality(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(== 5.0 2.0)"
    def test_multiple_equality(self, capfd):
        tokens = [
            Token(TOKEN_TYPE.NUMBER, "83", "83.0"),
            Token(TOKEN_TYPE.BANG_EQUAL, "!=", "null"),
            Token(TOKEN_TYPE.NUMBER, "99", "99.0"),
            Token(TOKEN_TYPE.EQUAL_EQUAL, "==", "null"),
            Token(TOKEN_TYPE.NUMBER, "115", "115.0"),
        ]
        print(Parser(tokens)._parse_equality(), end="")
        captured_print = capfd.readouterr()
        assert captured_print.out == "(== (!= 83.0 99.0) 115.0)"
class TestSyntacticError:
    def test_missing_right_operand(self):
        tokens = [
            Token(TOKEN_TYPE.LEFT_PAREN, "(", "null"),
            Token(TOKEN_TYPE.NUMBER, "72", "72.0"),
            Token(TOKEN_TYPE.PLUS, "+", "null"),
        ]
        with pytest.raises(ParserError) as e:
            Parser(tokens).parse()