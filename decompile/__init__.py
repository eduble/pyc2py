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

from decompile.bloc import decompile_bloc
from decompile.constructs import analyse_structures
from decompile.disassemble import disassemble_code


def decompile_func_body(func_code, known_globals, body_indent):
	asm_indexes, indexed_asm = disassemble_code(func_code)
	asm_indexes, indexed_asm = analyse_structures(asm_indexes, indexed_asm)
	return decompile_bloc(
			indexed_asm, func_code, known_globals, index=asm_indexes[0], indent=body_indent, 
			is_top_level_bloc=True)
	






