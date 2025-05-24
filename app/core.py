from flask import render_template
from app.lexical import Lexer
from app.parser import Parser

def run_compiler(code):
    print(f"Core: Received code:\n{code}")
    code = code.strip()
    if not code:
        print("Core: Empty input code")
        return render_template("index.html", tokens=[], parse_tree=None, symbol_table=None, error="Empty input", code="")

    code = code.replace('\r\n', '\n').replace('\r', '\n')
    lexer = Lexer(code)
    try:
        print("Core: Starting tokenization")
        tokens = lexer.tokenize()
        print("Core: Tokenization complete. Tokens:", tokens)
        parser = Parser(tokens)
        print("Core: Starting parsing")
        parse_tree, symbol_table = parser.parse()
        print("Core: Parsing complete. Parse Tree:", parse_tree)
        print("Core: Symbol Table:", symbol_table)
        return render_template("index.html", tokens=tokens, parse_tree=parse_tree, symbol_table=symbol_table, error=None, code=code)
    except Exception as e:
        tokens_up_to_error = lexer.tokens if hasattr(lexer, 'tokens') else []
        print(f"Core: Error occurred: {str(e)}")
        return render_template("index.html", tokens=tokens_up_to_error, parse_tree=None, symbol_table=None, error=str(e), code=code)