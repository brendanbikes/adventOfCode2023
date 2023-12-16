from adventOfCode2023.utils import read_input


def process_input(data: []):
    # split on empty rows
    patterns = []

    for idx, row in enumerate(data):
        if idx == 0:
            this_pattern = [row]
        elif not row or idx == len(data)-1:
            patterns.append(this_pattern)
            this_pattern = [] # reinitialize
        else:
            this_pattern.append(row)
    
    return patterns


def transpose_pattern(pattern: []):
    pattern_transposed = []
    for j in range(len(pattern[0])):
        new_row = "".join([row[j] for row in pattern])
        pattern_transposed.append(new_row)
    
    return pattern_transposed
        

def apply_smudge_to_pattern(smudge: tuple, pattern: []):
    # flip the value at the coordinate given by the tuple
    i,j = smudge
    if pattern[i][j] == ".":
        new = "#"
    else:
        new = "."

    modified_row = [x for x in pattern[i]]
    modified_row[j] = new
    pattern[i] = "".join(modified_row)

    return pattern


def analyze_pattern(pattern: []):
    horizontal_reflections = find_reflections(pattern=pattern)
    pattern_transposed = transpose_pattern(pattern=pattern)
    vertical_reflections = find_reflections(pattern=pattern_transposed) # rows_left is just rows_above when the pattern is tranposed

    reflections = []
    for horizontal_reflection in horizontal_reflections:
        horizontal_index, num_rows_horizontal = horizontal_reflection
        if isinstance(horizontal_index, int) and not isinstance(horizontal_index, bool):
            reflections.append((0, horizontal_index, num_rows_horizontal))

    for vertical_reflection in vertical_reflections:
        vertical_index, num_rows_vertical = vertical_reflection
        if isinstance(vertical_index, int) and not isinstance(vertical_index, bool):
            reflections.append((1, vertical_index, num_rows_vertical))

    return reflections
    

def find_reflections(pattern: []):
    # determine if a pattern is mirrored horizontally

    reflections = []

    for i in range(len(pattern)-1):
        if pattern[i] == pattern[i+1]:
            # possible reflection found -- verify that the remaining rows all match
            rows_before = [pattern[k] for k in range(i)][::-1]
            rows_after = [pattern[k] for k in range(min(i+2, len(pattern)), len(pattern))]
            valid = True

            for k in range(min(len(rows_before), len(rows_after))):
                if rows_before[k] != rows_after[k]: # this possible reflection is invalid, but there still could be another elsewhere
                    valid = False
        
            if not valid: # skip this current possible reflection because it's invalid
                continue
            reflections.append((i, len(rows_before)+1)) # row index just before the dividing line

    return reflections


def find_possible_smudges(pattern: []):
    return [(i,j) for i, row in enumerate(pattern) for j, __ in enumerate(row)]
        

def part1_and_2():
    data = read_input(file="day13Input.txt")
    patterns = process_input(data=data)

    # part 1
    results = [analyze_pattern(pattern=pattern) for pattern in patterns]
    total = sum([x[0][2] * 100 for x in results if x[0][0] == 0]) + sum([x[0][2] for x in results if x[0][0] == 1])
    print(total)

    # part 2 - find all possible smudges -- pairs of rows that have a single-index difference between them; test all such point changes to see if it produces a valid reflection
    total = 0
    
    for pattern, result in zip(patterns, results):
        possible_smudges = find_possible_smudges(pattern=pattern[:])

        for smudge in possible_smudges:
            smudged_pattern = apply_smudge_to_pattern(smudge=smudge, pattern=pattern[:])
            new_results = analyze_pattern(pattern=smudged_pattern[:])

            if not new_results or not [x for x in new_results if x not in result]: # no valid reflection
                num=0
                continue
            
            new_result = [x for x in new_results if x not in result][0] # filter out the old reflection
                
            if new_result:
                direction, __, rows = new_result
                if direction == 0:
                    num = 100*rows
                elif direction == 1:
                    num = rows
                else:
                    raise NotImplementedError("how did you get here?")
                        
                break # new result found, no need to keep searching
        
        total += num

    print(total)

if __name__ == "__main__":
    part1_and_2()