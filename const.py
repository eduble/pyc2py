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


# kinds of indexes used to point to the 
# next instruction
# values must reflect the order of clauses:
# IF_CLAUSE < ELSE_CLAUSE < END_OF_CONSTRUCT
# FOR_CLAUSE < END_OF_CONSTRUCT
NORMAL_FLOW =  -1
IF_CLAUSE =   10
ELSE_CLAUSE =  11
TRY_CLAUSE =   12
EXCEPT_EXPRESSION_CLAUSE = 13
EXCEPT_CLAUSE =  14
FINALLY_CLAUSE =  15
FOR_CLAUSE = 16
WHILE_CLAUSE = 17
END_OF_CONSTRUCT = 18    # end of 'if', 'for', 'try' constructs

# constants used when we want to specify that an action
# must be performed in any clause, none of the clauses
# of a given construct, the 'FORWARD' or the 'JUMP 'clause only.
# The FORWARD and JUMP clauses are different depending on the 
# construct (while or if-then-else) and the conditional jump
# used.
# 
# (values must be different from the values of clauses above)
NO_CLAUSE = 0
ANY_CLAUSE = 1
FORWARD_CLAUSE = 2
JUMP_CLAUSE = 3

# constants needed to specify if a statement is complete
# or not, or 'candidate'.
# For example if we have a function call, f(), this is a 
# candidate statement, because:
# - "f()" is a valid statement itself
# - but "g(f())" or "a = f()" are valid statements also
PARTIAL_STATEMENT = 0
COMPLETE_STATEMENT = 1
CANDIDATE_STATEMENT = 2

# data about branches and jumps
BRANCH_IS_OPTIONAL = {
    IF_CLAUSE: False,
    ELSE_CLAUSE: True,
    TRY_CLAUSE: False,
    EXCEPT_CLAUSE: False,
    FINALLY_CLAUSE: True,
    FOR_CLAUSE: False,
    WHILE_CLAUSE: False,
    EXCEPT_EXPRESSION_CLAUSE: True
}

CONDITIONAL_JUMPS_DESC = {
    'JUMP_IF_TRUE' : {                 # python 2.6
        'jump_cond' : True,
        'pop_cond' : NO_CLAUSE,
        'relative' : True
    },
    'JUMP_IF_FALSE' : {             # python 2.6
        'jump_cond' : False,
        'pop_cond' : NO_CLAUSE,
        'relative' : True
    },
    'POP_JUMP_IF_TRUE' : {             # python 2.7
        'jump_cond' : True,
        'pop_cond' : ANY_CLAUSE,
        'relative' : False
    },
    'POP_JUMP_IF_FALSE' : {         # python 2.7
        'jump_cond' : False,
        'pop_cond' : ANY_CLAUSE,
        'relative' : False
    },
    'JUMP_IF_TRUE_OR_POP' : {         # python 2.7
        'jump_cond' : True,
        'pop_cond' : FORWARD_CLAUSE,
        'relative' : False
    },
    'JUMP_IF_FALSE_OR_POP' : {         # python 2.7
        'jump_cond' : False,
        'pop_cond' : FORWARD_CLAUSE,
        'relative' : False
    }
}

CONDITIONAL_JUMPS = CONDITIONAL_JUMPS_DESC.keys() 
