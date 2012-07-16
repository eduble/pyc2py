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

from const import NO_CLAUSE, ANY_CLAUSE, FORWARD_CLAUSE, JUMP_CLAUSE

def update_pop_clauses_of_conditional(elem, pop_condition, jump_clause, forward_clause):
	if pop_condition == NO_CLAUSE:
		pop_clauses = []
	elif pop_condition == ANY_CLAUSE:
		pop_clauses = [ jump_clause, forward_clause ]
	elif pop_condition == FORWARD_CLAUSE:
		pop_clauses = [ forward_clause ]
	elif pop_condition == JUMP_CLAUSE:
		pop_clauses = [ jump_clause ]
	elem['pop_clauses'] = pop_clauses

def update_next_indexes_of_conditional(elem, jump_clause, jump_index,
								forward_clause, forward_index):
	next_indexes = {}
	next_indexes[jump_clause] = jump_index 
	next_indexes[forward_clause] = forward_index
	elem['next_indexes'] = next_indexes
