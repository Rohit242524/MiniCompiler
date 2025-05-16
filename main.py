from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# --- Lexical Analysis ---
token_specification = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('TYPE',     r'int|float'),
    ('ID',       r'[A-Za-z_]\w*'),
    ('ASSIGN',   r'='),
    ('END',      r';'),
    ('OP',       r'[+\-*/]'),
    ('SKIP',     r'[ \t]+'),
    ('NEWLINE',  r'\n'),
    ('MISMATCH', r'.'),
]
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

symbol_table = {}

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
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected token: {value}')
        return self.tokens

# --- Syntax & Semantic Analysis ---
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[self.pos] if tokens else (None, None)
        self.parse_tree = []

    def advance(self):
        self.pos += 1
        self.current = self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def match(self, expected_type):
        if self.current[1] == expected_type:
            self.parse_tree.append(self.current)
            self.advance()
        else:
            raise SyntaxError(f"Expected {expected_type}, got {self.current[1]}")

    def statement(self):
        # e.g., int x = 5;
        if self.current[1] == 'TYPE':
            var_type = self.current[0]
            self.match('TYPE')
            var_name = self.current[0]
            self.match('ID')
            self.match('ASSIGN')
            value = self.current[0]
            val_type = self.current[1]
            self.match(val_type)
            self.match('END')
            # Semantic check
            if ((var_type == 'int' and isinstance(value, int)) or
                (var_type == 'float' and isinstance(value, float))):
                symbol_table[var_name] = (var_type, value)
            else:
                raise TypeError(f"Type Mismatch: Cannot assign {type(value).__name__} to {var_type} variable '{var_name}'")
        else:
            raise SyntaxError(f"Unknown statement starting with {self.current}")

    def parse(self):
        while self.current[0] is not None:
            self.statement()
        return self.parse_tree

@app.route('/compile', methods=['POST'])
def compile_code():
    try:
        code = request.json.get('code', '')
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser.parse()

        output = ["--- Tokens ---"]
        output += [str(token) for token in tokens]
        output += ["\n--- Symbol Table ---"]
        for var, (typ, val) in symbol_table.items():
            output.append(f"{var}: {typ} = {val}")
        return '\n'.join(output)

    except SyntaxError as e:
        return f"[SYNTAX ERROR] {e}"
    except TypeError as e:
        return f"[SEMANTIC ERROR] {e}"
    except Exception as e:
        return f"[LEXICAL ERROR] {e}"

if __name__ == '__main__':
    app.run(debug=True)
