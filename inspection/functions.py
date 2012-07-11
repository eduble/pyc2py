#!/usr/bin/python2
from decompile import decompile_func_body
from tools import print_doc_string, print_code, print_code_line
import inspect

def show_function(func_name, func, known_globals, indent=0):
	f_args = inspect.getargspec(func)
	func_args = inspect.formatargspec(f_args.args, f_args.varargs, f_args.keywords, f_args.defaults)
	print_code_line(indent, 'def %s%s:' % (func_name, func_args))
	print_doc_string(indent+1, func)
	print_code(decompile_func_body(func.func_code, known_globals, indent+1))



