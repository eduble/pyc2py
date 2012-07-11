from decompile.branch_info import BranchDecompilationInfo
import decompile.decompilator

def decompile_bloc(indexed_asm, func_code, known_globals, index=0, indent=1, 
                   is_top_level_bloc=False):
    info = BranchDecompilationInfo(indent, 
                                   is_top_level_bloc=is_top_level_bloc)
    decompile.decompilator.Decompilator(
                    indexed_asm, func_code, known_globals).traverse(
                                        index=index, 
                                        data=info)
    return info.retrieve_statements()