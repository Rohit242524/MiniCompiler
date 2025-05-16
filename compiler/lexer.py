import re

from .token import tok_regex


class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        for mo in re.finditer(tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == "NUMBER":
                value = float(value) if "." in value else int(value)
                self.tokens.append((value, "NUMBER"))
            elif kind == "ID":
                self.tokens.append((value, "ID"))
            elif kind == "TYPE":
                self.tokens.append((value, "TYPE"))
            elif kind in ("ASSIGN", "END", "OP"):
                self.tokens.append((value, kind))
            elif kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                raise RuntimeError(f"Unexpected token: {value}")
        return self.tokens
