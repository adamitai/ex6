import parser2
from symbol_table import symbolTable # Import the symbol table that holds RAM/ROM addresses for Variable/Label Symbols

var_sym_start = 16 # Set a counter defining where memory allocation starts for Variable (RAM) symbols
asm_file_name = raw_input('Enter the name of the .asm file to process: ') #assemebly filename (assumes .asm file is in same directory as script)
asm = open(asm_file_name + '.asm') # open .asm file
lines = asm.readlines() # get lines from .asm file

commands = parser2.make_commands(lines,symbolTable) # turn lines into command objects using parser2's parse function

hack_file = open(asm_file_name + '.hack', 'w') # Open the .hack file for writing
parser2.write_commands(commands, hack_file, symbolTable, var_sym_start) # Send list of commands to parser to write to .hack file
hack_file.close() # Close the .hack file.