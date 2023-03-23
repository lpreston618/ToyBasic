#!/usr/bin/env python3

######
# A toy implementation of BASIC, for my own fun and entertainment.
# I'm loosely following the grammar I found on wikipedia:
# https://en.wikipedia.org/wiki/BASIC_interpreter
######


import re                       # for tokenizing input
import more_itertools as m_it   # for peeking at the first item of the token iterator
import readline                 # for my sanity

from toyBasicTypes import *

program_environment = {}    # stores BASIC program variables
program_lines = {}          # stores lines of code to be executed when the RUN command is entered
executing = False           # keeps track of if the program has been started with RUN
line = 0                    # the current line of the program being executed
call_stack = []             # keeps track of GOSUB calls

# think I've finally got it working
# here's the breakdown:  |   comments   |keywords|   numbers   |      strings      | relops |valid symbols | everything else
tokenizer = re.compile(r"((?:(?<=REM).*)|[a-z]\w*|\d+(?:\.\d+)?|(?:\"(?:\\.|.)*?\")|>=|<=|!=|[()+\-*\/>=<,]|[^\s\w]+)", flags=re.IGNORECASE)
# strings allow for escaped quotes. mismatched quotes result in a single " being captured,
# so if a token is just a single quote I know I can report a mismatched quotes error.
# keywords also includes valid variable names. numbers match both ints and floats.
# yeesh, this was a pain to get working. regexes are hard.

# enter a read-eval-print loop where a user can run statements
# directly or enter them into memory with line numbers
def main():
    global executing, line, program_environment, program_lines

    #loop until the user types "quit"
    while True:
        ### lex input into token stream:

        # an iterator over all re.match objects generated from the input
        token_re_matches = tokenizer.finditer(input("> ").upper())
        # an iterator over all tokens in the input, with the ability to peek at the first one
        # and to seek back to the beginning
        tokens = m_it.seekable(iter([i[0] for i in token_re_matches]))

        ### execute direct commands (QUIT, RUN, LIST, adding lines to program, direct statements)
        if tokens.peek(False):
            word = tokens.peek()
            if word == "QUIT": 
                break
            else:
                execute_line(tokens)

# executes a single line of BASIC code and catches and prints any BASIC errors           
def execute_line(tokens):
    global executing
    ### try to run the code
    try:
        # print(list(tokens)) # uncomment this to print tokenized input / test the lexer
        # tokens.seek(0)
        _line(tokens)
    ### if anything goes wrong, print the error message and return to the '> ' prompt
    except BasLangError as err:
        print(f"Error: {err}")
        executing = False

   

# parses a single line. if the line starts with a number, stores the rest of the line
# into program memory. if not, tries to parse and execute it directly
def _line(tokens):
    line_start = tokens.peek()
    if line_start.isnumeric():
        line_number = int(line_start)
        next(tokens)
        program_lines[line_number] = tokens
    else:
        _statement(tokens)

# parse a statement in the BASIC language
def _statement(tokens):
    ### if the statement is empty, just return. If not, consume a token and continue
    word = tokens.peek(None)
    if word == None:
        return
    else:
        next(tokens)

    ### statements must start with one of these commands
    if word == "PRINT":
        _PRINT(tokens)
    elif word == "IF":
        _IF(tokens)
    elif word == "GOTO":
        _GOTO(tokens)
    elif word == "INPUT":
        _INPUT(tokens)
    elif word == "LET":
        _LET(tokens)
    elif word == "GOSUB":
        _GOSUB(tokens)
    elif word == "RETURN":
        _RETURN(tokens)
    elif word == "CLEAR":
        _CLEAR(tokens)
    elif word == "LIST":
        _LIST(tokens)
    elif word == "RUN": # _RUN() doesn't need the token input stream, so we don't pass it
        _RUN()
    elif word == "END":
        _END(tokens)
    elif word == "REM":
        _REM(tokens)
    else:
        raise BasLangError(f"unknown symbol {word}")
    
    # if there are any tokens left at the end of parsing / executing,
    # it's a syntax error
    if next_token := tokens.peek(False):
        raise BasLangError(f"unexpected token {next_token} at end of statement")

