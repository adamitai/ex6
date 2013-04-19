import os
from exceptions import IOError
from Common import commandsType, OP_LENGTH, equalString
import Code

# Encapsulates access to the input code. Reads an assembly language
# command, parses it, and provides convenient access to the command's components
# (fields and symbols). In addition, removes all white space and comments
class Parser:

  def __init__(self, fileName, symbolTable):
    # Check if the requested file to parse exists
    if not os.path.exists(fileName):
      raise IOError("The file %s could not be found" % fileName)

    # initialize the commands array
    self.text = []
    self.symbolTable = symbolTable
    # open the requested file for reading
    with open(fileName, 'r') as f:
      # read each line from the file
      for line in f.readlines():
        # check if the line is valid for parsing ( Notice that here
        # all the comments  and the white spaces are removed)
        if not self.whiteSpaceOrComment(line):
          cleanLine = self.cleanEmptyLinesAndComments(line)
          self.text.insert(0,cleanLine)

    # init the current command line
    self.currentCommand = ""
    self.parsedCommand = ""
  def cleanEmptyLinesAndComments(self, line):
    line = line.replace(' ','').replace('\r','').replace('\n','')
    commentPosition = line.index('//') if '//' in line else -1
    if commentPosition > -1:
      line = line[0:commentPosition]
    return line

  def whiteSpaceOrComment(self, line):
    strippedLine = line.strip()

    # white spaces
    if not strippedLine or strippedLine in ['\n', '\r\n']:
      return True

    # comments
    if strippedLine.startswith('//'):
      return True

    return False

  def hasMoreCommands(self):
    return len(self.text) > 0

  def advance(self):
    if not self.hasMoreCommands:
      return ""

    self.currentCommand = self.text.pop()
    self.parseCommand()

  def parseCommand(self):
    if self.commandType() == commandsType.A_COMMAND:
      # remove the @
      command = self.currentCommand[1:]
      # check if the command is an address or in the symbol table
      if command.isdigit():
        self.parsedCommand = self.getDecimal(command)
      elif command in
    elif self.commandType() == commandsType.C_COMMAND:
        self.parsedCommand = self.getParsedEqual()

  def getParsedEqual(self):
    if '=' in self.currentCommand:
      parsedCommandArray = self.currentCommand.split('=')
      dest = Code.dest(parsedCommandArray[0])
      cmp  = Code.comp(parsedCommandArray[1])
      jmp = Code.jump(None)
    elif ';' in self.currentCommand:
      parsedCommandArray = self.currentCommand.split(';')
      dest = Code.dest(None)
      cmp = Code.comp(parsedCommandArray[0])
      jmp = Code.jump(parsedCommandArray[1])
    return equalString % (cmp, dest, jmp)

  def commandType(self):
    if '@' in self.currentCommand:
      return commandsType.A_COMMAND
    if '=' in self.currentCommand or ';' in self.currentCommand:
      return commandsType.C_COMMAND
    if '(' in self.currentCommand:
      return commandsType.L_COMMAND

    raise Exception("%s Not a valid command" % self.currentCommand)

  # returns the symbol or decimal Xxx of the current command @Xxx or (Xxx)
  def symbol(self):
    if self.commandType() in (commandsType.A_COMMAND, commandsType.L_COMMAND):
      if self.symbolTable.inSymbolTable(self.currentCommand):
        return self.symbolTable.symbolTable[self.currentCommand]
    raise Exception("The current command: %s does not carry a symbol" % self.currentCommand)

  def dest(self):
    if self.commandType() == commandsType.C_COMMAND:
      return Code.dest(self.currentCommand)
    raise Exception("The current command: %s does not carry a dest" % self.currentCommand)

  def comp(self):
    if self.commandType() == commandsType.C_COMMAND:
      return Code.comp(self.currentCommand)
    raise Exception("The current command: %s is not of a type %s" % (self.currentCommand, commandsType.C_COMMAND))

  def jump(self):
    if self.commandType() == commandsType.C_COMMAND:
      return Code.jump(self.currentCommand)
    raise Exception("The current command: %s is not of a type %s" % (self.currentCommand, commandsType.C_COMMAND))


  def getDecimal(self, command):
    if self.commandType() == commandsType.A_COMMAND:
      dec_value = int(command)
      # cast to binary
      bin_value = bin(dec_value)[2:]
      # pad with '0'
      return self.pad(bin_value, '0')
    raise Exception("Not an %s", commandsType.A_COMMAND)

  def pad(self, command, char):
    return "%s%s" % (char * (OP_LENGTH - len(command)), command)