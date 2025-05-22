from flask import render_template, request
from app.core import run_compiler

def setup_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/compile", methods=["POST"])
    def compile_code():
        code = request.form.get("code", "")
        return run_compiler(code)