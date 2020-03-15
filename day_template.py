from argparse import ArgumentParser
import doctest
from pathlib import Path

DEFAULT_INPUT_FILE_PATH = ""


def main_1(parsed_input) -> None:
    return None


def main_2(parsed_input) -> None:
    return None


def parse_input(input_path: Path) -> List:
    if not input_path.exists():
        print(f"Bad input path. '{input_path}' does not exist.")
        return
    input_text: str = input_path.read_text()

    # process input here

    return []


def build_arg_parser() -> ArgumentParser:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-i", "--input", help="Path for input file", default=DEFAULT_INPUT_FILE_PATH)
    arg_parser.add_argument("-r", "--run", help="Run the solution", action="store_true")
    arg_parser.add_argument("-t", "--test", help="Run the tests for this solution", action="store_true")
    return arg_parser


def run(arg_parser: ArgumentParser) -> None:
    args = arg_parser.parse_args()

    if args.test:
        print("Running Tests...")
        failures, num_tests = doctest.testmod()
        if not failures:
            print(f"Ran {num_tests} test, 0 failures")
        else:
            return

    if not args.test or args.run:
        print("Parsing input...")
        parsed_input = parse_input(Path(args.input))
        if not parsed_input:
            print("Could not parse input.")
            return
        print("Computing answer for part 1...")
        answer_1 = main_1(parsed_input)
        print(f"Answer for part 1: {answer_1}")
        print("Computing answer for part 2...")
        answer_2 = main_2(parsed_input)
        print(f"Answer for part 2: {answer_2}")


if __name__ == "__main__":
    parser = build_arg_parser()
    run(parser)