import unittest

from decoder import DecodeError, decode_instruction
from encoder import encode_instruction

LOAD_BYTES = b"\xac\x0c\x00\x00\x00"
READ_BYTES = b"\xbf\x08"
WRITE_BYTES = b"\x05"
SQRT_BYTES = b"\x8e\x14"


class TestSpecBytes(unittest.TestCase):
    

    def test_load_constant(self):
        instruction, following = decode_instruction(LOAD_BYTES, 0)
        self.assertEqual(instruction, {"A": 4, "B": 405})
        self.assertEqual(following, len(LOAD_BYTES))

    def test_read_memory(self):
        instruction, following = decode_instruction(READ_BYTES, 0)
        self.assertEqual(instruction, {"A": 7, "B": 279})
        self.assertEqual(following, len(READ_BYTES))

    def test_write_memory(self):
        instruction, following = decode_instruction(WRITE_BYTES, 0)
        self.assertEqual(instruction, {"A": 5})
        self.assertEqual(following, len(WRITE_BYTES))

    def test_sqrt(self):
        instruction, following = decode_instruction(SQRT_BYTES, 0)
        self.assertEqual(instruction, {"A": 6, "B": 657})
        self.assertEqual(following, len(SQRT_BYTES))


class TestStream(unittest.TestCase):

    def test_sequence_positions(self):
        code = LOAD_BYTES + READ_BYTES + WRITE_BYTES + SQRT_BYTES
        position = 0
        positions = []
        while position < len(code):
            _, position = decode_instruction(code, position)
            positions.append(position)
        self.assertEqual(positions, [5, 7, 8, 10])

    def test_roundtrip(self):
        program = [
            {"A": 4, "B": 0},
            {"A": 4, "B": (1 << 30) - 1},
            {"A": 7, "B": (1 << 11) - 1},
            {"A": 5},
            {"A": 6, "B": 1},
        ]
        for instruction in program:
            code = encode_instruction(instruction)
            self.assertEqual(decode_instruction(code, 0)[0], instruction)

    def test_bits_beyond_field_are_ignored(self):
        instruction, _ = decode_instruction(b"\xac\x0c\x00\x00\xfe", 0)
        self.assertEqual(instruction, {"A": 4, "B": 405})


class TestErrors(unittest.TestCase):

    def test_unknown_opcode(self):
        with self.assertRaises(DecodeError):
            decode_instruction(b"\x00", 0)

    def test_truncated_instruction(self):
        with self.assertRaises(DecodeError):
            decode_instruction(b"\xac\x0c", 0)


if __name__ == "__main__":
    unittest.main()