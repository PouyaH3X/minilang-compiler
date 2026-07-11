# Phase2 : Lexer with PLY for Minilang

import sys
from ply import lex


class MiniLanger:
    def __init__(self):
        self.lexer = lex.lex(module=self)

    # Tokens on minilang
    tokens = (
        'INT', 'BOOL', 'STRING', 'IF', 'ELSE', 'WHILE',
        'PRINT', 'INPUT', 'TRUE', 'FALSE',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'LT', 'GT', 'EQ', 'NE',
        'AND', 'OR', 'NOT',
        'ASSIGN',
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'COMMA',
        'ID', 'INT_LITERAL', 'STRING_LITERAL'
    )
    # Regular expression
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'

    t_LT = r'<'
    t_GT = r'>'
    t_EQ = r'=='
    t_NE = r'!='

    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'

    t_ASSIGN = r'='

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_SEMICOLON = r';'
    t_COMMA = r','

    t_ignore = ' \t'

    # Identifiers
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        reserved = {
            'int': 'INT', 'bool': 'BOOL', 'string': 'STRING',
            'if': 'IF', 'else': 'ELSE', 'while': 'WHILE',
            'print': 'PRINT', 'input': 'INPUT',
            'true': 'TRUE', 'false': 'FALSE'
        }
        t.type = reserved.get(t.value, 'ID')
        return t
    # Int

    def t_INT_LITERAL(self, t):
        r'\d+'
        t.value = int(t.value)
        return t
    # String

    def t_STRING_LITERAL(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        return t
    # Comment

    def t_STRING_LITERAL(self, t):
        r'(//[^\n]*)|(/\*([^*]|\*[^/])*\*+/)'
        pass

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        char = t.value[0]
        print(
            f"Lexical error at line {t.lexer.lineno}: Illegal character '{char}' (ASCII: {ord(char)})")
        t.lexer.skip(1)

    def tokenize(self, code):
        # Takes a list and returns a list of token directories
        self.lexer.input(code)
        tokens_list = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens_list.append({
                'type': tok.type,
                'value': tok.value,
                'lineno': tok.lineno,
                'lexpos': tok.lexpos
            })
        return tokens_list

    def tokenize_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            return self.tokenize(code)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found!")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

    def print_tokens(self, tokens_list):
        print("\n" + "=" * 70)
        print(f"{'Line':<10} {'Token Type':<20} {'Value':<30}")
        print("=" * 70)
        for tok in tokens_list:
            value = tok['value']
            if isinstance(value, str) and len(value) > 25:
                value = value[:22] + "..."
            print(f"{tok['lineno']:<10} {tok['type']:<20} {str(value):<30}")
        print("=" * 70)
        print(f"Total tokens: {len(tokens_list)}")

def main():
    lexer = MiniLanger()

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        print(f"Analyzing file: {filename} ...")
        tokens = lexer.tokenize_file(filename)
    else:
        print("\nPlease enter MiniLang code (press Ctrl+D or Ctrl+Z to finish):")
        try:
            code = sys.stdin.read()
        except KeyboardInterrupt:
            print("\nExiting program.")
            sys.exit(0)
        if not code:
            print("No input received.")
            sys.exit(0)
        tokens = lexer.tokenize(code)

    lexer.print_tokens(tokens)

if __name__ == "__main__":
    main()
