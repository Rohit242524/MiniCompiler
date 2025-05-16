class Parser:
    def __init__(self, tokens, symbol_table):
        self.tokens = tokens
        self.symbol_table = symbol_table
        self.pos = 0
        self.current = tokens[self.pos] if tokens else (None, None)
        self.parse_tree = []

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

    def statement(self):
        if self.current[1] == "TYPE":
            var_type = self.current[0]
            self.match("TYPE")
            var_name = self.current[0]
            self.match("ID")
            self.match("ASSIGN")
            value = self.current[0]
            val_type = self.current[1]
            self.match(val_type)
            self.match("END")
            if (var_type == "int" and isinstance(value, int)) or (
                var_type == "float" and isinstance(value, float)
            ):
                self.symbol_table[var_name] = (var_type, value)
            else:
                raise TypeError(
                    f"Type Mismatch: Cannot assign {type(value).__name__} to {var_type} variable '{var_name}'"
                )
        else:
            raise SyntaxError(f"Unknown statement starting with {self.current}")

    def parse(self):
        while self.current[0] is not None:
            self.statement()
        return self.parse_tree
