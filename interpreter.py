from enum import Enum
from dataclasses import dataclass
from typing import Self
from nodes import *

class BaseError:
    def __init__(self, fn: str, error_name: str, details: str) -> None:
        self.fn = fn
        self.error_name = error_name
        self.details = details

    def as_string(self) -> str:
        result  = f"{self.error_name}: {self.details}\n"
        result += f"File {self.fn}"

class IllegalCharError(BaseError):
    def __init__(self, fn, details) -> None:
        super().__init__(fn, "Illegal Character", details)

class InvalidSyntaxError(BaseError):
    def __init__(self, fn, details) -> None:
        super().__init__(fn, "Invalid Syntax", details)

class TokenType(Enum):
    INT    = "INT"
    FLOAT  = "FLOAT"
    PLUS   = "PLUS"
    MINUS  = "MINUS"
    MUL    = "MUL"
    DIV    = "DIV"
    POW    = "POW"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"

class Token:
    def __init__(self, type_: str, value: TokenType = None) -> None:
        self.type = type_
        self.value = value

    def __repr__(self) -> str:
        if self.value: return f"{self.type}:{self.value}"
        return f"{self.type}"
    
class Lexer:
    def __init__(self, fn: str, text: str) -> None:
        self.text: str = text
        self.pos: int = -1
        self.current_char: str = None
        self.advance()

    def advance(self) -> None:
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self) -> list[Token]:
        tokens: list[Token] = []
        while self.current_char != None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TokenType.PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TokenType.MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TokenType.MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TokenType.DIV))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(TokenType.POW))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TokenType.LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TokenType.RPAREN))
                self.advance()
            else:
                char = self.current_char
                self.advance()
                return [], IllegalCharError(self.fn, f"\"{char}\"")
        return tokens, None

    def make_number(self) -> Token:
        num_str = ""
        dot_count = 0
        while self.current_char != None and (self.current_char.isdigit() or self.current_char == "."):
            if self.current_char == ".":
                dot_count += 1
                if dot_count > 1:
                    break
            num_str += self.current_char
            self.advance()
        if dot_count == 0: return Token(TokenType.INT, int(num_str))
        return Token(TokenType.FLOAT, float(num_str))
        
@dataclass
class Number:
    value: any

    def __repr__(self) -> str:
        return f"{self.value}"
    
    def add(self, other: Self) -> Self:
        if isinstance(other, Number) and isinstance(self.value, Number):
            return self.value + other
        
    def sub(self, other: Self) -> Self:
        if isinstance(other, Number) and isinstance(self.value, Number):
            return self.value - other
        
    def mul(self, other: Self) -> Self:
        if isinstance(other, Number) and isinstance(self.value, Number):
            return self.value * other
        
    def div(self, other: Self) -> Self:
        if isinstance(other, Number) and isinstance(self.value, Number):
            return self.value / other
        
    def pow(self, other: Self) -> Self:
        if isinstance(other, Number) and isinstance(self.value, Number):
            return self.value ** other

class Parser:
    def __init__(self, fn: str, tokens: list[Token]) -> None:
        self.fn = fn
        self.tokens = iter(tokens)
        self.current_token = None
        self.advance()

    def raise_error(self) -> InvalidSyntaxError:
        return InvalidSyntaxError(self.fn,f"\"{self.current_token}\"")
    
    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        if self.current_token == None:
            return None
        result = self.expr()
        if self.current_token != None:
            return None, self.raise_error()
        return result, None
    
    def expr(self):
        result = self.term()
        while self.current_token != None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                result = AddNode(result, self.term())
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                result = SubtractNode(result, self.term())
