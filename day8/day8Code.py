from adventOfCode2023.utils import read_input
import re
from collections import deque
from math import lcm
from functools import reduce
from copy import deepcopy


def parse_data(data:[]):
    instructions = deque([*data[0]])

    # make lookup dict
    directions = {}

    for row in data[2:]:
        nodes = [m[0] for m in re.finditer(r'[A-Z0-9]+', row)]
        directions[nodes[0]] = {
            "L": nodes[1],
            "R": nodes[2],
        }

    return instructions, directions


def iterate(start: str, instructions: deque, directions: {}):
    moves=0
    origin = start
    while True:
        this_instruction = instructions[0]
        origin = directions[origin][this_instruction]
        moves += 1
        instructions.rotate(-1) # rotate the instructions deque to the left by 1

        if origin[-1] == "Z":
            return moves, origin

    return moves


def part1(data: []):
    # extract the instructions and the map
    instructions, directions = parse_data(data=data)
    print(iterate(start="AAA", instructions=instructions, directions=directions))


def part2(data: []):
    instructions, directions = parse_data(data=data)

    # for each possible starting point, compute the times taken to reach each possible destination, if reachable
    
    origins = [x for x in directions.keys() if x[-1] == "A"]

    # compute traversal times and which destinations each origin reaches
    traversal_times = [iterate(start=x, instructions=instructions, directions=directions) for x in origins]

    print(lcm(*[x[0] for x in traversal_times]))


if __name__ == "__main__":
    data = read_input("day8Input.txt")
    part1(data=data)
    part2(data=data)