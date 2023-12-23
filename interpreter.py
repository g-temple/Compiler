"""
Interpreter for compiler
"""

import lexer

# Module-level variables to keep track of the state of the interpreter
next = 0
symbols = {}
tokens = []


def match(expected):
    """
    Check if the next token matches what's expected

    If so, increment next
    If not, print and error and quit
    """

    global next
    if len(tokens) == 0:
        print("Unexpected end of input")
        quit()

    if tokens[next].type != expected:
        print("Expected", expected, "got", tokens[next].type)
        quit()

    # Advance to the next token
    next += 1


def expression():
    """
    Expression --> Term [('+' | '-') Expression]
    """
    first_term = term()
    if check("PLUS"):
        match("PLUS")
        expr = expression()
        return first_term + expr
    elif check("MINUS"):
        match("MINUS")
        expr = expression()
        return first_term - expr
    else:
        return first_term


def term():
    """
    Term --> Factor [( '*' | '/' ) Factor]
    """
    first_factor = factor()
    if check("MULTIPLY"):
        match("MULTIPLY")
        second_factor = factor()
        return first_factor * second_factor
    elif check("DIVIDE"):
        match("DIVIDE")
        second_factor = factor()
        return first_factor / second_factor
    else:  # there was no division or multiplication
        return first_factor


def factor():
    """
    Factor --> '-' Factor
     | Atom
    """
    if check("MINUS"):
        match("MINUS")
        return -1 * factor()
    else:
        return atom()


def check(test):
    """
    Helper method to check the next token without advancing
    """
    return tokens[next].type == test


def atom():
    """
    Atom --> Name | Number | '(' Expression ')'

    Atom returns a single value used in an expression

    For variables, it looks up the variable's associated value
    in the symbol table

    For numbers, it returns the number value saved in the token

    For parenthesized expressions, it evaluates that expression and
    returns the result
    """

    # Return the value of a variable
    if check("NAME"):
        var = symbols[tokens[next].value]
        match("NAME")
        return var

    ### Add more cases to handle Number and ( Expression )
    elif check("NUMBER"):
        num = tokens[next].value
        match("NUMBER")
        return num

    elif check("LPAREN"):
        match("LPAREN")
        val = expression()
        match("RPAREN")
        return val


def input_statement():
    """
    InputStatement --> 'input' Name
    """

    # Match the input token
    match("INPUT")

    # Get the name
    name = tokens[next].value
    match("NAME")

    # Read an input int and store it to that name
    print("Enter a value for", name)
    value = int(input())
    symbols[name] = value


def print_statement():
    """
    print -> print expression
    """
    match("PRINT")
    print(expression())


def relOp():
    if check("EQUALS"):
        match("EQUALS")
        return "="

    elif check("NOT_EQUAL"):
        match("NOT_EQUAL")
        return "<>"

    elif check("GREATER_THAN"):
        match("GREATER_THAN")
        return ">"

    elif check("LESS_THAN"):
        match("LESS_THAN")
        return "<"

    elif check("GREATER_THAN_OR_EQUAL"):
        match("GREATER_THAN_OR_EQUAL")
        return ">="

    elif check("LESS_THAN_OR_EQUAL"):
        match("LESS_THAN_OR_EQUAL")
        return "<="

    else:
        print("Unexpected token", tokens[0].type)
        quit()


def evaluate_condition(lhs, op, rhs):
    if op == "=":
        return lhs == rhs

    elif op == "<>":
        return lhs != rhs

    elif op == ">":
        return lhs > rhs

    elif op == "<":
        return lhs < rhs

    elif op == ">=":
        return lhs >= rhs

    elif op == "<=":
        return lhs <= rhs
    else:
        print("no valid relOp")
        quit()


def condition():
    """
    Condition --> Expression relOp Expression
    """
    lhs = expression()
    op = relOp()
    rhs = expression()
    return evaluate_condition(lhs, op, rhs)


