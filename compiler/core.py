from .lexer import Lexer
from .parser import Parser


def run_compilation(code):
    symbol_table = {}

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, symbol_table)
    parser.parse()

    output = ["--- Tokens ---"]
    output += [str(token) for token in tokens]
    output += ["\n--- Symbol Table ---"]
    for var, (typ, val) in symbol_table.items():
        output.append(f"{var}: {typ} = {val}")
    return "\n".join(output)
