from const import CANDIDATE_STATEMENT, PARTIAL_STATEMENT
from decompile.constructs import analyse_structures
from decompile.disassemble import disassemble_code
from tools import print_code_line, print_code
import decompile.bloc
import inspect

def pack_function_object(info, num_default_values):
    code_object = info.pop()
    default_values = []
    for _ in range(num_default_values):
        default_values.insert(0, info.pop())
    args, varargs, varkw = inspect.getargs(code_object)
    specs = []
    firstdefault = len(args) - len(default_values)
    #print args
    for i in range(len(args)):
        spec = str(args[i])
        if i >= firstdefault:
            spec = spec + '=' + default_values[i - firstdefault]
        specs.append(spec)
    if varargs is not None:
        specs.append('*' + varargs)
    if varkw is not None:
        specs.append('**' + varkw)
    #print specs
    args_string = ', '.join(specs)
    info.push({ 'code': code_object, 'args_string': args_string }, 
              PARTIAL_STATEMENT)

#def analyse_lambda_expression_code(lambda_code):
#    asm_indexes, indexed_asm = disassemble_code(lambda_code)
#    asm_indexes, indexed_asm = analyse_structures(asm_indexes, indexed_asm)
#    statements = decompile.bloc.decompile_bloc(
#            indexed_asm, lambda_code, index=asm_indexes[0], indent=0)
#    #print 'statements:', statements
#    expr_code = statements[0][1] # first statement, code part (first part is indent)
#    return expr_code

def analyse_generator_code(known_globals, generator_code):
    asm_indexes, indexed_asm = disassemble_code(generator_code)
    for i in range(len(asm_indexes)):
        index = asm_indexes[i]
        elem = indexed_asm[index]
        if elem['mnemo'] == 'STORE_FAST':
            variable_name = elem['indic']
            expr_start = i+1
            break
    asm_indexes = asm_indexes[expr_start:]
    asm_indexes, indexed_asm = analyse_structures(asm_indexes, indexed_asm)
    statements = decompile.bloc.decompile_bloc(
            indexed_asm, generator_code, known_globals, index=asm_indexes[0], indent=0)
    #print 'statements:', statements
    expr_code = statements[0][1] # first statement, code part (first part is indent)
    return expr_code, variable_name
    
def format_embedded_function(known_globals, func_name, func_object, info):
    indent = info.get_indent()
    info.add_statement('def %s(%s):' % (func_name, func_object['args_string']))
    info.append_bloc_of_statements(
                decompile.decompile_func_body(func_object['code'], known_globals, indent+1))

def handle_list_comprehension(known_globals, info):
    set_of_values_expr = info.pop()
    function_object = info.pop()
    generator_code = function_object['code']
    expression, variable_name = analyse_generator_code(known_globals, generator_code)
    info.push(expression + ' for ' + variable_name + ' in ' +  
              set_of_values_expr, CANDIDATE_STATEMENT)
    
