import unittest

from encoder import encode_program
from isa import OPCODE_SQRT
from vm import Machine, VMError

SMALL_MEMORY = 4


def build(*program):
    return b"".join(encode_program(program))


def load(value):
    return {"A": 4, "B": value}


def read(offset):
    return {"A": 7, "B": offset}

def sqrt(offset):
    return {"A": 6, "B": offset}


WRITE = {"A": 5}


class TestCommands(unittest.TestCase):
    def test_load_pushes_constant(self):
        machine = Machine(build(load(405)))
        machine.run()
        self.assertEqual(machine.stack, [405])

    def test_write_stores_value_at_address(self):
        machine = Machine(build(load(3), load(99), WRITE))
        machine.run()
        self.assertEqual(machine.data[3], 99)
        self.assertEqual(machine.stack, [])

    def test_read_adds_offset_to_address(self):
        machine = Machine(build(load(4), read(1)))
        machine.data[5] = 77
        machine.run()
        self.assertEqual(machine.stack, [77])

    def test_empty_program_does_nothing(self):
        machine = Machine(b"")
        machine.run()
        self.assertEqual(machine.stack, [])


class TestSqrt(unittest.TestCase):

    def test_sqrt_pushes_root_of_memory_value(self):
        machine = Machine(build(load(4), sqrt(1)))
        machine.data[5] = 49
        machine.run()
        self.assertEqual(machine.stack, [7])

    def test_sqrt_rounds_down(self):
        machine = Machine(build(load(0), sqrt(0)))
        machine.data[0] = 10
        machine.run()
        self.assertEqual(machine.stack, [3])

    def test_sqrt_result_can_be_written(self):
        machine = Machine(build(load(3), load(0), sqrt(1), WRITE))
        machine.data[1] = 81
        machine.run()
        self.assertEqual(machine.data[3], 9)
        self.assertEqual(machine.stack, [])

    def test_sqrt_does_not_change_source(self):
        machine = Machine(build(load(0), sqrt(0)))
        machine.data[0] = 16
        machine.run()
        self.assertEqual(machine.data[0], 16)


class TestMemoryModel(unittest.TestCase):

    def test_code_is_not_changed_by_data_writes(self):
        code = build(load(0), load(255), WRITE)
        machine = Machine(code)
        machine.run()
        self.assertEqual(machine.code, code)

    def test_data_memory_starts_zeroed(self):
        machine = Machine(b"", data_size=SMALL_MEMORY)
        self.assertEqual(machine.data, [0] * SMALL_MEMORY)


class TestErrors(unittest.TestCase):

    def run_program(self, *program):
        Machine(build(*program), data_size=SMALL_MEMORY).run()

    def test_stack_underflow(self):
        with self.assertRaises(VMError):
            self.run_program(WRITE)

    def test_read_address_out_of_memory(self):
        with self.assertRaises(VMError):
            self.run_program(load(SMALL_MEMORY), read(0))

    def test_write_address_out_of_memory(self):
        with self.assertRaises(VMError):
            self.run_program(load(SMALL_MEMORY), load(1), WRITE)

    def test_sqrt_address_out_of_memory(self):
        with self.assertRaises(VMError):
            self.run_program(load(SMALL_MEMORY), sqrt(0))

    def test_sqrt_with_empty_stack(self):
        with self.assertRaises(VMError):
            self.run_program(sqrt(0))

    def test_command_without_handler(self):
        machine = Machine(build(load(0), sqrt(0)))
        del machine.handlers[OPCODE_SQRT]
        with self.assertRaises(VMError):
            machine.run()


class TestDump(unittest.TestCase):

    def test_dump_range_is_inclusive(self):
        machine = Machine(b"", data_size=SMALL_MEMORY)
        machine.data[1] = 5
        self.assertEqual(machine.dump(1, 2), [(1, 5), (2, 0)])

    def test_dump_rejects_reversed_range(self):
        machine = Machine(b"", data_size=SMALL_MEMORY)
        with self.assertRaises(VMError):
            machine.dump(2, 1)

    def test_dump_rejects_range_outside_memory(self):
        machine = Machine(b"", data_size=SMALL_MEMORY)
        with self.assertRaises(VMError):
            machine.dump(0, SMALL_MEMORY)


if __name__ == "__main__":
    unittest.main()