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

from binary_ops import manage_binary_op
from const import PARTIAL_STATEMENT, BRANCH_IS_OPTIONAL, COMPLETE_STATEMENT, \
	ELSE_CLAUSE, TRY_CLAUSE, FINALLY_CLAUSE, IF_CLAUSE, FOR_CLAUSE, EXCEPT_CLAUSE, \
	EXCEPT_EXPRESSION_CLAUSE, WHILE_CLAUSE
from decompile.boolean_conditions import OR_CONDITION
from decompile.branch_info import BranchDecompilationInfo
from decompile.constructs.try_constructs import format_except_statement
from decompile.embedded_functions import pack_function_object
from decompile.unary_ops import manage_unary_op
from tree_traversal import TreeTraversal
import decompile.embedded_functions

# only when static, see below
BRANCH_PRELIMINARY_STATEMENT  = {
    ELSE_CLAUSE: "else:",
    TRY_CLAUSE: "try:",
    FINALLY_CLAUSE: "finally:",
    EXCEPT_EXPRESSION_CLAUSE: None
}

class Decompilator(TreeTraversal):
	def __init__(self, elems, func_code, known_globals):
		TreeTraversal.__init__(self, elems)
		self.func_code = func_code
		self.known_globals = known_globals
		self.bypass_next = False
	
	def build_compound_object(self, info, size, start_char, end_char):
		objs = []
		for _ in range(size): 
			objs.insert(0, info.pop())
		info.push(start_char + ', '.join(objs) + end_char, PARTIAL_STATEMENT)
		
	def pop_condition_if_needed(self, branch_info, construct_elem, branch_type):
		pop_clauses = construct_elem['pop_clauses']
		if branch_type in pop_clauses:
			branch_info.pop()
	
	def unpack_sequence(self, info, num):
		sequence_statement = info.pop();
		variables = [ 'item' + str(i) for i in range(num) ]
		info.push(', '.join(variables) + ' = ' + sequence_statement,
					COMPLETE_STATEMENT)
		variables.reverse()
		for var in variables:
			info.push(var, PARTIAL_STATEMENT)
	
	def get_branch_preliminary_statement(self, construct_elem, branch_type, info):
		statement = None
		if branch_type == IF_CLAUSE:
			# keep condition on the stack for now
			# but ensure that it is flagged as a PARTIAL_STATEMENT.
			# Otherwise, if it was a CANDIDATE_STATEMENT,
			# and a POP_TOP instruction follows,
			# we would validate this statement although the condition
			# has already been taken into account in this 'if' statement. 
			condition = info.pop()
			info.push(condition, PARTIAL_STATEMENT)	
			statement = 'if ' + condition + ':'
		elif branch_type == FOR_CLAUSE:
			statement = 'for ' + construct_elem['var'] + \
							' in ' + info.pop() + ':'
		elif branch_type == EXCEPT_CLAUSE:
			statement = format_except_statement(construct_elem)
		elif branch_type == WHILE_CLAUSE:
			jump_cond = construct_elem['jump_cond']
			condition = info.top()	# keep condition on the stack for now
			if jump_cond == True:
				# we leave the loop when the condition is True, then...
				statement = 'while not (' + condition + '):'
			else:
				# we leave the loop when the condition is False, then...
				statement = 'while ' + condition + ':'
		else:
			statement = BRANCH_PRELIMINARY_STATEMENT[branch_type]
		return statement
		
	def handle_new_branch_traversed(self, branch_type, jump_index, branch_start_index, info):
		construct_elem = self.elems[jump_index]
		preliminary_statement = self.get_branch_preliminary_statement(
										construct_elem, branch_type, info)
		if (preliminary_statement != None):
			preliminary_statement = (info.get_indent(), preliminary_statement)
		new_info = BranchDecompilationInfo(
						info.get_indent()+1, 
						stack=info.get_stack()[:], # copy
						optional_bloc=BRANCH_IS_OPTIONAL[branch_type],
						preliminary_statement=preliminary_statement
					)
		mnemo = construct_elem['mnemo']
		if mnemo in [ 'IF_CONSTRUCT', 'WHILE_LOOP' ]:
			self.pop_condition_if_needed(new_info, self.elems[jump_index], branch_type) 
		return new_info
	
	def handle_end_of_child_branch(self, branch_type, jump_index, 
								child_branch_info, parent_branch_info):
		if branch_type == EXCEPT_EXPRESSION_CLAUSE:
			try_elem = self.elems[jump_index]
			try_elem['except_expression'] = child_branch_info.pop()
		else:
			child_statements = child_branch_info.retrieve_statements()
			parent_branch_info.append_bloc_of_statements(child_statements)
			child_global_variables = child_branch_info.retrieve_global_variables()
			parent_branch_info.append_global_variables(child_global_variables)
	
	def comment(self, elem):
		return ' # ' + str(elem['index'])
	
	def handle_traversed_element(self, elem, info):
		#print "handle_traversed_element(), elem =", elem
		mnemo = elem['mnemo']
		indic = elem['indic']
		arg = elem['arg']
		if elem['decompiled']:
			info.warning('bytecode traversed several times')
		else:
			elem['decompiled'] = True # record that we passed through this
		if self.bypass_next:
			# bypass this element and
			# reset the variable to False for the next one. 
			self.bypass_next = False
		elif mnemo in [ 'LOAD_FAST', 'LOAD_GLOBAL', 'LOAD_CONST' ]:
			info.record_loading_of_variable(self.known_globals, mnemo, indic)
			info.push(indic, PARTIAL_STATEMENT)
		elif mnemo == 'LOAD_CONST_CODE':
			code_object = self.func_code.co_consts[arg]
			info.push(code_object, PARTIAL_STATEMENT)
		elif mnemo == 'MAKE_FUNCTION':
			pack_function_object(info, arg)
		elif mnemo in [ 'STORE_FAST', 'STORE_GLOBAL' ]:
			variable = indic
			value = info.pop()
			if type(value).__name__ != 'str':
				# this is supposedly an embedded function object
				decompile.embedded_functions.format_embedded_function(
									self.known_globals, variable, value, info)
			else:
				statement = variable + " = " + value
				info.push(statement, COMPLETE_STATEMENT)
		elif mnemo == 'UNPACK_SEQUENCE':
			self.unpack_sequence(info, arg)
		elif mnemo == 'LOAD_ATTR':
			s = info.pop()
			s += "." + indic
			info.push(s, PARTIAL_STATEMENT)
		elif mnemo == 'BUILD_MAP': # create a dictionary object
			info.push('{}', PARTIAL_STATEMENT)
		elif mnemo == 'STORE_ATTR':
			obj = info.pop()
			value = info.pop()
			statement = obj + "." + indic + " = " + value
			info.push(statement, COMPLETE_STATEMENT)
		elif mnemo == 'POP_TOP':
			info.delete_top()
		elif mnemo == 'DUP_TOP':
			info.dup_top()
		elif mnemo.startswith('ROT_'):
			info.rotate(mnemo)
		elif mnemo.startswith('CALL_FUNCTION'):
			info.function_call(mnemo, arg)
		elif mnemo == 'SLICE+0':
			obj = info.pop()
			info.push(obj + '[:]', PARTIAL_STATEMENT)
		elif mnemo == 'SLICE+1':
			sl = info.pop()
			obj = info.pop()
			info.push(obj + '[' + sl + ':]', PARTIAL_STATEMENT)
		elif mnemo == 'SLICE+2':
			sl = info.pop()
			obj = info.pop()
			info.push(obj + '[:' + sl + ']', PARTIAL_STATEMENT)
		elif mnemo == 'SLICE+3':
			sl_end = info.pop()
			sl_start = info.pop()
			obj = info.pop()
			info.push(obj + '[' + sl_start + ':' + sl_end + ']', PARTIAL_STATEMENT)
		elif mnemo == 'COMPARE_OP':
			obj2 = info.pop()
			obj1 = info.pop()
			info.push(obj1 + ' ' + indic + ' ' + obj2, PARTIAL_STATEMENT)
		elif mnemo == 'BUILD_TUPLE':
			size = arg
			if size == 1:
				# special case of tuples with 1 element
				info.push('(' + info.pop() + ',)', PARTIAL_STATEMENT)
			else:
				self.build_compound_object(info, size, '(', ')')
		elif mnemo == 'BUILD_LIST':
			self.build_compound_object(info, arg, '[', ']')
		elif mnemo == 'JUMP_ABSOLUTE': 	# nothing to do, next_index is already aware about the jump
			pass
		elif mnemo == 'RETURN_VALUE':
			value = info.pop()
			info.push('return ' + value, COMPLETE_STATEMENT)
			# next_indexes is empty, so it will stop below
		elif mnemo == 'YIELD_VALUE':
			value = info.pop()
			info.push(value, COMPLETE_STATEMENT)
			# next_indexes is empty, so it will stop below
		elif 	mnemo.startswith('BINARY_') or \
				mnemo.startswith('INPLACE_'):
			manage_binary_op(mnemo, info)
		elif 	mnemo.startswith('UNARY_'):
			manage_unary_op(mnemo, info)
		elif mnemo == 'STORE_SUBSCR':
			TOS = info.pop()
			TOS1 = info.pop()
			TOS2 = info.pop()
			info.push(TOS1 + '[' + TOS + '] = ' + TOS2, COMPLETE_STATEMENT)
		elif mnemo == 'STORE_MAP':
			# add a key-value pair in a dictionary
			key = info.pop()
			value = info.pop()
			d = info.pop()
			element = key + ': ' + value
			if d == '{}':
				info.push('{ ' + element + ' }', PARTIAL_STATEMENT)
			else:
				# d[:-1] will remove the ending '}'
				info.push(d[:-1] + ', ' + element + ' }', PARTIAL_STATEMENT)
		elif mnemo == 'PRINT_ITEM':
			TOS = info.pop()
			info.push('print ' + TOS + ',', COMPLETE_STATEMENT)
		elif mnemo == 'PRINT_NEWLINE':
			info.push('print', COMPLETE_STATEMENT)
		elif mnemo == 'RAISE_VARARGS':
			raise_args = []
			for _ in range(arg):
				raise_args.append(info.pop())
			statement = 'raise ' + ', '.join(raise_args)
			info.push(statement, COMPLETE_STATEMENT)
		elif mnemo == 'BREAK_LOOP':
			info.push('break', COMPLETE_STATEMENT)
		elif mnemo == 'CONTINUE':
			info.push('continue', COMPLETE_STATEMENT)
		elif mnemo == 'GET_ITER':
			# we consider it is a list comprehension
			# (other uses not handled yet)
			decompile.embedded_functions.handle_list_comprehension(
													self.known_globals, info)
			# bypass the following 'CALL_FUNCTION' instruction,
			# we handled everything here
			self.bypass_next = True
		elif mnemo in [ 'IF_CONSTRUCT', 'WHILE_LOOP' ]:
			condition = info.pop()
			for cond_type in elem['apply_conditions']:
				if cond_type == OR_CONDITION:
					bool_op = ' or '
				else:
					bool_op = ' and '
				condition = '(' + info.pop() + bool_op + condition + ')'
			info.push(condition, PARTIAL_STATEMENT)
			if elem['dup_cond']:
				info.push(condition, PARTIAL_STATEMENT)
		elif mnemo in [ 'SETUP_LOOP', 'POP_BLOCK', 'PASS', 
					'TRY_CONSTRUCT', 'FOR_LOOP', 'WHILE_LOOP',
					'END_OF_CLAUSE' ]:
			pass
		else:
			info.print_stack()
			raise Exception("Unknown instruction %s. Sorry." % mnemo)
