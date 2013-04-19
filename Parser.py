import os
from exceptions import IOError
from Common import commandsType, OP_LENGTH
import Code

# Encapsulates access to the input code. Reads an assembly language
# command, parses it, and provides convenient access to the command's components
# (fields and symbols). In addition, removes all white space and comments
class Parser:

  def __init__(self, fileName):
    # Check if the requested file to parse exists
    if not os.path.exists(fileName):
      raise IOError("The file %s could not be found" % fileName)

    # initialize the commands array
    self.text = []
    # open the requested file for reading
    with open(fileName, 'r') as f:
      # read each line from the file
      for line in f.readlines():
        # check if the line is valid for parsing ( Notice that here
        # all the comments  and the white spaces are removed)
        if not self.whiteSpaceOrComment(line):
          cleanLine = line.replace(' ','').replace('\r','').replace('\n','')
          self.text.insert(0,cleanLine)

    # init the current command line
    self.currentCommand = ""
    self.parsedCommand = ""

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
      if command.isdigit():
        print self.getDecimal(command)
    elif self.commandType() == commandsType.C_COMMAND:
        if '=' in self.currentCommand:
          print self.currentCommand
          print self.getParsedThrough()

  def getParsedThrough(self):
    if '=' in self.currentCommand:
      parsedCommandArray = self.currentCommand.split('=')
      dest = Code.dest(parsedCommandArray[0])
      cmp  = Code.comp(parsedCommandArray[1])
      jmp = Code.jump(None)
    else:
      pass
    return  "111%s%s%s\n" % (cmp, dest, jmp)

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
      #TODO Complete
      return Code.self.currentCommand
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
      return "%s%s" % ('0' * (OP_LENGTH - len(bin_value)), bin_value)
    raise Exception("Not an %s", commandsType.A_COMMAND)