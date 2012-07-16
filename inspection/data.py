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
