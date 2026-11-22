from isa import OPCODE_BITS, OPCODE_MASK, OPERAND_BITS, SIZES

BYTE_ORDER = "little"


class DecodeError(Exception):
    """Ошибка декодирования машинного кода."""


def decode_instruction(code, position):
    opcode = code[position] & OPCODE_MASK
    size = SIZES.get(opcode)
    if size is None:
        raise DecodeError(
            f"позиция {position}: неизвестный код операции {opcode}"
        )
    chunk = code[position:position + size]
    if len(chunk) != size:
        raise DecodeError(f"позиция {position}: команда обрезана")
    word = int.from_bytes(chunk, BYTE_ORDER)
    instruction = {"A": opcode}
    bits = OPERAND_BITS[opcode]
    if bits is not None:
        instruction["B"] = (word >> OPCODE_BITS) & ((1 << bits) - 1)
    return instruction, position + size