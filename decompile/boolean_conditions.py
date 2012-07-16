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

from const import IF_CLAUSE, ELSE_CLAUSE
from tree_traversal import TreeTraversal

OR_CONDITION = 0
AND_CONDITION = 1

def handle_boolean_conditions(indexed_asm, start_index):
	conditions_path = []
	handler = BooleanConditionsHandler(indexed_asm)
	handler.traverse(index=start_index, data=conditions_path)
	handler.store_results()

class BooleanConditionsHandler(TreeTraversal):
	def __init__(self, elems):
		TreeTraversal.__init__(self, elems)
		self.longest_condition_suite = {}
	
	def handle_new_branch_traversed(self, clause_type, jump_index, branch_start_index, 
						parent_branch_conditions_path):
		conditions_path = parent_branch_conditions_path[:] # copy
		if clause_type in [ IF_CLAUSE, ELSE_CLAUSE ]:
			cond_elem = self.elems[jump_index]
			conditions_path.append((cond_elem, clause_type))
			self.handle_boolean_suite_of_constructs(
						cond_elem, conditions_path)
		return conditions_path
	
	def analyse_consecutive_clauses(self, 
			cond_elem, conditions_path):
		num = 1
		types = []
		indexes = cond_elem['next_indexes']
		if	indexes[IF_CLAUSE] > cond_elem['index'] and \
			  indexes[ELSE_CLAUSE] > cond_elem['index']:
			while len(conditions_path) > num:
				other_elem = conditions_path[-1-num][0]
				other_indexes = other_elem['next_indexes']
				if len(other_indexes) < 2:
					break # we have already treated this element before
				elif indexes[IF_CLAUSE] == other_indexes[IF_CLAUSE]:
					# same if clause, this is an "or" operation
					types.append(OR_CONDITION)
					num += 1
				elif indexes[ELSE_CLAUSE] == other_indexes[ELSE_CLAUSE]:
					# same else clause, this is an "and" operation
					types.append(AND_CONDITION)
					num += 1
				else:
					break
		return num, types
	
	def handle_boolean_suite_of_constructs(self,
						cond_elem, conditions_path):
		num_conditions, condition_types = self.analyse_consecutive_clauses(
							cond_elem, conditions_path)
		self.update_condition_suite(cond_elem['index'], num_conditions, condition_types, conditions_path)
	
	def update_condition_suite(self, index, num_conditions, condition_types, conditions_path):
		if index in self.longest_condition_suite:
			previous_num_conditions = \
					self.longest_condition_suite[index]['num_conditions']
		else:
			self.longest_condition_suite[index] = {}
			previous_num_conditions = 0
		if num_conditions > previous_num_conditions:
			condition_suite = self.longest_condition_suite[index]
			condition_suite['num_conditions'] = num_conditions
			condition_suite['condition_types'] = condition_types
			condition_suite['conditions_path'] = conditions_path
	
	def store_results(self):
		# consider the longest suites of conditions first
		sorted_indexes = sorted(self.longest_condition_suite, 
					key=lambda index: self.longest_condition_suite[index]['num_conditions'],
					reverse=True)
		ignored_indexes = set([])
		for index in sorted_indexes:
			if index in ignored_indexes:
				continue
			condition_suite = self.longest_condition_suite[index]
			num_conditions = condition_suite['num_conditions']
			if num_conditions > 1:
				# yes, several if or else going to the same point,
				# that's an or-ed or and-ed condition.
				condition_types = condition_suite['condition_types']
				conditions_path = condition_suite['conditions_path'] 
				# record the combination of boolean conditions
				final_if_elem, clause = conditions_path[-1]
				final_if_elem['apply_conditions'] = condition_types
				# format previous if constructs accordingly
				for num in range(num_conditions-1):
					elem, clause = conditions_path[-2-num]
					# the path we took is the elected flow:
					elem['forced_index'] = elem['next_indexes'][clause]
					if clause in elem['pop_clauses']:
						elem['dup_cond'] = False
					else:
						# if the pop() operation was not specified 
						# at jump time, this means that we will
						# have a POP_TOP as the 1st instruction 
						# of the branch.
						# we want to keep the condition on the stack,
						# so we will have to duplicate it. 
						elem['dup_cond'] = True
					# elements considered in this conditions list
					# should be ignored in next ones, except
					# the first element.
					if num != num_conditions-2:
						ignored_indexes.add(elem['index'])
	
	def handle_traversed_element(self, elem, conditions_path):
		should_continue = True
		previous = self.get_previous_elem()
		if previous != None and elem['index'] < previous['index']:
			# going backward!
			should_continue = False
		return should_continue
