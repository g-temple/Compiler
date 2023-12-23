"""
Lexical analyzer for compiler
"""

import sys


class Token:
    """
    Class that represents a language token

    self.type is a string specifying the type of the token,
    e.g. 'PLUS' or 'NAME'

    'NAME' and 'NUMBER' tokens also have a non-None value field
    """

    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        """
        Return a string representation of this object's data
        """
        return "%s, %s" % (self.type, self.value)


def analyze(s):
    """
    The main lexical analyzer method

    Analyze input string s
    Return a list of the tokens identified in s
    """

    tokens = []

    next = 0
    while next < len(s):
        if s[next].isspace():
            next += 1

        elif s[next] == "=":
            tokens.append(Token("EQUALS", "="))
            next += 1

        elif s[next] == ">":
            if next < len(s) - 1 and s[next + 1] == "=":
                tokens.append(Token("GREATER_THAN_OR_EQUAL", ">="))
                next += 2
            else:
                tokens.append(Token("GREATER_THAN", ">"))
                next += 1

        elif s[next] == "<":
            if next < len(s) - 1 and s[next + 1] == "=":
                tokens.append(Token("LESS_THAN_OR_EQUAL", "<="))
                next += 2
            elif next < len(s) - 1 and s[next + 1] == ">":
                tokens.append(Token("NOT_EQUAL", "<>"))
                next += 2
            else:
                tokens.append(Token("LESS_THAN", "<"))
                next += 1

        # Recognize arithmetic operators
        elif s[next] == "+":
            tokens.append(Token("PLUS", "+"))
            next += 1

        elif s[next] == "-":
            tokens.append(Token("MINUS", "-"))
            next += 1

        elif s[next] == "*":
            tokens.append(Token("MULTIPLY", "*"))
            next += 1

        elif s[next] == "/":
            tokens.append(Token("DIVIDE", "/"))
            next += 1

        # recognize lparen and rparen
        elif s[next] == "(":
            tokens.append(Token("LPAREN", "("))
            next += 1

        elif s[next] == ")":
            tokens.append(Token("RPAREN", ")"))
            next += 1

        # recgonize a colon :
        elif s[next] == ":":
            if next < len(s) - 1 and s[next + 1] == "=":
                tokens.append(Token("ASSIGN", ":="))
                next += 2
            else:
                tokens.append(Token("COLON", ":"))
                next += 1

        elif s[next].isalpha():
            # Recognize identifiers
            identifier = s[next]
            next += 1
            while next < len(s) and s[next].isalnum():
                identifier += s[next]
                next += 1

            # Check for keyword matches
            if identifier == "for":
                tokens.append(Token("FOR", "for"))
            elif identifier == "if":
                tokens.append(Token("IF", "if"))
            elif identifier == "else":
                tokens.append(Token("ELSE", "else"))
            elif identifier == "while":
                tokens.append(Token("WHILE", "while"))

            # add similar logic for program, end, print, input, to
            ### extension, adding quit statements
            elif identifier == "program":
                tokens.append(Token("PROGRAM", "program"))
            elif identifier == "end":
                tokens.append(Token("END", "end"))
            elif identifier == "print":
                tokens.append(Token("PRINT", "print"))
            elif identifier == "input":
                tokens.append(Token("INPUT", "input"))
            elif identifier == "to":
                tokens.append(Token("TO", "to"))
            elif identifier == "quit":
                tokens.append(Token("QUIT", "quit"))
            else:
                tokens.append(Token("NAME", identifier))

        # Add a case to check for numbers
        # Add a NUMBER token, made from a sequence of 0-9 characters
        # The value of the token is the int value of the number
        elif s[next].isdigit():
            # Recognize numbers
            number = s[next]
            next += 1
            while next < len(s) and s[next].isdigit():
                number += s[next]
                next += 1
            tokens.append(Token("NUMBER", int(number)))

        else:
            print("Unexpected character: %s" % s[next])
            quit()

    # write all the tokens to a file

    # line_size = 20
    # with open("tokens.txt", "w") as f:
    #    for count, token in enumerate(tokens):
    #        pad = line_size - len(token.type) + len(str(token.value))
    #        f.write(str(token) + (pad * " ") + str(count) + "\n")

    return tokens


### Main
if __name__ == "__main__":
    # The name of the test file is the first command line argument
    filename = sys.argv[1]

    # Open it and read its contents into a string
    s = open(filename).read()

    # Analyze and print the resulting tokens
    tokens = analyze(s)

    for t in tokens:
        print(t)
