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

from decompile import decompile_func_body
from tools import print_doc_string, print_code, print_code_line
import inspect

def show_function(func_name, func, known_globals, indent=0):
	f_args = inspect.getargspec(func)
	func_args = inspect.formatargspec(f_args.args, f_args.varargs, f_args.keywords, f_args.defaults)
	print_code_line(indent, 'def %s%s:' % (func_name, func_args))
	print_doc_string(indent+1, func)
	print_code(decompile_func_body(func.func_code, known_globals, indent+1))



