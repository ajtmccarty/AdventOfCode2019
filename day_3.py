"""Solution for https://adventofcode.com/2019/day/3/"""
from argparse import ArgumentParser
import doctest
from pathlib import Path
from typing import Dict, List, Tuple

DEFAULT_INPUT_FILE_PATH = "input_3.txt"


def main_1(parsed_input) -> int:
    wires = [Wire(wire_input) for wire_input in parsed_input]
    cb = CircuitBox(*wires)
    intersections = cb.get_intersections()
    return min([manhattan_distance((0, 0), coord) for coord in intersections])


def main_2(parsed_input) -> int:
    wires = [Wire(wire_input) for wire_input in parsed_input]
    cb = CircuitBox(*wires)
    intersections = cb.get_intersections()
    total_steps_to_interections: List[int] = []
    for intsxn in intersections:
        total_steps_to_interections.append(
            sum([w.how_many_steps_to(intsxn) for w in cb.wires])
        )
    return min(total_steps_to_interections)


def parse_input(input_path: Path) -> List[List[str]]:
    if not input_path.exists():
        print(f"Bad input path. '{input_path}' does not exist.")
        return []
    input_text: str = input_path.read_text()
    wire_paths = []
    for wire_path in input_text.split("\n"):
        wire = []
        for path_piece in wire_path.split(","):
            wire.append(path_piece.strip())
        wire_paths.append(wire)
    return wire_paths


class Wire:

    direction_to_function_map = {
        "U": "add_one_up",
        "D": "add_one_down",
        "L": "add_one_left",
        "R": "add_one_right",
    }

    def __init__(self, path_list: List[str]):
        """
        >>> w = Wire(["U1", "R1", "D1", "L1"])
        >>> assert w.coords_list == [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]

        >>> w = Wire(["U1", "R2", "D1", "L2"])
        >>> assert w.coords_list == [(0, 0), (0, 1), (1, 1), (2, 1), (2, 0), (1, 0), (0, 0)]
        """
        self.coords_list: List[Tuple[int, int]] = [(0, 0)]
        for path_str in path_list:
            self.add_length(path_str)

    @property
    def last_position(self) -> Tuple[int, int]:
        return self.coords_list[-1]

    def add_length(self, length_str: str) -> None:
        direction: str = length_str[0]
        assert direction in self.direction_to_function_map
        distance: int = int(length_str[1:])

        function_name = self.direction_to_function_map[direction]
        direction_function = getattr(self, function_name)
        for _ in range(distance):
            direction_function()

    def add_one_up(self) -> None:
        last_pos = self.last_position
        new_pos: Tuple[int, int] = (last_pos[0], last_pos[1] + 1)
        self.coords_list.append(new_pos)

    def add_one_down(self) -> None:
        last_pos = self.last_position
        new_pos: Tuple[int, int] = (last_pos[0], last_pos[1] - 1)
        self.coords_list.append(new_pos)

    def add_one_left(self) -> None:
        last_pos = self.last_position
        new_pos: Tuple[int, int] = (last_pos[0] - 1, last_pos[1])
        self.coords_list.append(new_pos)

    def add_one_right(self) -> None:
        last_pos = self.last_position
        new_pos: Tuple[int, int] = (last_pos[0] + 1, last_pos[1])
        self.coords_list.append(new_pos)

    def how_many_steps_to(self, coord: Tuple[int, int]) -> int:
        return self.coords_list.index(coord)


class CircuitBox:
    def __init__(self, *args):
        """
        >>> w1 = Wire(["U3"])
        >>> w2 = Wire(["R1","U2","L2"])
        >>> cb = CircuitBox(w1, w2)
        >>> assert cb.get_intersections(include_origin=True) == [(0, 0), (0, 2)]
        >>> assert cb.get_intersections() == [(0, 2)]

        :param args:
        """
        self.wires: List[Wire] = args
        # format {x-val: {y-val: [Wire1, Wire2]}}
        self.coord_grid: Dict[int, Dict[int, list]] = {0: {0: []}}
        self._intersections: List[Tuple[int, int]] = []
        for wire in args:
            assert isinstance(wire, Wire)
            self.add_wire(wire)

    def add_wire(self, wire: Wire) -> None:
        for x, y in wire.coords_list:
            if x not in self.coord_grid:
                self.coord_grid[x] = {}
            if y not in self.coord_grid[x]:
                self.coord_grid[x][y] = []
            this_coord: List[Wire] = self.coord_grid[x][y]
            # if crossing another wire, add to _intersections
            if any((w is not wire for w in this_coord)):
                self._intersections.append((x, y))
            this_coord.append(wire)

    def get_intersections(self, include_origin: bool = False) -> List[Tuple[int, int]]:
        intersections_copy = self._intersections.copy()
        if not include_origin:
            intersections_copy.remove((0, 0))
        return intersections_copy


def manhattan_distance(coord_1, coord_2) -> int:
    """
    >>> manhattan_distance((0, 0), (3, 3))
    6
    >>> manhattan_distance((0, 0), (-3, 3))
    6
    >>> manhattan_distance((-3, 3), (-3, -3))
    6
    """
    return abs(coord_1[0] - coord_2[0]) + abs(coord_1[1] - coord_2[1])


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
