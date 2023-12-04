def process_input_4(input_4: list[str]) -> list[tuple[list[int]]]:
    processed_input = []
    for line in input_4:
        numbers = line.split(':')[1]
        winning_numbers, my_numbers = numbers.split(' | ')
        winning_numbers = winning_numbers.split()
        my_numbers = my_numbers.split()
        processed_input.append((winning_numbers, my_numbers))

    return processed_input


def scratchcard_matches(winning_numbers: list[str], scratchcard_numbers: list[str]) -> int:
    hash_map = {n: 1 for n in winning_numbers}
    return len([n for n in scratchcard_numbers if n in hash_map])


def scratchcard_score(n_matches: int) -> int:
    if n_matches == 0:
        return 0
    else:
        return 2**(n_matches-1)


def final_card_number(matches: list[int]) -> int:
    # Initialise the card numbers - 1 of each card:
    n_cards = len(matches)
    card_numbers = len(n_cards) * [1]

    for i in range(n_cards):
        n_matches = matches[i]
        for j in range(n_matches):
            # Add card_numbers[i] new copies of the next n_matches cards
            card_numbers[i + 1 + j] += card_numbers[i]

    return sum(card_numbers)
