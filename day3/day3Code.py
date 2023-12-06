from adventOfCode2023.utils import create_grid, read_input
import re


def find_numbers(data: list):
    # find all integer numbers in a given row, and compile their values and positions in a tuple, e.g. (205, (0, 9)) is integer 205 starting at position (0, 9)
    numbers = []
    for idx, row in enumerate(data):
        numbers += [(int(m[0]), (idx, m.start())) for m in re.finditer(r'\d+', row)]

    return numbers


def find_gears(data: list):
    # find positions of all gears to check
    gears = []
    for i, row in enumerate(data):
        gears += [(i,j) for j, char in enumerate([*row]) if char == "*"]

    return gears


def get_neighbors(number: tuple):
    # define neighbors to check: left endcap, right endcap, then row above and row below, including diagonals
    value, coord = number
    i, j = coord
    l = len(str(value))
    return [(i, j-1), (i, j+l)] + [(i-1, k) for k in range(j-1, j+l+1)] + [(i+1, k) for k in range(j-1, j+l+1)]


def is_part_number(number: tuple, grid: dict):
    # given a specific number (value, (i, j)) tuple and the overall grid, determine whether this number is a valid part number or not
    neighbors = get_neighbors(number=number)

    for neighbor in neighbors:
        value = grid.get(neighbor, ".")
        if value != "." and not value.isdigit():
            return True
    
    return False


def is_valid_gear(gear: tuple, valid_part_numbers: list, grid: dict):
    # given a specific gear's location (i, j), a list of valid part numbers, and the grid, determine whether a specific gear is valid
    # a valid gear is adjacent to 2 valid part numbers -- meaning the set of neighbor points of a given gear must intersect the sets of at least 2 different valid part numbers

    gear_neighbors = get_neighbors(number=("*", gear))
    adjacent_part_nums = []
    for num in valid_part_numbers:
        num_coords = [(num[1][0], j) for j in range(num[1][1], num[1][1]+len(str(num[0])))] #locations of the actual digits in the number
        if set(gear_neighbors) & set(num_coords):
            adjacent_part_nums.append(num)
        
    if len(adjacent_part_nums) == 2:
        return adjacent_part_nums
    else:
        return False
        

def parts_1_and_2():
    data = read_input(file="day3Input.txt")
    grid = create_grid(data=data)

    numbers = find_numbers(data=data)
    valid_part_numbers = [x for x in numbers if is_part_number(number=x, grid=grid)]
    total = sum([x[0] for x in valid_part_numbers])
    print(f"Total sum of valid part numbers: {total}")

    gears = find_gears(data=data)

    # use the combined information of gear locations and valid part numbers to identify valid gears
    total = 0
    for gear in gears:
        adjacent_part_nums = is_valid_gear(gear=gear, valid_part_numbers=valid_part_numbers, grid=grid)
        if adjacent_part_nums:
            total += adjacent_part_nums[0][0] * adjacent_part_nums[1][0]

    print(f"Total sum of gear ratios of valid gears: {total}")

if __name__ == "__main__":
    parts_1_and_2()