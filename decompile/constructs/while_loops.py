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

from const import NORMAL_FLOW, END_OF_CONSTRUCT, WHILE_CLAUSE
from decompile.constructs.conditionals import \
	update_next_indexes_of_conditional, update_pop_clauses_of_conditional

BEFORE_SETUP_LOOP = 0
AFTER_SETUP_LOOP = 1

def turn_if_to_while(elem, next_index_in_sequence):
	elem['mnemo'] = 'WHILE_LOOP'
	# we must also update the clauses describing this construct
	jump_clause, forward_clause = (END_OF_CONSTRUCT, WHILE_CLAUSE)
	pop_cond = elem['pop_cond']
	forward_index = next_index_in_sequence
	jump_index = elem['jump_index']
	update_next_indexes_of_conditional(elem, 
			jump_clause, jump_index, forward_clause, forward_index)
	update_pop_clauses_of_conditional(elem, pop_cond, jump_clause, forward_clause)

def recognise_while_loops(asm_indexes, indexed_asm):
	while_loop_indexes = []
	state = BEFORE_SETUP_LOOP
	for i in range(len(asm_indexes)):
		index = asm_indexes[i]
		elem = indexed_asm[index]
		mnemo = elem['mnemo']
		if state == BEFORE_SETUP_LOOP:
			if mnemo == 'SETUP_LOOP':
				state = AFTER_SETUP_LOOP
				loop_index = None
		else:
			if loop_index == None:
				loop_index = index # the index just after SETUP_LOOP
			if mnemo == 'FOR_LOOP':
				# this is actually a for loop, not while, give up
				state = BEFORE_SETUP_LOOP
			elif mnemo == 'IF_CONSTRUCT' and \
				'forced_index' not in elem:
				# this is actually a while loop! :)
				while_loop_indexes.append(loop_index)
				next_index_in_sequence = asm_indexes[i+1]
				turn_if_to_while(elem, next_index_in_sequence)
				state = BEFORE_SETUP_LOOP # done, look for next one			
	for elem in indexed_asm.values():
		if 		elem['mnemo'] == 'JUMP_ABSOLUTE' and \
				elem['next_indexes'][NORMAL_FLOW] in while_loop_indexes:
			#print '#Changing a jump to %d into a "continue" instruction' % elem['next_indexes'][NORMAL_FLOW]
			elem['mnemo'] = 'CONTINUE'
			elem['next_indexes'] = {}


