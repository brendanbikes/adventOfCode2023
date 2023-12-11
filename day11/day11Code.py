from adventOfCode2023.utils import read_input
from itertools import combinations



def expand_universe(galaxies: [], voids_horizontal: [], voids_vertical: [], expansion_factor: int):
    # for each horizontal void, increment the  component of all galaxies' positions higher in i position than the void by 1
    expansion_factor -= 1 # map from * of times bigger to how many rows/cols to add, accounting for the initial one
    while voids_horizontal:
        void_horizontal = voids_horizontal.pop(0)
        galaxies = [galaxy if galaxy[0] < void_horizontal else (galaxy[0]+expansion_factor, galaxy[1]) for galaxy in galaxies]
        voids_horizontal = [v + expansion_factor for v in voids_horizontal] # shift coords of other voids too

    while voids_vertical:
        void_vertical = voids_vertical.pop(0)
        galaxies = [galaxy if galaxy[1] < void_vertical else (galaxy[0], galaxy[1]+expansion_factor) for galaxy in galaxies]
        voids_vertical = [v + expansion_factor for v in voids_vertical]

    return galaxies


def map_universe(data: []):
    galaxies = []
    voids_horizontal = []
    voids_vertical = []
    for i, row in enumerate(data):
        if row == "."*len(row):
            voids_horizontal.append(i)
        for j, point in enumerate(row):
            if point == "#":
                galaxies.append((i,j))
    
    for j in range(len(data[0])):
        if [row[j] for row in data] == ["."]*len(data):
            voids_vertical.append(j)

    return galaxies, voids_horizontal, voids_vertical


def shortest_path(galaxy1: tuple, galaxy2: tuple):
    return abs(galaxy1[0]-galaxy2[0]) + abs(galaxy1[1]-galaxy2[1])
    

def part1_and_2():
    data = read_input("day11Input.txt")
    galaxies, voids_horizontal, voids_vertical = map_universe(data=data)
    galaxies_expanded = expand_universe(galaxies=galaxies[:], voids_horizontal=voids_horizontal[:], voids_vertical=voids_vertical[:], expansion_factor=2)
    print(sum([shortest_path(galaxy1=pair[0], galaxy2=pair[1]) for pair in combinations(galaxies_expanded, 2)]))

    galaxies_expanded = expand_universe(galaxies=galaxies[:], voids_horizontal=voids_horizontal[:], voids_vertical=voids_vertical[:], expansion_factor=1000000)
    print(sum([shortest_path(galaxy1=pair[0], galaxy2=pair[1]) for pair in combinations(galaxies_expanded, 2)]))


if __name__ == "__main__":
    part1_and_2()