"""Solution for https://adventofcode.com/2019/day/5/
Based on Solution for Day 2
"""
import abc
from argparse import ArgumentParser
import doctest
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Tuple
import sys

DEFAULT_INPUT_FILE_PATH = "input_5.txt"


class UnknownCommandError(Exception):
    pass


class EndOfProgramError(Exception):
    pass


def main_1(parsed_input) -> None:
    """Expected answer for sample input: 7259358"""
    InputCommand.set_default_input("1")
    icp = IntCodeProgram(parsed_input)
    icp.run()


def main_2(parsed_input) -> None:
    InputCommand.set_default_input("1")


class CommandParams:
    """Simple class used to track number of parameters for a given command and which parameters are inputs/outputs"""

    def __init__(self, input_indices: List[int], output_indices: List[int]):
        self.input_indices: List[int] = input_indices
        self.output_indices: List[int] = output_indices
        # reverse lookup for checking if a given parameter index is an input or output
        self.indices_to_type = {}
        for ind in self.input_indices:
            self.indices_to_type[ind] = "in"
        for ind in self.output_indices:
            self.indices_to_type[ind] = "out"

    @property
    def num_params(self) -> int:
        """Return the number of total parameters"""
        return len(self.input_indices) + len(self.output_indices)

    def is_index_input(self, index: int) -> bool:
        """Return True if this index is an input, False otherwise"""
        return self.indices_to_type[index] == "in"


class IntCodeCommand(abc.ABC):

    command_params: CommandParams = CommandParams([], [])

    @staticmethod
    def get_command_from_instruction(instr: str) -> "IntCodeCommand":
        """Get the opcode from the instruction (last 2 characters), return the correct command class"""
        opcode: str = instr[-2:]
        if len(opcode) == 1:
            opcode = "0" + opcode
        command_codes: dict = {
            "01": AddCommand,
            "02": MultiplyCommand,
            "03": InputCommand,
            "04": OutputCommand,
            "05": JumpIfTrueCommand,
            "06": JumpIfFalseCommand,
            "99": ExitCommand,
        }
        try:
            command_class: ClassVar = command_codes[opcode]
            return command_class()
        except KeyError as e:
            raise UnknownCommandError(f"No command for opcode '{opcode}'") from e

    @classmethod
    def get_command_params(cls):
        return cls.command_params

    @abc.abstractmethod
    def execute(self, *args) -> dict:
        """To be implemented by sub-classes

        Must return a Dict that maps index to updated value(s)
        The "position" key in the dict indicates that the programs position should be updated
        to a certain index
        """
        raise NotImplementedError("Cannot run 'execute' on base IntCodeCommand class")


class AddCommand(IntCodeCommand):
    """Add command takes 2 inputs and returns 1 output"""

    command_params = CommandParams(input_indices=[0, 1], output_indices=[2])

    def execute(self, num1: int, num2: int, out_index: int) -> dict:
        result: int = num1 + num2
        return {out_index: str(result)}


class MultiplyCommand(IntCodeCommand):
    """Add command takes 2 inputs and returns 1 output"""

    command_params = CommandParams(input_indices=[0, 1], output_indices=[2])

    def execute(self, num1: int, num2: int, out_index: int) -> dict:
        result: int = num1 * num2
        return {out_index: str(result)}


class InputCommand(IntCodeCommand):
    """Input command just sends a value to 1 output

    >>> InputCommand.set_default_input("5")
    >>> icp = IntCodeProgram(["103", "2", "34"])
    >>> icp._run_instruction()
    >>> assert icp.command_list[2] == "5"
    """

    command_params = CommandParams(input_indices=[], output_indices=[0])
    default_input: Any = "1"

    @classmethod
    def set_default_input(cls, default: Any):
        cls.default_input = default

    def execute(self, in_index: int) -> dict:
        return {in_index: self.default_input}


