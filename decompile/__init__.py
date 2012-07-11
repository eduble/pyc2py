#!/usr/bin/python2
from decompile.bloc import decompile_bloc
from decompile.constructs import analyse_structures
from decompile.disassemble import disassemble_code


def decompile_func_body(func_code, known_globals, body_indent):
	asm_indexes, indexed_asm = disassemble_code(func_code)
	asm_indexes, indexed_asm = analyse_structures(asm_indexes, indexed_asm)
	return decompile_bloc(
			indexed_asm, func_code, known_globals, index=asm_indexes[0], indent=body_indent, 
			is_top_level_bloc=True)
	






