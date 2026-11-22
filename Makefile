PYTHON ?= python3
OUT ?= out.bin
DUMP ?= dump.csv

.PHONY: test run copy sqrt vectors

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

run:
	$(PYTHON) src/assembler.py examples/spec_tests.csv $(OUT) --test

copy:
	$(PYTHON) src/assembler.py examples/copy_array.csv $(OUT)
	$(PYTHON) src/interpreter.py $(OUT) $(DUMP) --range 10 24

sqrt:
	$(PYTHON) src/assembler.py examples/sqrt_demo.csv $(OUT)
	$(PYTHON) src/interpreter.py $(OUT) $(DUMP) --range 10 26

vectors:
	$(PYTHON) src/assembler.py examples/vector_squares.csv $(OUT)
	$(PYTHON) src/interpreter.py $(OUT) squares.dump.csv --range 0 9
	$(PYTHON) src/assembler.py examples/vector_mixed.csv $(OUT)
	$(PYTHON) src/interpreter.py $(OUT) mixed.dump.csv --range 100 109
	$(PYTHON) src/assembler.py examples/vector_large.csv $(OUT)
	$(PYTHON) src/interpreter.py $(OUT) large.dump.csv --range 4086 4095