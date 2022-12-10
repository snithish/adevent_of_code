from typing import List
from textwrap import wrap

WIDTH = 40


def find_char(cycle: int, sprite_pos: int) -> str:
    if cycle % WIDTH in [sprite_pos - 1, sprite_pos, sprite_pos + 1]:
        return "#"
    return "."


def main(commands: List[str]) -> str:
    sprite_pos = 1
    screen = ""
    cycles = []
    for command in commands:
        match command.split(" "):
            case ['noop']:
                cycles.append(0)
            case ['addx', distance]:
                cycles.extend([0, int(distance)])
    for cycle, distance in enumerate(cycles):
        screen += find_char(cycle, sprite_pos)
        sprite_pos += distance
    return screen


if __name__ == '__main__':
    with open("./data/aoc_10.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]
    res = main(lines)
    for row in (wrap(res, width=WIDTH)):
        print(row)
