import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from assembler import EXIT_FAILURE, EXIT_OK, main

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLE_PATH = os.path.join(TESTS_DIR, "..", "examples", "spec_tests.csv")
EXPECTED_CODE = b"\xac\x0c\x00\x00\x00" b"\xbf\x08" b"\x05" b"\x8e\x14"
SIZE_LINE = f"Размер двоичного файла: {len(EXPECTED_CODE)} байт\n"
BYTES_TEXT = (
    "0xAC, 0x0C, 0x00, 0x00, 0x00\n"
    "0xBF, 0x08\n"
    "0x05\n"
    "0x8E, 0x14\n"
)


class TestCli(unittest.TestCase):
    """Проверка работы программы целиком."""

    def run_cli(self, *extra):
        with tempfile.TemporaryDirectory() as folder:
            target = os.path.join(folder, "out.bin")
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                status = main([EXAMPLE_PATH, target, *extra])
            with open(target, "rb") as file:
                return status, buffer.getvalue(), file.read()

    def test_binary_file_matches_spec(self):
        status, _, data = self.run_cli()
        self.assertEqual(status, EXIT_OK)
        self.assertEqual(data, EXPECTED_CODE)

    def test_size_is_printed(self):
        _, output, _ = self.run_cli()
        self.assertEqual(output, SIZE_LINE)

    def test_test_mode_prints_bytes(self):
        _, output, _ = self.run_cli("--test")
        self.assertEqual(output, BYTES_TEXT + SIZE_LINE)

    def test_missing_source_fails(self):
        errors = io.StringIO()
        with redirect_stderr(errors):
            status = main(["no_such_file.csv", "unused.bin"])
        self.assertEqual(status, EXIT_FAILURE)


if __name__ == "__main__":
    unittest.main()