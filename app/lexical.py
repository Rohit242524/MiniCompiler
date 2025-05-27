import re
from .token import tok_regex


class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.pos = 0

    def tokenize(self):
        if not self.code.strip():
            print("Lexer: Empty input code")
            return self.tokens

        self.pos = 0
        while self.pos < len(self.code):
            mo = re.match(tok_regex, self.code[self.pos :])
            if not mo:
                raise RuntimeError(
                    f"Lexer: Unexpected character at position {self.pos}: {self.code[self.pos]!r}"
                )

            kind = mo.lastgroup
            value = mo.group()
            self.pos += mo.end()

            print(
                f"Lexer: Found token - Type: {kind}, Value: {value}, Position: {self.pos}"
            )

            if kind == "INTEGER":
                try:
                    num_value = int(value.rstrip("uUlL"))
                    self.tokens.append((num_value, "INTEGER"))
                except ValueError as e:
                    raise RuntimeError(
                        f"Lexer: Invalid INTEGER at position {self.pos}: {value!r}"
                    )

            elif kind in ("FLOAT", "FLOAT_F", "FLOAT_L", "FLOAT_FL", "FLOAT_SCI"):
                self.tokens.append((value, kind))

            elif kind in ("ID", "TYPE", "KEYWORD", "PREPROCESSOR", "INCLUDE_PATH"):
                self.tokens.append((value, kind))
                
            elif kind in (
                "ASSIGN",
                "ARITHMETIC_OP",
                "BITWISE_OP",
                "LOGICAL_OP",
                "RELATIONAL_OP",
                "INC_DEC",
                "COMPOUND_ASSIGN",
                "SIZEOF",
                "LPAREN",
                "RPAREN",
                "LBRACE",
                "RBRACE",
                "LBRACKET",
                "RBRACKET",
                "COMMA",
                "SEMICOLON",
                "DOT",
                "ARROW",
            ):
                self.tokens.append((value, kind))

            elif kind in ("STRING", "CHAR"):
                self.tokens.append((value, kind))

            elif kind in ("WHITESPACE", "NEWLINE", "COMMENT"):
                continue
            elif kind == "MISMATCH":
                raise RuntimeError(
                    f"Lexer: Unexpected token at position {self.pos}: {value!r}"
                )

        return self.tokens

