#!/usr/bin/python2
from inspection.data import get_data
from inspection.functions import show_function
from tools import print_doc_string, print_code_line
import inspect

def show_class(class_name, cls, known_globals):
	base_names = []
	for base in cls.__bases__:
		baseclass_fullname = str(base).split("'")[1]
		baseclass_name = baseclass_fullname.split('.')[-1]
		base_names.append(baseclass_name)
	print 'class %s(%s):' % (class_name, ', '.join(base_names))
	print_doc_string(1, cls)
	# retrieve class attributes
	for name, value in get_data(cls):	
		print_code_line(1, name + ' = ' + repr(value))
	# retrieve methods
	for class_attr in inspect.classify_class_attrs(cls):
		#print '#', class_attr 
		name, kind, owner_cls, attr = class_attr
		# a method may be inherited from a parent class
		# we want to only print methods defined in this 
		# object.
		# also we only print methods.
		if owner_cls == cls and kind != 'data':
			show_function(name, attr, known_globals, indent=1)
			print
#			print class_name, name
#			if class_name.startswith('rs232') and name == 'reset':
	print

