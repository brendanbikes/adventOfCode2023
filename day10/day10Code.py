from adventOfCode2023.utils import read_input


def find_start(data: [], m: int, n: int):
    for i in range(m):
        for j in range(n):
            if data[i][j] == "S":
                return (i,j)


def cardinals(coord: tuple):
    i, j = coord
    return (i-1, j), (i+1, j), (i, j+1), (i, j-1) # north, south, east, west


def fix_start(data: [], graph: {}, start: (), m: int, n: int):
    # given the initial data, the parsed graph, and the start location, replace the "S" with the actual pipe that should be there
    
    neighbors = get_neighbors(coord=start, data=data, m=m, n=n)
    north, south, east, west = cardinals(coord=start)
    i, j = start

    # reverse the mapping from the get_neighbors function, oh well
    if neighbors == set([west, south]):
        c = "7"
    elif neighbors == set([west, east]):
        c = "-"
    elif neighbors == set([north, south]):
        c = "|"
    elif neighbors == set([north, west]):
        c = "J"
    elif neighbors == set([north, east]):
        c = "L"
    elif neighbors == set([east, south]):
        c = "F"
    data = [[x if x!= "S" else c for x in row] for row in data]
    return data


def get_neighbors(coord: tuple, data: [], m: int, n: int):
    # given a pipe character, its coordinate, and the grid size, return its connected neighbors
    i, j = coord
    char = data[i][j]
    north, south, east, west = cardinals(coord=coord)
    
    if char == "S":
        # look for this coordinate (i,j) in the set of all neighbors of the neighbors of (i,j) -- look in all directions; the possible neighbors that have this (i,j) in their own neighbors are true neighbors
        neighbors = [x for x in [west, east, south, north] if coord in get_neighbors(coord=x, data=data, m=m, n=n)]

    if char == "7":
        neighbors = west, south
    
    elif char == "-":
        neighbors = west, east
    
    elif char == "|":
        neighbors = north, south
    
    elif char == "J":
        neighbors = north, west
    
    elif char == "L":
        neighbors = north, east

    elif char == "F":
        neighbors = east, south

    elif char == ".":
        neighbors = ()

    return set([x for x in neighbors if x[0] in range(m) and x[1] in range(n)])


def parse_graph(data: [], m: int, n: int):
    # parse the graph into a dictionary describing the connectivity; keys are tuples (i,j), and values are lists of each pipe's 2 connecting neighbors (k1, k2), (k3, k4)
    # then when traversing the graph, each time we query the dict, we get a list of the node's 2 neighbors

    graph = {}
    for i, row in enumerate(data):
        for j in range(len(row)):
            graph[(i,j)] = get_neighbors(coord=(i,j), data=data, m=m, n=n)

    return graph
    

def part1_and_2():
    data = read_input("day10Input.txt")
    m = len(data)
    n = len(data[0])
    graph = parse_graph(data=data, m=m, n=n)
    start = find_start(data=data, m=m, n=n)
    data = fix_start(data=data, graph=graph, start=start, m=m, n=n) # replace the animal in the data with the actual pipe

    # from the start point, compute the # of unique nodes in its circular path back to itself
    # pursue both directions simultaneously -- while the set of new neighbors are not entirely contained within the set of visited nodes, keep proceeding

    path_nodes = set()
    origins=[start]
    while True:
        neighbors = set()
        for origin in origins:
            neighbors |= (get_neighbors(coord = origin, data=data, m=m, n=n))
        if set(neighbors).issubset(path_nodes) and len(path_nodes) > 0:
            break
        else:
            origins = [x for x in list(set(neighbors).difference(path_nodes))]
            path_nodes |= set(neighbors)

    n = len(path_nodes)
    opp = n // 2 # the opposition, or point the furthest network distance away, is floor division by 2 of the length of the path in # of unique nodes
    print(opp)

    # part 2 - given the list of coordinates in the loop, compute the enclosed area
    # for each row of the grid, add up the # of points between each pair of intersection points between the loop pipes and an imaginary horizontal line across the row
    # critically, pipes without a vertical component cannot intersect this imaginary line -- i.e. -, 7, and F pipes are not counted
    area = 0
    for i in range(m):
        cross_points = [j for j, char in enumerate(data[i]) if (char not in ("-", "7", "F") and (i,j) in path_nodes)]
        enclosed_ranges = [range(a, b) for a, b in zip(cross_points[::2], cross_points[1::2])]
        area += sum(len([y for y in x if y not in [p[1] for p in list(path_nodes) if p[0] == i]]) for x in enclosed_ranges)

    print(area)

if __name__ == "__main__":
    part1_and_2()