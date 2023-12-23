"""
Parser for compiler
"""

import lexer, sys


def check(tokens, expected):
    return len(tokens) > 0 and tokens[0].type == expected


def match(tokens, expected):
    """
    Check if the next token matches what's expected

    If so, remove that token from the front
    If not, print and error and quit
    """

    print("Matching " + str(tokens[0]) + " with " + str(expected))
    if len(tokens) == 0:
        print("Unexpected end of input")
        quit()

    if tokens[0].type != expected:
        print("Expected", expected, "got", tokens[0].type)
        quit()

    # Remove the first token, advance to the next token
    tokens.pop(0)


def input_statement(tokens):
    """
    InputStatement --> 'input' Name
    """
    match(tokens, "INPUT")
    match(tokens, "NAME")


def assign_statement(tokens):
    """
    AssignStatement --> Name ':=' Expression
    """
    # Match the starting name and assign operator
    match(tokens, "NAME")
    match(tokens, "ASSIGN")

    # Call the expression parsing function
    expression(tokens)


def print_statement(tokens):
    """
    PrintStatement --> 'print' ':=' Expression
    """
    match(tokens, "PRINT")
    expression(tokens)


def else_clause(tokens):
    """
    ElseClause --> ElseClause --> 'else' ':' Block
    """
    match(tokens, "ELSE")
    match(tokens, "COLON")
    block(tokens)


def if_statement(tokens):
    """
    IfStatement --> IfStatement --> 'if' Condition ':' Block [ElseClause] 'end'
    """
    match(tokens, "IF")
    condition(tokens)
    match(tokens, "COLON")
    block(tokens)
    if check(tokens, "ELSE"):
        else_clause(tokens)
    match(tokens, "END")


def while_statement(tokens):
    """
    WhileStatement --> 'while' Condition ':' Block 'end'
    """
    match(tokens, "WHILE")
    condition(tokens)
    match(tokens, "COLON")
    block(tokens)
    match(tokens, "END")


def for_statement(tokens):
    """
    ForStatement --> 'for' '(' Name ':=' Expression 'to' Expression ')' Statement
    """
    match(tokens, "FOR")
    match(tokens, "LPAREN")
    match(tokens, "NAME")
    match(tokens, "ASSIGN")
    expression(tokens)
    match(tokens, "TO")
    expression(tokens)
    match(tokens, "RPAREN")
    statement(tokens)


def RelOp(tokens):
    """
    RelOp --> '=' | '<>' | '>' | '<' | '>=' | '<='
    """
    if check(tokens, "EQUALS"):
        match(tokens, "EQUALS")

    elif check(tokens, "NOT_EQUAL"):
        match(tokens, "NOT_EQUAL")

    elif check(tokens, "GREATER_THAN"):
        match(tokens, "GREATER_THAN")

    elif check(tokens, "LESS_THAN"):
        match(tokens, "LESS_THAN")

    elif check(tokens, "GREATER_THAN_OR_EQUAL"):
        match(tokens, "GREATER_THAN_OR_EQUAL")

    elif check(tokens, "LESS_THAN_OR_EQUAL"):
        match(tokens, "LESS_THAN_OR_EQUAL")

    else:
        print("Unexpected token", tokens[0].type)
        quit()


def statement(tokens):
    """Statement --> PrintStatement
    | InputStatement
    | AssignStatement
    | IfStatement
    | WhileStatement
    | ForStatement"""
    if check(tokens, "INPUT"):
        input_statement(tokens)
    elif check(tokens, "NAME"):
        assign_statement(tokens)
    elif check(tokens, "PRINT"):
        print_statement(tokens)
    elif check(tokens, "IF"):
        if_statement(tokens)
    elif check(tokens, "WHILE"):
        while_statement(tokens)
    elif check(tokens, "FOR"):
        for_statement(tokens)


def block(tokens):
    """
    Block --> {Statement}
    """
    # This statement loops as long as it recognizes that the next token is
    # the beginning of a valid statement
    in_block = True

    while in_block:
        # Check the next token to determine the type of the next statement
        #
        # Add more checks for the other kinds of statements
        #
        # Add checks for printStatement, IfStatement, WhileStatement, and ForStatement
        if len(tokens) > 0 and tokens[0].type in [
            "PRINT",
            "INPUT",
            "ASSIGN",
            "IF",
            "WHILE",
            "FOR",
            "NAME",
        ]:
            statement(tokens)
        else:
            in_block = False


def program(tokens):
    """
    Program --> 'program' Name ':' Block 'end'
    """
    # Match the program keyword
    match(tokens, "PROGRAM")

    # The name of the program
    match(tokens, "NAME")

    # Colon
    match(tokens, "COLON")

    # Call the block() function to process the statement block
    block(tokens)

    # Match the closing 'end'
    match(tokens, "END")


def condition(tokens):
    """
    Condition --> Expression RelOp Expression
    """
    expression(tokens)
    RelOp(tokens)
    expression(tokens)


def factor(tokens):
    """
    Factor --> '-' Factor
     | Atom
    """
    if check(tokens, "MINUS"):
        match(tokens, "MINUS")
        factor(tokens)
    else:
        atom(tokens)


def term(tokens):
    """
    Term --> Factor [( '*' | '/' ) Factor]
    """
    factor(tokens)
    if check(tokens, "MULTIPLY"):
        match(tokens, "MULTIPLY")
        factor(tokens)
    elif check(tokens, "DIVIDE"):
        match(tokens, "DIVIDE")
        factor(tokens)

    # MULTEXPR??


def expression(tokens):
    """
    Expression --> Term [('+' | '-') Expression]
    """
    term(tokens)
    if check(tokens, "PLUS"):
        match(tokens, "PLUS")
        expression(tokens)
    elif check(tokens, "MINUS"):
        match(tokens, "MINUS")
        expression(tokens)


def atom(tokens):
    """
    Atom --> Name | Number | '(' Expression ')'
    """
    if check(tokens, "NAME"):
        match(tokens, "NAME")
    elif check(tokens, "NUMBER"):
        match(tokens, "NUMBER")
    else:
        match(tokens, "LPAREN")
        expression(tokens)
        match(tokens, "RPAREN")
    # Match the name or number


def parse(tokens):
    """
    Top-level method to parse an input token sequence
    """
    # Call the method to parse a top-level program
    program(tokens)

    # If parsing succeeds, then the sequence of tokens should be
    # empty after expr returns
    #
    # Every token should be matched during the parsing process
    if len(tokens) > 0:
        print("Parsing failed.")
        print("Unmatched token", tokens[0])
        quit()


### Main
if __name__ == "__main__":
    # The name of the test file is the first command line argument
    filename = sys.argv[1]

    # Open it and read its contents into a string
    source = open(filename).read()
    # print(source)
    print()

    # Turn the input source into its sequence of tokens
    tokens = lexer.analyze(source)
    # Parse the tokens
    parse(tokens)
    print("Parsing complete.")
