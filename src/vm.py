"""Модель УВМ: память команд, память данных, стек и цикл выполнения."""

import alu
from decoder import decode_instruction
from isa import (
    DATA_MEMORY_SIZE,
    OPCODE_LOAD,
    OPCODE_READ,
    OPCODE_SQRT,
    OPCODE_WRITE,
)


class VMError(Exception):
    """Ошибка выполнения программы на УВМ."""


class Machine:

    def __init__(self, code, data_size=DATA_MEMORY_SIZE):
        self.code = bytes(code)
        self.data = [0] * data_size
        self.stack = []
        self.handlers = {
            OPCODE_LOAD: self.op_load,
            OPCODE_READ: self.op_read,
            OPCODE_WRITE: self.op_write,
            OPCODE_SQRT: self.op_sqrt,
        }

    def pop(self):
        if not self.stack:
            raise VMError("стек пуст")
        return self.stack.pop()

    def check_address(self, address):
        if address not in range(len(self.data)):
            raise VMError(
                f"адрес {address} вне памяти данных "
                f"(0..{len(self.data) - 1})"
            )

    def fetch(self, instruction):
        address = self.pop() + instruction["B"]
        self.check_address(address)
        return self.data[address]

    def op_load(self, instruction):
        self.stack.append(instruction["B"])

    def op_read(self, instruction):
        self.stack.append(self.fetch(instruction))

    def op_write(self, instruction):
        value = self.pop()
        address = self.pop()
        self.check_address(address)
        self.data[address] = value

    def op_sqrt(self, instruction):
        self.stack.append(alu.sqrt(self.fetch(instruction)))

    def step(self, position):
        instruction, following = decode_instruction(self.code, position)
        handler = self.handlers.get(instruction["A"])
        if handler is None:
            raise VMError(
                f"позиция {position}: команда с кодом "
                f"{instruction['A']} не реализована"
            )
        handler(instruction)
        return following

    def run(self):
        position = 0
        while position < len(self.code):
            position = self.step(position)

    def dump(self, first, last):
        self.check_address(first)
        self.check_address(last)
        if first > last:
            raise VMError(f"начало диапазона {first} больше конца {last}")
        return [(address, self.data[address])
                for address in range(first, last + 1)]