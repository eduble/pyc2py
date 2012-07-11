#!/usr/bin/python2
from const import COMPLETE_STATEMENT, CANDIDATE_STATEMENT

FUNCTION_CALLS_DESC = {
		'CALL_FUNCTION': 		{ 'varargs': False, 'kw': False },
		'CALL_FUNCTION_VAR': 	{ 'varargs': True, 	'kw': False },
		'CALL_FUNCTION_KW': 	{ 'varargs': False, 'kw': True 	},
		'CALL_FUNCTION_VAR_KW': { 'varargs': True, 	'kw': True 	},
}

INT_VALUE = {
		'TWO': 2,
		'THREE': 3,
		'FOUR': 4,
}

class BranchDecompilationInfo(object):
	def __init__(self, indent, stack=[], optional_bloc=False, 
				preliminary_statement=None, is_top_level_bloc=False):
		self.stack = stack
		self.indent = indent
		self.optional_bloc = optional_bloc
		self.statements = []
		self.preliminary_statement = preliminary_statement
		self.warnings = set([])
		self.global_variables = set([])
		self.is_top_level_bloc = is_top_level_bloc
	def warning(self, text):
		self.warnings.add(text)
	def get_indent(self):
		return self.indent
	def get_stack(self):
		return self.stack
	def print_stack(self):
		print 'stack is:'
		for statement in self.stack:
			print statement[0]
	def add_statement(self, statement):
		complete_statement = statement
		if len(self.warnings) > 0:
			complete_statement += " # WARNING: " + "; ".join(self.warnings)
		self.warnings = set([])
		self.statements.append((self.indent, complete_statement))
	def append_bloc_of_statements(self, bloc_of_statements):
		self.statements += bloc_of_statements
	def append_global_variables(self, set_of_global_variables):
		self.global_variables = self.global_variables.union(set_of_global_variables)
	def push(self, obj, type_of_statement):
		if type_of_statement == COMPLETE_STATEMENT:
			self.validate_candidate_statements_if_any()
			self.add_statement(obj)
		else:
			self.stack.append((obj, type_of_statement))
	def pop(self):
		return self.stack.pop()[0]
	def top(self):
		return self.stack[-1][0]
	def delete_top(self):
		top_obj, top_type = self.stack[-1]
		if top_type == CANDIDATE_STATEMENT:
			self.add_statement(top_obj)
		self.stack.pop()
	def dup_top(self):
		top_obj, top_type = self.stack[-1]
		self.push(top_obj, top_type)
	def rotate(self, mnemo):
		after_underscore = mnemo.partition('_')[2]
		num = INT_VALUE[after_underscore]
		# rotate num top values
		new_stack = self.stack[:-num]
		new_stack.append(self.stack[-1])
		new_stack.extend(self.stack[-num:-1])
		# replace stack with this new one
		self.stack = new_stack
	def retrieve_global_variables(self):
		return self.global_variables
	def retrieve_statements(self):
		self.validate_candidate_statements_if_any()
		if len(self.statements) == 0 and self.optional_bloc == False:
			#print '# no statements: adding "pass"'
			self.add_statement('pass')					
		if 	len(self.statements) > 0:
			if self.preliminary_statement != None:
				# add the branch preliminary statement if any
				self.statements.insert(0, self.preliminary_statement)
			if self.is_top_level_bloc:
				# add global variables declarations
				for var in self.global_variables:
					stmt = 'global ' + var
					self.statements.insert(0, (self.get_indent(), stmt))
		return self.statements
	def validate_candidate_statements_if_any(self):
		new_stack = []
		for e in self.stack:
			obj, obj_type = e
			if obj_type == CANDIDATE_STATEMENT:
				self.add_statement(obj)
			else:
				new_stack.append(e)
		self.stack = new_stack
	def function_call(self, mnemo, param_info):
		desc = FUNCTION_CALLS_DESC[mnemo]
		params = []
		if desc['kw']:
			params.insert(0, '**' + self.pop())
		if desc['varargs']:
			params.insert(0, '*' + self.pop())
		num_positional_params = param_info % (1 << 8)
		num_keyword_params = param_info / (1 << 8)
		for _ in range(num_keyword_params):
			arg_value = self.pop()
			arg_name = self.pop()[1:-1]
			params.insert(0, arg_name + '=' + arg_value)
		for _ in range(num_positional_params):
			params.insert(0, self.pop())
		func_name = self.pop()
		full_call = '%s(%s)' % (func_name, ', '.join(params))
		self.push(full_call, CANDIDATE_STATEMENT)
	def record_loading_of_variable(self, known_globals, mnemo, name):
		if mnemo == 'LOAD_GLOBAL':
			# check that this variable is defined in our module
			if name in known_globals:
				self.global_variables.add(name)