#####
# The parser, more or less
#####

def _expr_list(tokens):
    # values_list = []

    # while next_token := tokens.peek(False):
    #     if next_token != ',':
    #         raise BasLangError('expressions must be separated by a ","')
        
    #     else:
    #         values_list.append(_expr_or_string(tokens))
    
    # return values_list

    values_list = [_expr_or_string(tokens)]
    while next_token := tokens.peek(False):
        if next_token != ',':
            raise BasLangError('expressions must be separated by a ","')
        next(tokens)
        values_list.append(_expr_or_string(tokens))
    return values_list

def _var_list(tokens):
    var_list = [next(tokens)]
    while next_token := tokens.peek(False):
        if next_token != ',':
            raise BasLangError('variables must be separated by a ","')
        var_list.append(next(tokens)) # todo: account for trailing ,
    return var_list

def _expr_or_string(tokens) -> BasLangValue:
    next_token = tokens.peek()
    if next_token[0] == '"':
        return _string(tokens)
    else:
        return _expression(tokens)

def _expression(tokens) -> BasLangValue:
    # Create an initial value of 0
    value = BasLangValue()
    first_token = tokens.peek()

    if first_token == "+":
        next(tokens)
        value.add(_term(tokens))
    elif first_token == "-":
        next(tokens)
        value.sub(_term(tokens))
    else:
        value.add(_term(tokens))

    while next_token := tokens.peek(False):
        if not next_token in "+-":
            break
        sign = next_token
        next(tokens)
        if sign == "+":
            value.add(_term(tokens))
        elif sign == "-":
            value.sub(_term(tokens))
    return value

def _string(tokens):
    next_token = next(tokens)
    if next_token == '"':
        raise BasLangError('unmatched "')
    else:
        return BasLangValue(init_type="string", init_value=next_token[1:-1])

def _term(tokens) -> BasLangValue:
    value = _factor(tokens)
    while next_token := tokens.peek(False):
        if not next_token in "*/":
            break
        op = next_token
        next(tokens)
        if op == "*":
            value.mul(_factor(tokens))
        elif op == "/":
            value.div(_factor(tokens))
    return value

def _factor(tokens) -> BasLangValue:
    next_token = next(tokens)
    if next_token == "(":
        value = _expression(tokens)
        close_paren = next(tokens)
        if close_paren != ")":
            raise BasLangError('expected ")", found ' + close_paren)
        return value
    elif is_number(next_token):
        return BasLangValue(init_value=next_token)
    elif not is_identifier(next_token):
        raise BasLangError(next_token + " is not a valid identifier")
    else:
        try:
            return program_environment[next_token]
        except KeyError:
            raise BasLangError("unrecognized variable " + next_token)


def _relop(tokens):
    op = next(tokens)
    if op == "=":
        return ["equal"]
    elif op == "<=":
        return ["less", "equal"]
    elif op == ">=":
        return ["greater", "equal"]
    elif op == "<":
        return ["less"]
    elif op == ">":
        return ["greater"]
    elif op == "!=":
        return ["less", "greater"]
    else:
        raise BasLangError("expected relational operator, found ", + op)

# Check if a string is a valid variable name
def is_identifier(string: str) -> bool:
    match = re.match("[A-Z]\w*", string, flags=re.IGNORECASE)
    if match:
        return match[0] == string
    return False

# Check if a string is a valid number
def is_number(string: str) -> bool:
    match = re.match(r"\d+(?:\.\d+)?", string)
    if match:
        return match[0] == string
    return False


#####
# Language constructs
#
#
#
#
#####

# execute a PRINT statement
# Print takes a comma-separated list of strings and expressions to print
def _PRINT(tokens):
    args = _expr_list(tokens)
    for arg in args:
        print(arg, end='\t')
    print()

# execute an IF ... THEN statement
def _IF(tokens):
    # op = next(tokens)
    # result = value1.compare(value2, op)

    value1 = _expr_or_string(tokens)
    valid_states = _relop(tokens)
    value2 = _expr_or_string(tokens)
    result = value1.compare(value2)
    if result in valid_states:
        then = next(tokens)
        if then != "THEN":
            raise BasLangError("expected keyword THEN, found " + then)
        _statement(tokens)
    # if the condition was not true, skip the rest of the line
    else:
        # constructing a list exhausts the iterator
        list(tokens)


