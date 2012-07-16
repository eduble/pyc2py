# pyc2py - The smart python decompiler.    
# Copyright (C) 2012  Centre National de la Recherche Scientifique
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Developper: Etienne Duble
# Contact me at: etienne _dot_ duble _at_ imag _dot_ fr

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

