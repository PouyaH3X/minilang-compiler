# MiniLang Scanner - Phase 1

class Scanner:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = []

    def current(self):
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None

    def advance(self):
        self.pos += 1

    def add(self, t, v):
        self.tokens.append(f"({t}, {v})")

    def scan_identifier(self):
        word = ""
        while self.current() and (self.current().isalnum() or self.current() == "_"):
            word += self.current()
            self.advance()

        if word == "if":
            self.add("IF", word)
        elif word == "while":
            self.add("WHILE", word)
        else:
            self.add("IDENTIFIER", word)

    def scan_integer(self):
        num = ""
        while self.current() and self.current().isdigit():
            num += self.current()
            self.advance()
        self.add("INTEGER", num)

    def scan(self):
        while self.current() is not None:
            ch = self.current()

            if ch.isspace():
                self.advance()

            elif ch.isalpha() or ch == "_":
                self.scan_identifier()

            elif ch.isdigit():
                self.scan_integer()

            elif ch == "+":
                self.add("PLUS", "+")
                self.advance()

            elif ch == "(":
                self.add("LPAREN", "(")
                self.advance()

            elif ch == ")":
                self.add("RPAREN", ")")
                self.advance()

            elif ch == "=":
                self.advance()
                if self.current() == "=":
                    self.advance()
                    self.add("EQUAL", "==")
                else:
                    self.add("ASSIGN", "=")

            else:
                self.add("LEXICAL_ERROR", ch)
                self.advance()

with open("input.txt","r",encoding="utf-8") as f:
    text=f.read()

scanner=Scanner(text)
scanner.scan()

with open("output.txt","w",encoding="utf-8") as out:
    for t in scanner.tokens:
        print(t)
        out.write(t+"\\n")
