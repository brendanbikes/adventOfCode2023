from adventOfCode2023.utils import read_input
import re


def parse_card(card: str):
    # parse a single card string into useful information
    __, nums = card.split(": ")
    winning_numbers, drawn_numbers = nums.split(" | ")
    winning_numbers = [int(m[0]) for m in re.finditer(f'\d+', winning_numbers)]
    drawn_numbers = [int(m[0]) for m in re.finditer(f'\d+', drawn_numbers)]

    return winning_numbers, drawn_numbers


def get_num_matches(card: str):
    winning_numbers, drawn_numbers = parse_card(card=card)
    num_matches = len(set(winning_numbers) & set(drawn_numbers))
    return num_matches
    

def get_card_value_part_1(card: str):
    num_matches = get_num_matches(card=card)
    if num_matches > 0:
        return 2**(num_matches-1)
    else:
        return 0


def update_card_count(card: str, index: int, card_counts: int):
    num_matches = get_num_matches(card=card)
    card_counts[index] = 1 + sum([card_counts.get(index-k, 0) for k in range(1, num_matches+1)])
    return card_counts


def parts_1_and_2():
    data = read_input(file="day4Input.txt")
    total = sum([get_card_value_part_1(card=card) for card in data])
    print(f"Total value of all cards is {total}")

    # compute the values of cards in reverse order so we can do this deterministically instead of recursively
    card_counts = {} # keep track of # of cards/copies won by each starting card
    for i, card in enumerate(data[::-1]):
        card_counts = update_card_count(card=card, index=i, card_counts=card_counts)
    
    print(f"There are {sum([v for v in card_counts.values()])} total cards")


if __name__ == "__main__":
    parts_1_and_2()