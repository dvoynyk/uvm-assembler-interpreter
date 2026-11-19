import argparse
import sys

from encoder import encode_program
from translator import AsmError, assemble_text

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
        help="режим тестирования: вывести машинный код в байтах",
    )
    return parser


def read_source(path):
    with open(path, encoding="utf-8", newline="") as file:
        return file.read().splitlines()


def write_binary(path, data):
    with open(path, "wb") as file:
        file.write(data)


def format_bytes(code):
    return ", ".join(f"0x{byte:02X}" for byte in code)


def run(args):
    program = assemble_text(read_source(args.source))
    chunks = encode_program(program)
    code = b"".join(chunks)
    write_binary(args.output, code)
    if args.test:
        for chunk in chunks:
            print(format_bytes(chunk))
    print(f"Размер двоичного файла: {len(code)} байт")


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        run(args)
    except (OSError, AsmError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return EXIT_FAILURE
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())