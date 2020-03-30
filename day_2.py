"""Solution for https://adventofcode.com/2019/day/2/"""
from argparse import ArgumentParser
import doctest
from pathlib import Path
from typing import List

DEFAULT_INPUT_FILE_PATH = "input_2.txt"


class UnknownCommandError(Exception):
    pass


class EndOfProgramError(Exception):
    pass


def main_1(parsed_input) -> int:
    icp = IntCodeProgram(parsed_input)
    icp.command_list[1] = 12
    icp.command_list[2] = 2
    icp.run()
    return icp.command_list[0]


def main_2(parsed_input) -> int:
    # this brute force solution is lame, but i could not think
    # of a way to reverse engineer the starting input
    # for example, if i know that two numbers must multiply to 19690720,
    # how could i possibly determine what those numbers are?
    for i in range(100):
        for j in range(100):
            print(f"Noun: {i}, Verb: {j}")
            icp = IntCodeProgram(parsed_input)
            icp.command_list[1] = i
            icp.command_list[2] = j
            try:
                icp.run()
            except (UnknownCommandError, EndOfProgramError):
                continue
            if icp.command_list[0] == 19690720:
                return 100 * i + j


class IntCodeProgram:
    command_map: dict = {1: "execute_add", 2: "execute_multiply", 99: "set_exit"}

    def __init__(self, command_list: List[int]):
        # so we don't modify the input list in place
        self.command_list: List[int] = command_list.copy()
        self.position: int = 0
        self.is_complete: bool = False

    def execute_add(self):
        num1: int = self.get_position_value(self.position + 1)
        num2: int = self.get_position_value(self.position + 2)
        dest: int = self.command_list[self.position + 3]
        self.command_list[dest] = num1 + num2
        self.position += 4

    def execute_multiply(self):
        num1: int = self.get_position_value(self.position + 1)
        num2: int = self.get_position_value(self.position + 2)
        dest: int = self.command_list[self.position + 3]
        self.command_list[dest] = num1 * num2
        self.position += 4

    def set_exit(self):
        self.is_complete = True

    def run(self) -> None:
        """
        >>> icp = IntCodeProgram([1, 1, 1, 4, 99, 5, 6, 0, 99])
        >>> icp.run()
        >>> print(icp.command_list == [30, 1, 1, 4, 2, 5, 6, 0, 99])
        True

        :return:
        """
        while not self.is_complete:
            self.run_one_command()

    def get_current_command_function(self):
        try:
            opcode: int = self.command_list[self.position]
        except KeyError:
            raise EndOfProgramError("Passed end of program.")
        try:
            command_name: str = self.command_map[opcode]
        except KeyError:
            raise UnknownCommandError(f"'{opcode}' is not a known command.")

        return getattr(self, command_name)

    def get_position_value(self, pos: int) -> int:
        index: int = self.command_list[pos]
        return self.command_list[index]

    def run_one_command(self) -> None:
        """
        >>> icp = IntCodeProgram([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
        >>> icp.run_one_command()
        >>> print(icp.command_list == [1, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50])
        True
        >>> print(icp.position)
        4
        >>> icp.run_one_command()
        >>> print(icp.command_list == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50])
        True

        >>> icp = IntCodeProgram([1, 0, 0, 0, 99])
        >>> icp.run_one_command()
        >>> print(icp.command_list == [2, 0, 0, 0, 99])
        True

        >>> icp = IntCodeProgram([2, 3, 0, 3, 99])
        >>> icp.run_one_command()
        >>> print(icp.command_list == [2, 3, 0, 6, 99])
        True

        >>> icp = IntCodeProgram([2, 4, 4, 5, 99, 0])
        >>> icp.run_one_command()
        >>> print(icp.command_list == [2, 4, 4, 5, 99, 9801])
        True
        """
        command_function = self.get_current_command_function()
        command_function()


def parse_input(input_path: Path) -> List[int]:
    if not input_path.exists():
        print(f"Bad input path. '{input_path}' does not exist.")
        return []
    input_text: str = input_path.read_text()
    command_list: List[int] = []
    for comm in input_text.split(","):
        command_list.append(int(comm.strip()))
    return command_list


def build_arg_parser() -> ArgumentParser:
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "-i", "--input", help="Path for input file", default=DEFAULT_INPUT_FILE_PATH
    )
    arg_parser.add_argument("-r", "--run", help="Run the solution", action="store_true")
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
