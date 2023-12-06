from adventOfCode2023.utils import read_input
from math import prod

MAXIMUMS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

def parts_1_and_2():
    # part 1: sum the IDs of valid games
    # part 2: sum the "power" (product of minimum # of cubes of each color required to allow the drawn sample) for each valid game
    data = read_input("day2Input.txt")

    valid_games_id_sum = 0
    total_power = 0
    i=1
    for game in data:
        game = parse_game(game=game)
        if validate_game(game=game):
            valid_games_id_sum += i
        total_power += compute_power(game=game)
        i+=1

    print(f"The total of the IDs of all valid games is {valid_games_id_sum}")
    print(f"The total power of all valid games is {total_power}")


def validate_game(game: list[dict]):
    # validate each sample in a game

    for sample in game:
        for color in sample.keys():
            if sample[color] > MAXIMUMS[color]:
                # a sample is invalid, so the whole game is invalid
                return False
    return True


def compute_power(game: list[dict]):
    # compute the power of a valid game, by flattening the samples into a single dict, taking the maximum of any conflicts, and multiplying the results
    
    minimums = {}
    for sample in game:
        for color, num in sample.items():
            if color in minimums.keys():
                minimums[color] = max(num, minimums[color])
            else:
                minimums[color] = num

    print(minimums.values())
    print(prod([x for x in minimums.values()]))
    
    return prod([x for x in minimums.values()])


def parse_game(game: str):
    # parse a game string into [{}] list of dicts
    __, samples = game.split(": ")

    samples = samples.split("; ")

    parsed_samples = []
    for sample in samples:
        cubes = {}
        cubes_string = sample.split(", ")
        for cube in cubes_string:
            num, color = cube.split(" ")
            cubes[color] = int(num)

        parsed_samples.append(cubes)

    return parsed_samples


if __name__ == "__main__":
    parts_1_and_2()