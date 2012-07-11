#!/usr/bin/python2
from const import NORMAL_FLOW, FOR_CLAUSE, END_OF_CONSTRUCT
from decompile.disassemble import parse_absolute_index_from_indic

def recognise_for_loops(asm_indexes, indexed_asm):
	last_mnemos = []
	last_indics = []
	last_indexes = []
	detected_loops = []
	for index in asm_indexes:
		elem = indexed_asm[index]
		last_mnemos.append(elem['mnemo'])
		last_mnemos = last_mnemos[-3:]
		last_indics.append(elem['indic'])
		last_indics = last_indics[-2:]
		last_indexes.append(index)
		last_indexes = last_indexes[-3:]
		if last_mnemos == [ 'GET_ITER', 'FOR_ITER', 'STORE_FAST' ]:
			detected_loops.append({
				'get_iter_index': last_indexes[-3],
				'for_iter_index': last_indexes[-2],
				'for_clause_index': elem['next_indexes'][NORMAL_FLOW],
				'end_for_index': parse_absolute_index_from_indic(
					last_indics[-2]),
				'var': last_indics[-1]
			})
	for loop in detected_loops:
		get_iter_index = loop['get_iter_index']
		for_iter_index = loop['for_iter_index']
		indexed_asm[get_iter_index]['mnemo'] = 'PASS'
		next_indexes = {}
		next_indexes[FOR_CLAUSE] = loop['for_clause_index']
		next_indexes[END_OF_CONSTRUCT] = loop['end_for_index']
		for_elem = indexed_asm[for_iter_index]
		for_elem['next_indexes'] = next_indexes
		for_elem['var'] = loop['var']
		for_elem['mnemo'] = 'FOR_LOOP'
		max_index = -1
		for elem in indexed_asm.values():
			if 		elem['mnemo'] == 'JUMP_ABSOLUTE' and \
					elem['next_indexes'][NORMAL_FLOW] == for_iter_index:
				elem['mnemo'] = 'CONTINUE'
				elem['next_indexes'] = {}
				if elem['index'] > max_index:
					max_index = elem['index']


