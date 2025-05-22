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
        if self.current[1] in ("LOGICAL_OP", "BITWISE_OP", "INC_DEC") and self.current[0] in ("!", "~", "++", "--"):
            op = self.current[0]
            self.match(self.current[1])
            operand = self.expression()
            return (op, operand)

        if self.current[1] == "LPAREN":
            self.match("LPAREN")
            expr = self.expression()
            self.match("RPAREN")
            left = expr
        elif self.current[1] in ["NUMBER", "ID", "KEYWORD"]:
            if self.current[1] == "KEYWORD" and self.current[0] in ("true", "false"):
                left = self.current[0]
                self.match("KEYWORD")
            else:
                left = self.current[0]
                self.match(self.current[1])
                if self.current[1] == "LBRACKET":
                    self.match("LBRACKET")
                    index = self.expression()
                    self.match("RBRACKET")
                    left = ("ARRAY_ACCESS", left, index)
                if self.current[1] == "ARROW":
                    self.match("ARROW")
                    member = self.current[0]
                    self.match("ID")
                    left = ("MEMBER_ACCESS", left, member)
        else:
            raise SyntaxError(f"Expected number, variable, string, true/false, or (, got {self.current[1]}")

        while self.current[1] in ("OP", "COMP_OP", "LOGICAL_OP", "BITWISE_OP", "INC_DEC"):
            if self.current[1] == "OP":
                op = self.current[0]
                self.match("OP")
            elif self.current[1] == "COMP_OP":
                op = self.current[0]
                self.match("COMP_OP")
            elif self.current[1] == "LOGICAL_OP":
                op = self.current[0]
                self.match("LOGICAL_OP")
            elif self.current[1] == "BITWISE_OP":
                op = self.current[0]
                self.match("BITWISE_OP")
            elif self.current[1] == "INC_DEC":
                op = self.current[0] + "_postfix"
                self.match("INC_DEC")
                left = (op, left)
                return left
            else:
                break

            if self.current[1] == "LPAREN":
                self.match("LPAREN")
                right = self.expression()
                self.match("RPAREN")
            elif self.current[1] in ["NUMBER", "ID"]:
                right = self.current[0]
                self.match(self.current[1])
                if self.current[1] == "LBRACKET":
                    self.match("LBRACKET")
                    index = self.expression()
                    self.match("RBRACKET")
                    right = ("ARRAY_ACCESS", right, index)
                if self.current[1] == "ARROW":
                    self.match("ARROW")
                    member = self.current[0]
                    self.match("ID")
                    right = ("MEMBER_ACCESS", right, member)
            else:
                raise SyntaxError(
                    f"Expected number, variable, or (, got {self.current[1]}"
                )

            left = (left, op, right)

        return left

    def evaluate_expression(self, expr):
        if isinstance(expr, (int, float)):
            return expr

        if isinstance(expr, str):
            if expr == "true":
                return True
            elif expr == "false":
                return False
            elif expr.startswith('"') and expr.endswith('"'):
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
            if len(expr) == 2:
                op, operand = expr
                operand_val = self.evaluate_expression(operand)
                if op == "!":
                    return not operand_val
                elif op == "~":
                    return ~operand_val
                elif op == "++":
                    return operand_val + 1
                elif op == "--":
                    return operand_val - 1
                elif op == "++_postfix":
                    return operand_val
                elif op == "--_postfix":
                    return operand_val
                else:
                    raise ValueError(f"Unknown unary operator: {op}")

            elif len(expr) == 3:
                if expr[0] == "ARRAY_ACCESS":
                    array_name, index = expr[1], expr[2]
                    index_val = self.evaluate_expression(index)
                    return f"{array_name}[{index_val}]"
                elif expr[0] == "MEMBER_ACCESS":
                    struct_name, member = expr[1], expr[2]
                    return f"{struct_name}->{member}"
                else:
                    left, op, right = expr
                    left_val = self.evaluate_expression(left)
                    right_val = self.evaluate_expression(right)

                    if op in ("+", "-", "*", "/"):
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
                        raise ValueError(f"Unknown operator: {op}")

        else:
            raise TypeError(f"Unknown expression type: {type(expr)}")

    def function_call(self):
        func_name = self.current[0]
        self.match("ID")
        self.match("LPAREN")
        args = []
        if self.current[1] != "RPAREN":
            args.append(self.expression())
            while self.current[1] == "COMMA":
                self.match("COMMA")
                args.append(self.expression())
        self.match("RPAREN")
        return (func_name, args)

    def preprocessor_directive(self):
        if self.current[1] == "INCLUDE_DIRECTIVE":
            self.match("INCLUDE_DIRECTIVE")
            include_path = self.current[0]
            self.match("INCLUDE_PATH")
            directive_str = f"#include {include_path}"
            return ("PREPROCESSOR", directive_str)

        elif self.current[1] == "PREPROC_SYMBOL":
            self.match("PREPROC_SYMBOL")
            keyword = self.current[0]
            self.match("PREPROC_KEYWORD")

            if keyword == "define":
                macro_name = self.current[0]
                self.match("ID")
                macro_value = self.current[0]
                if self.current[1] in ("NUMBER", "ID", "STRING"):
                    self.match(self.current[1])
                else:
                    raise SyntaxError(f"Expected NUMBER, ID, or STRING for macro value, got {self.current[1]}")
                self.symbol_table[macro_name] = ("macro", macro_value)
                return ("MACRO", macro_name, macro_value)

        else:
            raise SyntaxError(f"Unknown preprocessor directive starting with {self.current}")

    def struct_or_union(self):
        keyword = self.current[0]
        self.match("KEYWORD")
        struct_name = self.current[0]
        self.match("ID")
        self.match("LBRACE")
        members = []
        while self.current[1] != "RBRACE":
            member_type = self.current[0]
            self.match("TYPE")
            member_name = self.current[0]
            self.match("ID")
            self.match("END")
            members.append((member_type, member_name))
        self.match("RBRACE")
        return (keyword.upper(), struct_name, members)

    def switch_statement(self):
        self.match("KEYWORD")
        self.match("LPAREN")
        expr = self.expression()
        self.match("RPAREN")
        self.match("LBRACE")
        cases = []
        default = None
        while self.current[1] != "RBRACE":
            if self.current[1] == "KEYWORD" and self.current[0] == "case":
                self.match("KEYWORD")
                value = self.expression()
                self.match("COLON")
                body = []
                while self.current[1] not in ("RBRACE", "KEYWORD"):
                    body.append(self.statement())
                cases.append(("CASE", value, body))
            elif self.current[1] == "KEYWORD" and self.current[0] == "default":
                self.match("KEYWORD")
                self.match("COLON")
                body = []
                while self.current[1] not in ("RBRACE", "KEYWORD"):
                    body.append(self.statement())
                default = ("DEFAULT", body)
            else:
                raise SyntaxError(f"Expected case or default in switch, got {self.current[1]}")
        self.match("RBRACE")
        return ("SWITCH", expr, cases, default)

    def do_while_statement(self):
        self.match("KEYWORD")
        self.match("LBRACE")
        body = []
        while self.current[1] != "RBRACE":
            body.append(self.statement())
        self.match("RBRACE")
        self.match("KEYWORD")
        self.match("LPAREN")
        condition = self.expression()
        self.match("RPAREN")
        self.match("END")
        return ("DO_WHILE", body, condition)

    def if_statement(self):
        self.match("KEYWORD")
        self.match("LPAREN")
        condition = self.expression()
        self.match("RPAREN")
        self.match("LBRACE")
        body = []
        while self.current[1] != "RBRACE":
            body.append(self.statement())
        self.match("RBRACE")
        else_body = None
        if self.current[1] == "KEYWORD" and self.current[0] == "else":
            self.match("KEYWORD")
            self.match("LBRACE")
            else_body = []
            while self.current[1] != "RBRACE":
                else_body.append(self.statement())
            self.match("RBRACE")
        return ("IF", condition, body, else_body)

    def while_statement(self):
        self.match("KEYWORD")
        self.match("LPAREN")
        condition = self.expression()
        self.match("RPAREN")
        self.match("LBRACE")
        body = []
        while self.current[1] != "RBRACE":
            body.append(self.statement())
        self.match("RBRACE")
        return ("WHILE", condition, body)

    def for_statement(self):
        self.match("KEYWORD")
        self.match("LPAREN")

        init = None
        if self.current[1] != "END":
            init = self.statement()

        condition = self.expression()
        self.match("END")

        update = None
        if self.current[1] != "RPAREN":
            if self.current[1] == "ID":
                var_name = self.current[0]
                self.match("ID")
                if self.current[1] in ("ASSIGN", "COMPOUND_ASSIGN", "INC_DEC"):
                    if self.current[1] == "ASSIGN":
                        self.match("ASSIGN")
                        value = self.expression()
                        update = ("ASSIGN", var_name, value)
                    elif self.current[1] == "COMPOUND_ASSIGN":
                        op = self.current[0]
                        self.match("COMPOUND_ASSIGN")
                        value = self.expression()
                        update = (op, var_name, value)
                    elif self.current[1] == "INC_DEC":
                        op = self.current[0]
                        self.match("INC_DEC")
                        update = (op, var_name)
        self.match("RPAREN")

        self.match("LBRACE")
        body = []
        while self.current[1] != "RBRACE":
            body.append(self.statement())
        self.match("RBRACE")
        return ("FOR", init, condition, update, body)

    def statement(self):
        if self.current[1] == "KEYWORD" and self.current[0] in ("const", "static"):
            qualifier = self.current[0]
            self.match("KEYWORD")
            var_type = self.current[0]
            self.match("TYPE")
            var_name = self.current[0]
            self.match("ID")
            self.match("ASSIGN")
            value = self.expression()
            self.match("END")
            evaluated_value = self.evaluate_expression(value)
            if (var_type == "int" and isinstance(evaluated_value, int)) or (
                    var_type == "float" and isinstance(evaluated_value, float)
            ):
                self.symbol_table[var_name] = (f"{qualifier} {var_type}", evaluated_value)
            else:
                raise TypeError(
                    f"Type Mismatch: Cannot assign {type(evaluated_value).__name__} to {var_type} variable '{var_name}'"
                )
            return ("VAR_DECL", f"{qualifier} {var_type}", var_name, evaluated_value)

        elif self.current[1] == "KEYWORD" and self.current[0] in ("struct", "union"):
            return self.struct_or_union()

        elif self.current[1] == "TYPE":
            var_type = self.current[0]
            self.match("TYPE")
            var_name = self.current[0]
            self.match("ID")

            if self.current[1] == "LBRACKET":
                self.match("LBRACKET")
                size = self.current[0]
                self.match("NUMBER")
                self.match("RBRACKET")
                if self.current[1] == "ASSIGN":
                    self.match("ASSIGN")
                    value = self.expression()
                    self.match("END")
                    evaluated_value = self.evaluate_expression(value)
                    self.symbol_table[var_name] = (var_type + "[]", evaluated_value)
                    return ("ARRAY_DECL", var_type, var_name, size, evaluated_value)
                else:
                    self.match("END")
                    self.symbol_table[var_name] = (var_type + "[]", None)
                    return ("ARRAY_DECL", var_type, var_name, size, None)

            if self.current[1] == "LPAREN":
                self.match("LPAREN")
                params = []
                if self.current[1] != "RPAREN":
                    pass
                self.match("RPAREN")
                self.match("LBRACE")
                body = []
                while self.current[1] != "RBRACE" and self.current[0] is not None:
                    stmt = self.statement()
                    if stmt:
                        body.append(stmt)
                self.match("RBRACE")
                return ("FUNCTION", var_type, var_name, params, body)

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

        elif self.current[1] == "ID":
            var_name = self.current[0]
            self.match("ID")

            if self.current[1] == "LBRACKET":
                self.match("LBRACKET")
                index = self.expression()
                self.match("RBRACKET")
                if self.current[1] in ("ASSIGN", "COMPOUND_ASSIGN"):
                    if self.current[1] == "ASSIGN":
                        self.match("ASSIGN")
                        value = self.expression()
                        self.match("END")
                        evaluated_value = self.evaluate_expression(value)
                        self.symbol_table[var_name] = ("int[]", evaluated_value)
                        return ("ARRAY_ASSIGN", var_name, index, evaluated_value)
                    elif self.current[1] == "COMPOUND_ASSIGN":
                        op = self.current[0]
                        self.match("COMPOUND_ASSIGN")
                        value = self.expression()
                        self.match("END")
                        evaluated_value = self.evaluate_expression(value)
                        self.symbol_table[var_name] = ("int[]", evaluated_value)
                        return (op, var_name, index, evaluated_value)

            elif self.current[1] == "ARROW":
                self.match("ARROW")
                member = self.current[0]
                self.match("ID")
                self.match("ASSIGN")
                value = self.expression()
                self.match("END")
                evaluated_value = self.evaluate_expression(value)
                return ("MEMBER_ASSIGN", var_name, member, evaluated_value)

            elif self.current[1] in ("ASSIGN", "COMPOUND_ASSIGN", "INC_DEC"):
                if self.current[1] == "ASSIGN":
                    self.match("ASSIGN")
                    value = self.expression()
                    self.match("END")
                    evaluated_value = self.evaluate_expression(value)
                    self.symbol_table[var_name] = (self.symbol_table.get(var_name, ("int", None))[0], evaluated_value)
                    return ("ASSIGN", var_name, evaluated_value)
                elif self.current[1] == "COMPOUND_ASSIGN":
                    op = self.current[0]
                    self.match("COMPOUND_ASSIGN")
                    value = self.expression()
                    self.match("END")
                    evaluated_value = self.evaluate_expression(value)
                    self.symbol_table[var_name] = (self.symbol_table.get(var_name, ("int", None))[0], evaluated_value)
                    return (op, var_name, evaluated_value)
                elif self.current[1] == "INC_DEC":
                    op = self.current[0]
                    self.match("INC_DEC")
                    self.match("END")
                    return (op, var_name)

            self.pos -= 1
            self.current = self.tokens[self.pos]
            func_call = self.function_call()
            self.match("END")
            return ("FUNC_CALL", func_call)

        elif self.current[1] == "KEYWORD":
            keyword = self.current[0]
            if keyword == "return":
                self.match("KEYWORD")
                value = self.expression()
                self.match("END")
                return ("RETURN", value)
            elif keyword == "if":
                return self.if_statement()
            elif keyword == "while":
                return self.while_statement()
            elif keyword == "for":
                return self.for_statement()
            elif keyword == "switch":
                return self.switch_statement()
            elif keyword == "do":
                return self.do_while_statement()
            elif keyword in ("break", "continue"):
                self.match("KEYWORD")
                self.match("END")
                return (keyword.upper(),)

        else:
            raise SyntaxError(f"Unknown statement starting with {self.current}")

    def parse(self):
        program = []
        while self.current[0] is not None:
            if self.current[1] in ("INCLUDE_DIRECTIVE", "PREPROC_SYMBOL"):
                directive = self.preprocessor_directive()
                program.append(directive)
            else:
                stmt = self.statement()
                if stmt:
                    program.append(stmt)
        return program, self.symbol_table