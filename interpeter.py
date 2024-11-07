from enum import Enum
from dataclasses import dataclass
from typing import Self

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
    def __init__(self, text: str) -> None:
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
            elif self.current_char == '(':
                tokens.append(Token(TokenType.LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TokenType.RPAREN))
                self.advance()
            else:
                print("err")
        return tokens

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

lexer = Lexer("1+2 * 9 * (10-4.5)")
print(lexer.make_tokens())
 