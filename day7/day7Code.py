from adventOfCode2023.utils import read_input
from copy import deepcopy

LETTER_CHAR_VALUES = {
    "T": 10,
    "J": 1,
    "Q": 12,
    "K": 13,
    "A": 14,
}

HAND_TYPE_RANK = { # by # of unique keys in the frequency map, and the max and min frequencies)
    (1, 5, 5): 6, # 5 of a kind
    (2, 4, 1): 5, # 4 of a kind
    (2, 3, 2): 4, # full house
    (3, 3, 1): 3, # 3 of a kind
    (3, 2, 1): 2, # 2 pair
    (4, 2, 1): 1, # 1 pair
    (5, 1, 1): 0, # high card
}


def char_value(char: str):
    if char.isdigit():
        return int(char)
    else:
        return LETTER_CHAR_VALUES[char]


def encode_hand_values(hand: str):
    # assign a type rank based on overall hand type, and encode to integers
    hand = [char_value(char) for char in hand]
    hand_value_counts = {}
    for value in hand:
        if value not in hand_value_counts.keys():
            hand_value_counts[value] = 1
        else:
            hand_value_counts[value] += 1

    # assign a numerical ranking -- 0 for high card, 1 for 1 pair, 2 for 2 pair, 3 for 3 of a kind, 4 for full house, 5 for 4 of a kind, and 6 for 5 of a kind
    keys = [k for k in hand_value_counts.keys()]
    unique_keys = len(keys)
    max_freq = max([x for x in hand_value_counts.values()])
    min_freq = min([x for x in hand_value_counts.values()])
        
    hand_type_rank = HAND_TYPE_RANK[(unique_keys, max_freq, min_freq)]
    
    if LETTER_CHAR_VALUES["J"] == 1: # we're in part 2
        # given the non-joker elements of the hand, can we easily find the most optimal hand? probably check if it's possible to create a 5 of a kind, 4 of a kind, etc. and pick the first hand we can create
        # divide based on number of jokers present?
        if 1 in hand_value_counts.keys():
            jokers = hand_value_counts.pop(1)
            other_types = len(hand_value_counts.keys())
        
            if jokers == 5:
                # best hand is 5 of a kind, of the highest-value card possible
                hand_type_rank = 6
            
            elif jokers == 4:
                # 4 jokers -- best hand is 5 of a kind, of the 1 other card present
                hand_type_rank = 6
        
            elif jokers == 3:
                # 3 jokers -- best hand is 5 of a kind if the other 2 are a pair, or 4 of a kind with the higher-valued card of the 2
                
                if other_types == 1: # remaining 2 cards are a pair, so make 5 of a kind
                    hand_type_rank = 6

                else: # remaining 2 cards are not a pair, so it's 4 of a kind
                    hand_type_rank = 5

            elif jokers == 2:
                # 2 jokers: 5 of a kind if other 3 are 3 of a kind; 4 of a kind if there is a pair; otherwise 3 of a kind
                if other_types == 1:
                    hand_type_rank = 6
                elif other_types == 2:
                    hand_type_rank = 5
                else:
                    hand_type_rank = 3

            elif jokers == 1:
                # 1 joker: 5 of a kind if the other 4 are 4 of a kind; 4 of a kind if there is a 3 of a kind; full house if there are 2 pairs; 3 of a kind if there is 1 pair; 1 pair if there are 4 unique values
                if other_types == 1:
                    hand_type_rank = 6
                elif other_types == 2:
                    if max_freq == 3:
                        hand_type_rank = 5 # 4 of a kind
                    else:
                        hand_type_rank = 4 # full house
                elif other_types == 3: # 3 other kinds in 4, so there must be a pair -- make 3 of a kind
                        hand_type_rank = 3 # 3 of a kind
                elif other_types == 4: # 4 unique cards -- make 1 pair
                    hand_type_rank = 1

    return (hand_type_rank, *hand)


def rank_hands(data=[]):
    # convert the input to a list of tuples, and use a bubble sorting algorithm, comparing 2 hands at a time, proceeding until there are no changes

    hands = []
    for row in data:
        hand, bet = row.split(" ")
        hands.append((*encode_hand_values(hand=[*hand]), int(bet))) # flatten so the rank is the first number sorted on

    return sum([i * hand[-1] for i,hand in enumerate(sorted(hands), start=1)])


def part1_and_2():
    data = read_input(file="day7Input.txt")
    print(rank_hands(data=data))


if __name__ == "__main__":
    part1_and_2()