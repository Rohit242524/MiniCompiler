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
            error=None,
            code=code
        )
    except Exception as e:
        # Find the tokens up to the point of the error
        error_pos = parser.pos if 'parser' in locals() else 0
        tokens_up_to_error = tokens[:error_pos] if 'tokens' in locals() else []

        return render_template(
            "index.html",
            tokens=tokens_up_to_error,  # Only show tokens up to the error
            parse_tree=None,
            symbol_table=None,
            error=f"Error occurred here: {str(e)}",
            code=code
        )