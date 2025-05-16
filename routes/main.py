from flask import render_template, request

from compiler.core import run_compilation


def setup_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/compile", methods=["POST"])
    def compile_code():
        try:
            code = request.json.get("code", "")
            return run_compilation(code)
        except SyntaxError as e:
            return f"[SYNTAX ERROR] {e}"
        except TypeError as e:
            return f"[SEMANTIC ERROR] {e}"
        except Exception as e:
            return f"[LEXICAL ERROR] {e}"
