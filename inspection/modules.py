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



