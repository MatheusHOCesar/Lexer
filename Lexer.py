from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Iterator


class TokenKind(enum.Enum):
    """Classe já implementada: nomes e números não devem ser alterados."""

    EOF = -1

    IDENTIFIER = 1
    INT_LITERAL = 2
    STRING_LITERAL = 3

    KW_INT = 10
    KW_BOOL = 11
    KW_VOID = 12
    KW_TRUE = 13
    KW_FALSE = 14
    KW_IF = 15
    KW_ELSE = 16
    KW_WHILE = 17
    KW_RETURN = 18
    KW_PRINT = 19

    PLUS = 20
    MINUS = 21
    STAR = 22
    SLASH = 23
    PERCENT = 24
    LESS = 25
    LESS_EQUAL = 26
    GREATER = 27
    GREATER_EQUAL = 28
    EQUAL_EQUAL = 29
    NOT_EQUAL = 30
    LOGICAL_AND = 31
    LOGICAL_OR = 32
    LOGICAL_NOT = 33
    ASSIGN = 34

    LEFT_PAREN = 40
    RIGHT_PAREN = 41
    LEFT_BRACE = 42
    RIGHT_BRACE = 43
    COMMA = 44
    SEMICOLON = 45


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    lexeme: str
    value: int | str | bool | None
    line: int
    column: int

    def __str__(self) -> str:
        return (
            f"<{self.kind.value}, {self.kind.name}, {self.lexeme!r}, "
            f"{self.value!r}, {self.line}, {self.column}>"
        )


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"erro léxico em {self.line}:{self.column}: {self.message}"


class Lexer:
    """Converte texto-fonte MicroC em uma sequência de tokens."""

    COMPOUND_OPS = {
        '=': ('=', TokenKind.EQUAL_EQUAL, TokenKind.ASSIGN),
        '!': ('=', TokenKind.NOT_EQUAL, TokenKind.LOGICAL_NOT),
        '<': ('=', TokenKind.LESS_EQUAL, TokenKind.LESS),
        '>': ('=', TokenKind.GREATER_EQUAL, TokenKind.GREATER),
        '&': ('&', TokenKind.LOGICAL_AND, None),
        '|': ('|', TokenKind.LOGICAL_OR, None)
    }

    SINGLE_OPS = {
        '+': TokenKind.PLUS, '-': TokenKind.MINUS, '*': TokenKind.STAR,
        '/': TokenKind.SLASH, '%': TokenKind.PERCENT, '(': TokenKind.LEFT_PAREN,
        ')': TokenKind.RIGHT_PAREN, '{': TokenKind.LEFT_BRACE, '}': TokenKind.RIGHT_BRACE,
        ',': TokenKind.COMMA, ';': TokenKind.SEMICOLON
    }

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.length = len(source)

    def is_at_end(self) -> bool:
        return self.pos >= self.length

    def peek(self, offset = 0) -> str:
        if self.pos + offset >= self.length:
            return "\0"
        return self.source[self.pos + offset]

    def advance(self) -> str:
        if self.is_at_end():
            return "\0"
        char = self.source[self.pos]
        self.pos += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def scan_operator_and_punctuation(self) -> Token:
        start_line, start_col = self.line, self.column
        char = self.advance()
        next_char = self.peek()

        if char in self.COMPOUND_OPS:
            expected, kind_of_match, kind_if_not = self.COMPOUND_OPS[char]
            if next_char == expected:
                self.advance()
                return Token(kind_of_match, char + expected, None, start_line, start_col)
            if kind_if_not:
                return Token(kind_if_not, char, None, start_line, start_col)

            raise LexerError(f"caractere invalido", start_line, start_col)

        if char in self.SINGLE_OPS:
            return Token(self.SINGLE_OPS[char], char, None, start_line, start_col)

        raise LexerError(f"caractere invalido", start_line, start_col)

    def tokens(self) -> Iterator[Token]:
        """Produza todos os tokens significativos e um único EOF ao final."""
        raise NotImplementedError("implemente o analisador léxico")
        yield  # mantém este método como gerador durante o desenvolvimento

    def scan(self) -> list[Token]:
        return list(self.tokens())

