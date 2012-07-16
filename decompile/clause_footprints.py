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

from const import ELSE_CLAUSE, IF_CLAUSE, TRY_CLAUSE, EXCEPT_CLAUSE, ANY_CLAUSE
from decompile.tree_traversal import TreeTraversal

OPPOSITE_CLAUSES = {
			IF_CLAUSE: ELSE_CLAUSE,
			ELSE_CLAUSE: IF_CLAUSE,
			TRY_CLAUSE: EXCEPT_CLAUSE,
			EXCEPT_CLAUSE: TRY_CLAUSE	
}

CLAUSES_THAT_NEED_A_FOOTPRINT = OPPOSITE_CLAUSES.keys()

def add_clause_footprint(clause_footprints, construct_index, clause_type):
	merged = False
	if not construct_index in clause_footprints:
		clause_footprints[construct_index] = clause_type
	else:
		curr_clause_footprint = clause_footprints[construct_index]
		if curr_clause_footprint == clause_type:
			pass	# already recorded (could happen in case of 
					# 2 imbricated if constructs)
		else:	# 2 opposite clauses pass through this instruction
				# => indicate the merge (by returning True)
			clause_footprints[construct_index] = ANY_CLAUSE
			merged = True
	return merged

def record_clause_footprints(elem, clause_footprints, merge_infos):
	elem_clause_footprints = elem['clause_footprints']
	at_least_one_merge = False
	for construct_index in clause_footprints:
		merged = add_clause_footprint(
					elem_clause_footprints, 
					construct_index, 
					clause_footprints[construct_index])
		if merged: 
			if construct_index not in merge_infos:
				# first time we merge with the other branch
				# (that's the end of the if construct)
				merge_infos[construct_index] = elem['index']
			at_least_one_merge = True
	return at_least_one_merge


def get_opposite_clause(clause):
	if clause not in OPPOSITE_CLAUSES:
		raise Exception("Wrong clause number in get_opposite_clause()! Sorry.")
	else:
		return OPPOSITE_CLAUSES[clause]

# our goal here is to deduce information in order 
# to retrieve 'if then [else]' or 'try except' constructs.
# we traverse the tree and, at each instruction traversed,
# we record a 'footprint' of the current path of clauses.
# we we pass twice on the same instruction, and we observe
# that we have both opposite clauses (if and else, or try and except),
# then we know that this instruction is a merge point 
# (i.e.  we just left the construct).
class BranchMergingDetector(TreeTraversal):
	def __init__(self, elems):
		TreeTraversal.__init__(self, elems)
	
	def handle_traversed_element(self, elem, if_construct_infos):
		#if elem['mnemo'] == 'JUMP_ABSOLUTE' and elem['next_indexes'][NORMAL_FLOW] < elem['index']:
		#	raise Exception('Jumping backward at the following element. Giving up.' + elem)
		branch_clause_footprints = if_construct_infos['branch_clause_footprints']
		merge_infos = if_construct_infos['merge_infos']
		merge_point_detected = record_clause_footprints(elem, branch_clause_footprints, merge_infos)
		# if we detect a merge point we can stop the branch traversal
		# because what follows was already traversed when inspecting
		# the opposite clause.
		should_continue = not merge_point_detected
		return should_continue
	
	def handle_new_branch_traversed(self, branch_type, jump_index, branch_start_index, if_construct_infos):
		# update clause_footprints for this new branch
		#print "#BranchMergingDetector: new branch detected", branch_type, jump_index, branch_start_index, if_construct_infos
		branch_clause_footprints = if_construct_infos['branch_clause_footprints'].copy()
		branch_path = if_construct_infos['branch_path']
		branch_path = branch_path[:]
		branch_path.append(str(jump_index) + '.' + str(branch_type))
		#print branch_path
		if branch_type in CLAUSES_THAT_NEED_A_FOOTPRINT:
			cond = branch_type
			add_clause_footprint(	branch_clause_footprints,
					jump_index, 
					cond)
		return	{	'branch_clause_footprints' : branch_clause_footprints,
					'merge_infos' : if_construct_infos['merge_infos'], 
					'branch_path' : branch_path
				}
