class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[0] if tokens else (None, None)
        self.parse_tree = []
        self.symbol_table = {}

    def advance(self):
        self.pos += 1
        self.current = self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)
        print(f"Parser: Advanced to position {self.pos}, Current token: {self.current}")

    def match(self, expected_type):
        if self.current[1] == expected_type:
            print(f"Parser: Matched {expected_type}: {self.current}")
            self.parse_tree.append(self.current)
            self.advance()
        else:
            raise SyntaxError(f"Parser: Expected {expected_type}, got {self.current[1] if self.current[1] else 'EOF'} at position {self.pos}")

    def expression(self):
        print(f"Parser: Parsing expression at position {self.pos}")
        if self.current[1] in ("LOGICAL_OP", "BITWISE_OP") and self.current[0] in ("!", "~"):
            op = self.current[0]
            self.match(self.current[1])
            operand = self.expression()
            return (op, operand)

        if self.current[1] == "LPAREN":
            self.match("LPAREN")
            expr = self.expression()
            self.match("RPAREN")
            left = expr
        elif self.current[1] in ["INTEGER", "FLOAT", "FLOAT_F", "FLOAT_L", "FLOAT_FL", "FLOAT_SCI", "ID", "STRING", "CHAR"]:
            token_type = self.current[1]
            token_value = self.current[0]
            self.match(self.current[1])
            left = (token_value, token_type)
        else:
            raise SyntaxError(f"Parser: Expected number, variable, string, char, or (, got {self.current[1] if self.current[1] else 'EOF'} at position {self.pos}")

        while self.current[1] in ("ARITHMETIC_OP", "RELATIONAL_OP", "LOGICAL_OP", "BITWISE_OP"):
            if self.current[1] == "ARITHMETIC_OP":
                op = self.current[0]
                self.match("ARITHMETIC_OP")
            elif self.current[1] == "RELATIONAL_OP":
                op = self.current[0]
                self.match("RELATIONAL_OP")
            elif self.current[1] == "LOGICAL_OP":
                op = self.current[0]
                self.match("LOGICAL_OP")
            elif self.current[1] == "BITWISE_OP":
                op = self.current[0]
                self.match("BITWISE_OP")
            else:
                break

            if self.current[1] == "LPAREN":
                self.match("LPAREN")
                right = self.expression()
                self.match("RPAREN")
            elif self.current[1] in ["INTEGER", "FLOAT", "FLOAT_F", "FLOAT_L", "FLOAT_FL", "FLOAT_SCI", "ID", "STRING", "CHAR"]:
                token_type = self.current[1]
                token_value = self.current[0]
                self.match(self.current[1])
                right = (token_value, token_type)
            else:
                raise SyntaxError(f"Parser: Expected number, variable, string, char, or (, got {self.current[1] if self.current[1] else 'EOF'} at position {self.pos}")

            left = (left, op, right)

        return left

    def evaluate_expression(self, expr):
        print(f"Parser: Evaluating expression: {expr}")
        if isinstance(expr, tuple) and len(expr) == 2 and expr[1] in ("INTEGER", "FLOAT", "FLOAT_F", "FLOAT_L", "FLOAT_FL", "FLOAT_SCI", "STRING", "CHAR", "ID"):
            value, token_type = expr
            if token_type == "INTEGER":
                return int(value)
            elif token_type in ("FLOAT", "FLOAT_F", "FLOAT_L", "FLOAT_FL", "FLOAT_SCI"):
                try:
                    if token_type == "FLOAT_F":
                        return float(value.rstrip('fF'))
                    elif token_type == "FLOAT_L":
                        return float(value.rstrip('lL'))
                    elif token_type == "FLOAT_FL":
                        return float(value.rstrip('fFlL').rstrip('lL').rstrip('fF'))
                    elif token_type == "FLOAT_SCI":
                        return float(value)
                    else:  # FLOAT
                        return float(value)
                except ValueError as e:
                    raise ValueError(f"Parser: Invalid float value: {value}")
            elif token_type == "STRING":
                return value[1:-1]
            elif token_type == "CHAR":
                return value[1:-1]
            elif token_type == "ID":
                if value in self.symbol_table:
                    return self.symbol_table[value][1]
                else:
                    raise NameError(f"Parser: Undefined variable '{value}'")

        elif isinstance(expr, tuple):
            if len(expr) == 2:
                op, operand = expr
                operand_val = self.evaluate_expression(operand)
                if op == "!":
                    return not operand_val
                elif op == "~":
                    return ~operand_val
                else:
                    raise ValueError(f"Parser: Unknown unary operator: {op}")

            elif len(expr) == 3:
                left, op, right = expr
                left_val = self.evaluate_expression(left)
                right_val = self.evaluate_expression(right)

                if op in ("+", "-", "*", "/", "%"):
                    if op == "+":
                        return left_val + right_val
                    elif op == "-":
                        return left_val - right_val
                    elif op == "*":
                        return left_val * right_val
                    elif op == "/":
                        if right_val == 0:
                            raise ZeroDivisionError("Parser: Division by zero")
                        return left_val / right_val
                    elif op == "%":
                        return left_val % right_val
                elif op in ("==", "!=", "<", ">", "<=", ">="):
                    if op == "==":
                        return left_val == right_val
                    elif op == "!=":
                        return left_val != right_val
                    elif op == "<":
                        return left_val < right_val
                    elif op == ">":
                        return left_val > right_val
                    elif op == "<=":
                        return left_val <= right_val
                    elif op == ">=":
                        return left_val >= right_val
                elif op in ("&&", "||"):
                    if op == "&&":
                        return left_val and right_val
                    elif op == "||":
                        return left_val or right_val
                elif op in ("&", "|", "^", "<<", ">>"):
                    if op == "&":
                        return left_val & right_val
                    elif op == "|":
                        return left_val | right_val
                    elif op == "^":
                        return left_val ^ right_val
                    elif op == "<<":
                        return left_val << right_val
                    elif op == ">>":
                        return left_val >> right_val
                else:
                    raise ValueError(f"Parser: Unknown operator: {op}")

        else:
            raise TypeError(f"Parser: Unknown expression type: {type(expr)}")

    def preprocessor_directive(self):
        directive = self.current[0]
        self.match("PREPROCESSOR")
        if directive.startswith("#include"):
            include_path = self.current[0]
            self.match("INCLUDE_PATH")
            return ("PREPROCESSOR", f"#include {include_path}")
        elif directive.startswith("#define"):
            macro_name = self.current[0]
            self.match("ID")
            if self.current[1] in ("INTEGER", "FLOAT", "FLOAT_F", "FLOAT_L", "FLOAT_FL", "FLOAT_SCI", "ID", "STRING", "CHAR"):
                macro_value = self.current[0]
                self.match(self.current[1])
            else:
                macro_value = None
            self.symbol_table[macro_name] = ("macro", macro_value)
            return ("MACRO", macro_name, macro_value)
        else:
            return ("PREPROCESSOR", directive)

    def if_statement(self):
        self.match("KEYWORD")
        self.match("LPAREN")
        condition = self.expression()
        self.match("RPAREN")
        self.match("LBRACE")
        body = []
        while self.current[1] != "RBRACE" and self.current[1] is not None:
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        self.match("RBRACE")
        else_body = None
        if self.current[1] == "KEYWORD" and self.current[0] == "else":
            self.match("KEYWORD")
            self.match("LBRACE")
            else_body = []
            while self.current[1] != "RBRACE" and self.current[1] is not None:
                stmt = self.statement()
                if stmt:
                    else_body.append(stmt)
            self.match("RBRACE")
        return ("IF", condition, body, else_body)

    def function_parameters(self):
        params = []
        if self.current[1] != "RPAREN":
            while True:
                if self.current[1] == "TYPE":
                    param_type = self.current[0]
                    self.match("TYPE")
                    param_name = self.current[0]
                    self.match("ID")
                    params.append((param_type, param_name))
                    self.symbol_table[param_name] = (param_type, None)
                if self.current[1] == "COMMA":
                    self.match("COMMA")
                elif self.current[1] == "RPAREN":
                    break
                else:
                    raise SyntaxError(f"Parser: Expected comma or closing parenthesis in function parameters, got {self.current[1]} at position {self.pos}")
        self.match("RPAREN")
        return params

    def function_definition(self, return_type, func_name):
        self.match("LPAREN")
        params = self.function_parameters()
        self.match("LBRACE")
        body = []
        while self.current[1] != "RBRACE" and self.current[1] is not None:
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        self.match("RBRACE")
        return ("FUNC_DEF", return_type, func_name, params, body)

    def return_statement(self):
        self.match("KEYWORD")
        expr = self.expression()
        self.match("SEMICOLON")
        evaluated_value = self.evaluate_expression(expr)
        return ("RETURN", evaluated_value)

    def statement(self):
        if self.current[1] is None:
            print("Parser: Reached EOF in statement")
            return None

        print(f"Parser: Parsing statement at position {self.pos}, Current token: {self.current}")

        if self.current[1] == "SEMICOLON":
            self.match("SEMICOLON")
            return ("EMPTY",)

        if self.current[1] == "PREPROCESSOR":
            return self.preprocessor_directive()

        if self.current[1] == "TYPE":
            var_type = self.current[0]
            self.match("TYPE")
            var_name = self.current[0]
            self.match("ID")
            if self.current[1] == "LPAREN":
                return self.function_definition(var_type, var_name)
            elif self.current[1] == "ASSIGN":
                self.match("ASSIGN")
                value = self.expression()
                self.match("SEMICOLON")
                evaluated_value = self.evaluate_expression(value)
                if var_type in ("int", "short", "long", "signed", "unsigned", "_Bool") and isinstance(evaluated_value, int):
                    self.symbol_table[var_name] = (var_type, evaluated_value)
                elif var_type in ("float", "double") and isinstance(evaluated_value, float):
                    self.symbol_table[var_name] = (var_type, evaluated_value)
                elif var_type == "char" and isinstance(evaluated_value, str) and len(evaluated_value) == 1:
                    self.symbol_table[var_name] = (var_type, evaluated_value)
                else:
                    raise TypeError(f"Parser: Type mismatch for '{var_name}': Expected {var_type}, got {type(evaluated_value)}")
                return ("VAR_DECL", var_type, var_name, evaluated_value)
            else:
                self.match("SEMICOLON")
                self.symbol_table[var_name] = (var_type, None)
                return ("VAR_DECL", var_type, var_name, None)

        elif self.current[1] == "ID":
            var_name = self.current[0]
            self.match("ID")
            if self.current[1] == "ASSIGN":
                self.match("ASSIGN")
                value = self.expression()
                self.match("SEMICOLON")
                evaluated_value = self.evaluate_expression(value)
                var_type = self.symbol_table.get(var_name, ("int", None))[0]
                if var_type in ("int", "short", "long", "signed", "unsigned", "_Bool") and isinstance(evaluated_value, int):
                    self.symbol_table[var_name] = (var_type, evaluated_value)
                elif var_type in ("float", "double") and isinstance(evaluated_value, float):
                    self.symbol_table[var_name] = (var_type, evaluated_value)
                elif var_type == "char" and isinstance(evaluated_value, str) and len(evaluated_value) == 1:
                    self.symbol_table[var_name] = (var_type, evaluated_value)
                else:
                    raise TypeError(f"Parser: Type mismatch for assignment to '{var_name}': Expected {var_type}, got {type(evaluated_value)}")
                return ("ASSIGN", var_name, evaluated_value)
            else:
                raise SyntaxError(f"Parser: Expected '=', got {self.current[1] if self.current[1] else 'EOF'} at position {self.pos}")

        elif self.current[1] == "KEYWORD" and self.current[0] == "if":
            return self.if_statement()

        elif self.current[1] == "KEYWORD" and self.current[0] == "return":
            return self.return_statement()

        else:
            raise SyntaxError(f"Parser: Unknown statement: {self.current[1] if self.current[1] else 'EOF'} at position {self.pos}")

    def parse(self):
        print("Parser: Starting parse")
        program = []
        while self.current[0] is not None:
            stmt = self.statement()
            if stmt:
                program.append(stmt)
        print("Parser: Parse complete")
        return program, self.symbol_table