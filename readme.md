# Mini Compiler

A web-based mini compiler implementation that performs lexical analysis, syntax parsing, and semantic analysis for a simple programming language. Built with Flask and Python.

## Features

- Lexical Analysis (Tokenization)
- Syntax Parsing
- Semantic Analysis
- Symbol Table Management
- Web Interface for Code Input and Analysis
- Real-time Error Reporting

## Project Structure

```
MiniCompiler/
├── app/
│   ├── __init__.py
│   ├── core.py         # Core compiler logic
│   ├── lexical.py      # Lexical analyzer implementation
│   ├── parser.py       # Parser implementation
│   └── token.py        # Token specifications
├── routes/
│   ├── __init__.py
│   └── main.py         # Flask route definitions
├── static/
│   └── css/
│       └── style.css   # Web interface styling
├── templates/
│   └── index.html      # Main web interface template
├── app.py              # Flask application entry point
├── requirements.txt    # Project dependencies
└── readme.md          # Project documentation
```

## Setup and Installation

1. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Features Description

### 1. Lexical Analysis
- Tokenizes input code using regular expressions
- Recognizes:
  - Numbers (integers and floats)
  - Data types (int, float, char)
  - Identifiers
  - Operators
  - Strings
  - Assignment operators
  - Statement terminators

### 2. Syntax Parsing
- Implements a recursive descent parser
- Validates code structure
- Generates parse tree
- Handles arithmetic expressions
- Type checking

### 3. Semantic Analysis
- Symbol table management
- Type checking
- Variable declaration and initialization
- Expression evaluation

### 4. Error Handling
- Lexical errors
- Syntax errors
- Semantic errors
- Runtime errors (e.g., division by zero)

## Supported Language Features

- Variable declarations
- Basic data types (int, float, char)
- Arithmetic operations (+, -, *, /)
- String literals
- Type checking
- Expression evaluation

## Example Usage

```
int x = 5;
float y = 3.14;
int z = x + 10;
```

## Dependencies

- Flask==3.1.1
- Werkzeug==3.1.3
- Jinja2==3.1.6
- MarkupSafe==3.0.2
- itsdangerous==2.2.0
- click==8.2.0
- blinker==1.9.0
- colorama==0.4.6

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
