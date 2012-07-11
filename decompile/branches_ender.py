#!/usr/bin/python2

from tree_traversal import TreeTraversal

class BranchesEnder(TreeTraversal):
	def __init__(self, elems):
		TreeTraversal.__init__(self, elems)
	
	def handle_traversed_element(self, elem, end_of_constructs):
		index = elem['index']
		next_indexes = elem['next_indexes']
		for next_index_type in next_indexes.copy():
			next_index = next_indexes[next_index_type]
			if next_index in end_of_constructs:
				# if jumping to the end of another construct
				if index != end_of_constructs[next_index]:
					del next_indexes[next_index_type]
