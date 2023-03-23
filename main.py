#!/usr/bin/env python3

######
# A toy implementation of BASIC, for my own fun and entertainment.
# I'm loosely following the grammar I found on wikipedia:
# https://en.wikipedia.org/wiki/BASIC_interpreter
######


import re
from toyBasicTypes import BasLangError

program_environment = {}
program_lines = {}

# think I've finally got it working
# here's the breakdown:  |keywords|   numbers   |      strings      | relops |valid symbols | everything else
tokenizer = re.compile(r"([a-z]\w*|\d+(?:\.\d+)?|(?:\"(?:\\.|.)*?\")|>=|<=|!=|[()+\-*\/>=<,]|[^\s\w]+)", flags=re.IGNORECASE)
# strings allow for escaped quotes. mismatched quotes result in a single " being captured,
# so if a token is just a single quote I know I can report a mismatched quotes error.
# keywords also includes valid variable names. numbers match both ints and floats.
# yeesh, this was a pain to get working. regexes are hard.

def main():
    while True:
        tokens = tokenizer.findall(input("> ").upper())
        if tokens[0] == "QUIT": #todo add run
            break
        try:
            _line(tokens)
        except BasLangError as err:
            print(err)


def _line(tokens):
    line_start = tokens[0]
    if line_start[0].isnumeric():
        try:
            line_number = int(line_start)
        except ValueError:
            raise BasLangError("Line numbers must be integers: " + line_start + "is invalid")
        program_lines[line_number] = tokens[1:]
    else:
        _statement(tokens)

# todo account for empty statements
def _statement(tokens):
    word = tokens[0]
    if word == "PRINT":
        _PRINT(tokens[1:])
    elif word == "IF":
        _IF(tokens[1:])
    elif word == "GOTO":
        _GOTO(tokens[1:])
    elif word == "INPUT":
        _INPUT(tokens[1:])
    elif word == "LET":
        _LET(tokens[1:])
    elif word == "GOSUB":
        _GOSUB(tokens[1:])
    elif word == "RETURN":
        _RETURN(tokens[1:])
    elif word == "CLEAR":
        _CLEAR(tokens[1:])
    elif word == "LIST":
        _LIST(tokens[1:])
    elif word == "RUN":
        _RUN(tokens[1:])
    elif word == "END":
        _END(tokens[1:])
    elif word == "REM":
        _REM(tokens[1:])
    else:
        raise BasLangError("Unknown symbol " + word)

def _expr_list(tokens):
    

def _var_list(text):
    return [_var(x.trim()) for x in text.split(',')]

def _expression(text):
    index = 0
    sign_match = re.match(r"+|-", text)
    if sign_match:
        sign = sign_match.string()
        index = sign_match.end()
    else:
        sign = '+'
    value, index = _term(text)
    if sign == '-':
        value *= -1
    return value + _expression(text[index:])

def _term(text):
    value, index = _factor(text)
    if index < len(text):
        op_match




