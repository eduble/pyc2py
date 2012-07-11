from const import PARTIAL_STATEMENT

BINARY_OPS = {
	'POWER': '**',
	'MULTIPLY': '*',
	'DIVIDE': '/',
	'FLOOR_DIVIDE': '//',
	'MODULO': '%',
	'ADD': '+',
	'SUBTRACT': '-',
	'SUBSCR': '',
	'LSHIFT': '<<',
	'RSHIFT': '>>',
	'AND': '&',
	'XOR': '^',
	'OR': '|'
}

def manage_binary_op(mnemo, info):
	after_underscore = mnemo.partition('_')[2]
	TOS = info.pop()
	TOS1 = info.pop()
	if after_underscore == 'SUBSCR':
		full_op = TOS1 + '[' + TOS + ']'
	else:
		full_op = TOS1 + ' ' + BINARY_OPS[after_underscore] + ' ' + TOS
	info.push('(' + full_op + ')', PARTIAL_STATEMENT)


