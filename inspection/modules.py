#!/usr/bin/python2
from inspection.classes import show_class
from inspection.functions import show_function
from inspection.data import get_data
import inspect

def is_imported_obj(mod, obj):
	obj_mod = inspect.getmodule(obj)
	return (inspect.isroutine(obj) or inspect.isclass(obj)) and \
			obj_mod != mod and \
			obj_mod.__name__ != '__builtin__'

def show_module(mod):
	
	for key, value in inspect.getmembers(mod, inspect.ismodule):
		print 'import ' + key
	for key, value in inspect.getmembers(mod, 
										lambda obj: is_imported_obj(mod, obj)):
		print 'from ' + value.__module__ + ' import ' + key

	print
	known_globals = set([])
	for name, value in get_data(mod):	
		print name, '=', repr(value)
		known_globals.add(name)
	
	print
	
	for key, value in inspect.getmembers(mod, inspect.isclass):
		if inspect.getmodule(value) == mod:
			show_class(key, value, known_globals)
	
	print
	
	for key, value in inspect.getmembers(mod, inspect.isfunction):
		if inspect.getmodule(value) == mod:
			show_function(key, value, known_globals)
			print