class OutputCommand(IntCodeCommand):
    """
    Output command prints a value from 1 input

    >>> icp = IntCodeProgram(["104", "4"])
    >>> icp._run_instruction()
    4
    >>> icp = IntCodeProgram(["04", "2", "7"])
    >>> icp._run_instruction()
    7
    """

    command_params = CommandParams(input_indices=[0], output_indices=[])

    def execute(self, int_to_output: int) -> dict:
        print(int_to_output)
        return {}


class JumpIfTrueCommand(IntCodeCommand):
    """
    JumpIfTrue command returns a new pointer index if the first input is nonzero

    >>> icp = IntCodeProgram(["5", "3", "4", "0", "27"])
    >>> icp._run_instruction()
    >>> assert icp.command_list == ["5", "3", "4", "0", "27"]
    >>> assert icp.position == 3
    >>> icp = IntCodeProgram(["05", "3", "4", "1", "21"])
    >>> icp._run_instruction()
    >>> assert icp.command_list == ["05", "3", "4", "1", "21"]
    >>> assert icp.position == 21
    >>> icp = IntCodeProgram(["1105", "0", "4"])
    >>> icp._run_instruction()
    >>> assert icp.command_list == ["1105", "0", "4"]
    >>> assert icp.position == 3
    >>> icp = IntCodeProgram(["1105", "3", "4", "1", "21"])
    >>> icp._run_instruction()
    >>> assert icp.command_list == ["1105", "3", "4", "1", "21"]
    >>> assert icp.position == 4
    """

    command_params = CommandParams(input_indices=[0, 1], output_indices=[])

    def execute(self, param_to_check: int, jump_to_ind: int) -> dict:
        if param_to_check != 0:
            return {"position": jump_to_ind}
        return {}


class JumpIfFalseCommand(IntCodeCommand):
    """
    JumpIfFalse command returns a new pointer index if the first input is zero

    >>> icp = IntCodeProgram(["6", "3", "4", "0", "27"])
    >>> icp._run_instruction()
    >>> assert icp.command_list == ["6", "3", "4", "0", "27"]
    >>> assert icp.position == 27
    >>> icp = IntCodeProgram(["06", "3", "4", "1", "21"])
    >>> icp._run_instruction()
    >>> assert icp.command_list == ["06", "3", "4", "1", "21"]
    >>> assert icp.position == 3
    >>> icp = IntCodeProgram(["1106", "0", "4"])
    >>> icp._run_instruction()
    >>> assert icp.command_list == ["1106", "0", "4"]
    >>> assert icp.position == 4
    >>> icp = IntCodeProgram(["1106", "3", "4", "1", "21"])
    >>> icp._run_instruction()
    >>> assert icp.command_list == ["1106", "3", "4", "1", "21"]
    >>> assert icp.position == 3
    """

    command_params = CommandParams(input_indices=[0, 1], output_indices=[])

    def execute(self, param_to_check: int, jump_to_ind: int) -> dict:
        if param_to_check == 0:
            return {"position": jump_to_ind}
        return {}


class ExitCommand(IntCodeCommand):
    """Exit command just quits everything"""

    def execute(self, *args) -> None:
        sys.exit(0)


