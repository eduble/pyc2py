#!/usr/bin/python2
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



