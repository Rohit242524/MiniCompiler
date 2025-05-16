token_specification = [
    ("NUMBER", r"\d+(\.\d+)?"),
    ("TYPE", r"int|float"),
    ("ID", r"[A-Za-z_]\w*"),
    ("ASSIGN", r"="),
    ("END", r";"),
    ("OP", r"[+\-*/]"),
    ("SKIP", r"[ \t]+"),
    ("NEWLINE", r"\n"),
    ("MISMATCH", r"."),
]

tok_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specification)
