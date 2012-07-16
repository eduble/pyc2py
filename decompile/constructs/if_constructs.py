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

from const import IF_CLAUSE, ELSE_CLAUSE, CONDITIONAL_JUMPS_DESC
from decompile.constructs.conditionals import update_next_indexes_of_conditional, \
	update_pop_clauses_of_conditional
from decompile.disassemble import parse_absolute_index_from_elem_indic

IF_CONSTRUCT_CLAUSES = { True: IF_CLAUSE, False: ELSE_CLAUSE }

def get_jump_index_of_conditional(elem, desc):
	# depending on the python version the jump
	# index may be given relative or absolute
	if desc['relative']:
		jump_index = parse_absolute_index_from_elem_indic(elem)
	else:
		jump_index = elem['arg']
	return jump_index

def get_if_jump_and_forward_clauses(jump_condition):
	forward_condition = not jump_condition
	jump_clause = IF_CONSTRUCT_CLAUSES[jump_condition]
	forward_clause = IF_CONSTRUCT_CLAUSES[forward_condition]
	return jump_clause, forward_clause
	
def prepare_if_element(elem, mnemo, next_index_in_sequence):
	desc = CONDITIONAL_JUMPS_DESC[mnemo]
	jump_cond = desc['jump_cond']
	elem['jump_cond'] = jump_cond	# useful for while loops
	jump_clause, forward_clause = get_if_jump_and_forward_clauses(jump_cond)
	jump_index = get_jump_index_of_conditional(elem, desc)
	elem['jump_index'] = jump_index # useful for while loops
	forward_index = next_index_in_sequence
	pop_cond = desc['pop_cond']
	elem['pop_cond'] = pop_cond		# useful for while loops
	update_next_indexes_of_conditional(elem, 
			jump_clause, jump_index, forward_clause, forward_index)
	update_pop_clauses_of_conditional(elem, pop_cond, jump_clause, forward_clause)
	elem['mnemo'] = 'IF_CONSTRUCT'
	elem['apply_conditions'] = []
	elem['dup_cond'] = False
