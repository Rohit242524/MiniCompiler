token_specification = [
    ("NUMBER", r"\d+(\.\d+)?"),
    ("TYPE", r"\bint\b|\bfloat\b|\bchar\b"),
    ("KEYWORD", r"\breturn\b|\bvoid\b"),
    ("PREPROC_SYMBOL", r"#"),
    ("PREPROC_KEYWORD", r"\binclude\b|\bdefine\b"),  # Moved up to take precedence over ID
    ("ID", r"[A-Za-z_]\w*"),  # Moved after PREPROC_KEYWORD
    ("ASSIGN", r"="),
    ("END", r";"),
    ("OP", r"[+\-*/]"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"{"),
    ("RBRACE", r"}"),
    ("COMMA", r","),
    ("NEWLINE", r"\r\n|\n|\r"),
    ("SKIP", r"[ \t]+"),
    ("STRING", r'"[^"\n]*"'),
    ("COMMENT", r"//.*?\n|/\*.*?\*/"),
    ("PUNCTUATOR", r"[<>]|\."),
    ("MISMATCH", r"."),
]
tok_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specification)