class IntCodeProgram:
    def __init__(self, command_list: List[str]):
        # so we don't modify the input list in place
        self.command_list: List[str] = command_list.copy()
        self.position: int = 0

    def run(self) -> None:
        """Run until we reach the exit or encounter an error"""
        while True:
            self._run_instruction()

    def _run_instruction(self) -> None:
        """Run a single instruction and increment the position pointer
        >>> icp = IntCodeProgram(["1002", "4", "3", "4", "33"])
        >>> icp._run_instruction()
        >>> assert icp.command_list[4] == "99"
        >>> icp = IntCodeProgram(["1101", "7", "3", "3"])
        >>> icp._run_instruction()
        >>> assert icp.command_list[3] == "10"
        >>> InputCommand.set_default_input("1")
        >>> icp = IntCodeProgram(["3", "4", "3", "3", "59"])
        >>> icp._run_instruction()
        >>> assert icp.command_list[4] == "1"
        """
        # get the class for the command
        instr: str = self.command_list[self.position]
        command_class: IntCodeCommand = IntCodeCommand.get_command_from_instruction(
            instr
        )
        # get the arguments we send to the command
        command_params: CommandParams = command_class.get_command_params()
        command_args = self.__get_input_params(instr, command_params)
        # run the command
        output_map = command_class.execute(*command_args)
        # update the indices with the value(s) returned from the command
        has_jumped: bool = False
        for index, value in output_map.items():
            # special handling for jump commands
            if index == "position":
                self.position = value
                has_jumped = True
            else:
                self.command_list[index] = value
        # increment the position appropriately
        if not has_jumped:
            self.position += command_params.num_params + 1

    def __get_input_params(
        self, instr: str, command_params: CommandParams
    ) -> List[int]:
        """Get the actual input for a given instruction

        :param instr: raw instruction
        :param command_params: CommandParams tell us which params are inputs vs outputs
                               b/c they are handled differently
        :return: List[int] input for the given instruction
        >>> icp = IntCodeProgram(["110", "1"])
        >>> cp = CommandParams(input_indices=[0], output_indices=[1])
        >>> icp._IntCodeProgram__get_input_params("110", cp)
        [1]
        >>> icp = IntCodeProgram(["010", "2", "3"])
        >>> cp = CommandParams(input_indices=[0], output_indices=[])
        >>> icp._IntCodeProgram__get_input_params("010", cp)
        [3]
        >>> icp = IntCodeProgram(["1010", "3", "3", "900"])
        >>> cp = CommandParams(input_indices=[0, 1], output_indices=[])
        >>> icp._IntCodeProgram__get_input_params("1010", cp)
        [900, 3]
        >>> icp = IntCodeProgram(["1002", "4", "3", "4", "33"])
        >>> cp = CommandParams(input_indices=[0, 1], output_indices=[2])
        >>> icp._IntCodeProgram__get_input_params("1002", cp)
        [33, 3, 4]
        >>> icp = IntCodeProgram(["1101", "100", "-1", "4", "0"])
        >>> cp = CommandParams(input_indices=[0, 1], output_indices=[2])
        >>> icp._IntCodeProgram__get_input_params("1101", cp)
        [100, -1, 4]
        >>> icp = IntCodeProgram(["11101", "100", "-1", "4", "0"])
        >>> cp = CommandParams(input_indices=[0, 1], output_indices=[2])
        >>> icp._IntCodeProgram__get_input_params("1101", cp)
        [100, -1, 4]
        >>> icp = IntCodeProgram(["3", "5", "-1", "4", "0", "27"])
        >>> cp = CommandParams(input_indices=[0], output_indices=[])
        >>> icp._IntCodeProgram__get_input_params("3", cp)
        [27]
        """
        # pad front with 0s b/c leading 0s are assumed
        expected_len: int = 2 + command_params.num_params
        instr = "0" * (expected_len - len(instr)) + instr
        # reverse order b/c the rightmost param mode goes with the first param
        param_modes: str = instr[: command_params.num_params][::-1]
        instr_args: List[str] = self.command_list[
            self.position + 1 : self.position + command_params.num_params + 2
        ]
        final_args: List[int] = []
        # loops over a tuple of parameter mode, value of instruction, index of parameter relative to instruction
        for (p_mode, arg, index) in zip(
            param_modes, instr_args, range(command_params.num_params)
        ):
            # input params
            if command_params.is_index_input(index):
                # position mode
                if p_mode == "0":
                    index: int = int(arg)
                    f_arg = self.command_list[index]
                    final_args.append(int(f_arg))
                # immediate mode
                elif p_mode == "1":
                    final_args.append(int(arg))
            # output params are different b/c outputs are always in position mode
            else:
                final_args.append(int(arg))
        return final_args


def parse_input(input_path: Path) -> List[str]:
    if not input_path.exists():
        print(f"Bad input path. '{input_path}' does not exist.")
        return []
    input_text: str = input_path.read_text()
    command_list: List[str] = []
    for comm in input_text.split(","):
        command_list.append(comm.strip())
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
