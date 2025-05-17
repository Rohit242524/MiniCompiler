from flask import render_template, request

from app.core import run_compiler


def setup_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/compile", methods=["POST"])
    def compile_code():
        try:
            code = request.form.get("code", "")
            return run_compiler(code)
        except SyntaxError as e:
            return render_template("index.html", output=f"[SYNTAX ERROR] {e}")
        except TypeError as e:
            return render_template("index.html", output=f"[SEMANTIC ERROR] {e}")
        except ZeroDivisionError as e:
            return render_template("index.html", output=f"[RUNTIME ERROR] {e}")
        except Exception as e:
            return render_template("index.html", output=f"[LEXICAL ERROR] {e}")
