import argparse
import sys

VECTOR_LENGTH = 10
EXIT_OK = 0
EXIT_FAILURE = 1


def init_lines(base, values):
    lines = ["# Инициализация вектора: load адрес; load значение; write"]
    for index, value in enumerate(values):
        lines += [f"load,{base + index}", f"load,{value}", "write"]
    return lines


def sqrt_lines(base, length):
    lines = ["# sqrt на месте: load адрес; load база; sqrt индекс; write"]
    for index in range(length):
        lines.append(f"load,{base + index}")
        lines.append(f"load,{base}")
        lines.append(f"sqrt,{index}")
        lines.append("write")
    return lines


def program_lines(base, values):
    last = base + len(values) - 1
    header = f"# Этап 5: sqrt над вектором, адреса {base}..{last}"
    return [header] + init_lines(base, values) + sqrt_lines(base, len(values))


def build_parser():
    parser = argparse.ArgumentParser(
        description="Генератор программ sqrt над вектором из 10 чисел."
    )
    parser.add_argument("output", help="путь к создаваемому файлу (CSV)")
    parser.add_argument("base", type=int, help="адрес начала вектора")
    parser.add_argument("values", type=int, nargs="+", help="10 чисел")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if len(args.values) != VECTOR_LENGTH:
        print(f"Ошибка: нужно {VECTOR_LENGTH} значений", file=sys.stderr)
        return EXIT_FAILURE
    text = "\n".join(program_lines(args.base, args.values)) + "\n"
    with open(args.output, "w", encoding="utf-8", newline="\n") as file:
        file.write(text)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())