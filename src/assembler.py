import argparse
import sys

from translator import AsmError, assemble_text, format_instruction

EXIT_OK = 0
EXIT_FAILURE = 1


def build_parser():
    parser = argparse.ArgumentParser(
        description="Ассемблер учебной виртуальной машины (вариант 10)."
    )
    parser.add_argument("source", help="путь к исходному файлу (CSV)")
    parser.add_argument("output", help="путь к двоичному файлу-результату")
    parser.add_argument(
        "--test",
        action="store_true",
        help="режим тестирования: вывести внутреннее представление",
    )
    return parser


def read_source(path):
    with open(path, encoding="utf-8", newline="") as file:
        return file.read().splitlines()


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        program = assemble_text(read_source(args.source))
    except (OSError, AsmError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return EXIT_FAILURE
    if args.test:
        for instruction in program:
            print(format_instruction(instruction))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())