def skip_to_end():
    global next
    depth = 0

    while next < len(tokens):
        if check("END"):
            if depth == 0:
                break
            else:
                depth -= 1

        elif check("IF") or check("WHILE") or check("FOR"):
            depth += 1

        next += 1


def while_statement():
    """
    WhileStatement --> 'while' Condition ':' Block 'end'
    """
    global next

    match("WHILE")
    condition_start = next
    val = condition()
    match("COLON")

    # simulated while loop
    while val:
        block()

        # reset to top of loop
        next = condition_start
        val = condition()
        match("COLON")

    # scan through till corresponding end statement has been reached
    skip_to_end()

    match("END")


def for_statement():
    """
    ForStatement --> 'for' '(' Name ':=' Expression 'to' Expression ')'  block end
    """
    global next
    match("FOR")
    match("LPAREN")
    index_var = tokens[next].value  # get the name of the loop variable, not its value
    assign_statement()
    match("TO")
    right_expr = expression()
    match("RPAREN")
    start_of_block = next

    while symbols[index_var] <= right_expr:
        block()
        next = start_of_block
        symbols[index_var] += 1

    # skip to the outermost end
    skip_to_end()
    match("END")


def if_statement():
    """
    IfStatement -->  'if' Condition ':' Block [ElseClause] 'end'
    """
    global next

    match("IF")
    val = condition()
    match("COLON")

    if val:
        block()

        depth = 0
        while next < len(tokens):
            if check("IF") or check("WHILE") or check("FOR"):
                depth += 1
            elif check("END"):
                if depth == 0:
                    break
                else:
                    depth -= 1
            next += 1

        match("END")

    else:
        # skip ahead in token sequence
        depth = 0

        while next < len(tokens):
            if check("ELSE") and depth == 0:
                else_clause()  # we want to evalute this else clause
                break

            elif check("END"):
                if depth == 0:
                    break
                else:
                    depth -= 1

            elif check("IF") or check("WHILE") or check("FOR"):
                depth += 1

            next += 1

        match("END")


def else_clause():
    """
    else ':' block
    """
    match("ELSE")
    match("COLON")
    block()


def assign_statement():
    """
    AssignStatement --> Name ':=' Expression
    """

    # Get the variable name
    name = tokens[next].value
    match("NAME")

    # Match the := symbol
    match("ASSIGN")

    # Evaluate the expression on the right hand side
    #
    # The expression function RETURNS its result
    expr_value = expression()

    # Assign the expression result to the variable
    symbols[name] = expr_value


def quit_statement():
    """
    quit -> quit expr
    """
    match("QUIT")
    quit_val = expression()
    print(quit_val)
    quit()


def block():
    """
    block --> {Statement}

    A block can be any number of statements. This function uses a
    loop that runs as long as the next token corresponds to the
    beginning of some statement.

    Extend this function to add calls to the different statement
    functions.
    """

    in_block = True

    while in_block:
        # The next token determines the statement type
        if check("INPUT"):
            input_statement()
        elif check("NAME"):
            assign_statement()
        elif check("PRINT"):
            print_statement()
        elif check("IF"):
            if_statement()
        elif check("WHILE"):
            while_statement()
        elif check("FOR"):
            for_statement()
        elif check("QUIT"):
            quit_statement()
        else:
            in_block = False


def program():
    """
    program --> 'program' Name ':' Block 'end'
    """

    # Match the first three tokens
    match("PROGRAM")
    match("NAME")
    match("COLON")

    # Process the block of statements
    block()

    # Match the closing end token
    match("END")


def interpret(source):
    """
    The interpreter uses the same strategy as the parser, but
    functions may return values representing the results of
    evaluating those parts of the program
    """

    # Lexical analysis
    global tokens
    tokens = lexer.analyze(source)

    # Start with the top-level declaration
    program()


### Main
#
# Load and run one test program
#
# Write more test programs
if __name__ == "__main__":
    source = open("test.p").read()
    print(source)
    interpret(source)
