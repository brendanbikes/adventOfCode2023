from adventOfCode2023.utils import read_input
from math import prod


def part1():
    data = read_input("day15Input.txt")[0].split(",")

    results = []
    for instruction in data:
        current_value = 0
        for char in instruction:
            current_value += ord(char)
            current_value *= 17
            current_value = current_value % 256
        results.append(current_value)
    
    print(sum(results))
        


def part2():
    data = read_input("day15Input.txt")[0].split(",")
    boxes = {
        k: []
        for k in range(256)
    }

    for instruction in data:
        if "-" in instruction:
            code = instruction.split("-")[0]
    
        elif "=" in instruction:
            code, focal_length = instruction.split("=")

        box_number = 0
        for char in code:
            box_number += ord(char)
            box_number *= 17
            box_number = box_number % 256
        
        if "-" in instruction:
            # go to box box_number and remove lens with the specified label, if present, and shift others forward
            boxes[box_number] = [lens for lens in boxes[box_number] if lens[0] != code]

        elif "=" in instruction:
            # replace existing lens with same label, if present; otherwise append new lens
            if code in [x[0] for x in boxes[box_number]]:
                index = [x[0] for x in boxes[box_number]].index(code)
                boxes[box_number][index] = (code, focal_length)

            else:
                boxes[box_number].append((code, focal_length))

    # sum the products of lens focal lengths    
    total = 0
    for box_number, box in boxes.items():
        if box:
            total += sum([(box_number+1) * (lens_slot+1) * int(lens[1]) for lens_slot, lens in enumerate(box)])
    print(total)


if __name__ == "__main__":
    part1()
    part2()