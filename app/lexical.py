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
            elif kind in ("ID", "TYPE", "KEYWORD", "PREPROC_KEYWORD"):
                self.tokens.append((value, kind))
            elif kind in ("ASSIGN", "END", "OP", "LPAREN", "RPAREN", "LBRACE", "RBRACE", "COMMA", "PREPROC_SYMBOL", "PUNCTUATOR"):
                self.tokens.append((value, kind))
            elif kind in ("SKIP", "NEWLINE", "COMMENT"):  # Skip comments
                continue
            elif kind == "STRING":
                self.tokens.append((value, "STRING"))
            elif kind == "MISMATCH":
                raise RuntimeError(f"Unexpected token: {value!r}")
        return self.tokens