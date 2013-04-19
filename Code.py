from Common import jumpMap, destMap, compMap

# Translates Hack assembly language mnemonics into binary codes
# returns the binary code of the dest mnemonic(line).
def dest(line):
  if line in destMap.keys():
    return destMap[line]
  raise Exception("syntax error in the dest: %s command" % line)

# returns the binary code of the comp mnemonic(line).
def comp(line):
  a = '1' if ('M' in line) else '0'
  if line in compMap.keys():
    return "%s%s" % (a, compMap[line])
  raise Exception("syntax error in the comp: %s command" % line)

# returns the binary code of the jump mnemonic.
def jump(line):
  if line in jumpMap.keys():
    return jumpMap[line]
  raise Exception("syntax error in the jump: %s command" % line)
