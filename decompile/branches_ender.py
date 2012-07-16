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
