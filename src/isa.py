from collections import namedtuple

OPCODE_LOAD = 4
OPCODE_READ = 7
OPCODE_WRITE = 5
OPCODE_SQRT = 6

OPCODE_BITS = 3
CONST_BITS = 30
OFFSET_BITS = 11

SIZE_LOAD = 5
SIZE_READ = 2
SIZE_WRITE = 1
SIZE_SQRT = 2

Command = namedtuple("Command", ["opcode", "operand_bits", "size"])

COMMANDS = {
    "load": Command(OPCODE_LOAD, CONST_BITS, SIZE_LOAD),
    "read": Command(OPCODE_READ, OFFSET_BITS, SIZE_READ),
    "write": Command(OPCODE_WRITE, None, SIZE_WRITE),
    "sqrt": Command(OPCODE_SQRT, OFFSET_BITS, SIZE_SQRT),
}

SIZES = {command.opcode: command.size for command in COMMANDS.values()}