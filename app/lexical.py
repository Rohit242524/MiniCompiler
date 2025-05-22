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
            elif kind in ("INCLUDE_DIRECTIVE", "INCLUDE_PATH", "ASSIGN", "COMPOUND_ASSIGN", "END", "OP", "INC_DEC", "BITWISE_OP", "COMP_OP", "LOGICAL_OP", "ARROW", "LPAREN", "RPAREN", "LBRACE", "RBRACE", "LBRACKET", "RBRACKET", "COMMA", "COLON", "PREPROC_SYMBOL", "PUNCTUATOR"):
                self.tokens.append((value, kind))
            elif kind in ("SKIP", "NEWLINE", "COMMENT"):
                continue
            elif kind == "STRING":
                self.tokens.append((value, "STRING"))
            elif kind == "UNTERMINATED_STRING":
                raise SyntaxError(f"Unterminated string literal: {value}")
            elif kind == "MISMATCH":
                raise RuntimeError(f"Unexpected token: {value!r}")
        return self.tokens