from adventOfCode2023.utils import read_input
import re
import math



def calculate(times: [], distances = []):
    all_wins = []
    for race in zip(times, distances):
        time, max_distance = race

        for x in range(time):
            distance = x * (time-x)
            if distance > max_distance:
                # first win identified, so all numbers corresponding to a button press time between [x, time-x] will win, because deterministic linear process
                all_wins.append(len(range(x, time-x+1))) # +1 to make range() include the last value
                break

    return math.prod(all_wins)


def part1_and_2():
    data = read_input(file="day6Input.txt")

    times = [int(x[0]) for x in re.finditer(r'\d+', data[0])]
    distances = [int(x[0]) for x in re.finditer(f'\d+', data[1])]

    print(calculate(times=times, distances=distances))

    # part 2 - combine the nums
    time = int("".join([str(x) for x in times]))
    distance = int("".join([str(x) for x in distances]))

    print(calculate(times=[time], distances=[distance]))

if __name__ == "__main__":
    part1_and_2()
