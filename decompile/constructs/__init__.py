#!/usr/bin/python
from const import END_OF_CONSTRUCT, NORMAL_FLOW, CONDITIONAL_JUMPS
from decompile.branches_ender import BranchesEnder
from decompile.clause_footprints import BranchMergingDetector, \
    get_opposite_clause
from decompile.constructs.for_loops import recognise_for_loops
from decompile.constructs.if_constructs import prepare_if_element
from decompile.constructs.try_constructs import prepare_try_element
from decompile.constructs.while_loops import recognise_while_loops
from decompile.disassemble import parse_absolute_index_from_elem_indic
from decompile.boolean_conditions import handle_boolean_conditions

def analyse_structures(asm_indexes, indexed_asm):
    next_asm_indexes = {}
    # compute a dict of next indexes in the sequence
    for i in range(len(asm_indexes)-1):
        index = asm_indexes[i]
        next_index = asm_indexes[i+1]
        next_asm_indexes[index] = next_index
    next_asm_indexes[next_index] = None
    for index in asm_indexes:
        next_index_in_sequence = next_asm_indexes[index]
        elem = indexed_asm[index]
        # by default next index is the next instruction
        elem['next_indexes'] = { NORMAL_FLOW: next_index_in_sequence }
        mnemo = elem['mnemo']
        if mnemo == 'JUMP_FORWARD':
            # replace relative indexes by absolute ones
            elem['mnemo'] = 'JUMP_ABSOLUTE'
            elem['arg'] = None # for clarity
            elem['next_indexes'] = { NORMAL_FLOW: parse_absolute_index_from_elem_indic(elem) }
        elif mnemo == 'JUMP_ABSOLUTE':
            # set next index to the jump target
            elem['next_indexes'] = { NORMAL_FLOW: elem['arg'] }
        elif mnemo == 'LOAD_CONST' and elem['indic'].startswith('<code object'):
            elem['mnemo'] = 'LOAD_CONST_CODE'
        elif mnemo in 'SETUP_EXCEPT':
            prepare_try_element(indexed_asm, next_asm_indexes, 
                                elem, next_index_in_sequence)
        elif mnemo in [ 'RETURN_VALUE', 'BREAK_LOOP', 
                    'RAISE_VARARGS', 'END_OF_CLAUSE', 'YIELD_VALUE' ]:
            elem['next_indexes'] = {}
        # and initialize info about conditions
        elem['clause_footprints'] = {}
    recognise_for_loops(asm_indexes, indexed_asm)
    for index in asm_indexes:
        elem = indexed_asm[index]
        mnemo = elem['mnemo']
        if mnemo in CONDITIONAL_JUMPS:
            next_index_in_sequence = elem['next_indexes'][NORMAL_FLOW]
            prepare_if_element(elem, mnemo, next_index_in_sequence)
    #for index in asm_indexes:
    #    print indexed_asm[index]
    handle_boolean_conditions(indexed_asm, asm_indexes[0])
    recognise_while_loops(asm_indexes, indexed_asm)
    set_constructs_boundaries(asm_indexes, indexed_asm)
    return asm_indexes, indexed_asm


def set_constructs_boundaries(asm_indexes, indexed_asm):
    merge_infos = {}
    constructs_infos = {
        'branch_clause_footprints': {},
        'merge_infos': merge_infos,
        'branch_path': []
    }
    # detect if branches
    BranchMergingDetector(indexed_asm).traverse(
                        index=asm_indexes[0], data=constructs_infos)
    # record merge info 
    for clause_index in merge_infos:
        merge_index = merge_infos[clause_index]
        if_construct_elem = indexed_asm[clause_index]
        indexes = if_construct_elem['next_indexes']
        indexes[END_OF_CONSTRUCT] = merge_index
    
    # collect all end of constructs
    end_of_constructs = {}
    for index in asm_indexes:
        elem = indexed_asm[index]
        if END_OF_CONSTRUCT in elem['next_indexes']:
            end_of_construct_index = elem['next_indexes'][END_OF_CONSTRUCT]
            construct_index = elem['index']
            if end_of_construct_index in end_of_constructs:
                # this index is already reported to be the end
                # of a construct!
                # this may occur with imbricated constructs.
                # the end_of_construct_index is actually the one
                # of the top-level one, i.e. the one with lowest
                # construct_index.
                previous_construct_index = end_of_constructs[end_of_construct_index]
                if construct_index < previous_construct_index:
                    end_of_constructs[end_of_construct_index] = construct_index
            else:
                end_of_constructs[end_of_construct_index] = construct_index
    #print 'End of constructs:', end_of_constructs
    # when jumping to the end of a construct
    # record that it is the end of the branch
    BranchesEnder(indexed_asm).traverse(index=asm_indexes[0], data=end_of_constructs)
