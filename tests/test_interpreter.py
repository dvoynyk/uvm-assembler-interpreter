"""Сквозные тесты: ассемблер -> бинарный файл -> интерпретатор -> дамп."""

import csv
import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from assembler import main as assemble
from interpreter import EXIT_FAILURE, EXIT_OK, main as interpret

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLES_DIR = os.path.join(TESTS_DIR, "..", "examples")
COPY_PATH = os.path.join(EXAMPLES_DIR, "copy_array.csv")
SQRT_PATH = os.path.join(EXAMPLES_DIR, "sqrt_demo.csv")
SOURCE_BASE = 10
TARGET_BASE = 20
COPY_VALUES = (11, 22, 33, 44, 55)
SQRT_INPUTS = (0, 1, 49, 144, 1000000, 10, 1073741823)
SQRT_ROOTS = (0, 1, 7, 12, 1000, 3, 32767)
HEADER = ["address", "value"]


def run_pipeline(program, folder, first, last):
    binary = os.path.join(folder, "program.bin")
    dump = os.path.join(folder, "dump.csv")
    with redirect_stdout(io.StringIO()):
        assemble([program, binary])
        return interpret([binary, dump, "--range", str(first), str(last)])


def read_dump(folder):
    with open(os.path.join(folder, "dump.csv"), newline="") as file:
        return list(csv.reader(file))


def expected_rows(source, target):
    memory = {}
    for index, value in enumerate(source):
        memory[SOURCE_BASE + index] = value
    for index, value in enumerate(target):
        memory[TARGET_BASE + index] = value
    last = TARGET_BASE + len(target) - 1
    rows = [HEADER]
    for address in range(SOURCE_BASE, last + 1):
        rows.append([str(address), str(memory.get(address, 0))])
    return rows


class TestCopyArray(unittest.TestCase):

    def test_array_is_copied(self):
        last = TARGET_BASE + len(COPY_VALUES) - 1
        with tempfile.TemporaryDirectory() as folder:
            status = run_pipeline(COPY_PATH, folder, SOURCE_BASE, last)
            self.assertEqual(status, EXIT_OK)
            self.assertEqual(
                read_dump(folder), expected_rows(COPY_VALUES, COPY_VALUES)
            )

    def test_dump_of_subrange(self):
        with tempfile.TemporaryDirectory() as folder:
            run_pipeline(COPY_PATH, folder, TARGET_BASE, TARGET_BASE + 1)
            rows = read_dump(folder)
            self.assertEqual(rows[1:], [["20", "11"], ["21", "22"]])


class TestSqrtDemo(unittest.TestCase):

    def test_roots_are_saved_to_memory(self):
        last = TARGET_BASE + len(SQRT_INPUTS) - 1
        with tempfile.TemporaryDirectory() as folder:
            status = run_pipeline(SQRT_PATH, folder, SOURCE_BASE, last)
            self.assertEqual(status, EXIT_OK)
            self.assertEqual(
                read_dump(folder), expected_rows(SQRT_INPUTS, SQRT_ROOTS)
            )


class TestFailures(unittest.TestCase):

    def test_missing_binary(self):
        arguments = ["no_such.bin", "dump.csv", "--range", "0", "1"]
        with redirect_stderr(io.StringIO()):
            status = interpret(arguments)
        self.assertEqual(status, EXIT_FAILURE)

    def test_reversed_range(self):
        with tempfile.TemporaryDirectory() as folder:
            binary = os.path.join(folder, "empty.bin")
            with open(binary, "wb"):
                pass
            dump = os.path.join(folder, "dump.csv")
            with redirect_stderr(io.StringIO()):
                status = interpret([binary, dump, "--range", "5", "1"])
        self.assertEqual(status, EXIT_FAILURE)


if __name__ == "__main__":
    unittest.main()