from flask import render_template
from app.lexical import Lexer
from app.parser import Parser

def run_compiler(code):
    # Normalize the input code
    code = code.strip()  # Remove leading/trailing whitespace
    code = code.replace('\r\n', '\n').replace('\r', '\n')  # Standardize line endings to \n

    try:
        print("Starting tokenization...")  # Debug print
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"Tokens generated: {tokens}")  # Debug print

        print("Starting parsing...")  # Debug print
        parser = Parser(tokens)
        parse_tree, symbol_table = parser.parse()
        print(f"Parse tree: {parse_tree}")  # Debug print
        print(f"Symbol table: {symbol_table}")  # Debug print

        return render_template(
            "index.html",
            tokens=tokens,
            parse_tree=parse_tree,
            symbol_table=symbol_table,
            error=None,
            code=code
        )
    except Exception as e:
        # Determine tokens up to the error point
        if 'lexer' in locals() and hasattr(lexer, 'tokens'):
            tokens_up_to_error = lexer.tokens  # Tokens up to error if tokenization failed
        elif 'parser' in locals() and 'tokens' in locals():
            tokens_up_to_error = tokens[:parser.pos]  # Tokens up to error if parsing failed
        else:
            tokens_up_to_error = []

        print(f"Error occurred: {str(e)}")  # Debug print
        print(f"Tokens up to error: {tokens_up_to_error}")  # Debug print

        return render_template(
            "index.html",
            tokens=tokens_up_to_error,
            parse_tree=None,
            symbol_table=None,
            error=f"Error occurred here: {str(e)}",
            code=code
        )