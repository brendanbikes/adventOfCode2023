from adventOfCode2023.utils import read_input
import re
from copy import deepcopy


def parse_data(data: []):
    # parse into usable stuff: list of seed IDs, and dict maps

    seed_ids = [int(m[0]) for m in re.finditer(f'\d+', data[0])] # seed IDs in 1st row of data

    maps = {}
    for row in data[2:]: # extract mappings
        if not row:
            continue
        elif row[0].isalpha(): # key to a new map
            key, __ = row.split(" ")
            key = key.split('-')
            key = (key[0], key[2]) # e.g. (seed, soil) for seed-to-soil map
            maps[key] = []
        
        else:
            row = [int(x) for x in row.split(" ")]
            row = (row[1], row[2], row[0]-row[1]) # source_range_start, range_length, modifier [to translate source to destination]
            maps[key].append(row)

    # sort the maps
    for key, m in maps.items():
        maps[key] = sorted(m, key=lambda x: x[0]) # sort by the first element of the tuples to make applying the maps easier

    return seed_ids, maps


def get_destination_from_source(source: str, maps: dict):
    k = [key[1] for key in maps.keys() if key[0] == source]
    if k:
        return k[0]
    else:
        return None


def map_seed_to_location(id: int, maps: dict):
    # given a seed ID, map it to its final location using the maps

    # initial source, destination
    source = "seed"
    destination = get_destination_from_source(source=source, maps=maps)

    while source != "location":
        for mapping in maps[(source, destination)]:
            if id >= mapping[0] and id <= mapping[0] + mapping[1]:
                id += mapping[2] # change ID by its modifier, if in range
                break # only a single match expected
        source = destination
        destination = get_destination_from_source(source=source, maps=maps)

    return id


def map_range_to_mapping(id_ranges: [tuple], maps: list, key: tuple):
    # algorithm to map a range onto 1 single mapping; returns a chopped up seed range, with mapping modifiers applied; output format is also (start_of_range, length_of_range)
    
    modified_ranges = [] # list of modified tuples
    for id_range in id_ranges:
        # chop up a given range using the starting points of all map segments
        this_map = deepcopy(maps.get(key))
        map_segment_start_points = [segment[0] for segment in this_map]
            
        dissolved_start_points = sorted([id_range[0]] + [m for m in map_segment_start_points if (id_range[0] <= m and m <= (id_range[0] + id_range[1]-1))])
        dissolved_ranges = [(x[0], x[1]-x[0]) for x in zip(dissolved_start_points, dissolved_start_points[1:] + [id_range[0]+id_range[1]])]

        # get range modifiers by looking at the map
        matches = []
        for dr in dissolved_ranges:
            for segment in this_map:
                if dr[0] >= segment[0] and dr[0] <= segment[0] + segment[1]-1:
                    modified_ranges.append((dr[0], dr[1], segment[2]))
                    matches.append(True)

            if not any(matches):
                modified_ranges.append((dr[0], dr[1], 0))

    # apply modifiers to split ranges simultaneously
    modified_ranges = [(x[0] + x[2], x[1]) for x in modified_ranges]
    
    return modified_ranges

        
def part1_and_2():
    data = read_input("day5Input.txt")
    seed_ids, maps = parse_data(data=data)

    location_ids = [map_seed_to_location(id=seed_id, maps=maps) for seed_id in seed_ids]
    print(f"The lowest location number is {sorted(location_ids)[0]}")

    # transform seed_ids to range tuples
    seed_id_ranges = [x for x in zip(seed_ids[0::2], seed_ids[1::2])]

    # initialize
    modified_ranges = deepcopy(seed_id_ranges)
    source = "seed"
    destination = get_destination_from_source(source=source, maps=maps)

    while source != "location":
        modified_ranges = map_range_to_mapping(id_ranges=modified_ranges, maps=maps, key=(source, destination))
        source = destination
        destination = get_destination_from_source(source=source, maps=maps)

    # find minimum location from all the ranges of location numbers
    print(min([x[0] for x in modified_ranges]))

if __name__ == "__main__":
    part1_and_2()