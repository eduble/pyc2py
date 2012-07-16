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

from tools.out_saver import out_saver
import dis
import re

def disassemble(code_object):
	saver = out_saver()
	saver.start()
	dis.disassemble(code_object)
	s = saver.stop()
	return s

def disassemble_code(func_code):
	asm_indexes = []
	indexed_asm = {}
	elem = None
	for line in disassemble(func_code).splitlines():
		#print line
		if len(line.strip()) > 0:
			elem = parse_bytecode_line(line)
			index = elem['index']
			asm_indexes.append(index)
			indexed_asm[index] = elem
	return asm_indexes, indexed_asm

def parse_absolute_index_from_elem_indic(elem):
	return parse_absolute_index_from_indic(elem['indic'])

def parse_absolute_index_from_indic(indic):
	return int(indic.split()[1])

def parse_bytecode_line(line):
	m = re.match('.* ([0-9]+ \w.*)', line)
	interesting_part = m.group(1)
	words = interesting_part.split()
	index, mnemo = words[:2]
	arg = None
	indic = None
	if len(words) > 2:
		arg = int(words[2])
	m = re.match('[^(]*\((.*)\)$', interesting_part)
	if m is not None:
		indic = m.group(1)
	return 	{  	'mnemo' : mnemo,
			'arg' : arg,
			'indic': indic,
			'index': int(index),
			'decompiled': False	# for now
		}



