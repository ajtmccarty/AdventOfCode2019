"""Solution for https://adventofcode.com/2019/day/4"""
from argparse import ArgumentParser
import doctest
from math import floor
from typing import List


def main_1(start: int, end: int) -> int:
    """Sad brute force solution"""
    return sum(
        [_is_valid(num) for num in range(start, end + 1)]
    )


def main_2(start, end) -> None:
    return None


def _is_valid(number: int):
    """
    >>> _is_valid(111111)
    True
    >>> _is_valid(223450)
    False
    >>> _is_valid(123789)
    False

    :param number: number to check
    :return: bool, True if number passes the checks
    """
    has_double: bool = False
    str_number: str = str(number)
    index: int = 1
    while index < len(str_number):
        if not has_double and str_number[index] == str_number[index - 1]:
            has_double = True
        if str_number[index] < str_number[index - 1]:
            return False
        index += 1
    return has_double


def build_arg_parser() -> ArgumentParser:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-s", "--start", type=int, help="Beginning of range")
    arg_parser.add_argument("-e", "--end", type=int, help="End of range")
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

    if args.start or args.end:
        if not (args.start and args.end):
            raise ValueError("Must include START and END when running")
        print("Computing answer for part 1...")
        answer_1 = main_1(args.start, args.end)
        print(f"Answer for part 1: {answer_1}")
        print("Computing answer for part 2...")
        answer_2 = main_2(args.start, args.end)
        print(f"Answer for part 2: {answer_2}")


if __name__ == "__main__":
    parser = build_arg_parser()
    run(parser)
