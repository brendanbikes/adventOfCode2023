from adventOfCode2023.utils import read_input
from itertools import combinations
import re
import multiprocessing



def parse_pattern(pattern: str):
    # parse a pattern into component indices using regex
    working_springs = [m.start() for m in re.finditer(r'\#', pattern)]
    uncertains = [m.start() for m in re.finditer(r'\?', pattern)]
    return working_springs, uncertains, len(pattern)


def make_combinations(uncertains: [], n: int):
    # find the indices of the ? in the string, and enumerate the number of combinations of picking n of them
    return combinations(uncertains, n)


def repeat_pattern(springs: [], length: int):
    # repeat a given supposed pattern of working springs 2x to ensure the wrap-around works
    return springs + [x+length for x in springs]


def validate(working_springs: [], groups: [], possible: []):
    # validate whether the given possible indices for working springs, in the given pattern, satisfies the given groupings
    all_working = sorted(working_springs + possible) # indices of all possible working springs
    new_groups = []
    
    full_all_working = []
    for i in range(len(all_working)):
        if not new_groups:
            new_groups.append(1)
        else:
            if all_working[i] - all_working[i-1] == 1: #adjacent -- add to this group
                new_groups[-1]+=1
            else:
                new_groups.append(1) # start next group
    
    if new_groups == groups:
        return True
    else:
        return False


def analyze(pattern: str, groups:[]):
    working_springs, uncertains, pattern_length = parse_pattern(pattern=pattern)
    to_allocate = sum(groups) - len(working_springs) # how many to allocate, among the uncertains?
    possibles = make_combinations(uncertains=uncertains, n=to_allocate)
    validated = [x for x in possibles if validate(working_springs=working_springs, groups=groups, possible=list(x))]
    return len(validated)


def run(row: str, idx: int, return_dict: {}):
    pattern, groups = row.split(" ")
    groups = [int(x) for x in groups.split(",")]

    start_to_end = analyze(pattern=pattern, groups=groups)

    # for part 2:
    # 1) compute the # of expected valid arrangements within 1 iteration of the pattern, without the linkage component
    # 2) compute the # of expected valid arrangements within 1 iteration of the pattern, WITH the linkage component
    # 3) compute the # of expected valid arrangements for 2 iterations of the pattern with linkage
    # 4) if the value from #2 differs from the value from #3 squared, then the repeated patterns are dependent, and the difference is their interactivity; if #2 == (#3)^2, then the interactivity component is 0

    pattern2 = pattern + "?"
    repeated_pattern_2 = pattern2 + pattern2
    repeated_groups = groups*2

    start_to_linkage = analyze(pattern=pattern2, groups=groups)
    start_to_linkage_repeated = analyze(pattern=repeated_pattern_2, groups=repeated_groups)

    interactivity_factor = start_to_linkage_repeated / (start_to_linkage**2)

    result_part_2 = int(start_to_linkage**4 * interactivity_factor**4 * start_to_end)

    print(f"Finished for row {idx}")

    return_dict[idx] = [start_to_end, result_part_2]

        
def part1_and_2():
    data = read_input("day12Input.txt")

    valids_part_1 = []
    valids_part_2 = []
    z = 0

        
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    jobs = []
    for idx, row in enumerate(data):
        p = multiprocessing.Process(target=run, args=(row, idx, return_dict))
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()
    
    print(sum([x[0] for x in return_dict.values()]))
    print(sum([x[1] for x in return_dict.values()]))


if __name__ == "__main__":
    part1_and_2()