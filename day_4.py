"""Solution for https://adventofcode.com/2019/day/4"""
from argparse import ArgumentParser
import doctest
from typing import List, Optional, Tuple


def main_1(start: int, end: int) -> int:
    """Sad brute force solution
    >>> main_1(372304, 847060)
    475
    """
    return sum([_is_valid_1(num) for num in range(start, end + 1)])


def main_2(start, end) -> int:
    """Also a brute force solution
    >>> main_2(372304, 847060)
    297
    """
    return sum([_is_valid_2(num) for num in range(start, end + 1)])


def _is_valid_1(number: int):
    """
    >>> _is_valid_1(111111)
    True
    >>> _is_valid_1(223450)
    False
    >>> _is_valid_1(123789)
    False

    :param number: number to check
    :return: bool, True if number passes the checks
    """
    chunks = _chunkify(str(number))
    has_double: bool = False
    previous_int: Optional[int] = None
    for char, count in chunks:
        if count >= 2:
            has_double = True
        if previous_int and previous_int > int(char):
            return False
        previous_int = int(char)
    return has_double


def _is_valid_2(number: int):
    """
    >>> _is_valid_2(112233)
    True
    >>> _is_valid_2(123444)
    False
    >>> _is_valid_2(111122)
    True

    :param number: number to check
    :return: bool, True if number passes the checks
    """
    chunks = _chunkify(str(number))
    has_double: bool = False
    previous_int: Optional[int] = None
    for char, count in chunks:
        if count == 2:
            has_double = True
        if previous_int and previous_int > int(char):
            return False
        previous_int = int(char)
    return has_double


def _chunkify(input_str: str):
    """Return a list of tuples where each tuple is a single character and an integer
    indicating how many of that character occur in a row.

    >>> _chunkify("111")
    [('1', 3)]
    >>> _chunkify("1122")
    [('1', 2), ('2', 2)]
    >>> _chunkify("1234")
    [('1', 1), ('2', 1), ('3', 1), ('4', 1)]
    >>> _chunkify("121")
    [('1', 1), ('2', 1), ('1', 1)]

    :param input_str: string to turn into chunks
    :return: List of tuples where each tuple is a length-1 string and an integer
    """
    chunks: List[Tuple[str, int]] = []
    previous_char: str = input_str[0]
    count: int = 1
    for i in range(1, len(input_str)):
        if input_str[i] == previous_char:
            count += 1
            continue
        chunks.append((previous_char, count))
        previous_char = input_str[i]
        count = 1
    chunks.append((previous_char, count))
    return chunks


def build_arg_parser() -> ArgumentParser:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-s", "--start", type=int, help="Beginning of range")
    arg_parser.add_argument("-e", "--end", type=int, help="End of range")
    arg_parser.add_argument(
        "-t", "--test", help="Run the tests for this solution", action="store_true"
    )
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
