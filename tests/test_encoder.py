import unittest

from encoder import encode_instruction, encode_program
from isa import SIZES

LOAD_BYTES = b"\xac\x0c\x00\x00\x00"
READ_BYTES = b"\xbf\x08"
WRITE_BYTES = b"\x05"
SQRT_BYTES = b"\x8e\x14"


class TestSpecBytes(unittest.TestCase):

    def test_load_constant(self):
        result = encode_instruction({"A": 4, "B": 405})
        self.assertEqual(result, LOAD_BYTES)

    def test_read_memory(self):
        result = encode_instruction({"A": 7, "B": 279})
        self.assertEqual(result, READ_BYTES)

    def test_write_memory(self):
        self.assertEqual(encode_instruction({"A": 5}), WRITE_BYTES)

    def test_sqrt(self):
        result = encode_instruction({"A": 6, "B": 657})
        self.assertEqual(result, SQRT_BYTES)


class TestProgram(unittest.TestCase):

    def test_encode_program(self):
        program = [{"A": 5}, {"A": 6, "B": 657}]
        self.assertEqual(
            encode_program(program), [WRITE_BYTES, SQRT_BYTES]
        )

    def test_empty_program(self):
        self.assertEqual(encode_program([]), [])

    def test_sizes_match_specification(self):
        self.assertEqual(SIZES, {4: 5, 7: 2, 5: 1, 6: 2})

    def test_maximum_operands_fit(self):
        load_max = (1 << 30) - 1
        read_max = (1 << 11) - 1
        self.assertEqual(
            len(encode_instruction({"A": 4, "B": load_max})), SIZES[4]
        )
        self.assertEqual(
            len(encode_instruction({"A": 7, "B": read_max})), SIZES[7]
        )


if __name__ == "__main__":
    unittest.main()