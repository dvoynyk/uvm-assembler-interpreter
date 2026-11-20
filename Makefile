PYTHON ?= python3
OUT ?= out.bin
DUMP ?= dump.csv

.PHONY: test run copy sqrt

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