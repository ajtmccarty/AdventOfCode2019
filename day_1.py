import argparse
import doctest
from math import floor
from pathlib import Path
import sys
from typing import List

INPUT_FILE_NAME = "input_1.txt"


def main_1(module_masses: List[int]) -> int:
    return sum([fuel_requirement(mod_mass) for mod_mass in module_masses])


def main_2(module_masses: List[int]) -> int:
    return sum([fuel_requirement(mod_mass, add_fuel_for_fuel=True) for mod_mass in module_masses])


def parse_input() -> List[int]:
    input_file_path: Path = Path(INPUT_FILE_NAME)
    input_text: str = input_file_path.read_text()
    module_masses: List[int] = []
    for str_mod_mass in input_text.split("\n"):
        stripped_mod_mass: str = str_mod_mass.strip()
        if stripped_mod_mass:
            module_masses.append(int(stripped_mod_mass))
    return module_masses


def fuel_requirement(module_mass: int, add_fuel_for_fuel: bool = False) -> int:
    """

    >>> fuel_requirement(12)
    2
    >>> fuel_requirement(14)
    2
    >>> fuel_requirement(1969)
    654
    >>> fuel_requirement(100756)
    33583

    >>> fuel_requirement(14, add_fuel_for_fuel=True)
    2
    >>> fuel_requirement(1969, add_fuel_for_fuel=True)
    966
    >>> fuel_requirement(100756, add_fuel_for_fuel=True)
    50346

    :param module_mass: int, mass of the module
    :param add_fuel_for_fuel: bool, default False, whether to recursively
        calculate fuel required for weight of fuel added
    :return: int, amount of fuel required
    """
    fuel_required: int = floor(module_mass / 3) - 2
    if not add_fuel_for_fuel:
        return fuel_required
    if fuel_required <= 0:
        return 0
    return fuel_required + fuel_requirement(fuel_required, add_fuel_for_fuel)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-r", "--run", help="Run the solution", action="store_true")
    arg_parser.add_argument("-t", "--test", help="Run the tests for this solution", action="store_true")
    args = arg_parser.parse_args()

    if args.test:
        print("Running Tests...")
        failures, num_tests = doctest.testmod()
        if not failures:
            print(f"Ran {num_tests} test, 0 failures")
        else:
            sys.exit(1)
    if not args.test or args.run:
        print("Parsing input...")
        parsed_input = parse_input()
        print("Computing answer for part 1...")
        answer_1 = main_1(parsed_input)
        print(f"Answer for part 1: {answer_1}")
        print("Computing answer for part 2...")
        answer_2 = main_2(parsed_input)
        print(f"Answer for part 2: {answer_2}")
