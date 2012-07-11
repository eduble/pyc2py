#!/usr/bin/python2
from const import EXCEPT_CLAUSE, TRY_CLAUSE, EXCEPT_EXPRESSION_CLAUSE
from decompile.disassemble import parse_absolute_index_from_elem_indic

def analyse_except_startup_code(elems, next_asm_indexes, except_index):
	# there are different kinds of startup clauses, 
	# as shown in the following examples:
	# 'except:'
	# 'except Exception:'
	# 'except Exception, e:'
	# we analyse it here.
	# We also have to remove 3 (or 4) POP_TOP instructions.	
	info = {
		'except_expression_index': None,
		'except_target': None
	}
	index = except_index
	pop_top_to_be_removed = 3
	while pop_top_to_be_removed > 0:
		elem = elems[index]
		next_index = next_asm_indexes[index]
		if elem['mnemo'] == 'DUP_TOP':
			info['except_expression_index'] = next_index
			pop_top_to_be_removed += 1
		elif elem['mnemo'] == 'COMPARE_OP':
			if elem['indic'] == 'exception match':
				elem['mnemo'] = 'END_OF_CLAUSE'
		elif elem['mnemo'] == 'STORE_FAST':
			info['except_target'] = elem['indic']
			pop_top_to_be_removed -= 1
		elif elem['mnemo'] == 'POP_TOP':
			pop_top_to_be_removed -= 1
		index = next_index
	info['except_adapted_index'] = index
	return info

def prepare_try_element(elems, next_asm_indexes, 
						elem, next_index_in_sequence):
	elem['mnemo'] = 'TRY_CONSTRUCT' # update name for clarity
	next_indexes = {}
	except_index = parse_absolute_index_from_elem_indic(elem)
	except_info = analyse_except_startup_code(
						elems, next_asm_indexes, except_index)
	except_expr_index = except_info['except_expression_index']
	if except_expr_index != None:
		next_indexes[EXCEPT_EXPRESSION_CLAUSE] = \
							except_info['except_expression_index'] 
	next_indexes[EXCEPT_CLAUSE] = except_info['except_adapted_index'] 
	next_indexes[TRY_CLAUSE] = next_index_in_sequence 
	elem['next_indexes'] = next_indexes
	elem['except_target'] = except_info['except_target']
	elem['except_expression'] = None # if any, we don't know it yet anyway

def format_except_statement(try_construct_elem):
	statement = "except"
	except_expression = try_construct_elem['except_expression']
	except_target = try_construct_elem['except_target']
	if except_expression != None:
		statement += ' ' + except_expression
		if except_target != None:
			statement += ', ' + except_target
	return statement + ":"