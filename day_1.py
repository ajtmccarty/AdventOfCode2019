from math import floor
from pathlib import Path
from typing import List

INPUT_FILE_NAME = "input_1.txt"


def main_1(module_masses: List[int]) -> None:
    print("Computing answer for part 1...")
    total_fuel: int = sum([fuel_requirement(mod_mass) for mod_mass in module_masses])
    print(f"Total fuel required: {total_fuel}")


def main_2(module_masses: List[int]) -> None:
    print("Computing answer for part 2...")


def parse_input() -> List[int]:
    input_file_path: Path = Path(INPUT_FILE_NAME)
    input_text: str = input_file_path.read_text()
    module_masses: List[int] = []
    for str_mod_mass in input_text.split("\n"):
        stripped_mod_mass: str = str_mod_mass.strip()
        if stripped_mod_mass:
            module_masses.append(int(stripped_mod_mass))
    return module_masses


def fuel_requirement(module_mass: int) -> int:
    return floor(module_mass / 3) - 2


if __name__ == "__main__":
    print()
    print("Parsing input...")
    parsed_input = parse_input()
    print()
    main_1(parsed_input)
    print()
    main_2(parsed_input)
