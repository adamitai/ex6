from Parser import Parser
import argparse
import SymbolTable

argParser = argparse.ArgumentParser(description='nand2tetris Assembler.')

argParser.add_argument('file_name', help='The .asm file to be parsed.')

args = argParser.parse_args()
#print(args.file_name)


asmFileName = args.file_name
symTable = SymbolTable()
parser = Parser(asmFileName, symTable)
while parser.hasMoreCommands():
  parser.advance()
  print parser.parsedCommand

    #if (command not in symbolTable.keys()): # Check if the A_Command is a variable label, and not already entered into symbolTable
    #				symbolTable[label] = var_sym_start # Enter new Variable Label into Symobl Table
    #				var_sym_start = var_sym_start + 1 # Set memory location of next Variable Symbol
    #if parser.currentCommand in symbolTable.keys(): # If the A_Command is a Variable Symbol for a RAM address
    # 				address = int(symbolTable[command.cmd_string]) # Grab the corresponding decimal address
    #else:
      # The line contains a decimal

    #elif ';' in command.cmd_string: # Same thing if there is an ';' in the command, except the dest bits are '000'
    #				dest = None
    #				cmp = command.cmd_string.partition(';')[0]
    #				jmp = command.cmd_string.partition(';')[2]
    #			hack_file.write('111' + code.cmp(cmp) + code.dest(dest) + code.jmp(jmp) + '\n') # Write the C_Command to the .hack file.
  #else:
    #pass