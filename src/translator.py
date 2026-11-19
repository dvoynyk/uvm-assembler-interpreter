import csv

from isa import COMMANDS

COMMENT_PREFIX = "#"
EXPECTED_OPERANDS = 1
NUMBER_BASE_AUTO = 0


class AsmError(Exception):
    """Ошибка ассемблирования."""


def error_at(line_no, message):
    return AsmError(f"строка {line_no}: {message}")


def parse_operand(text, bits, line_no):
    try:
        value = int(text.strip(), NUMBER_BASE_AUTO)
    except ValueError:
        raise error_at(
            line_no, f"операнд '{text}' не является числом"
        ) from None
    limit = 1 << bits
    if value not in range(limit):
        raise error_at(
            line_no, f"операнд {value} вне диапазона 0..{limit - 1}"
        )
    return value


def is_skippable(row):
    if not any(cell.strip() for cell in row):
        return True
    return row[0].lstrip().startswith(COMMENT_PREFIX)


def translate_row(row, line_no):
    mnemonic = row[0].strip().lower()
    command = COMMANDS.get(mnemonic)
    if command is None:
        raise error_at(line_no, f"неизвестная команда '{row[0]}'")
    operands = [cell for cell in row[1:] if cell.strip()]
    if command.operand_bits is None:
        if operands:
            raise error_at(line_no, f"команда '{mnemonic}' без операнда")
        return {"A": command.opcode}
    if len(operands) != EXPECTED_OPERANDS:
        raise error_at(line_no, f"команде '{mnemonic}' нужен 1 операнд")
    value = parse_operand(operands[0], command.operand_bits, line_no)
    return {"A": command.opcode, "B": value}


def assemble_text(lines):
    program = []
    reader = csv.reader(lines)
    for row in reader:
        if is_skippable(row):
            continue
        program.append(translate_row(row, reader.line_num))
    return program
