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


from const import NORMAL_FLOW, END_OF_CONSTRUCT

class TreeTraversal(object):
	def __init__(self, elems):
		self.elems = elems
		self.previous_element = None
	def get_previous_elem(self):
		return self.previous_element
	def handle_traversed_element(self, elem, data):
		pass # override in subclass if needed
	def handle_new_branch_traversed(self, branch_type, jump_index, branch_start_index, parent_branch_data):
		return parent_branch_data # override in subclass if needed
	def handle_end_of_child_branch(self, branch_type, jump_index, child_branch_data, parent_branch_data):
		pass # override in subclass if needed
	def traverse(self, index=0, data={}, previous_elem=None):
		self.previous_element = previous_elem
		while True:
			elem = self.elems[index]
			#print '#traversing element ' + str(index), elem
			should_continue = self.handle_traversed_element(elem, data)
			if should_continue == False:
				break
			curr_index = elem['index']
			next_indexes = elem['next_indexes']
			self.previous_element = elem # if we do not break the loop below
			if 'forced_index' in elem:
				index = elem['forced_index']
			elif len(next_indexes) == 0:
				break	# end of a branch
			elif NORMAL_FLOW in next_indexes:
				index = next_indexes[NORMAL_FLOW] # continue with next instruction
			else:
				should_continue = False
				for branch_type in sorted(next_indexes):
					if branch_type == END_OF_CONSTRUCT:
						should_continue = True
						break
					branch_start_index = next_indexes[branch_type]
					new_data = self.handle_new_branch_traversed(
								branch_type, curr_index, 
								branch_start_index, data)
					self.traverse(index=branch_start_index, data=new_data, 
									previous_elem=elem)
					self.handle_end_of_child_branch(
								branch_type, curr_index, new_data, data)
				if should_continue:
					index = next_indexes[END_OF_CONSTRUCT]
				else:
					break	# no more code after this construct



