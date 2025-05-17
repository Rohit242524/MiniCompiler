from flask import Flask, render_template, request
import re

app = Flask(__name__)

# --- Lexical Token Specification ---
token_specification = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('TYPE',     r'\bint\b|\bfloat\b|\bchar\b'),
    ('ID',       r'[A-Za-z_]\w*'),
    ('ASSIGN',   r'='),
    ('END',      r';'),
    ('OP',       r'[+\-*/]'),
    ('NEWLINE',  r'\r\n|\n|\r'),  # Handles all newline types
    ('SKIP',     r'[ \t]+'),
    ('STRING', r'"[^"\n]*"'),
    ('MISMATCH', r'.'),
]
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

# --- Lexer ---
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
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected token: {value!r}')
        return self.tokens


# --- Parser ---
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[self.pos] if tokens else (None, None)
        self.parse_tree = []
        self.symbol_table = {}

    def advance(self):
        self.pos += 1
        self.current = self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def match(self, expected_type):
        if self.current[1] == expected_type:
            self.parse_tree.append(self.current)
            self.advance()
        else:
            raise SyntaxError(f"Expected {expected_type}, got {self.current[1]}")

    def expression(self):
        if self.current[1] not in ['NUMBER', 'ID', 'STRING']:
            raise SyntaxError(f"Expected number, variable, got {self.current[-1]}")

        left = self.current[0]
        self.match(self.current[1])

        while self.current[1] == 'OP':
            op = self.current[0]
            self.match('OP')

            if self.current[1] not in ['NUMBER', 'ID']:
                raise SyntaxError(f"Expected number or variable after operator, got {self.current[1]}")
            right = self.current[0]
            self.match(self.current[1])

            left = (left, op, right)

        return left

    def evaluate_expression(self, expr):
        if isinstance(expr, (int, float)):
            return expr

        if isinstance(expr, str):
            if expr.startswith('"') and expr.endswith('"'):
                return expr[1:-1]  # Strip quotes for strings
            elif expr.isdigit():
                return int(expr)
            elif expr.replace('.', '', 1).isdigit():
                return float(expr)
            elif expr in self.symbol_table:
                return self.symbol_table[expr][1]
            else:
                raise NameError(f"Undefined variable '{expr}'")

        elif isinstance(expr, tuple):
            left, op, right = expr
            left_val = self.evaluate_expression(left)
            right_val = self.evaluate_expression(right)

            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '*':
                return left_val * right_val
            elif op == '/':
                if right_val == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                return left_val / right_val
            else:
                raise ValueError(f"Unknown operator: {op}")

        else:
            raise TypeError(f"Unknown expression type: {type(expr)}")

    def statement(self):
        if self.current[1] == 'TYPE':
            var_type = self.current[0]
            self.match('TYPE')
            var_name = self.current[0]
            self.match('ID')
            self.match('ASSIGN')
            value = self.expression()
            self.match('END')

            evaluated_value = self.evaluate_expression(value)
            if ((var_type == 'int' and isinstance(evaluated_value, int)) or
                (var_type == 'float' and isinstance(evaluated_value, float))):
                self.symbol_table[var_name] = (var_type, evaluated_value)
            else:
                raise TypeError(
                    f"Type Mismatch: Cannot assign {type(evaluated_value).__name__} to {var_type} variable '{var_name}'")
        else:
            raise SyntaxError(f"Unknown statement starting with {self.current}")

    def parse(self):
        while self.current[0] is not None:
            self.statement()
        return self.parse_tree, self.symbol_table


# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    try:
        code = request.form.get('code', '')
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parse_tree, symbol_table = parser.parse()

        output = ["--- Tokens ---"]
        output += [str(token) for token in tokens]
        output += ["\n--- Symbol Table ---"]
        for var, (typ, val) in symbol_table.items():
            output.append(f"{var}: {typ} = {val}")
        return render_template('index.html', output='\n'.join(output))

    except SyntaxError as e:
        return render_template('index.html', output=f"[SYNTAX ERROR] {e}")
    except TypeError as e:
        return render_template('index.html', output=f"[SEMANTIC ERROR] {e}")
    except ZeroDivisionError as e:
        return render_template('index.html', output=f"[RUNTIME ERROR] {e}")
    except Exception as e:
        return render_template('index.html', output=f"[LEXICAL ERROR] {e}")


if __name__ == '__main__':
    app.run(debug=True)
