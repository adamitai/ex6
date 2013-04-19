import code # Imports the required funcitons for a C_Command

class command(object):
	def __init__(self, cmd_string):
		if '@' in cmd_string: # The @ defines an A_Command
			self.cmd_string = cmd_string[1:] # Pre-emptively remove '@', leaving only address or variable symbol
			self.type = 'A_Command'
		elif any(symbol in cmd_string for symbol in ['=', ';']): # The '=' or ';' defines C_Command
			self.cmd_string = cmd_string # Whole string becomes the C_Command
			self.type = 'C_Command'

# This is the first read through the lines of the file. The purpose of this read-through is to:
# a) Parse the commands from the commments, whitespace, and blank lines.
# c) Identify and obtain Label (ROM) symbols, and add them to symbolTable. This happens here because
#	all ROM address references (label symbols) are encased in parentheses.
# d) Identify and obtain C_Commands. These become instances of the command class w/ a C_Command attribute.
# e) Identify and obtain A_Commands. These become instances of the command class w/ a A_Command attribute.
def make_commands(lines, symbolTable):
	commands = []
	for line in lines: # Cycle through all lines in .asm file
		line = line.strip() # remove whitespace/new lines on ends of string
		line = line.replace(' ', '') # remove spaces within string
		
		if '//' in line: # Identify comments
			index = line.index('//') # Finds the start of comments
			line = line[:index] # Removes comment from current line
		
		if line == '': # If line is empty (could have been empty to begin with or after having comments removed)
			continue # ...go to the next item in the for loop
		
		elif line[0] == '(': # If the line starts with a (, then this line corresponds to a Label Symbol
			label = line.strip('()') # Grabl the label
			symbolTable[label] = len(commands) # Insert the label in the symbol table w/ corresponding ROM line
											   # which is equal to the number of commands in parsed_lines so far.
		elif line[0] == '@': # If the line starts with a '@', then this line corresponds to an A_Command
			label = line[1:] # Grab address label (either a number or a Label Symbol)
			commands.append(command(line)) # Add an instance of the command class to the commands list

		else: # Otherwise, this line is a C_Command
			commands.append(command(line)) # Add an instance of the command class to the commands list
	
	return commands

# This reads through the commands extracted from make_commands. This time through, all the command objects in
# the commands object list are translated to binary and written to the .hack file. Also, since all label symbols
# have been identified and added to symbolTable in the previous loop (make_commands), we can now add all RAM
# addresses (i.e. variable labels)
# Note that in this loop, we are working with command class instances, as opposed to a list of file lines,
# as was the case in the first loop through.
def write_commands(commands, hack_file, symbolTable, var_sym_start):
	for command in commands: # For all commands
		if command.type == 'A_Command': # In the case of A_Commands
			label = command.cmd_string # ...grab the A_Command itself
			if (not label.isdigit()) and (label not in symbolTable.keys()): # Check if the A_Command is a variable label, and not already entered into symbolTable
				symbolTable[label] = var_sym_start # Enter new Variable Label into Symobl Table
				var_sym_start = var_sym_start + 1 # Set memory location of next Variable Symbol
			if command.cmd_string in symbolTable.keys(): # If the A_Command is a Variable Symbol for a RAM address
				address = int(symbolTable[command.cmd_string]) # Grab the corresponding decimal address
			else:
				address = int(command.cmd_string) # Otherwise, get the decimal address explicitly from the A_Command
			address = bin(address)[2:] # Turn the address from decimal to binary
			address = (16-len(address))*'0' + address # Pad the binary address with zeros so it is 16 bits
			hack_file.write(address + '\n') # Write the address specified by the A_Command to the .hack file

		elif command.type == 'C_Command': # In the case of a C_Command
			if '=' in command.cmd_string: # If there is an equal sign in the command:
				dest = command.cmd_string.partition('=')[0] # Get the dest bits
				cmp = command.cmd_string.partition('=')[2] # Get the cmp bits
				jmp = None # Get the jmp bits (note that when there is an = in the C_Command, the jump bits are '000'
			elif ';' in command.cmd_string: # Same thing if there is an ';' in the command, except the dest bits are '000'
				dest = None
				cmp = command.cmd_string.partition(';')[0]
				jmp = command.cmd_string.partition(';')[2]
			hack_file.write('111' + code.cmp(cmp) + code.dest(dest) + code.jmp(jmp) + '\n') # Write the C_Command to the .hack file.
