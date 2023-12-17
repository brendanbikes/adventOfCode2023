from adventOfCode2023.utils import read_input


def compute_load(rocks: [], size: int):
    # compute load on the left rail -- sum of distances of each rock from the right rail
    return sum([sum([size - rock for rock in row]) for row in rocks])


def rotate_cw(indices: [], is_barriers: bool, size: int):
    # rotate clockwise 90 degrees
    new_indices = []
    for j in range(size):
        new_row = []
        for i, row in enumerate(indices[::-1]):
            if j in row:
                new_row.append(i)
        if is_barriers:
            new_row = [-1] + new_row + [size]
        new_indices.append(new_row)

    return new_indices
    

def rotate_ccw(indices: [], is_barriers: bool, size: int):
    # rotate the grid counterclockwise 90 degrees, because the "tilt" mechanism/function only tilts to the left
    new_indices = []
    for j in range(size)[::-1]:
        new_row = []
        for i, row in enumerate(indices):
            if j in row:
                new_row.append(i)
        if is_barriers:
            new_row = [-1] + new_row + [size]
        new_indices.append(new_row)
    
    return new_indices


def tilt(barriers: [], rocks: []):
    # given a current list of rocks and barriers, tilt the grid to the left and find the new rock positions
    barrier_index = 0
    new_index = 0
    all_new_rocks = []

    for barriers, rocks in zip(barriers, rocks):
        # for each barrier j, find the rocks indices between it and the next barrier, and line them up from j+1
        new_rocks = []
        for k, barrier in enumerate(barriers[:-1]):
            num_rocks = len([x for x in rocks if x > barrier and x < barriers[k+1]])
            this_group = [x for x in range(barrier+1, barrier+1 + num_rocks)]
            new_rocks += this_group

        all_new_rocks.append(new_rocks)

    return all_new_rocks


def analyze_grid(grid: []):
    # from initial grid, determine each row or column's barrier points, using the "west" end as the reference endpoint
    all_barriers = []
    all_rocks = []

    for i, row in enumerate(grid):
        barriers = [-1] # label left barrier as -1 for computations
        rocks = []
        for j, x in enumerate(row):
            if x == "O":
                rocks.append(j)
            elif x == "#":
                barriers.append(j)
        
        barriers.append(j+1) # label right barrier/railing as j+1 for computations
        all_barriers.append(barriers)
        all_rocks.append(rocks)

    return all_barriers, all_rocks


def iterate_cycle(rocks: [], barriers: [], size: int, N: int):
    start_rocks = rocks[:]
    all_states = [start_rocks]
    
    for k in range(N * 4): # each cycle consists of 4 90-degree rotations, and 4 tilts
        # first tilt toward the left
        rocks = tilt(barriers=barriers[:], rocks=rocks[:])
        # rotate CW 90 degrees
        rocks = rotate_cw(indices=rocks[:], is_barriers=False, size=size)
        barriers = rotate_cw(indices=barriers[:], is_barriers=True, size=size)
        if rocks in all_states:
            # loop encountered
            print('loop encountered')
            idx = all_states.index(rocks)
            return idx, all_states, barriers
        else:
            all_states.append(rocks)

    return None, rocks


def part1_and_2():
    grid = read_input(file="day14Input.txt")
    m = len(grid) # grid is mxm by inspection

    barriers, rocks = analyze_grid(grid=grid)

    # part 1 -- rotate grid 90 degrees CCW 1x, and measure the load
    start_rocks = rotate_ccw(indices=rocks[:], is_barriers=False, size=m)
    start_barriers = rotate_ccw(indices=barriers[:], is_barriers=True, size=m)
    tilted_rocks = tilt(barriers=start_barriers[:], rocks=start_rocks[:])
    print(compute_load(rocks=tilted_rocks[:], size=m))

    # part 2 -- starting with the orientation from part 1, complete 1000000000 cycles of tilting towards N, E, S, W
    # also, if the rock positions ever equal the starting positions, stop, because we have hit a loop and can determine the final state from that
    rocks = start_rocks[:]
    barriers = start_barriers[:]

    N = 1000000000

    M, rocks, barriers = iterate_cycle(rocks=start_rocks[:], barriers=start_barriers[:], size=m, N=N)

    # loop encountered, starting at index M, and lasting for len(rocks) - M (size of loop)
    loop_size = len(rocks) - M
    R = (4*N - M) % loop_size # remainder
    print(compute_load(rocks=rocks[M+R], size=m))


if __name__ == "__main__":
    part1_and_2()