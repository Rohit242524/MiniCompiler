token_specification = [
    ("NUMBER", r"\d+(\.\d+)?"),
    ("TYPE", r"\bint\b|\bfloat\b|\bchar\b|\b_Bool\b"),
    ("KEYWORD", r"\breturn\b|\bvoid\b|\bif\b|\belse\b|\bwhile\b|\bfor\b|\bbreak\b|\bcontinue\b|\bswitch\b|\bcase\b|\bdefault\b|\bdo\b|\bconst\b|\bstatic\b|\bstruct\b|\bunion\b|\btrue\b|\bfalse\b"),
    ("INCLUDE_DIRECTIVE", r"#include"),  # Matches #include as a single token
    ("INCLUDE_PATH", r"<[^>]+>"),  # Matches <stdio.h> or similar as a single token
    ("PREPROC_SYMBOL", r"#"),
    ("PREPROC_KEYWORD", r"\bdefine\b"),
    ("ID", r"[A-Za-z_]\w*"),
    ("ASSIGN", r"="),
    ("COMPOUND_ASSIGN", r"\+=|-=|\*=|/=|&=|\|=|\^=|<<=|>>="),
    ("END", r";"),
    ("OP", r"[+\-*/]"),
    ("INC_DEC", r"\+\+|--"),
    ("BITWISE_OP", r"&|\||\^|~|<<|>>"),
    ("COMP_OP", r"==|!=|<=|>=|<|>"),
    ("LOGICAL_OP", r"&&|\|\||\!"),
    ("ARROW", r"->"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"{"),
    ("RBRACE", r"}"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("COMMA", r","),
    ("COLON", r":"),
    ("NEWLINE", r"\r\n|\n|\r"),
    ("SKIP", r"[ \t]+"),
    ("STRING", r'"[^"\n]*"'),  # Valid string
    ("UNTERMINATED_STRING", r'"[^"\n]*'),  # Unterminated string (starts with " but doesn't end with ")
    ("COMMENT", r"//.*?\n|/\*.*?\*/"),
    ("PUNCTUATOR", r"\."),
    ("MISMATCH", r"."),
]
tok_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specification)