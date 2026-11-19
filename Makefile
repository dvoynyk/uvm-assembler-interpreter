PYTHON ?= python3
OUT ?= out.bin

.PHONY: test run

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

run:
	$(PYTHON) src/assembler.py examples/spec_tests.csv $(OUT) --test