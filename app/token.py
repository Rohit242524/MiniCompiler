token_specification = [
    ("NUMBER", r"\d+(\.\d+)?"),
    ("TYPE", r"\bint\b|\bfloat\b|\bchar\b"),
    ("ID", r"[A-Za-z_]\w*"),
    ("ASSIGN", r"="),
    ("END", r";"),
    ("OP", r"[+\-*/]"),
    ("NEWLINE", r"\r\n|\n|\r"),
    ("SKIP", r"[ \t]+"),
    ("STRING", r'"[^"\n]*"'),
    ("MISMATCH", r"."),
]
tok_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specification)
