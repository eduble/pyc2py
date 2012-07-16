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

from const import PARTIAL_STATEMENT

UNARY_OPS = {
	'POSITIVE': '+',
	'NEGATIVE': '-',
	'NOT': 'not ',
	'CONVERT': '',
	'INVERT': '~',
}

def manage_unary_op(mnemo, info):
	after_underscore = mnemo.partition('_')[2]
	TOS = info.pop()
	if after_underscore == 'CONVERT':
		full_op = '`' + TOS + '`'
	else:
		full_op = UNARY_OPS[after_underscore] + TOS
	info.push('(' + full_op + ')', PARTIAL_STATEMENT)


