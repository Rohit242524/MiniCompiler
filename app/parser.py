class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[self.pos] if tokens else (None, None)
        self.parse_tree = []
        self.symbol_table = {}

    def advance(self):
        self.pos += 1
        self.current = (
            self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)
        )

    def match(self, expected_type):
        if self.current[1] == expected_type:
            self.parse_tree.append(self.current)
            self.advance()
        else:
            raise SyntaxError(f"Expected {expected_type}, got {self.current[1]}")

    def expression(self):
        if self.current[1] not in ["NUMBER", "ID", "STRING"]:
            raise SyntaxError(f"Expected number, variable, or string, got {self.current[1]}")

        left = self.current[0]
        self.match(self.current[1])

        while self.current[1] == "OP":
            op = self.current[0]
            self.match("OP")

            if self.current[1] not in ["NUMBER", "ID"]:
                raise SyntaxError(
                    f"Expected number or variable after operator, got {self.current[1]}"
                )
            right = self.current[0]
            self.match(self.current[1])

            left = (left, op, right)

        return left

    def evaluate_expression(self, expr):
        if isinstance(expr, (int, float)):
            return expr

        if isinstance(expr, str):
            if expr.startswith('"') and expr.endswith('"'):
                return expr[1:-1]
            elif expr.isdigit():
                return int(expr)
            elif expr.replace(".", "", 1).isdigit():
                return float(expr)
            elif expr in self.symbol_table:
                return self.symbol_table[expr][1]
            else:
                raise NameError(f"Undefined variable '{expr}'")

        elif isinstance(expr, tuple):
            left, op, right = expr
            left_val = self.evaluate_expression(left)
            right_val = self.evaluate_expression(right)

            if op == "+":
                return left_val + right_val
            elif op == "-":
                return left_val - right_val
            elif op == "*":
                return left_val * right_val
            elif op == "/":
                if right_val == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                return left_val / right_val
            else:
                raise ValueError(f"Unknown operator: {op}")

        else:
            raise TypeError(f"Unknown expression type: {type(expr)}")

    def function_call(self):
        func_name = self.current[0]
        self.match("ID")  # e.g., printf
        self.match("LPAREN")  # (
        args = []
        if self.current[1] != "RPAREN":
            args.append(self.expression())
            while self.current[1] == "COMMA":
                self.match("COMMA")
                args.append(self.expression())
        self.match("RPAREN")  # )
        return (func_name, args)

    def preprocessor_directive(self):
        directive = []
        self.match("PREPROC_SYMBOL")  # #
        self.match("PREPROC_KEYWORD")  # include
        self.match("PUNCTUATOR")  # <
        self.match("ID")  # stdio
        self.match("PUNCTUATOR")  # .
        self.match("ID")  # h
        self.match("PUNCTUATOR")  # >
        # Reconstruct the directive for the parse tree
        directive = ("PREPROCESSOR", "#include <stdio.h>")
        return directive

    def statement(self):
        if self.current[1] == "TYPE":
            # Handle variable declarations (e.g., int x = 5 + 3;)
            var_type = self.current[0]
            self.match("TYPE")
            var_name = self.current[0]
            self.match("ID")

            # Check if this is a function definition (e.g., int main())
            if self.current[1] == "LPAREN":
                self.match("LPAREN")
                params = []  # Add parameter parsing if needed
                if self.current[1] != "RPAREN":
                    # Parse parameters (not implemented for now)
                    pass
                self.match("RPAREN")
                self.match("LBRACE")
                body = []
                while self.current[1] != "RBRACE":
                    body.append(self.statement())
                self.match("RBRACE")
                return ("FUNCTION", var_type, var_name, params, body)

            # Otherwise, it's a variable declaration
            self.match("ASSIGN")
            value = self.expression()
            self.match("END")

            evaluated_value = self.evaluate_expression(value)
            if (var_type == "int" and isinstance(evaluated_value, int)) or (
                var_type == "float" and isinstance(evaluated_value, float)
            ):
                self.symbol_table[var_name] = (var_type, evaluated_value)
            else:
                raise TypeError(
                    f"Type Mismatch: Cannot assign {type(evaluated_value).__name__} to {var_type} variable '{var_name}'"
                )
            return ("VAR_DECL", var_type, var_name, evaluated_value)

        elif self.current[1] == "KEYWORD" and self.current[0] == "return":
            self.match("KEYWORD")
            value = self.expression()
            self.match("END")
            return ("RETURN", value)

        elif self.current[1] == "ID":  # Function call (e.g., printf("Hello, World!\n");)
            func_call = self.function_call()
            self.match("END")
            return ("FUNC_CALL", func_call)

        else:
            raise SyntaxError(f"Unknown statement starting with {self.current}")

    def parse(self):
        program = []
        while self.current[0] is not None:
            if self.current[1] == "PREPROC_SYMBOL":
                directive = self.preprocessor_directive()
                program.append(directive)
            else:
                stmt = self.statement()
                if stmt:
                    program.append(stmt)
        return program, self.symbol_table