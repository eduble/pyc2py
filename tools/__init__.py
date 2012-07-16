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


def print_doc_string(indent, obj):
    doc_string = obj.__doc__
    if doc_string:
        lines = doc_string.splitlines()
        if len(lines) < 2:
            print_code_line(indent, '"""' + doc_string + '"""')
        else:
            print_code_line(indent, '"""')
            for line in lines:
                print_code_line(indent, line)
            print_code_line(indent, '"""')

def print_code(statements):
    for statement in statements:
        indent, text = statement
        space = ('%' + str(2*indent) + 's') % ''
        print '%s%s' % (space, text)

def print_code_line(indent, statement):
    print_code([(indent, statement)])
