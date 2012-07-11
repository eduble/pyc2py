#!/usr/bin/python2
import inspect

def isdata(attr):
	"""Check if an object is of a type that probably means it's data."""
	return not (inspect.ismodule(attr) or inspect.isclass(attr) or
                inspect.isroutine(attr) or inspect.isframe(attr) or
                inspect.istraceback(attr) or inspect.iscode(attr))

def visiblename(name):
	"""Decide whether to show a data variable."""
	_hidden_names = ('__builtins__', '__doc__', '__file__', '__path__',
	             '__module__', '__name__', '__slots__', '__package__',
	             '__dict__', '__weakref__')
	return not name in _hidden_names

def can_be_evaluated(value):
	"""Check if the textual representation of this value 
	can be re-read."""
	try:
		eval(repr(value))
	except:
		return False
	return True

def get_data(obj):
	"""Retrieve internal data attributes of an object."""
	data = []
	for key, value in inspect.getmembers(obj, isdata):
		if visiblename(key):
			if not can_be_evaluated(value):
				value = None
			data.append((key, value))
	return data
