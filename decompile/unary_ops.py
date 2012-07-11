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


