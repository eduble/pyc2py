#!/usr/bin/env python2

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


from inspection.modules import show_module
import os
import sys

def usage():
	print "Usage:", sys.argv[0], '<path/to/file.pyc>'

if len(sys.argv) < 2:
	usage()
	sys.exit(1)
	
file_path = sys.argv[1]
module_dir = os.path.dirname(file_path)
if module_dir != '':
	sys.path.append(module_dir)
module_name, ext = os.path.splitext(os.path.basename(file_path))
mod = __import__(module_name)

show_module(mod)

