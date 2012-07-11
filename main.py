#!/usr/bin/python2

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

