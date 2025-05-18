from flask import render_template
from app.lexical import Lexer
from app.parser import Parser

def run_compiler(code):
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        parse_tree, symbol_table = parser.parse()

        return render_template(
            "index.html",
            tokens=tokens,
            parse_tree=parse_tree,
            symbol_table=symbol_table,
            error=None
        )
    except Exception as e:
        return render_template(
            "index.html",
            tokens=None,
            parse_tree=None,
            symbol_table=None,
            error=str(e)
        )
