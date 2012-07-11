#!/usr/bin/python

def print_doc_string(indent, obj):
    doc_string = obj.__doc__
    if doc_string:
        lines = doc_string.splitlines()
        if len(lines) < 2:
            print_code_line(indent, '"""' + doc_string + '"""')
        else:
            print_code_line(indent, '"""')
            for line in lines:
                print_code_line(indent, line)
            print_code_line(indent, '"""')

def print_code(statements):
    for statement in statements:
        indent, text = statement
        space = ('%' + str(2*indent) + 's') % ''
        print '%s%s' % (space, text)

def print_code_line(indent, statement):
    print_code([(indent, statement)])