# in a running program, jump to a specified line number
# (might add computed GOTO later, which allows for whole expressions
#    instead of just number literals)
# currently expects "GOTO <line number>"
def _GOTO(tokens):
    global line

    if not executing:
        raise BasLangError("GOTO can only be called in a running program")
    new_line_number = next(tokens)
    if not new_line_number.isnumeric():
        raise BasLangError(f"GOTO expects integer, found {new_line_number}")
    line = int(new_line_number)
    

def _INPUT():
    pass

# defines or redefines a variable in the program environment
# expects the form "LET <identifier> = <expression or string>"
def _LET(tokens):
    identifier = next(tokens)
    if not is_identifier(identifier):
        raise BasLangError(f"{identifier} is not a valid identifier")
    equals_sign = next(tokens)
    if equals_sign != "=":
        raise BasLangError(f"expected =, found {equals_sign}")
    value = _expr_or_string(tokens)
    program_environment[identifier] = value

def _GOSUB():
    pass

def _RETURN():
    pass

def _CLEAR():
    pass

# print a listing of the current program in memory
# expects either "LIST" or "LIST <line number>"
def _LIST(tokens):
    # don't LIST if we're running a stored program
    if executing:
        raise BasLangError("cannot LIST while the program is running")
    
    # if the user supplies a line number, try to print just that line
    elif line_number := tokens.peek(False):
        next(tokens) # consume the next (presumably line number) token
        if not line_number.isnumeric():
            raise BasLangError(f"LIST expects an integer, found {line_number}") 
        # if the user types a line number that doesn't exist, raise an error
        try:
            tokens = program_lines[int(line_number)]
            print(f"{line_number}", end=' ')
            tokens.seek(1) # go to second item of token stream, SKIPPING the line number
            for token in tokens:
                print(token, end=' ')
            print()
        except KeyError:
            raise BasLangError(f"line {line_number} not found")
    
    # otherwise, print all the lines in order
    else:
        for (line, tokens) in sorted(program_lines.items()):
            tokens.seek(1) # rewind to beginning of token stream, then skip the line number

            print(str(line), end=' ')
            for token in tokens:
                print(token, end=' ')
            print()


# begin execution of the stored program. can only be called from command-line
# mode, not from the stored program itself
def _RUN():
    global line, executing
    # if the program is already running when we call RUN, raise an error
    if executing:
        raise BasLangError("cannot call RUN from an already running program")
    
    # otherwise, begin running
    executing = True
    lines = sorted(list(program_lines.keys())) # an ordered list of all program line numbers
    if len(lines) == 0:
        raise BasLangError("cannot RUN an empty program")
    
    line = lines[0]
    while executing:
        ### retireve the current line and prepare to move to the next line, if any
        line_index = lines.index(line) + 1
        tokens = program_lines[line]
        ### try to run the program
        try:
            old_line_number = line
            tokens.seek(1) # rewind token stream, skipping the line number token

            _statement(tokens) # execute the statement

            # if the executed statement hasn't modified the line number
            # (basically if no GOTO or GOSUB happened)
            if old_line_number == line:
                # if we just executed the last line, stop execution
                if line == lines[-1]:
                    executing = False
                # otherwise, advance to the next line
                else:
                    line = lines[line_index]
            
        
        ### if there's a problem, raise an error that includes the line number
        except BasLangError as err:
            raise BasLangError(f"(line {line}) {err}")
        ### if the user hits CTRL-c to keyboard interrupt, we stop
        except KeyboardInterrupt:
            print(f"User break on {line}")
            executing = False
        ### if we run out of lines, the program simply ends
        except IndexError: # we've reached the end of the program
            executing = False
            return


def _END():
    pass

# if we encounter a comment, skip the "comment" token and continue
def _REM(tokens):
    next(tokens)


if __name__ == "__main__":
    main()

