def dest(dest_string):
	destination = {
		None : '000',
		'M' : '001',
		'D' : '010',
		'MD' : '011',
		'A' : '100',
		'AM' : '101',
		'AD' : '110',
		'AMD' : '111'
		}
	return destination[dest_string]

def cmp(cmp_string):
	#print cmp_string
	if 'A' in cmp_string:
		a_bit = '0'
		cmp_string = cmp_string.replace('A', '*')
	elif 'M' in cmp_string:
		a_bit = '1'
		cmp_string = cmp_string.replace('M', '*')
	else:
		a_bit = '0'

	compute = {
		'0' : '101010',
		'1' : '111111',
		'-1' : '111010',
		'D' : '001100',
		'*' : '110000',
		'!D' : '001101',
		'!*' : '110001',
		'-D' : '001111',
		'-*' : '110011',
		'D+1' : '011111',
		'*+1' : '110111',
		'D-1' : '001110',
		'*-1' : '110010',
		'D+*' : '000010',
		'D-*' : '010011',
		'*-D' : '000111',
		'D&*' : '000000',
		'D|*' : '010101'
		}
	
	return a_bit + compute[cmp_string]

def jmp(jmp_string):
	jump = {
		None : '000',
		'JGT' : '001',
		'JEQ' : '010',
		'JGE' : '011',
		'JLT' : '100',
		'JNE' : '101',
		'JLE' : '110',
		'JMP' : '111'
		}
	return jump[jmp_string]
	


