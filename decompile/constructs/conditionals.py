#!/usr/bin/python2
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
