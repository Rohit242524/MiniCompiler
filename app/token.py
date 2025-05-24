token_specification = [
    # Floating-point numbers
    ("FLOAT_SCI", r"-?\d+\.\d*[eE][+-]?\d+"),
    ("FLOAT_FL", r"-?\d+\.\d*([fF][lL]|[lL][fF])"),
    ("FLOAT_F", r"-?\d+\.\d*[fF](?![lL])"),
    ("FLOAT_L", r"-?\d+\.\d*[lL](?![fF])"),
    ("FLOAT", r"-?\d+\.\d*(?![fFlLeE])"),
    # Integers
    ("INTEGER", r"-?\d+([uU]|[lL]|[uU][lL]|[lL][uU])?"),
    # Types
    ("TYPE", r"\b(int|float|double|char|short|long|void|signed|unsigned|_Bool|_Complex|_Imaginary)\b"),
    
    # Keywords
    ("KEYWORD", r"\b(auto|break|case|const|continue|default|do|else|enum|extern|for|goto|if|inline|register|restrict|return|sizeof|static|struct|switch|typedef|union|volatile|while)\b"),
    
    # Preprocessor
    ("PREPROCESSOR", r"#\s*(include|define|undef|if|ifdef|ifndef|else|elif|endif|line|error|pragma)"),
    ("INCLUDE_PATH", r"(<[^>]+>|\"[^\"]+\")"),
    # Identifiers
    ("ID", r"[a-zA-Z_]\w*"),
    # Operators
    ("ASSIGN", r"="),
    ("ARITHMETIC_OP", r"\+|-|\*|/|%"),
    ("BITWISE_OP", r"&|\||\^|~|<<|>>"),
    ("LOGICAL_OP", r"&&\|\||!"),
    ("RELATIONAL_OP", r"==|!=|<|>|<=|>="),
    ("INC_DEC", r"\+\+|--"),
    ("COMPOUND_ASSIGN", r"\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>="),
    ("SIZEOF", r"sizeof"),
    # Punctuators
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("COMMA", r","),
    ("SEMICOLON", r";"),
    ("DOT", r"\."),
    ("ARROW", r"->"),
    # Strings and chars
    ("STRING", r'"(?:\\.|[^"\\])*"'),
    ("CHAR", r"'(?:\\.|[^'\\])'"),
    # Whitespace and comments (to skip)
    ("WHITESPACE", r"[ \t]+"),
    ("NEWLINE", r"\r\n|\n|\r"),
    ("COMMENT", r"//.*?\n|/\*[\s\S]*?\*/"),
    # Mismatch (must be last)
    ("MISMATCH", r"."),
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)