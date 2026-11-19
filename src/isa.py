from collections import namedtuple

OPCODE_LOAD = 4
OPCODE_READ = 7
OPCODE_WRITE = 5
OPCODE_SQRT = 6

CONST_BITS = 30
OFFSET_BITS = 11

Command = namedtuple("Command", ["opcode", "operand_bits"])

COMMANDS = {
    "load": Command(OPCODE_LOAD, CONST_BITS),
    "read": Command(OPCODE_READ, OFFSET_BITS),
    "write": Command(OPCODE_WRITE, None),
    "sqrt": Command(OPCODE_SQRT, OFFSET_BITS),
}