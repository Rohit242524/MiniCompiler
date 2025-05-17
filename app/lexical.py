# lexer.py
import re
token_specification = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('TYPE',     r'\bint\b|\bfloat\b|\bchar\b'),
    ('ID',       r'[A-Za-z_]\w*'),
    ('ASSIGN',   r'='),
    ('END',      r';'),
    ('OP',       r'[+\-*/]'),
    ('NEWLINE',  r'\r\n|\n|\r'),
    ('SKIP',     r'[ \t]+'),
    ('STRING',   r'"[^"\n]*"'),
    ('MISMATCH', r'.'),
]
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        for mo in re.finditer(tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
                self.tokens.append((value, 'NUMBER'))
            elif kind == 'ID':
                self.tokens.append((value, 'ID'))
            elif kind == 'TYPE':
                self.tokens.append((value, 'TYPE'))
            elif kind in ('ASSIGN', 'END', 'OP'):
                self.tokens.append((value, kind))
            elif kind in ('SKIP', 'NEWLINE'):
                continue
            elif kind == 'STRING':
                self.tokens.append((value, 'STRING'))
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected token: {value!r}')
        return self.tokens
