#!/usr/bin/env python3

######
# A toy implementation of BASIC, for my own fun and entertainment.
# I'm loosely following the grammar I found on wikipedia:
# https://en.wikipedia.org/wiki/BASIC_interpreter
######


import re                       # for tokenizing input
import more_itertools as m_it   # for peeking at the first item of the token iterator

from toyBasicTypes import *

program_environment = {}
program_lines = {}
executing = False
line = 0

# think I've finally got it working
# here's the breakdown:  |keywords|   numbers   |      strings      | relops |valid symbols | everything else
tokenizer = re.compile(r"([a-z]\w*|\d+(?:\.\d+)?|(?:\"(?:\\.|.)*?\")|>=|<=|!=|[()+\-*\/>=<,]|[^\s\w]+)", flags=re.IGNORECASE)
# strings allow for escaped quotes. mismatched quotes result in a single " being captured,
# so if a token is just a single quote I know I can report a mismatched quotes error.
# keywords also includes valid variable names. numbers match both ints and floats.
# yeesh, this was a pain to get working. regexes are hard.

def main():
    global executing, line, program_environment, program_lines
    while True:
        # an iterator over all tokens is the input, with the ability to peek at the first one
        tokens = m_it.peekable(tokenizer.finditer(input("> ").upper()))
        if tokens[0] == "QUIT": #todo add run
            break
        try:
            _line(tokens)
        except BasLangError as err:
            print(err)


def _line(tokens):
    line_start = tokens.peek()
    if line_start.isnumeric():
        line_number = int(line_start)
        tokens.next()
        program_lines[line_number] = tokens
    else:
        _statement(tokens)

# todo account for empty statements
def _statement(tokens):
    word = tokens.next()
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
    elif word == "RUN":
        _RUN(tokens)
    elif word == "END":
        _END(tokens)
    elif word == "REM":
        _REM(tokens)
    else:
        raise BasLangError("Unknown symbol " + word)

#####
# The parser, more or less
#####

def _expr_list(tokens):
    values_list = [_expr_or_string(tokens)]
    while next_token := tokens.peek(False):
        if next_token != ',':
            raise BasLangError('expressions must be separated by a ","')
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
    first_token = tokens.peek()
    sign = "+"
    if first_token in "+-":
        sign = first_token
        next(tokens)
    value = _term(tokens)
    if sign == "-":
        value.value *= -1

    while (next_token := tokens.peek('')) in "+-":
        sign = next_token
        next(tokens)
        if sign == "+":
            value = value.add(_term(tokens))
        elif sign == "-":
            value = value.sub(_term(tokens))
    return value

def _string(tokens):
    next_token = next(tokens)
    if len(next_token) == 1:
        raise BasLangError('unmatched "')

def _term(tokens) -> BasLangValue:
    value = _factor(tokens)
    while (next_token := tokens.peek('')) in "*/":
        op = next_token
        next(tokens)
        if op == "*":
            value = value.mul(_factor(tokens))
        elif op == "/":
            value = value.div(_factor(tokens))
    return value

def _factor(tokens) -> BasLangValue:
    next_token = next(tokens)
    if next_token == "(":
        value = _expression(tokens)
        close_paren = next(tokens)
        if close_paren != ")":
            raise BasLangError('expected "(", found ' + close_paren)
        return value
    elif next_token[0].isnumeric:
        try:
            return BasLangValue(init_value=next_token)
        except ValueError:
            raise BasLangError(str(next_token) + ' is not a valid number')
    elif not is_identifier(next_token):
        raise BasLangError(next_token + " is not a valid identifier")
    else:
        try:
            value = program_environment[next_token]
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

def is_identifier(string: str) -> bool:
    return string == re.match("[A-Z]\w*", string, flags=re.IGNORECASE)[0]


#####
# Language constructs
#####

def _PRINT(tokens):
    args = _expr_list(tokens)
    for arg in args:
        print(arg, end='\t')

def _IF(tokens):
    value1 = _expr_or_string(tokens)
    valid_states = _relop(tokens)
    value2 = _expr_or_string(tokens)
    result = value1.compare(value2)
    if result in valid_states:
        then = next(tokens)
        if then != "THEN":
            raise BasLangError("expected keyword THEN, found " + then)
        _statement(tokens)

def _GOTO():
    pass

def _INPUT():
    pass

def _LET():
    pass

def _GOSUB():
    pass

def _RETURN():
    pass

def _CLEAR():
    pass

def _LIST():
    pass

def _RUN():
    pass

def _END():
    pass

def _REM():
    pass




