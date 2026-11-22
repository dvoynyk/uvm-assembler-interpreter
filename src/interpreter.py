import argparse
import csv
import sys

from decoder import DecodeError
from vm import Machine, VMError

EXIT_OK = 0
EXIT_FAILURE = 1
DUMP_HEADER = ("address", "value")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Интерпретатор учебной виртуальной машины (вариант 10)."
    )
    parser.add_argument("binary", help="путь к бинарному файлу программы")
    parser.add_argument("dump", help="путь к CSV-файлу для дампа памяти")
    parser.add_argument(
        "--range",
        nargs=2,
        type=int,
        required=True,
        metavar=("FIRST", "LAST"),
        dest="addresses",
        help="диапазон адресов дампа (границы включаются)",
    )
    return parser


def read_binary(path):
    with open(path, "rb") as file:
        return file.read()


def write_dump(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(DUMP_HEADER)
        writer.writerows(rows)


def run(args):
    first, last = args.addresses
    machine = Machine(read_binary(args.binary))
    machine.run()
    write_dump(args.dump, machine.dump(first, last))
    print(f"Дамп памяти {first}..{last} сохранен в {args.dump}")


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        run(args)
    except (OSError, DecodeError, VMError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return EXIT_FAILURE
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())