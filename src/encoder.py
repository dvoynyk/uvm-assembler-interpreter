from isa import OPCODE_BITS, SIZES

BYTE_ORDER = "little"
NO_OPERAND = 0


def encode_instruction(instruction):
    operand = instruction.get("B", NO_OPERAND)
    word = instruction["A"] | (operand << OPCODE_BITS)
    return word.to_bytes(SIZES[instruction["A"]], BYTE_ORDER)


def encode_program(program):
    return [encode_instruction(instruction) for instruction in program]