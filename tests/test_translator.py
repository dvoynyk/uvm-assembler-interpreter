"""Тесты ассемблера по спецификации УВМ (вариант 10)."""

import io
import os
import unittest
from contextlib import redirect_stdout

from assembler import main
from isa import CONST_BITS, OFFSET_BITS
from translator import AsmError, assemble_text

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLE_PATH = os.path.join(TESTS_DIR, "..", "examples", "spec_tests.csv")
MAX_CONST = (1 << CONST_BITS) - 1
MAX_OFFSET = (1 << OFFSET_BITS) - 1


class TestSpecExamples(unittest.TestCase):

    def test_load_constant(self):
        self.assertEqual(assemble_text(["load,405"]), [{"A": 4, "B": 405}])

    def test_read_memory(self):
        self.assertEqual(assemble_text(["read,279"]), [{"A": 7, "B": 279}])

    def test_write_memory(self):
        self.assertEqual(assemble_text(["write"]), [{"A": 5}])

    def test_sqrt(self):
        self.assertEqual(assemble_text(["sqrt,657"]), [{"A": 6, "B": 657}])


class TestLanguage(unittest.TestCase):

    def test_blank_and_comment_lines_are_skipped(self):
        lines = ["# комментарий", "", "write", ",,"]
        self.assertEqual(assemble_text(lines), [{"A": 5}])

    def test_hex_operand_and_register_case(self):
        self.assertEqual(
            assemble_text(["LOAD,0x195"]), [{"A": 4, "B": 405}]
        )

    def test_boundary_operands(self):
        program = assemble_text([f"load,{MAX_CONST}", f"read,{MAX_OFFSET}"])
        self.assertEqual(program[0]["B"], MAX_CONST)
        self.assertEqual(program[1]["B"], MAX_OFFSET)


class TestErrors(unittest.TestCase):

    def assert_rejected(self, line):
        with self.assertRaises(AsmError):
            assemble_text([line])
    def test_unknown_command(self):
        self.assert_rejected("jump,1")
    def test_missing_operand(self):
        self.assert_rejected("load")
    def test_extra_operand(self):
        self.assert_rejected("write,1")
    def test_not_a_number(self):
        self.assert_rejected("read,abc")
    def test_negative_operand(self):
        self.assert_rejected("load,-1")
    def test_const_overflow(self):
        self.assert_rejected(f"load,{MAX_CONST + 1}")
    def test_offset_overflow(self):
        self.assert_rejected(f"sqrt,{MAX_OFFSET + 1}")
class TestCli(unittest.TestCase):

    def test_test_mode_output(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            main([EXAMPLE_PATH, "unused.bin", "--test"])
        expected = "A=4, B=405\nA=7, B=279\nA=5\nA=6, B=657\n"
        self.assertEqual(buffer.getvalue(), expected)
if __name__ == "__main__":
    unittest.main()