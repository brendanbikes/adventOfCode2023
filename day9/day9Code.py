import re
from adventOfCode2023.utils import read_input


def extrapolate_history(history: [], direction: str):
    trace = [history]

    i = 0
    while True:
        # calculate a diff array
        diffs = [trace[-1][i+1]-trace[-1][i] for i in range(len(trace[-1])-1)]
        trace.append(diffs)

        if diffs == [0]*len(diffs):
            break
        i+=1

    # add another 0 to final row
    trace[-1].append(0)
    
    for i in range(len(trace)-1): # propagate upwards N-1 times
        if direction == "forward":
            trace[-1-(i+1)].append(trace[-1-i][-1]+trace[-1-(i+1)][-1])
        elif direction == "backward":
            trace[-1-(i+1)].append(trace[-1-i][-1]-trace[-1-(i+1)][-1])

    return trace
        

def part1_and_2():
    data = read_input("day9Input.txt")

    histories = []
    for row in data:
        histories.append([int(x) for x in row.split(" ")])
    
    traces = [extrapolate_history(history=history, direction="forward") for history in histories]
    print(sum([trace[0][-1] for trace in traces]))

    # part 2 - reverse the original history arrays, and set the extrapolation direction to "backwards"
    traces = [extrapolate_history(history=history[::-1], direction="backward") for history in histories]
    print(sum([trace[0][-1] for trace in traces]))


if __name__ == "__main__":
    part1_and_2()